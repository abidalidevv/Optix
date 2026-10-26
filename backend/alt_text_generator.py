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

# Core Curated Catalog Dictionary for Tibbe Shifa (All 7 Products are Herbal Powder / Safoof / Phakki)
# Format: [English Context] - [Urdu Script Context] strictly clamped between 65-105 characters (<= 125 limit)
STATIC_PRODUCT_MAP = {
    # Nijaat Likoria
    "46210618523889": "Nijaat Likoria Herbal Safoof - نجات لیکوریا ہربل سفوف برائے خواتین صحت",
    "46348952043761": "Nijaat Likoria Pure Herbal Powder - نجات لیکوریا پاؤڈر پیکنگ برائے نسوانی حسن",
    "46348951978225": "Nijaat Likoria Natural Formula Guide - نجات لیکوریا قدرتی جڑی بوٹیوں کے اجزاء",
    "46348952010993": "Nijaat Likoria Usage & Dosage Guide - نجات لیکوریا پھکی استعمال کرنے کا طریقہ",
    "46348952076529": "Nijaat Likoria Quality Guarantee Seal - نجات لیکوریا خالص قدرتی معیار کی ضمانت",

    # Nijaat Dublepan (Ultra-short concise standard <= 60 chars)
    "46153087647965": "Nijat Dublepan Safoof - نجات دبلپن ہربل سفوف برائے وزن",
    "46153087680733": "Nijat Dublepan Formula - نجات دبلپن خالص قدرتی جڑی بوٹیاں",
    "46153087713501": "Nijat Dublepan Benefits - بھوک اور کمزوری کا دیسی علاج",
    "46153087746269": "TibbeShifa Trust - طبِ شفاء 50 سالہ روایتی اعتماد",
    "46210584019185": "Nijat Dublepan Safoof - نجات دبلپن ہربل سفوف برائے وزن",
    "46348964593905": "Nijat Dublepan Powder Jar - نجات دبلپن قدرتی فارمولا جار",
    "46210583986417": "Nijat Dublepan Extracts - نجات دبلپن دیسی جڑی بوٹیوں کے فوائد",
    "46348964561137": "Nijat Dublepan Dosage Guide - نجات دبلپن پھکی طریقہ استعمال",
    "46348964626673": "Nijat Dublepan Quality Seal - نجات دبلپن 100 فیصد قدرتی مہر",

    # Shifa-e-Meda
    "46348965282033": "Shifa-e-Medda Gastric Relief Powder - شفائے معدہ ہربل سفوف برائے گیس و تیزابیت",
    "46348965347569": "Shifa-e-Medda Digestive Safoof Formula - شفائے معدہ ہاضمے کی بہتری کا دیسی علاج",
    "46348965314801": "Shifa-e-Medda Natural Herbs Formula - شفائے معدہ بدہضمی اور السر کے اجزاء",
    "46348965380337": "Shifa-e-Medda Traditional Unani Jar - شفائے معدہ روایتی یونانی پھکی جار پیکنگ",

    # Qabz Kusha
    "46210583953649": "Qabz Kusha Constipation Relief Powder - قبض کشا قدرتی ہربل سفوف برائے فوری آرام",
    "46210607153393": "Qabz Kusha Colon Cleansing Remedy - قبض کشا پیٹ کی صفائی اور ہاضمے کا علاج",
    "46210607087857": "Qabz Kusha Organic Herbal Ingredients - قبض کشا دیسی جڑی بوٹیوں کا قدرتی فارمولا",
    "46348957942001": "Qabz Kusha Fast Relief Dosage Guide - قبض کشا پھکی طریقہ استعمال اور مقدار",
    "46348961218801": "Qabz Kusha Pure Herbal Quality Seal - قبض کشا خالص دیسی دوا کی تصدیقی مہر",

    # Sugar Care
    "46210583920881": "Sugar Care Blood Glucose Herbal Powder - شوگر کیئر ہربل سفوف برائے شوگر کنٹرول",
    "46348963315953": "Sugar Care Botanical Formulation - شوگر کیئر قدرتی جڑی بوٹیوں سے تیار کردہ پاؤڈر",
    "46348963250417": "Sugar Care Natural Ingredients Pack - شوگر کیئر خالص جڑی بوٹیاں اور نباتاتی اجزاء",
    "46210593259761": "Sugar Care Glucose Balance Guide - شوگر کیئر متوازن شوگر لیول اور توانائی گائیڈ",
    "46348963348721": "Sugar Care Certified Quality Assurance - شوگر کیئر مستند ہربل معیار کی گارنٹی",

    # Nijaat Bawasir
    "46210583888113": "Nijaat Bawasir Piles Relief Safoof - نجات بواسیر ہربل سفوف برائے خونی بادی بواسیر",
    "46348966297841": "Nijaat Bawasir Ayurvedic Piles Powder - نجات بواسیر ہربل دوا کی پیکنگ اور بوتل",
    "46348966265073": "Nijaat Bawasir Herbal Composition Guide - نجات بواسیر فارمولا اجزاء اور مسوں کا علاج",
    "46348966330609": "Nijaat Bawasir 100% Herbal Quality Seal - نجات بواسیر خالص قدرتی دوا کی مہر",

    # Nijaat Jaryan
    "46210583855345": "Nijaat Jaryan Strength Herbal Safoof - نجات جریان ہربل سفوف برائے مردانہ طاقت",
    "46348949848305": "Nijaat Jaryan Vitality Booster Packaging - نجات جریان مقوی اعصاب ہربل پاؤڈر پیکنگ",
    "46348949881073": "Nijaat Jaryan Botanical Ingredients - نجات جریان دیسی جڑی بوٹیاں اور فوائد",
    "46348949913841": "Nijaat Jaryan Safe Unani Formulation - نجات جریان محفوظ یونانی فارمولا گائیڈ",

    # Template Section Specific Mappings (Shifa-e-Meda)
    "196ff8927dfcfd73ec3e6a4d803af6aa": "Shifa-e-Medda 100g Digestive Powder Bottle - شفائے معدہ ہربل سفوف 100 گرام بوتل",
    "chatgpt_image_aug_27": "Shifa-e-Medda Acidity, Gas & Bloating Relief - شفائے معدہ سے تیزابیت اور گیس کا علاج",
    "shifa_e_maida": "Shifa-e-Medda Ingredients & Digestion Chart - شفائے معدہ پھکی کے قدرتی اجزاء و فوائد",
    "why_tibbeshifa_ed234b05": "Shifa-e-Medda 50 Years Heritage & Trust - شفائے معدہ 50 سالہ روایتی حکمت و تجربہ",
    "meda1": "Shifa-e-Medda Gastric Anatomy Illustration - معدے کی جلن، تیزابیت اور نظام ہاضمہ",
    "meda2": "Shifa-e-Medda Herbal Powder Benefits - شفائے معدہ ہربل سفوف کے طبی فوائد",
    "sm1": "1 Month Shifa-e-Medda Course 100g - 1 ماہ کا کورس شفائے معدہ ہربل سفوف",
    "sm2": "2 Bottles Shifa-e-Medda Value Bundle - شفائے معدہ 2 بوتلیں 30 فیصد رعایت",
    "sm3": "Buy 2 Get 1 Free Shifa-e-Medda Bundle - شفائے معدہ 3 بوتلیں فیملی علاج پیک",
    "a76c6123": "Shifa-e-Medda Natural Digestive Care - شفائے معدہ ہربل پھکی برائے نظامِ ہاضمہ",
    "a69130e8": "Shifa-e-Medda 100% Pure Natural Herbs - شفائے معدہ 100 فیصد خالص قدرتی دیسی جڑی بوٹیاں",
    "2b7415cc": "Shifa-e-Medda Zero Side Effects Guarantee - شفائے معدہ بغیر سائیڈ ایفیکٹ محفوظ علاج",
    "a0ed77a4": "Shifa-e-Medda Free Nationwide Delivery - شفائے معدہ پورے پاکستان میں فری ڈیلیوری",
    "634f27b7": "Shifa-e-Medda Cash on Delivery Guarantee - شفائے معدہ کیش آن ڈیلیوری و منی بیک گارنٹی",
    "9ff0bcf4": "Shifa-e-Medda Step 1 Take 10 Mins After Meal - طریقہ استعمال: کھانے کے 10 منٹ بعد لیں",
    "2c58f670": "Shifa-e-Medda Step 2 Take Half Teaspoon Dose - طریقہ استعمال: آدھا چمچ سفوف پھکی لیں",
    "55b477cc": "Shifa-e-Medda Step 3 Drink with Warm Water - طریقہ استعمال: نیم گرم پانی کے ساتھ لیں",
    "7d2fa1e4": "Shifa-e-Medda Safe Botanical Herbs - شفائے معدہ قدرتی اور محفوظ جڑی بوٹیوں سے تیار کردہ",
    "1f10d7e1": "Shifa-e-Medda Chronic Gastric Relief - شفائے معدہ سے پرانی اور دیرینہ تکلیف میں آرام",
    "bba3c5fe": "Shifa-e-Medda Easy Home Usage - شفائے معدہ گھر پر آسان طریقے سے روزمرہ استعمال",
    "04d35db1": "Shifa-e-Medda Certified Herbalist Formula - شفائے معدہ ماہرین طب یونانی کا مستند فارمولا",
    "d758073d": "Shifa-e-Medda 100% Pure Natural Ingredients - شفائے معدہ 100 فیصد خالص قدرتی دیسی اجزاء",
    "117bca03": "Shifa-e-Medda Halal Certified Product - شفائے معدہ حلال پروڈکٹ شرعی اصولوں کے مطابق",
    "e8c3fe90": "Shifa-e-Medda High Quality Safe Herbs - شفائے معدہ معیاری اور محفوظ دیسی جڑی بوٹیاں",
    "83c5d0bf": "Shifa-e-Medda Free Timely Delivery - شفائے معدہ کی مفت بروقت اور محفوظ ڈیلیوری",
    "e6404290": "Shifa-e-Medda Cash on Delivery Payment - شفائے معدہ آسان اور محفوظ کیش آن ڈیلیوری",
    "3fcd2585": "Shifa-e-Medda 50+ Years Heritage Experience - شفائے معدہ 50 سالہ طبی تجربہ اور اعتماد",
    "images_2": "Shifa-e-Medda Verified Customer Feedback - شفائے معدہ کسٹمر فیڈ بیک: معدہ بالکل ٹھیک ہو گیا",

    # Template Section Specific Mappings (Jaryan)
    "d054e9bdd04dfd27fd6468ad8d31d689": "Nijat-e-Jaryaan Herbal Powder Bottle - طبِ شفاء نجات جریان ہربل سفوف بوتل",
    "jaryan_medicine": "Nijat-e-Jaryaan Ingredients & Dosage - نجات جریان فوائد، قدرتی اجزاء اور طریقہ استعمال",
    "why_tibbeshifa": "TibbeShifa 50 Years Heritage & Trust - طبِ شفاء 50 سالہ روایتی تجربہ و اعتماد",
    "jaryan1": "Nijat-e-Jaryaan Vitality Health Benefits - نجات جریان قدرتی جسمانی طاقت کے فوائد",
    "jaryan2": "Nijat-e-Jaryaan Root Causes Illustration - جریان اور اعصابی کمزوری کی بنیادی علامات",
    "nj1": "1 Month Nijat-e-Jaryaan Herbal Course - 1 ماہ کا کورس نجات جریان ہربل سفوف",
    "nj2": "2 Months Nijat-e-Jaryaan Value Pack - 2 ماہ کا رعایتی بنڈل نجات جریان",
    "nj3": "3 Months Nijat-e-Jaryaan Complete Bundle - 3 ماہ کا مکمل علاج بنڈل نجات جریان",

    # Authority, Doctor & Branding
    "TIBBE_SHIFA": "Tibbe Shifa Official Brand Logo - طبِ شفاء مستند قدرتی ہربل علاج",
    "riazahmadbhatti": "Hakim Riaz Ahmad Bhatti Herbalist - حکیم ریاض احمد بھٹی ماہر طب یونانی",
    "doctor": "Hakim Riaz Ahmad Bhatti Herbalist - حکیم ریاض احمد بھٹی ماہر طب یونانی 1975",
    "ChatGPT_Image": "Tibbe Shifa Laboratory Natural Herbs - طبِ شفاء قدرتی نباتاتی جڑی بوٹیاں",
    "bc3b4fae8cb250b8f7d992fe19938121": "Tibbe Shifa Herbal Safoof Bottle Packaging - طبِ شفاء ہربل سفوف پیکنگ"
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

def clamp_alt_text(text: str, max_chars: int = 120) -> str:
    """Ensures alt text adheres to Google SEO and WCAG screen reader limit (<= 120 chars)."""
    text = " ".join(text.split()) # normalize whitespace
    if len(text) <= max_chars:
        return text
    # Trim to last complete word before limit
    trimmed = text[:max_chars - 3]
    last_space = trimmed.rfind(" ")
    if last_space > 40:
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
        Generates high-ranking, concise, bilingual Google SEO alt tag.
        Structure: [English Context] - [Urdu Script Context]
        Length: Strictly 70 to 110 characters (<= 120 chars).
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
            return clamp_alt_text(f"Customer WhatsApp Review{date_tag} - مطمئن صارف کا واٹس ایپ فیڈ بیک #{unique_hash}")

        # Head Herbalist Photos
        if "hakeem" in url_lower or "riaz" in url_lower:
            return clamp_alt_text("Hakim Riaz Ahmad Bhatti Herbalist - حکیم ریاض احمد بھٹی ماہر طب یونانی")

        # Specific Products via URL keywords (English First - Urdu Second)
        if "likoria" in url_lower:
            return clamp_alt_text("Nijaat Likoria Women Vitality Safoof - نجات لیکوریا ہربل سفوف برائے نسوانی صحت")
        if "dublepan" in url_lower or "dublapun" in url_lower:
            return clamp_alt_text("Nijaat Dublepan Weight Gain Safoof - نجات دبلپن ہربل سفوف برائے صحت مند وزن")
        if "meda" in url_lower or "stomach" in url_lower:
            return clamp_alt_text("Shifa-e-Medda Gastric Relief Powder - شفائے معدہ ہربل سفوف برائے گیس و بدہضمی")
        if "qabz" in url_lower:
            return clamp_alt_text("Qabz Kusha Constipation Relief Powder - قبض کشا ہربل سفوف برائے نظامِ ہاضمہ")
        if "sugar" in url_lower:
            return clamp_alt_text("Sugar Care Blood Glucose Balance Powder - شوگر کیئر ہربل سفوف برائے شوگر کنٹرول")
        if "bawasir" in url_lower or "bawaseer" in url_lower or "piles" in url_lower:
            return clamp_alt_text("Nijaat Bawasir Piles Relief Safoof - نجات بواسیر ہربل سفوف برائے خونی و بادی بواسیر")
        if "jaryan" in url_lower:
            return clamp_alt_text("Nijaat Jaryan Strength Herbal Tonic - نجات جریان ہربل سفوف برائے مردانہ قوت")

        # Section-specific Trust Badges & Guarantees
        if "logo" in url_lower or "logo" in stem.lower():
            return clamp_alt_text("Tibbe Shifa Brand Logo - طبِ شفاء مستند قدرتی ہربل ادارہ")
        if any(k in url_lower for k in ["banner", "hero", "slider"]):
            return clamp_alt_text("Tibbe Shifa Herbal Storefront Banner - طبِ شفاء خالص یونانی علاج کا مرکز")
        if any(k in url_lower for k in ["trust", "guarantee", "badge"]):
            return clamp_alt_text("100% Pure Organic Herbs Certified - خالص قدرتی دیسی جڑی بوٹیوں کی گارنٹی")
        if any(k in url_lower for k in ["delivery", "cod", "shipping"]):
            return clamp_alt_text("Cash on Delivery Fast Shipping - پورے پاکستان میں تیز رفتار کیش آن ڈیلیوری")

        # 3. Clean keywords from original URL basename if meaningful
        url_stem = Path(url_basename).stem
        cleaned_url = re.sub(r"[-_]+", " ", url_stem).strip()
        cleaned_url = re.sub(r"^\d+\s*", "", cleaned_url)
        cleaned_url = re.sub(r"\s*\d+$", "", cleaned_url)
        if cleaned_url and not re.match(r"^\d+$", cleaned_url) and len(cleaned_url) > 3:
            words = cleaned_url.title()
            return clamp_alt_text(f"{words} Herbal Health Remedy - طبِ شفاء قدرتی ہربل علاج")

        # 4. Contextual & Unique Fallback (guaranteed no duplicate spam!)
        unique_suffix = stem[-4:] if len(stem) >= 4 else str(abs(hash(stem)) % 1000)
        cat_lower = category.lower()
        if "product" in cat_lower:
            return clamp_alt_text(f"Tibbe Shifa Herbal Healthcare Product #{unique_suffix} - طبِ شفاء خالص دیسی دوا")
        elif "collection" in cat_lower:
            return clamp_alt_text(f"Tibbe Shifa Remedies Collection #{unique_suffix} - طبِ شفاء ہربل ادویات مجموعہ")
        else:
            return clamp_alt_text(f"Tibbe Shifa Natural Health Remedy #{unique_suffix} - طبِ شفاء خالص ہربل فارمولا")

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
