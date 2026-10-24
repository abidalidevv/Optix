import time
import json
import logging
import requests
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from backend.config import settings
from backend.auth import auth_manager

logger = logging.getLogger("optix.shopify")

class LeakyBucketLimiter:
    """
    Guards Shopify GraphQL API against rate limit / throttling.
    Restores points continuously based on restore_rate.
    """
    def __init__(self, max_points: int = 1000, restore_rate: int = 50):
        self.max_points = max_points
        self.current_points = max_points
        self.restore_rate = restore_rate
        self.last_update = time.time()

    def consume(self, requested_points: int = 20):
        now = time.time()
        elapsed = now - self.last_update
        self.current_points = min(self.max_points, self.current_points + elapsed * self.restore_rate)
        self.last_update = now

        if self.current_points < requested_points:
            deficit = requested_points - self.current_points
            sleep_time = deficit / self.restore_rate
            logger.info(f"Rate limiter active. Sleeping for {sleep_time:.2f}s...")
            time.sleep(sleep_time)
            self.current_points = requested_points

        self.current_points -= requested_points

    def update_from_throttle_status(self, throttle_status: Dict[str, Any]):
        if not throttle_status:
            return
        currently_avail = throttle_status.get("currentlyAvailable")
        restore_rate = throttle_status.get("restoreRate")
        if currently_avail is not None:
            self.current_points = float(currently_avail)
        if restore_rate is not None:
            self.restore_rate = float(restore_rate)
        self.last_update = time.time()

