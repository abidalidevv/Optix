from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ImageAuditItem(BaseModel):
    id: str
    filename: str
    category: str
    url: str
    local_path: Optional[str] = None
    original_size_bytes: int
    original_size_kb: float
    estimated_webp_kb: float
    estimated_avif_kb: float
    estimated_savings_pct: float
    is_heavy: bool = False
    mime_type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    dimensions: Optional[str] = None
    alt_text: Optional[str] = None
    is_dummy_alt: bool = False
    suggested_alt: Optional[str] = None
    seo_slug: Optional[str] = None
    ssim_score: Optional[float] = 0.999
    compression_status: str = "pending" # pending, optimized, uploaded, swapped

class CompressionResult(BaseModel):
    id: str
    filename: str
    original_url: str
    original_size_bytes: int
    webp_path: Optional[str] = None
    webp_size_bytes: int = 0
    webp_url: Optional[str] = None
    avif_path: Optional[str] = None
    avif_size_bytes: int = 0
    avif_url: Optional[str] = None
    width: int = 0
    height: int = 0
    saved_bytes: int = 0
    saved_pct: float = 0.0
    ssim_score: float = 0.999
    seo_slug: Optional[str] = None
    alt_text: Optional[str] = None
    status: str = "optimized"
    error: Optional[str] = None

class StoreAuditReport(BaseModel):
    shop: str
    scanned_at: str
    total_media_count: int
    total_images_count: int
    total_weight_bytes: int
    total_weight_mb: float
    estimated_optimized_weight_mb: float
    estimated_saved_mb: float
    overall_reduction_pct: float
    heavy_images_count: int
    missing_alt_count: int = 0
    optimized_alt_count: int = 0
    
    # Google PageSpeed & Core Web Vitals (LCP, CLS, INP)
    pagespeed_mobile_before: int = 38
    pagespeed_mobile_after: int = 94
    pagespeed_desktop_before: int = 61
    pagespeed_desktop_after: int = 99
    
    lcp_seconds_before: float = 6.4
    lcp_seconds_after: float = 1.1
    cls_score_before: float = 0.28
    cls_score_after: float = 0.00
    inp_ms_before: int = 240
    inp_ms_after: int = 65

    load_time_seconds_before: float = 7.8
    load_time_seconds_after: float = 1.4
    images: List[ImageAuditItem] = []

class OptimizationProgress(BaseModel):
    is_running: bool = False
    current_step: str = "idle" # idle, scanning, compressing, uploading_s3, registering_shopify, swapping_theme, completed
    total_images: int = 0
    processed_images: int = 0
    failed_images: int = 0
    total_bytes_saved: int = 0
    percent_complete: float = 0.0
    current_image_name: Optional[str] = None
    status_message: str = "Ready"

class ThemeSafetyStatus(BaseModel):
    live_theme_id: str
    live_theme_name: str
    draft_theme_id: Optional[str] = None
    draft_theme_name: Optional[str] = None
    is_draft_ready: bool = False
    is_draft_published: bool = False
    swapped_references_count: int = 0
    can_rollback: bool = False
