import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import logging

from backend.config import DATA_DIR, settings

logger = logging.getLogger("optix.alt_text")

ALT_MAPPING_FILE = DATA_DIR / "alt_text_mapping.json"
PRODUCTS_JSON_PATH = Path(r"C:\Users\Ali\Desktop\Matrixify\tibbeshifa-migrator\backups\source-store\json\products.json")
MANIFEST_PATH = Path(r"C:\Users\Ali\Desktop\Matrixify\tibbeshifa-migrator\backups\source-store\manifests\media-manifest.json")

# Core Curated Catalog Dictionary for Tibbe Shifa
STATIC_PRODUCT_MAP = {
    # Nijaat Likoria
    "46210618523889": "Nijaat Likoria (نجات لیکوریا) - Women Health & Vitality Herbal Capsule | Tibbe Shifa",
    "46348952043761": "Nijaat Likoria (نجات لیکوریا) - Pure Herbal Capsule Packaging | Tibbe Shifa",
    "46348951978225": "Nijaat Likoria (نجات لیکوریا) - Formula Ingredients Guide | Tibbe Shifa",
    "46348952010993": "Nijaat Likoria (نجات لیکوریا) - Usage & Dosage Instructions | Tibbe Shifa",
    "46348952076529": "Nijaat Likoria (نجات لیکوریا) - Customer Benefits & Guarantee | Tibbe Shifa",
    # Nijaat Dublepan
    "46210584019185": "Nijaat Dublepan (نجات دبلپن) - Natural Weight Gain & Muscle Tonic | Tibbe Shifa",
    "46348964593905": "Nijaat Dublepan (نجات دبلپن) - Herbal Weight Gain Formula Bottle | Tibbe Shifa",
    "46210583986417": "Nijaat Dublepan (نجات دبلپن) - Pure Botanical Extracts | Tibbe Shifa",
    "46348964561137": "Nijaat Dublepan (نجات دبلپن) - Nutrition Facts & Dosage | Tibbe Shifa",
    "46348964626673": "Nijaat Dublepan (نجات دبلپن) - Certified Herbal Guarantee Seal | Tibbe Shifa",
    # Shifa-e-Meda
    "46348965282033": "Shifa-e-Meda (شفائے معدہ) - Stomach Acidity & Gas Relief Powder | Tibbe Shifa",
    "46348965347569": "Shifa-e-Meda (شفائے معدہ) - Digestive Health Herbal Formula | Tibbe Shifa",
    "46348965314801": "Shifa-e-Meda (شفائے معدہ) - Fast Relief Botanical Ingredients | Tibbe Shifa",
    "46348965380337": "Shifa-e-Meda (شفائے معدہ) - Traditional Unani Medicine Jar | Tibbe Shifa",
    # Qabz Kusha
    "46210583953649": "Qabz Kusha (قبض کشا) - Natural Constipation Relief Powder | Tibbe Shifa",
    "46210607153393": "Qabz Kusha (قبض کشا) - Gut Health & Colon Cleansing Remedy | Tibbe Shifa",
    "46210607087857": "Qabz Kusha (قبض کشا) - Gentle Organic Herbal Ingredients | Tibbe Shifa",
    "46348957942001": "Qabz Kusha (قبض کشا) - Fast Relief Dosage Guide | Tibbe Shifa",
    "46348961218801": "Qabz Kusha (قبض کشا) - Pure Herbal Quality Seal | Tibbe Shifa",
    # Sugar Care
    "46210583920881": "Sugar Care (شوگر کیئر) - Blood Sugar & Glucose Support Herbal Powder | Tibbe Shifa",
    "46348963315953": "Sugar Care (شوگر کیئر) - Diabetes Care Botanical Formulation | Tibbe Shifa",
    "46348963250417": "Sugar Care (شوگر کیئر) - Natural Herbal Ingredients Pack | Tibbe Shifa",
    "46210593259761": "Sugar Care (شوگر کیئر) - Blood Glucose Balance Guide | Tibbe Shifa",
    "46348963348721": "Sugar Care (شوگر کیئر) - Certified Quality Assurance | Tibbe Shifa",
    # Nijaat Bawasir
    "46210583888113": "Nijaat Bawasir (نجات بواسیر) - Hemorrhoids & Piles Relief Capsule | Tibbe Shifa",
    "46348966297841": "Nijaat Bawasir (نجات بواسیر) - Ayurvedic Piles Care Bottle | Tibbe Shifa",
    "46348966265073": "Nijaat Bawasir (نجات بواسیر) - Herbal Formula Composition Guide | Tibbe Shifa",
    "46348966330609": "Nijaat Bawasir (نجات بواسیر) - 100% Herbal Quality Seal | Tibbe Shifa",
    "46348967444721": "Hakim Riaz Ahmad Bhatti Certified Herbal Expert - Tibbe Shifa",
    # Nijaat Jaryan
    "46210583855345": "Nijaat Jaryan (نجات جریان) - Men Physical Strength & Stamina Tonic | Tibbe Shifa",
    "46348949848305": "Nijaat Jaryan (نجات جریان) - Vitality Booster Packaging | Tibbe Shifa",
    "46348949881073": "Nijaat Jaryan (نجات جریان) - Botanical Energy Ingredients | Tibbe Shifa",
    "46348949913841": "Nijaat Jaryan (نجات جریان) - Safe Unani Tonic Formulation | Tibbe Shifa",
    # Branding, Authority & Seals
    "TIBBE_SHIFA": "Tibbe Shifa Official Brand Logo - Pure Herbal Health Solutions",
    "riazahmadbhatti": "Hakeem Riaz Ahmad Bhatti - Head Herbalist at Tibbe Shifa Laboratories",
    "ChatGPT_Image": "Tibbe Shifa Laboratory Natural Herbal Botanical Ingredients",
    "bc3b4fae8cb250b8f7d992fe19938121": "Tibbe Shifa Natural Herbal Capsules Bottle Product Packaging"
}