class ShopifyGraphQLClient:
    def __init__(self):
        self.limiter = LeakyBucketLimiter(
            max_points=settings.max_bucket_size,
            restore_rate=settings.restore_rate_per_sec
        )

    def execute_graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.limiter.consume(requested_points=15)
        token = auth_manager.get_access_token()
        endpoint = f"https://{settings.shop}/admin/api/{settings.api_version}/graphql.json"

        headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        resp = requests.post(endpoint, json={"query": query, "variables": variables or {}}, headers=headers, timeout=30)
        
        if resp.status_code == 429:
            retry_after = float(resp.headers.get("Retry-After", 2.0))
            logger.warning(f"Shopify 429 Throttled. Waiting {retry_after}s...")
            time.sleep(retry_after)
            return self.execute_graphql(query, variables)

        resp.raise_for_status()
        data = resp.json()

        # Update rate limiter from response extensions
        throttle_status = data.get("extensions", {}).get("cost", {}).get("throttleStatus")
        if throttle_status:
            self.limiter.update_from_throttle_status(throttle_status)

        return data

    def create_staged_upload(self, filename: str, mime_type: str = "image/webp") -> Optional[Dict[str, Any]]:
        """
        Calls stagedUploadsCreate mutation to get a presigned URL & upload parameters.
        """
        mutation = """
        mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
          stagedUploadsCreate(input: $input) {
            stagedTargets {
              url
              resourceUrl
              parameters {
                name
                value
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        variables = {
            "input": [
                {
                    "filename": filename,
                    "mimeType": mime_type,
                    "httpMethod": "POST",
                    "resource": "IMAGE"
                }
            ]
        }

        res = self.execute_graphql(mutation, variables)
        targets = res.get("data", {}).get("stagedUploadsCreate", {}).get("stagedTargets", [])
        user_errors = res.get("data", {}).get("stagedUploadsCreate", {}).get("userErrors", [])

        if user_errors:
            logger.error(f"stagedUploadsCreate error for {filename}: {user_errors}")
            return None

        if targets:
            return targets[0]
        return None

    def upload_binary_to_s3(self, staged_target: Dict[str, Any], file_path: Path) -> bool:
        """
        Directly uploads binary to Shopify's presigned S3 / GCS storage target.
        """
        url = staged_target.get("url")
        parameters = staged_target.get("parameters", [])
        if not url:
            return False

        # Assemble multipart form data
        data = {param["name"]: param["value"] for param in parameters}
        
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "image/webp")}
            upload_resp = requests.post(url, data=data, files=files, timeout=60)
            
        if upload_resp.status_code in (200, 201, 204):
            return True
        else:
            logger.error(f"S3/Staged Upload failed with status {upload_resp.status_code}: {upload_resp.text[:300]}")
            return False

    def create_file_in_shopify(self, resource_url: str, alt_text: str = "") -> Optional[Dict[str, Any]]:
        """
        Registers the uploaded binary into Shopify Media Library via fileCreate mutation.
        """
        mutation = """
        mutation fileCreate($files: [FileCreateInput!]!) {
          fileCreate(files: $files) {
            files {
              id
              alt
              createdAt
              fileStatus
              ... on MediaImage {
                image {
                  url
                  width
                  height
                }
              }
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        variables = {
            "files": [
                {
                    "originalSource": resource_url,
                    "contentType": "IMAGE",
                    "alt": alt_text or "Optix Optimized Image"
                }
            ]
        }

        res = self.execute_graphql(mutation, variables)
        files = res.get("data", {}).get("fileCreate", {}).get("files", [])
        user_errors = res.get("data", {}).get("fileCreate", {}).get("userErrors", [])

        if user_errors:
            logger.error(f"fileCreate userErrors: {user_errors}")
            return None

        if files:
            return files[0]
        return None

    def upload_and_register_image(self, file_path: Path, alt_text: str = "") -> Optional[str]:
        """
        End-to-end pipeline:
        1. stagedUploadsCreate
        2. Direct binary S3 upload
        3. fileCreate mutation
        Returns the new Shopify CDN URL.
        """
        filename = file_path.name
        target = self.create_staged_upload(filename, mime_type="image/webp")
        if not target:
            return None

        success = self.upload_binary_to_s3(target, file_path)
        if not success:
            return None

        resource_url = target.get("resourceUrl")
        file_record = self.create_file_in_shopify(resource_url, alt_text=alt_text)
        if not file_record:
            return None

        # Return new CDN URL
        image_obj = file_record.get("image")
        if image_obj and image_obj.get("url"):
            return image_obj["url"]

        return resource_url

    def update_file_alt(self, file_id: str, alt_text: str) -> bool:
        """
        Updates alt text of an existing Shopify media file using GraphQL fileUpdate mutation.
        file_id can be numeric ID or full GID (e.g. gid://shopify/MediaImage/46348966297841).
        """
        gid = file_id if file_id.startswith("gid://shopify/") else f"gid://shopify/MediaImage/{file_id}"
        mutation = """
        mutation fileUpdate($files: [FileUpdateInput!]!) {
          fileUpdate(files: $files) {
            files {
              id
              alt
            }
            userErrors {
              field
              message
            }
          }
        }
        """
        variables = {
            "files": [
                {
                    "id": gid,
                    "alt": alt_text
                }
            ]
        }
        try:
            res = self.execute_graphql(mutation, variables)
            user_errors = res.get("data", {}).get("fileUpdate", {}).get("userErrors", [])
            if user_errors:
                logger.warning(f"fileUpdate userErrors for {file_id}: {user_errors}")
                return False
            return True
        except Exception as e:
            logger.error(f"Error executing fileUpdate for {file_id}: {e}")
            return False

    def batch_update_files_alt(self, updates: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Updates alt text for multiple media files in Shopify with rate limit protection.
        updates = [{"id": file_id, "alt": alt_text}, ...]
        """
        success_count = 0
        error_count = 0
        for item in updates:
            ok = self.update_file_alt(item["id"], item["alt"])
            if ok:
                success_count += 1
            else:
                error_count += 1
        return {
            "success": True,
            "updated": success_count,
            "failed": error_count,
            "total": len(updates)
        }

    def get_themes(self) -> List[Dict[str, Any]]:
        query = """
        {
          themes(first: 10) {
            nodes {
              id
              name
              role
              createdAt
              updatedAt
            }
          }
        }
        """
        res = self.execute_graphql(query)
        return res.get("data", {}).get("themes", {}).get("nodes", [])

    def get_shop_info(self) -> Dict[str, Any]:
        query = """
        {
          shop {
            name
            myshopifyDomain
            currencyCode
            plan {
              displayName
              partnerDevelopment
            }
          }
        }
        """
        res = self.execute_graphql(query)
        return res.get("data", {}).get("shop", {})

shopify_client = ShopifyGraphQLClient()
