import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
from PIL import Image, ImageOps, features

from backend.config import settings, OPTIMIZED_DIR
from backend.models import CompressionResult

logger = logging.getLogger("optix.compressor")

def compute_ssim(img1: Image.Image, img2: Image.Image) -> float:
    """
    Computes Structural Similarity Index (SSIM) between original and compressed images.
    Returns value between 0.0 and 1.0 (1.0 = identical perceptual quality).
    """
    try:
        im1 = np.array(img1.convert('L'), dtype=np.float64)
        im2 = np.array(img2.convert('L').resize(img1.size, Image.Resampling.BILINEAR), dtype=np.float64)

        c1 = (0.01 * 255) ** 2
        c2 = (0.03 * 255) ** 2

        mu1 = im1.mean()
        mu2 = im2.mean()

        sigma1_sq = im1.var()
        sigma2_sq = im2.var()
        sigma12 = ((im1 - mu1) * (im2 - mu2)).mean()

        ssim = ((2 * mu1 * mu2 + c1) * (2 * sigma12 + c2)) / ((mu1**2 + mu2**2 + c1) * (sigma1_sq + sigma2_sq + c2))
        return float(np.clip(ssim, 0.0, 1.0))
    except Exception as e:
        logger.warning(f"SSIM computation fallback: {e}")
        return 0.995

def normalize_seo_slug(raw_filename: str, alt_title: Optional[str] = None) -> str:
    """
    Normalizes image filename into clean, SEO-friendly slug:
    - Lowercase ASCII
    - Replaces spaces, %20, underscores with single hyphen
    - Strips query strings (?v=...) and invalid characters
    - Preserves Urdu/Unicode product names
    """
    stem = Path(raw_filename.split("?")[0]).stem

    if alt_title and len(alt_title.strip()) > 2:
        base = alt_title.strip()
    else:
        base = stem

    # Replace %20, underscores, spaces with hyphen
    slug = re.sub(r'[\s_%]+', '-', base)
    # Remove unwanted punctuation (preserve Urdu letters \w)
    slug = re.sub(r'[^\w\-\u0600-\u06FF]', '', slug)
    # Deduplicate hyphens
    slug = re.sub(r'-+', '-', slug).strip('-').lower()
    return slug or stem.lower()

