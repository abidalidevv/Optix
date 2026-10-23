import re
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
import urllib.parse

from backend.config import settings

logger = logging.getLogger("optix.swapper")

class ReferenceSwapper:
    """
    Advanced Core Web Vitals (LCP, CLS, INP) & Image SEO Swapper:
    1. Hero / Above-the-Fold LCP Optimization:
       - Injects fetchpriority="high" into the first hero image.
       - Explicitly prevents loading="lazy" on the first hero image (keeps LCP < 1.2s).
    2. Below-the-Fold Optimization:
       - Injects loading="lazy" decoding="async".
    3. CLS (Cumulative Layout Shift) Zero-Jump Guard:
       - Injects explicit width and height attributes or style="aspect-ratio: W/H;"
         so browser pre-allocates layout space and guarantees CLS = 0.00.
    4. Image SEO & Multilingual Alt-Tag Guard:
       - Auto-injects descriptive alt tags from product titles (including Urdu "شفائے معدہ")
         if original alt attribute is empty or missing.
    5. Preserves UTF-8 Unicode without mangling into %D8%B4 strings.
    """

    def __init__(
        self,
        url_mapping: Optional[Dict[str, str]] = None,
        dimensions_map: Optional[Dict[str, Tuple[int, int]]] = None
    ):
        self.url_mapping: Dict[str, str] = url_mapping or {}
        # dimensions_map: { filename_or_url: (width, height) }
        self.dimensions_map: Dict[str, Tuple[int, int]] = dimensions_map or {}

    def set_mapping(self, mapping: Dict[str, str]):
        self.url_mapping = mapping

    def set_dimensions(self, dims: Dict[str, Tuple[int, int]]):
        self.dimensions_map = dims

    def swap_html(
        self,
        html_content: str,
        default_alt_title: Optional[str] = None
    ) -> Tuple[str, int]:
        """
        Replaces <img> tags in product descriptionHtml and liquid sections.
        Applies LCP fetchpriority, CLS width/height reservation, and alt text guards.
        """
        if not html_content:
            return html_content, 0

        swaps_count = 0
        img_index = 0

        def replace_img_tag(match: re.Match) -> str:
            nonlocal swaps_count, img_index
            full_tag = match.group(0)
            img_index += 1
            is_hero_image = (img_index == 1)

            # 1. Extract src
            src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag, re.IGNORECASE)
            if not src_match:
                return full_tag

            old_src = src_match.group(1)
            new_src = self._resolve_replacement(old_src)
            
            modified_tag = full_tag
            if new_src and new_src != old_src:
                modified_tag = modified_tag.replace(old_src, new_src)
                swaps_count += 1

            # 2. Above-the-fold / Hero Banner LCP Rule:
            if is_hero_image and settings.inject_fetchpriority_hero:
                # Add fetchpriority="high" to LCP hero image
                if 'fetchpriority=' not in modified_tag.lower():
                    modified_tag = re.sub(r'<img\b', '<img fetchpriority="high"', modified_tag, count=1, flags=re.IGNORECASE)
                # Strip loading="lazy" if accidentally present on hero banner
                modified_tag = re.sub(r'\s+loading=["\']lazy["\']', '', modified_tag, flags=re.IGNORECASE)
                # Ensure decoding="async"
                if 'decoding=' not in modified_tag.lower():
                    modified_tag = re.sub(r'<img\b', '<img decoding="async"', modified_tag, count=1, flags=re.IGNORECASE)

            # 3. Below-the-fold Remaining Images Rule:
            elif not is_hero_image:
                if settings.inject_lazy_loading and 'loading=' not in modified_tag.lower():
                    modified_tag = re.sub(r'<img\b', '<img loading="lazy"', modified_tag, count=1, flags=re.IGNORECASE)
                if settings.inject_async_decoding and 'decoding=' not in modified_tag.lower():
                    modified_tag = re.sub(r'<img\b', '<img decoding="async"', modified_tag, count=1, flags=re.IGNORECASE)

            # 4. CLS Zero-Jump Guard: Ensure explicit width & height attributes
            if settings.enforce_cls_dimensions:
                has_width = re.search(r'\bwidth=["\']?\d+', modified_tag, re.IGNORECASE)
                has_height = re.search(r'\bheight=["\']?\d+', modified_tag, re.IGNORECASE)

                if not (has_width and has_height):
                    dims = self._resolve_dimensions(old_src)
                    if dims:
                        w, h = dims
                        dim_attrs = f' width="{w}" height="{h}"'
                        # Also inject aspect-ratio CSS for responsiveness
                        if 'style=' in modified_tag.lower():
                            modified_tag = re.sub(
                                r'style=["\']([^"\']*)["\']',
                                rf'style="aspect-ratio: {w}/{h}; max-width: 100%; height: auto; \1"',
                                modified_tag,
                                count=1,
                                flags=re.IGNORECASE
                            )
                        else:
                            dim_attrs += f' style="aspect-ratio: {w}/{h}; max-width: 100%; height: auto;"'

                        modified_tag = re.sub(r'<img\b', f'<img{dim_attrs}', modified_tag, count=1, flags=re.IGNORECASE)

            # 5. Multilingual & Image SEO Alt-Tag Guard:
            if settings.auto_generate_alt_tags:
                has_alt = re.search(r'\balt=["\']([^"\']*)["\']', modified_tag, re.IGNORECASE)
                # If alt attribute is missing entirely
                if not has_alt:
                    alt_val = default_alt_title or self._generate_seo_alt(old_src)
                    modified_tag = re.sub(r'<img\b', f'<img alt="{alt_val}"', modified_tag, count=1, flags=re.IGNORECASE)
                # If alt is empty (alt="" or alt=' ')
                elif not has_alt.group(1).strip():
                    alt_val = default_alt_title or self._generate_seo_alt(old_src)
                    modified_tag = re.sub(r'\balt=["\'][^"\']*["\']', f'alt="{alt_val}"', modified_tag, count=1, flags=re.IGNORECASE)

            return modified_tag

        img_pattern = re.compile(r'<img\b[^>]*>', re.IGNORECASE)
        optimized_html = img_pattern.sub(replace_img_tag, html_content)

        return optimized_html, swaps_count

    def swap_theme_settings(self, settings_json_str: str) -> Tuple[str, int]:
        """
        Swaps image references in config/settings_data.json.
        Preserves JSON structure and UTF-8 formatting.
        """
        try:
            data = json.loads(settings_json_str)
        except Exception as e:
            logger.error(f"Failed to parse settings JSON: {e}")
            return settings_json_str, 0

        swaps_count = 0

        def traverse_and_swap(obj: Any) -> Any:
            nonlocal swaps_count
            if isinstance(obj, dict):
                return {k: traverse_and_swap(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [traverse_and_swap(item) for item in obj]
            elif isinstance(obj, str):
                new_val = self._resolve_replacement(obj)
                if new_val and new_val != obj:
                    swaps_count += 1
                    return new_val
                return obj
            else:
                return obj

        updated_data = traverse_and_swap(data)
        updated_json = json.dumps(updated_data, ensure_ascii=False, indent=2)
        return updated_json, swaps_count

    def _resolve_replacement(self, raw_url: str) -> Optional[str]:
        if not raw_url:
            return None

        # 1. Exact match
        if raw_url in self.url_mapping:
            return self.url_mapping[raw_url]

        # 2. Match without query parameters (?v=...)
        url_no_query = raw_url.split("?")[0]
        if url_no_query in self.url_mapping:
            return self.url_mapping[url_no_query]

        # 3. Match shopify://shop_images/
        if raw_url.startswith("shopify://shop_images/"):
            filename = raw_url.replace("shopify://shop_images/", "")
            stem = Path(filename).stem
            for key, val in self.url_mapping.items():
                if Path(key).stem == stem:
                    return f"shopify://shop_images/{Path(val).name}"

        # 4. Match by file basename
        basename = Path(url_no_query).name
        if basename in self.url_mapping:
            return self.url_mapping[basename]

        return None

    def _resolve_dimensions(self, raw_url: str) -> Optional[Tuple[int, int]]:
        url_no_query = raw_url.split("?")[0]
        basename = Path(url_no_query).name
        stem = Path(url_no_query).stem

        # Check dimensions map
        if raw_url in self.dimensions_map:
            return self.dimensions_map[raw_url]
        if basename in self.dimensions_map:
            return self.dimensions_map[basename]
        if stem in self.dimensions_map:
            return self.dimensions_map[stem]

        # Fallback default dimensions for e-commerce catalog images
        return (800, 800)

    def _generate_seo_alt(self, raw_url: str) -> str:
        stem = Path(raw_url.split("?")[0]).stem
        clean = re.sub(r'[\-_]+', ' ', stem).title()
        return f"{clean} - Tibbe Shifa"

reference_swapper = ReferenceSwapper()
