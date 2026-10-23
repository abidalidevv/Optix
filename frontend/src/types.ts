export interface ImageAuditItem {
  id: string;
  filename: string;
  category: string;
  url: string;
  local_path?: string;
  original_size_bytes: number;
  original_size_kb: number;
  estimated_webp_kb: number;
  estimated_avif_kb: number;
  estimated_savings_pct: number;
  is_heavy: boolean;
  mime_type?: string;
  width?: number;
  height?: number;
  dimensions?: string;
  alt_text?: string;
  seo_slug?: string;
  ssim_score?: number;
  compression_status: 'pending' | 'optimized' | 'uploaded' | 'swapped';
}

export interface StoreAuditReport {
  shop: string;
  scanned_at: string;
  total_media_count: number;
  total_images_count: number;
  total_weight_bytes: number;
  total_weight_mb: number;
  estimated_optimized_weight_mb: number;
  estimated_saved_mb: number;
  overall_reduction_pct: number;
  heavy_images_count: number;
  
  // Google PageSpeed & Core Web Vitals
  pagespeed_mobile_before: number;
  pagespeed_mobile_after: number;
  pagespeed_desktop_before: number;
  pagespeed_desktop_after: number;
  
  lcp_seconds_before: number;
  lcp_seconds_after: number;
  cls_score_before: number;
  cls_score_after: number;
  inp_ms_before: number;
  inp_ms_after: number;

  load_time_seconds_before: number;
  load_time_seconds_after: number;
  images: ImageAuditItem[];
}

export interface OptimizationProgress {
  is_running: boolean;
  current_step: 'idle' | 'scanning' | 'compressing' | 'uploading_s3' | 'registering_shopify' | 'swapping_theme' | 'completed';
  total_images: number;
  processed_images: number;
  failed_images: number;
  total_bytes_saved: number;
  percent_complete: number;
  current_image_name?: string;
  status_message: string;
}

export interface ThemeSafetyStatus {
  live_theme_id: string;
  live_theme_name: string;
  draft_theme_id?: string;
  draft_theme_name?: string;
  is_draft_ready: boolean;
  is_draft_published: boolean;
  swapped_references_count: number;
  can_rollback: boolean;
}

export interface SettingsConfig {
  shop: string;
  quality_webp: number;
  quality_avif: number;
  strip_metadata: boolean;
  inject_lazy_loading: boolean;
  inject_async_decoding: boolean;
  inject_fetchpriority_hero: boolean;
  enforce_cls_dimensions: boolean;
  auto_generate_alt_tags: boolean;
  normalize_seo_slugs: boolean;
  max_width_banner: number;
  max_width_product: number;
  sandbox_theme_guard: boolean;
}
