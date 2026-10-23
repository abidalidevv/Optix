import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OPTIMIZED_DIR = BASE_DIR / "optimized"
OPTIMIZED_DIR.mkdir(exist_ok=True)

class Settings(BaseModel):
    # Shopify Store Configuration
    shop: str = os.getenv("SHOPIFY_SHOP", "ph0igg-jv.myshopify.com")
    client_id: str = os.getenv("SHOPIFY_CLIENT_ID", "")
    client_secret: str = os.getenv("SHOPIFY_CLIENT_SECRET", "")
    admin_token: str = os.getenv("SHOPIFY_ADMIN_TOKEN", "")
    api_version: str = "2024-10"

    # Local Source Media Baseline (TibbeShifa backup)
    source_media_dir: Path = Path(r"C:\Users\Ali\Desktop\Matrixify\tibbeshifa-migrator\backups\source-store\media")
    source_manifest_path: Path = Path(r"C:\Users\Ali\Desktop\Matrixify\tibbeshifa-migrator\backups\source-store\manifests\media-manifest.json")
    source_theme_dir: Path = Path(r"C:\Users\Ali\Desktop\Matrixify\tibbeshifa-migrator\backups\source-store\theme")

    # Optimization Parameters (Google Core Web Vitals & Scientific SEO Standard)
    quality_webp: int = 82
    quality_avif: int = 74
    effort_webp: int = 6
    effort_avif: int = 4
    strip_metadata: bool = True
    inject_lazy_loading: bool = True
    inject_async_decoding: bool = True
    inject_fetchpriority_hero: bool = True
    enforce_cls_dimensions: bool = True
    auto_generate_alt_tags: bool = True
    normalize_seo_slugs: bool = True

    # Maximum Dimension Caps (Downscaling Rules)
    max_width_banner: int = 1600
    max_width_product: int = 1200
    max_width_thumbnail: int = 800

    # Leaky Bucket Rate Limiter
    max_bucket_size: int = 1000
    restore_rate_per_sec: int = 50
    concurrency_limit: int = 5

    # Storage paths
    mapping_file: Path = DATA_DIR / "url_mapping.json"
    audit_file: Path = DATA_DIR / "audit_cache.json"

settings = Settings()
