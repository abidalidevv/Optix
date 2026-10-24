import json
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import logging

from backend.config import DATA_DIR, settings

logger = logging.getLogger("optix.alt_text")

ALT_MAPPING_FILE = DATA_DIR / "alt_text_mapping.json"

# Known High-Fidelity Product Mapping for TibbeShifa Catalog
PRODUCT_KNOWLEDGE = {
    # Nijaat Likoria
    "46210618523889": "Nijaat Likoria (نجات لیکوریا) - Women Health & Vitality Herbal Capsule | Tibbe Shifa",
    # Nijaat Dublepan
    "46210584019185": "Nijaat Dublepan (نجات دبلپن) - Natural Weight Gain & Muscle Vitality Herbal Tonic | Tibbe Shifa",
    # Shifa-e-Meda
    "46210583986417": "Shifa-e-Meda (شفائے معدہ) - Herbal Stomach Acid, Gas & Digestion Relief Powder | Tibbe Shifa",
    # Qabz Kusha
    "46210583953649": "Qabz Kusha (قبض کشا) - Natural Constipation Relief & Gut Health Powder | Tibbe Shifa",
    # Sugar Care
    "46210583920881": "Sugar Care (شوگر کیئر) - Blood Sugar & Glucose Support Herbal Formulation | Tibbe Shifa",
    # Nijaat Bawasir
    "46210583888113": "Nijaat Bawasir (نجات بواسیر) - Herbal Hemorrhoids & Piles Relief Capsule | Tibbe Shifa",
    "46348966297841": "Nijaat Bawasir (نجات بواسیر) - Ayurvedic Piles Care Herbal Formulation | Tibbe Shifa",
    # Nijaat Jaryan
    "46210583855345": "Nijaat Jaryan (نجات جریان) - Men Physical Strength & Stamina Herbal Tonic | Tibbe Shifa",
    # Branding & Key Assets
    "TIBBE_SHIFA": "Tibbe Shifa Official Brand Logo - Pure Herbal Health Solutions",
    "riazahmadbhatti": "Hakeem Riaz Ahmad Bhatti - Head Herbalist at Tibbe Shifa Laboratories",
    "ChatGPT_Image": "Tibbe Shifa Laboratory Natural Herbal Botanical Ingredients",
    "bc3b4fae8cb250b8f7d992fe19938121": "Tibbe Shifa Natural Herbal Capsules Bottle Product Packaging"
}

# Generic words that indicate dummy or unoptimized alt text
DUMMY_KEYWORDS = {
    "untitled", "image", "img", "photo", "picture", "file", "test", "temp",
    "screenshot", "banner", "thumbnail", "asset", "dsc", "null", "none"
}

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

def is_dummy_alt(alt: Optional[str], filename: str) -> bool:
    """Detects if an alt text is missing, generic, or dummy."""
    if not alt or not alt.strip():
        return True
    
    clean = alt.strip().lower()
    
    # Check if purely numbers or numbers with simple suffix like '46210618523889 - Tibbe Shifa'
    if re.match(r"^\d+[\s\-_]*(tibbe[\s\-_]*shifa)?$", clean):
        return True
    
    # Check if equal to filename
    stem = Path(filename).stem.lower()
    if clean == stem or clean == filename.lower():
        return True
        
    # Check if only generic dummy word
    words = set(re.findall(r"\b[a-z0-9]+\b", clean))
    if words and words.issubset(DUMMY_KEYWORDS):
        return True
        
    return False

def generate_smart_alt(filename: str, category: str = "files", existing_alt: Optional[str] = None) -> str:
    """Generates a high-ranking, descriptive SEO alt tag based on product knowledge and clean heuristics."""
    stem = Path(filename).stem
    
    # 1. Direct Knowledge Base Match
    for key, smart_text in PRODUCT_KNOWLEDGE.items():
        if key in stem or key == stem:
            return smart_text
            
    # 2. Check existing non-dummy text
    if existing_alt and not is_dummy_alt(existing_alt, filename):
        return existing_alt.strip()
        
    # 3. Clean keywords from filename
    # Remove leading/trailing numbers, hashes, timestamps
    cleaned_name = re.sub(r"^\d+[\-_]*", "", stem)
    cleaned_name = re.sub(r"[\-_]*\d+$", "", cleaned_name)
    cleaned_name = re.sub(r"[_\-]+", " ", cleaned_name).strip()
    
    # If cleaned name still has meaningful characters
    if cleaned_name and not re.match(r"^\d+$", cleaned_name) and len(cleaned_name) > 3:
        words = cleaned_name.title()
        if "tibbe" not in words.lower():
            return f"{words} - Natural Herbal Product | Tibbe Shifa"
        return f"{words} | Tibbe Shifa"
        
    # 4. Contextual Category Fallback
    cat_lower = category.lower()
    if "product" in cat_lower:
        return f"Tibbe Shifa Herbal Medicinal Supplement - Pure Organic Catalog Product"
    elif "review" in cat_lower or "testimonial" in cat_lower:
        return f"Verified Customer Review & Satisfaction Rating - Tibbe Shifa"
    elif "banner" in cat_lower or "hero" in cat_lower:
        return f"Tibbe Shifa Official Storefront Banner - 100% Herbal Natural Remedies"
    else:
        return f"Tibbe Shifa Authentic Herbal Health Solution - Catalog Media"

class AltTextManager:
    def __init__(self):
        self.mapping = load_alt_mapping()
        
    def get_alt(self, filename: str, fallback_alt: Optional[str] = None, category: str = "files") -> Tuple[str, bool]:
        """Returns (alt_text, is_optimized)."""
        if filename in self.mapping:
            return self.mapping[filename], True
            
        if fallback_alt and not is_dummy_alt(fallback_alt, filename):
            return fallback_alt, True
            
        smart = generate_smart_alt(filename, category, fallback_alt)
        return smart, False

    def set_alt(self, filename: str, alt_text: str):
        self.mapping[filename] = alt_text.strip()
        save_alt_mapping(self.mapping)

    def optimize_all(self, images: list) -> Dict[str, Any]:
        """Scans all images, replaces empty/dummy alt texts, and persists."""
        updated = 0
        for img in images:
            fn = getattr(img, "filename", None) or img.get("filename")
            cat = getattr(img, "category", "files") or img.get("category", "files")
            curr_alt = getattr(img, "alt_text", None) or img.get("alt_text")
            
            if is_dummy_alt(curr_alt, fn) or fn not in self.mapping:
                smart_alt = generate_smart_alt(fn, cat, curr_alt)
                self.mapping[fn] = smart_alt
                if hasattr(img, "alt_text"):
                    img.alt_text = smart_alt
                elif isinstance(img, dict):
                    img["alt_text"] = smart_alt
                updated += 1
                
        save_alt_mapping(self.mapping)
        return {
            "success": True,
            "total_images": len(images),
            "optimized_count": updated,
            "message": f"Successfully generated smart SEO alt tags for {updated} images!"
        }

alt_manager = AltTextManager()