DUMMY_KEYWORDS = {
    "untitled", "image", "img", "photo", "picture", "file", "test", "temp",
    "screenshot", "banner", "thumbnail", "asset", "dsc", "null", "none", "optix"
}

def load_manifest_lookup() -> Dict[str, Dict[str, Any]]:
    """Loads manifest to map numeric image IDs to original URLs and categories."""
    lookup = {}
    if MANIFEST_PATH.exists():
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                items = json.load(f)
            for it in items:
                fn = it.get("filename", "")
                stem = Path(fn).stem
                lookup[fn] = it
                lookup[stem] = it
        except Exception as e:
            logger.error(f"Error loading manifest lookup: {e}")
    return lookup

def load_alt_mapping() -> Dict[str, str]:
    if ALT_MAPPING_FILE.exists():
        try:
            with open(ALT_MAPPING_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading alt mapping: {e}")
    return {}

def save_alt_mapping(mapping: Dict[str, str]):
    try:
        with open(ALT_MAPPING_FILE, "w", encoding="utf-8") as f:
            json.dump(mapping, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving alt mapping: {e}")

def is_dummy_alt(alt: Optional[str], filename: str = "") -> bool:
    """Detects if an alt text is missing, generic, dummy, or boilerplate fallback."""
    if not alt or not alt.strip():
        return True
    
    clean = alt.strip().lower()
    
    # Pure numbers (e.g. '46210618523889')
    if re.match(r"^\d+$", clean):
        return True
        
    # Numbers with simple suffix like '46210618523889 - Tibbe Shifa'
    if re.match(r"^\d+[\s\-_]*(tibbe[\s\-_]*shifa)?$", clean):
        return True
    
    # File extensions in alt text (e.g. '46210618523889.png', 'hero.jpg')
    if re.search(r"\.(png|jpg|jpeg|webp|avif|gif)$", clean, re.IGNORECASE):
        return True

    # Exact filename match
    if filename:
        stem = Path(filename).stem.lower()
        if clean == stem or clean == filename.lower():
            return True
        
    # Only generic dummy words
    words = set(re.findall(r"\b[a-z0-9]+\b", clean))
    if words and words.issubset(DUMMY_KEYWORDS):
        return True
        
    return False

def clamp_alt_text(text: str, max_chars: int = 125) -> str:
    """Ensures alt text adheres to Google SEO and WCAG screen reader 125-char limit."""
    text = " ".join(text.split()) # normalize whitespace
    if len(text) <= max_chars:
        return text
    # Trim to last complete word before limit
    trimmed = text[:max_chars - 3]
    last_space = trimmed.rfind(" ")
    if last_space > 60:
        trimmed = trimmed[:last_space]
    return trimmed + "..."

class AltTextManager:
    def __init__(self):
        self.mapping = load_alt_mapping()
        self.manifest_lookup = load_manifest_lookup()
        self._url_counter = 1

    def get_alt(self, filename: str, fallback_alt: Optional[str] = None, category: str = "files") -> Tuple[str, bool]:
        """Returns (alt_text, is_optimized)."""
        # 1. User/AI confirmed in mapping
        if filename in self.mapping:
            return self.mapping[filename], True
            
        # 2. Existing valid custom alt text from Shopify
        if fallback_alt and not is_dummy_alt(fallback_alt, filename):
            return fallback_alt.strip(), True
            
        # 3. Dummy / Missing: return suggested alt, but marked as UNOPTIMIZED (is_optimized = False)
        suggested = self.generate_smart_alt(filename, category, fallback_alt)
        return suggested, False

    def generate_smart_alt(self, filename: str, category: str = "files", existing_alt: Optional[str] = None) -> str:
        """
        Generates high-ranking, unique, descriptive Google SEO alt tag.
        Leverages product knowledge, original URL slugs, and unique view indicators to avoid duplicate spam.
        """
        stem = Path(filename).stem
        
        # 1. Direct Knowledge Base Match
        if stem in STATIC_PRODUCT_MAP:
            return clamp_alt_text(STATIC_PRODUCT_MAP[stem])
        for key, smart_text in STATIC_PRODUCT_MAP.items():
            if key in stem:
                return clamp_alt_text(smart_text)

        # 2. Inspect original URL in media-manifest.json
        manifest_item = self.manifest_lookup.get(filename) or self.manifest_lookup.get(stem)
        orig_url = manifest_item.get("url", "") if manifest_item else ""
        url_basename = orig_url.split("/")[-1].split("?")[0] if "/" in orig_url else ""
        url_lower = url_basename.lower()

        # WhatsApp Customer Reviews / Testimonials
        if "whatsapp" in url_lower:
            match = re.search(r"(\d{4}-\d{2}-\d{2})", url_basename)
            date_tag = f" ({match.group(1)})" if match else ""
            unique_hash = stem[-4:] if len(stem) >= 4 else str(abs(hash(stem)) % 999)
            return clamp_alt_text(f"Tibbe Shifa Customer WhatsApp Review & Positive Health Feedback{date_tag} #{unique_hash}")

        # Head Herbalist Photos
        if "hakeem" in url_lower or "riaz" in url_lower:
            return clamp_alt_text("Hakim Riaz Ahmad Bhatti - Head Herbalist & Certified Expert at Tibbe Shifa")

        # Specific Products via URL keywords
        if "likoria" in url_lower:
            return clamp_alt_text("Nijaat Likoria (نجات لیکوریا) - Women Health & Vitality Herbal Capsule | Tibbe Shifa")
        if "dublepan" in url_lower or "dublapun" in url_lower:
            return clamp_alt_text("Nijaat Dublepan (نجات دبلپن) - Natural Weight Gain & Muscle Tonic | Tibbe Shifa")
        if "meda" in url_lower or "stomach" in url_lower:
            return clamp_alt_text("Shifa-e-Meda (شفائے معدہ) - Herbal Stomach Acid, Gas & Digestion Powder | Tibbe Shifa")
        if "qabz" in url_lower:
            return clamp_alt_text("Qabz Kusha (قبض کشا) - Natural Constipation Relief & Gut Health Powder | Tibbe Shifa")
        if "sugar" in url_lower:
            return clamp_alt_text("Sugar Care (شوگر کیئر) - Blood Sugar & Glucose Support Herbal Formulation | Tibbe Shifa")
        if "bawasir" in url_lower or "bawaseer" in url_lower or "piles" in url_lower:
            return clamp_alt_text("Nijaat Bawasir (نجات بواسیر) - Herbal Hemorrhoids Piles Relief Capsule | Tibbe Shifa")
        if "jaryan" in url_lower:
            return clamp_alt_text("Nijaat Jaryan (نجات جریان) - Men Physical Strength & Stamina Herbal Tonic | Tibbe Shifa")

        # UI & Trust Badges
        if "logo" in url_lower or "logo" in stem.lower():
            return clamp_alt_text("Tibbe Shifa Official Brand Logo - Pure Herbal Health Solutions")
        if any(k in url_lower for k in ["banner", "hero", "slider"]):
            return clamp_alt_text("Tibbe Shifa Storefront Hero Banner - Authentic Natural Herbal Solutions")
        if any(k in url_lower for k in ["trust", "guarantee", "badge"]):
            return clamp_alt_text("100% Pure Organic Herbal Medicine Certified Guarantee Badge | Tibbe Shifa")
        if any(k in url_lower for k in ["delivery", "cod", "shipping"]):
            return clamp_alt_text("Cash on Delivery Across Pakistan Fast Shipping Seal | Tibbe Shifa")

        # 3. Clean keywords from original URL basename if meaningful
        url_stem = Path(url_basename).stem
        cleaned_url = re.sub(r"[-_]+", " ", url_stem).strip()
        cleaned_url = re.sub(r"^\d+\s*", "", cleaned_url)
        cleaned_url = re.sub(r"\s*\d+$", "", cleaned_url)
        if cleaned_url and not re.match(r"^\d+$", cleaned_url) and len(cleaned_url) > 3:
            words = cleaned_url.title()
            return clamp_alt_text(f"{words} - Tibbe Shifa Natural Herbal Product")

        # 4. Contextual & Unique Fallback (guaranteed no duplicate spam!)
        unique_suffix = stem[-4:] if len(stem) >= 4 else str(abs(hash(stem)) % 1000)
        cat_lower = category.lower()
        if "product" in cat_lower:
            return clamp_alt_text(f"Tibbe Shifa Natural Herbal Supplement - Authentic Catalog Item #{unique_suffix}")
        elif "collection" in cat_lower:
            return clamp_alt_text(f"Tibbe Shifa Herbal Healthcare Remedies & Collections Media #{unique_suffix}")
        else:
            return clamp_alt_text(f"Tibbe Shifa Authentic Natural Herbal Health Solution Media #{unique_suffix}")

    def set_alt(self, filename: str, alt_text: str):
        self.mapping[filename] = clamp_alt_text(alt_text.strip())
        save_alt_mapping(self.mapping)

    def optimize_all(self, images: list) -> Dict[str, Any]:
        """Scans all images, generates smart non-duplicate SEO alt tags, and returns the full mapping."""
        updated = 0
        for img in images:
            fn = getattr(img, "filename", None) or (img.get("filename") if isinstance(img, dict) else "")
            cat = getattr(img, "category", "files") or (img.get("category", "files") if isinstance(img, dict) else "files")
            curr_alt = getattr(img, "alt_text", None) or (img.get("alt_text") if isinstance(img, dict) else None)
            
            # Generate and assign if not already in mapping or is dummy
            if fn not in self.mapping or is_dummy_alt(curr_alt, fn):
                smart_alt = self.generate_smart_alt(fn, cat, curr_alt)
                self.mapping[fn] = smart_alt
                if hasattr(img, "alt_text"):
                    img.alt_text = smart_alt
                    img.is_dummy_alt = False
                elif isinstance(img, dict):
                    img["alt_text"] = smart_alt
                    img["is_dummy_alt"] = False
                updated += 1
                
        save_alt_mapping(self.mapping)
        return {
            "success": True,
            "total_images": len(images),
            "optimized_count": updated,
            "mapping": self.mapping,
            "message": f"Successfully generated high-ranking SEO alt tags for {updated} images!"
        }

alt_manager = AltTextManager()
generate_smart_alt = alt_manager.generate_smart_alt
