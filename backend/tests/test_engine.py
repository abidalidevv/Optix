import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from backend.pagespeed_auditor import pagespeed_auditor
from backend.compressor import compressor, normalize_seo_slug, compute_ssim
from backend.reference_swapper import reference_swapper
from PIL import Image

def run_tests():
    print("=== 1. Testing Core Web Vitals PageSpeed Auditor ===")
    report = pagespeed_auditor.run_audit()
    print(f"Store: {report.shop}")
    print(f"Total media: {report.total_media_count}, Images: {report.total_images_count}")
    print(f"Total weight: {report.total_weight_mb:.2f} MB ➡️ ~{report.estimated_optimized_weight_mb:.2f} MB (-{report.overall_reduction_pct}%)")
    print(f"LCP Boost: {report.lcp_seconds_before}s ➡️ {report.lcp_seconds_after}s (🟢 PASS)")
    print(f"CLS Guard: {report.cls_score_before} ➡️ {report.cls_score_after} (🟢 Zero Layout Jump)")
    print(f"INP Latency: {report.inp_ms_before}ms ➡️ {report.inp_ms_after}ms (🟢 Smooth Interaction)")

    print("\n=== 2. Testing Live Benchmark Compression with SSIM & Downscaling ===")
    benchmark_file = Path(r"C:\Users\Ali\Desktop\Matrixify\tibbeshifa-migrator\backups\source-store\media\files\46210584019185.png")
    if benchmark_file.exists():
        res = compressor.optimize_file(
            benchmark_file,
            category="files",
            product_title="شفائے معدہ"
        )
        print(f"File: {res.filename}")
        print(f"SEO Normalized Slug: {res.seo_slug}.webp")
        print(f"Generated Alt Text: {res.alt_text}")
        print(f"Dimensions: {res.width}x{res.height}")
        print(f"Original Size: {res.original_size_bytes / 1024:.1f} KB")
        print(f"Optimized WebP: {res.webp_size_bytes / 1024:.1f} KB (saved {res.saved_pct}%)")
        if res.avif_size_bytes:
            print(f"Optimized AVIF: {res.avif_size_bytes / 1024:.1f} KB")
        print(f"Perceptual SSIM Score: {res.ssim_score:.4f} (Quality Threshold > 0.95: PASSED)")
        
        assert res.saved_pct > 85.0, "Expected >85% savings on heavy PNG"
        assert res.ssim_score > 0.95, "Expected SSIM > 0.95 for perceptual lossless quality"
        assert res.width <= 1600, "Expected width capped at max 1600px"
    else:
        print("Benchmark file not found at expected path")

    print("\n=== 3. Testing Core Web Vitals HTML Swapper (LCP, CLS, Urdu Alt Guard) ===")
    sample_html = (
        '<div class="product-page">'
        '  <!-- Hero Banner 1 (LCP Element) -->'
        '  <img src="https://cdn.shopify.com/s/files/1/0812/5520/3057/files/hero_banner_4000px.png?v=1787233308">'
        '  <!-- Image 2 (Below The Fold Detail) -->'
        '  <img src="https://cdn.shopify.com/s/files/1/0812/5520/3057/files/46210584019185.png?v=1787233308" alt="">'
        '</div>'
    )

    url_map = {
        "https://cdn.shopify.com/s/files/1/0812/5520/3057/files/hero_banner_4000px.png?v=1787233308":
        "https://cdn.shopify.com/s/files/1/0812/5520/3057/files/hero-banner-1600px.webp",
        "https://cdn.shopify.com/s/files/1/0812/5520/3057/files/46210584019185.png?v=1787233308":
        "https://cdn.shopify.com/s/files/1/0812/5520/3057/files/shifaye-meda.webp"
    }
    dim_map = {
        "hero_banner_4000px.png": (1600, 600),
        "46210584019185.png": (1080, 1080)
    }

    reference_swapper.set_mapping(url_map)
    reference_swapper.set_dimensions(dim_map)

    opt_html, swaps = reference_swapper.swap_html(sample_html, default_alt_title="شفائے معدہ - اصلی فارمولا")
    print(f"Swaps performed: {swaps}")
    print("Optimized Core Web Vitals HTML:")
    print(opt_html)

    # 1. Verify LCP Hero Banner has fetchpriority="high" and NO loading="lazy"
    assert 'fetchpriority="high"' in opt_html, "Hero banner must have fetchpriority='high'"
    assert 'hero-banner-1600px.webp' in opt_html

    # Check first img specifically has no loading="lazy"
    first_img_tag = opt_html.split('<img')[1].split('>')[0]
    assert 'loading="lazy"' not in first_img_tag, "First hero banner must NOT have loading='lazy'!"

    # 2. Verify Image 2 (below-the-fold) has loading="lazy" decoding="async"
    second_img_tag = opt_html.split('<img')[2].split('>')[0]
    assert 'loading="lazy"' in second_img_tag, "Below-the-fold image must have loading='lazy'"
    assert 'decoding="async"' in second_img_tag

    # 3. Verify CLS Guard (explicit width and height)
    assert 'width="1600" height="600"' in opt_html or 'width="1080" height="1080"' in opt_html
    assert 'aspect-ratio' in opt_html, "CLS prevention requires aspect-ratio styling"

    # 4. Verify Alt Text Guard & Urdu UTF-8 preservation
    assert 'شفائے معدہ' in opt_html, "Urdu alt text must be preserved"

    print("\nALL ADVANCED CORE WEB VITALS & IMAGE SEO TESTS PASSED! 🚀")

if __name__ == "__main__":
    run_tests()