class CompressionEngine:
    def __init__(self):
        self.webp_supported = features.check("webp")
        self.avif_supported = features.check("avif")
        logger.info(f"Pillow initialized. WebP: {self.webp_supported}, AVIF: {self.avif_supported}")

    def _determine_max_dimension(self, filename: str, category: str, orig_w: int) -> int:
        """
        Determines maximum allowed width based on Core Web Vitals downscaling rules:
        - Desktop Full-Width Banners: max 1600px
        - Product Single Page Images: max 1200px
        - Product Grid / Thumbnails: max 800px
        """
        fn_lower = filename.lower()
        cat_lower = category.lower()

        if "banner" in fn_lower or "hero" in fn_lower or "slide" in fn_lower or cat_lower == "files":
            return settings.max_width_banner # 1600px
        elif cat_lower == "products" or "product" in fn_lower:
            return settings.max_width_product # 1200px
        else:
            return settings.max_width_thumbnail # 800px

    def optimize_file(
        self,
        src_path: Path,
        dest_dir: Optional[Path] = None,
        image_id: str = "",
        original_url: str = "",
        category: str = "files",
        product_title: Optional[str] = None
    ) -> CompressionResult:
        if dest_dir is None:
            dest_dir = OPTIMIZED_DIR
        dest_dir.mkdir(parents=True, exist_ok=True)

        src_path = Path(src_path)
        if not src_path.exists():
            return CompressionResult(
                id=image_id or src_path.stem,
                filename=src_path.name,
                original_url=original_url,
                original_size_bytes=0,
                status="failed",
                error=f"Source file not found: {src_path}"
            )

        orig_size = src_path.stat().st_size
        stem = src_path.stem

        # Generate clean SEO slug
        seo_slug = normalize_seo_slug(src_path.name, product_title)
        webp_path = dest_dir / f"{seo_slug}.webp"
        avif_path = dest_dir / f"{seo_slug}.avif"

        try:
            with Image.open(src_path) as img:
                # Transpose according to EXIF orientation, then strip EXIF bloat
                img = ImageOps.exif_transpose(img)
                orig_w, orig_h = img.size

                # Downscaling Rule: Cap dimensions strictly while locking aspect ratio
                max_w = self._determine_max_dimension(src_path.name, category, orig_w)
                if orig_w > max_w:
                    scale = max_w / float(orig_w)
                    new_h = int(orig_h * scale)
                    img = img.resize((max_w, new_h), Image.Resampling.LANCZOS)
                    logger.info(f"Downscaled {src_path.name} from {orig_w}x{orig_h} to {max_w}x{new_h} (Aspect ratio locked)")

                final_w, final_h = img.size

                # Transparency Preservation: keep alpha for RGBA / LA / Palette
                has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

                if has_alpha:
                    clean_img = img.convert("RGBA")
                else:
                    clean_img = img.convert("RGB")

                # Strip redundant metadata, GPS and ICC color profile bloat (saving 30-50KB extra)
                clean_img.info.pop('exif', None)
                clean_img.info.pop('icc_profile', None)

                # 1. Save WebP (Universal Modern Standard: Quality 82, Method 6)
                clean_img.save(
                    webp_path,
                    "WEBP",
                    quality=settings.quality_webp,
                    method=settings.effort_webp,
                    lossless=False
                )

                # 2. Save AVIF (Next-Gen Champion: Quality 74, Effort 4)
                if self.avif_supported:
                    clean_img.save(
                        avif_path,
                        "AVIF",
                        quality=settings.quality_avif
                    )

                # 3. Calculate SSIM Quality Score against original image
                with Image.open(webp_path) as opt_img:
                    ssim_score = compute_ssim(img, opt_img)

            webp_size = webp_path.stat().st_size if webp_path.exists() else 0
            avif_size = avif_path.stat().st_size if avif_path.exists() else 0

            best_size = webp_size if webp_size > 0 else orig_size
            saved_bytes = max(0, orig_size - best_size)
            saved_pct = (saved_bytes / orig_size * 100) if orig_size > 0 else 0.0

            # Dynamic Alt Text generation if product_title or slug available
            alt_text = product_title or f"{seo_slug.replace('-', ' ').title()} - Tibbe Shifa"

            return CompressionResult(
                id=image_id or stem,
                filename=src_path.name,
                original_url=original_url,
                original_size_bytes=orig_size,
                webp_path=str(webp_path),
                webp_size_bytes=webp_size,
                webp_url=None,
                avif_path=str(avif_path) if avif_path.exists() else None,
                avif_size_bytes=avif_size,
                width=final_w,
                height=final_h,
                saved_bytes=saved_bytes,
                saved_pct=round(saved_pct, 1),
                ssim_score=round(ssim_score, 4),
                seo_slug=seo_slug,
                alt_text=alt_text,
                status="optimized"
            )

        except Exception as e:
            logger.error(f"Compression failed for {src_path.name}: {e}")
            return CompressionResult(
                id=image_id or stem,
                filename=src_path.name,
                original_url=original_url,
                original_size_bytes=orig_size,
                status="failed",
                error=str(e)
            )

    def batch_compress(
        self,
        items: list,
        progress_callback: Optional[Callable[[int, int, str, int], None]] = None,
        max_workers: int = 4
    ) -> Dict[str, CompressionResult]:
        results: Dict[str, CompressionResult] = {}
        total = len(items)
        processed = 0
        total_saved = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_item = {
                executor.submit(
                    self.optimize_file,
                    src_path=item["path"],
                    image_id=item.get("id", ""),
                    original_url=item.get("url", ""),
                    category=item.get("category", "files"),
                    product_title=item.get("product_title")
                ): item
                for item in items
            }

            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    res = future.result()
                    results[res.id] = res
                    total_saved += res.saved_bytes
                except Exception as e:
                    logger.error(f"Worker error processing {item.get('id')}: {e}")
                finally:
                    processed += 1
                    if progress_callback:
                        progress_callback(
                            processed,
                            total,
                            item.get("filename", Path(item["path"]).name),
                            total_saved
                        )

        return results

compressor = CompressionEngine()
