import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
import logging

from backend.config import DATA_DIR, settings

logger = logging.getLogger("optix.alt_text")

ALT_OVERRIDES_FILE = DATA_DIR / "alt_text_overrides.json"

# Curated bilingual medical & product dictionary for Tibbe Shifa catalog
KNOWN_HERBAL_PRODUCTS = {
    "46210618523889": "Nijaat Likoria (نجات لیکوریا) - Women Health & Vitality Herbal Formulation | Tibbe Shifa",
    "46210584019185": "Nijaat Dublepan (نجات دبلپن) - Natural Weight Gain & Muscle Vitality Herbal Tonic | Tibbe Shifa",
    "46210583986417": "Shifa-e-Meda (شفائے معدہ) - Herbal Stomach Acid, Gas & Digestion Relief Powder | Tibbe Shifa",
    "46210583953649": "Qabz Kusha (قبض کشا) - Natural Constipation Relief & Gut Health Powder | Tibbe Shifa",
    "46210583920881": "Sugar Care (شوگر کیئر) - Blood Sugar & Glucose Support Herbal Formulation | Tibbe Shifa",
    "46210583888113": "Nijaat Bawasir (نجات بواسیر) - Herbal Hemorrhoids Piles Relief Capsule | Tibbe Shifa",
    "46210583855345": "Nijaat Jaryan (نجات جریان) - Men Physical Strength & Stamina Herbal Tonic | Tibbe Shifa",
    "46348966297841": "Nijaat Bawasir Piles Capsule Packaging - Tibbe Shifa",
    "46348966265073": "Tibbe Shifa Herbal Formula Composition Guide",
    "46348966330609": "Tibbe Shifa Official Pure Herbal Seal & Logo",
    "46348967444721": "Hakim Riaz Ahmad Bhatti Certified Herbal Expert - Tibbe Shifa",
}

GENERIC_TERMS = {
    "image", "photo", "picture", "untitled", "test", "temp", "banner", 
    "placeholder", "screenshot", "graphic", "asset", "file"
}

def load_alt_overrides() -> Dict[str, str]:
    if ALT_OVERRIDES_FILE.exists():
        try:
            with open(ALT_OVERRIDES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading alt overrides: {e}")
    return {}

def save_alt_overrides(overrides: Dict[str, str]):
    try:
        with open(ALT_OVERRIDES_FILE, "w", encoding="utf-8") as f:
            json.dump(overrides, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error saving alt overrides: {e}")

def is_dummy_alt(alt: str) -> bool:
    """Detects if an alt text is empty, a numeric ID, or a generic placeholder."""
    if not alt or not alt.strip():
        return True
    
    clean = alt.strip()
    
    # Check if purely digits (e.g. "46210618523889")
    if re.match(r"^\d+$", clean):
        return True
    
    # Check if pattern is "{digits} - Tibbe Shifa" (dummy fallback from old auditor)
    if re.match(r"^\d+\s*-\s*Tibbe\s*Shifa$", clean, re.IGNORECASE):
        return True
        
    # Check if contains file extension (e.g. "46210618523889.png", "hero.jpg")
    if re.search(r"\.(png|jpg|jpeg|webp|avif|gif)$", clean, re.IGNORECASE):
        return True
        
    # Check if generic term
    lower = clean.lower()
    if lower in GENERIC_TERMS:
        return True
        
    return False

def generate_seo_alt_text(filename: str, category: str = "files", existing_alt: str = "") -> str:
    """Generates clean, descriptive, high-ranking Google SEO alt text for any image."""
    stem = Path(filename).stem
    
    # 1. Check curated herbal catalog dictionary by stem
    if stem in KNOWN_HERBAL_PRODUCTS:
        return KNOWN_HERBAL_PRODUCTS[stem]
        
    # 2. Check for theme / UI patterns
    lower_name = stem.lower()
    if "logo" in lower_name:
        return "Tibbe Shifa Official Brand Logo - Authentic Herbal Health Remedies"
    if any(k in lower_name for k in ["banner", "hero", "slider"]):
        return "Tibbe Shifa Storefront Hero Banner - Authentic Natural Herbal Solutions"
    if any(k in lower_name for k in ["review", "rating", "star"]):
        return "Tibbe Shifa Verified Customer Reviews & 5-Star Quality Rating Badge"
    if any(k in lower_name for k in ["trust", "guarantee", "badge"]):
        return "100% Pure Herbal Ingredients Certified Guarantee Badge - Tibbe Shifa"
    if any(k in lower_name for k in ["delivery", "shipping", "cod"]):
        return "Fast Nationwide Cash on Delivery Available Across Pakistan - Tibbe Shifa"
        
    # 3. Clean filename words
    cleaned = re.sub(r"[-_]+", " ", stem).strip()
    # Remove leading/trailing numbers if attached to words
    cleaned = re.sub(r"^\d+\s*", "", cleaned)
    cleaned = re.sub(r"\s*\d+$", "", cleaned)
    
    if cleaned and not re.match(r"^\d+$", cleaned) and len(cleaned) > 2:
        return f"{cleaned.title()} - Tibbe Shifa Herbal Products"
        
    # 4. Contextual fallback by category
    if category == "products":
        return "Tibbe Shifa Natural Herbal Supplement Catalog Product Media"
    elif category == "collections":
        return "Tibbe Shifa Natural Herbal Health Collections & Remedies"
    elif category == "theme-assets":
        return "Tibbe Shifa Authentic Storefront Visual Media"
        
    return "Tibbe Shifa Authentic Herbal Healthcare & Natural Wellness Media"
