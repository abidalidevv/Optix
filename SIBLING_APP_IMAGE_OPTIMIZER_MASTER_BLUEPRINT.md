# ⚡ SIBLING APP MASTER BLUEPRINT: SHOPIFY IMAGE COMPRESSION & PAGESPEED ENGINE

> **Project Code Name:** Optix / Compreso (Sibling of Clonix)  
> **Source Store Baseline:** `ph0igg-jv.myshopify.com` (tibbeshifa.com)  
> **Target Goal:** Autonomous lossy/lossless image optimization, WebP/AVIF conversion, URL remapping, and Google PageSpeed Insights acceleration for Shopify stores.  
> **Date:** October 2026

---

## 1. BRAND IDENTITY & NAME SUGGESTIONS

Since Clonix is a punchy, enterprise-style name ending in **"-ix"**, here are tailored brand names for its sibling:

| Name | Vibe / Pitch | Fit |
|---|---|---|
| **Optix** *(Recommended)* | Clean, premium, matches "Clonix" perfectly (*"Clonix & Optix by Clonix Labs"*). Represents optical clarity and speed optimization. | ⭐️⭐️⭐️⭐️⭐️ (Best Match) |
| **Compreso** | As suggested by you! Intuitive, European SaaS feel, instantly communicates file size reduction. | ⭐️⭐️⭐️⭐️⭐️ |
| **Pressix** | Short, modern developer branding ("Compress + Matrix"). | ⭐️⭐️⭐️⭐️ |
| **Velocix** | Rooted in Velocity / Speed; emphasizes PageSpeed Lighthouse score boost. | ⭐️⭐️⭐️⭐️ |
| **TinyPix AI** | Direct competitor vibe to TinyIMG and TinyPNG. | ⭐️⭐️⭐️ |

---

## 2. OLD STORE BASELINE & LIVE BENCHMARK (REAL DATA FROM CLONIX)

Clonix has already extracted and verified the complete physical media archive of `ph0igg-jv.myshopify.com`:

### 📊 Baseline Store Metrics:
* **Total Media Assets:** 533 files (399.84 MB total disk footprint)
* **Total Image Assets:** **528 image files**
* **Total Image Weight:** **243.08 MB**
* **The Culprit:** Heavy, uncompressed PNG banners and WhatsApp JPG photos taking **2.4 MB – 2.6 MB each**.

### 🧪 Live Benchmark Test (Tested on Store File `files/46210584019185.png`):
| Format | File Size | Size Reduction | Visual Quality |
|---|---|---|---|
| **Original PNG** | `2,598.8 KB` (~2.6 MB) | Baseline (0%) | 100% |
| **Optimized WebP (Quality 82)** | `236.5 KB` | **-90.9% reduction** | Indistinguishable from PNG |
| **Optimized AVIF (Quality 75)** | `220.9 KB` | **-91.5% reduction** | Indistinguishable from PNG |

> 🚀 **Overall Store Impact:**  
> Compressing all 528 images will reduce store weight from **243 MB down to ~23 MB** — eliminating **~220 MB of redundant payload** from mobile network transfers.

---

## 3. COMPETITOR TEARDOWN & REVENUE MODEL

### Key Competitors on Shopify App Store:
1. **TinyIMG (Shopify Speed & Image Optimizer):**
   * *Pricing:* $9.99/mo (1,000 images/mo) up to $19.99/mo (3,000 images/mo).
   * *Features:* WebP conversion, image compression, SEO metadata generator, broken link checker.
2. **Crush.pics:**
   * *Pricing:* $4.99/mo (500MB) up to $19.99/mo (2GB).
   * *Features:* Automated background compression, original backup retention.
3. **Booster Apps Image Optimizer:**
   * *Pricing:* $19.99/mo unlimited.
   * *Features:* Alt-tag sync, image compression.

### Our Competitive Advantage (What Makes Optix / Compreso Superior):
1. **True Dual Modern Formats (WebP + AVIF):** Most apps only do WebP. We support next-gen AVIF (saving an extra 10–15% over WebP).
2. **In-Place Liquid & HTML Swapping:** Rather than relying only on redirect proxies, we update the real `<img>` tags in product descriptions and theme settings with `loading="lazy"` and `decoding="async"`.
3. **Multilingual & Urdu Support:** Native UTF-8 support ensures Urdu titles (`شفائے معدہ`) and handles are never broken or escaped into ugly `%D8%B4...` strings.
4. **1-Click Theme Safety Rollback:** Zero risk of breaking store layout by working on a duplicate draft theme before publishing.

---

## 4. TECHNICAL ARCHITECTURE FOR THE NEW APP

```
   ┌───────────────────────────────────────────────────────────────┐
   │                  OPTIX / COMPRESO ENGINE                      │
   └───────────────────────────────┬───────────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
 [1. BATCH PROCESSOR]      [2. SHOPIFY UPLOADER]     [3. REFERENCE SWAPPER]
 • Scans Store Media       • StagedUploadsCreate     • Scans Theme Liquid
 • Lossless/Lossy Engine   • Direct Binary S3 PUT    • Scans Product HTML
 • WebP & AVIF output      • FileCreate Mutation     • Replaces src URLs
 • Generates swap map      • Gets New Shopify URLs   • Adds lazy loading
```

### Module 1: Compression Engine (`compressor.py` / `compressor.ts`)
* Uses Python `Pillow 12.3.0` (which has native WebP & AVIF support enabled on your system) or Node.js `sharp`.
* Preserves image dimensions while stripping bloated metadata (camera EXIF, thumbnails, color profiles).
* Converts images:
  * For WebP: Quality `82`, Method `6` (highest compression effort).
  * For AVIF: Quality `75`, Effort `4`.

### Module 2: Shopify GraphQL Staged Upload Pipeline
To add compressed files into Shopify without browser interaction:
1. **Mutation `stagedUploadsCreate`:**
   ```graphql
   mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
     stagedUploadsCreate(input: $input) {
       stagedTargets {
         url
         resourceUrl
         parameters {
           name
           value
         }
       }
       userErrors {
         field
         message
       }
     }
   }
   ```
2. **Binary Multi-Part POST:** Send the compressed WebP/AVIF file to the target URL provided by Shopify.
3. **Mutation `fileCreate`:**
   ```graphql
   mutation fileCreate($files: [FileCreateInput!]!) {
     fileCreate(files: $files) {
       files {
         id
         alt
         createdAt
         fileStatus
         ... on MediaImage {
           image {
             url
             width
             height
           }
         }
       }
       userErrors {
         field
         message
       }
     }
   }
   ```

### Module 3: URL Swapper & Theme Accelerator
Once new URLs are generated, the engine swaps them in 3 key places:
1. **Theme Settings (`config/settings_data.json`):** Replaces banner IDs and hero image paths.
2. **Product Descriptions (`descriptionHtml`):**
   * Finds `<img [^>]*src="([^"]+)"[^>]*>`
   * Swaps old CDN URL with new WebP URL.
   * Injects `loading="lazy" decoding="async"` if missing.
3. **Liquid Templates:** Replaces hardcoded image references in section files.

---

## 5. CRITICAL CHALLENGES & MITIGATION STRATEGIES

| # | Challenge | Risk | Mitigation Strategy |
|---|---|---|---|
| **1** | **Theme Breakage** | Replacing an image might break desktop/mobile layout or slider aspect ratio. | Never mutate the live theme directly! Always call `themeCreate` to duplicate the live theme as `[Optix] Speed-Optimized Theme`, apply changes there, test, then publish. |
| **2** | **Shopify GraphQL Throttling** | Uploading 528 images at once will hit the 50 points/sec rate limit. | Implement a leaky-bucket queue with 5 concurrent workers and 250ms sleep delays between requests. |
| **3** | **Browser Fallbacks for AVIF** | Older iOS or Safari browsers (<16.4) might not render AVIF properly. | Use WebP as the primary universal format (99.8% browser support worldwide), or use `<picture><source type="image/avif"><img></picture>` markup. |
| **4** | **Urdu & Non-ASCII Handles** | Urdu product names (`شفائے-معدہ`) might get mangled during URL replacement. | Use `decodeURIComponent` before matching and `encodeURI` when outputting HTML links. |
| **5** | **Cache Invalidation** | Merchants might still see the old image due to browser caching. | Append a version query parameter (e.g. `?v=1787233308`) or use Shopify's freshly generated CDN URL. |

---

## 6. STARTER READY-TO-USE SCRIPTS

### Script A: Local Batch Compressor (`batch_compress.py`)
```python
import os
from PIL import Image

def optimize_image(src_path, dest_dir, quality_webp=82, quality_avif=75):
    os.makedirs(dest_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    
    with Image.open(src_path) as img:
        # Convert RGBA to RGB if saving without alpha channel
        if img.mode in ('RGBA', 'LA') and not ('png' in src_path.lower() or 'webp' in src_path.lower()):
            img = img.convert('RGB')
            
        webp_path = os.path.join(dest_dir, f"{base_name}.webp")
        img.save(webp_path, "WEBP", quality=quality_webp, method=6)
        
        avif_path = os.path.join(dest_dir, f"{base_name}.avif")
        img.save(avif_path, "AVIF", quality=quality_avif)
        
        orig_sz = os.path.getsize(src_path)
        webp_sz = os.path.getsize(webp_path)
        avif_sz = os.path.getsize(avif_path)
        
        return {
            "file": base_name,
            "orig_kb": orig_sz / 1024,
            "webp_kb": webp_sz / 1024,
            "avif_kb": avif_sz / 1024,
            "saved_pct": (1 - (webp_sz / orig_sz)) * 100
        }
```

### Script B: HTML Image Reference Swapper (`html_swapper.py`)
```python
import re

def swap_images_in_html(html_content, url_map):
    """
    Replaces old image URLs with new compressed URLs and ensures lazy loading.
    url_map: dict of { "old_cdn_url": "new_cdn_url" }
    """
    def replacer(match):
        img_tag = match.group(0)
        src = match.group(1)
        
        new_src = url_map.get(src, src)
        new_tag = img_tag.replace(src, new_src)
        
        if 'loading=' not in new_tag:
            new_tag = new_tag.replace('<img', '<img loading="lazy" decoding="async"')
            
        return new_tag

    pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>')
    return pattern.sub(replacer, html_content)
```

---

## 7. STEP-BY-STEP WORKFLOW FOR YOUR NEW PROJECT FOLDER

When you create your new folder (e.g. `Desktop/Compreso` or `Desktop/Optix`) and open a new session:

1. **Step 1:** Copy this file (`SIBLING_APP_IMAGE_OPTIMIZER_MASTER_BLUEPRINT.md`) into your new project directory.
2. **Step 2:** Point the new app to the existing downloaded images in `Matrixify/tibbeshifa-migrator/backups/source-store/media` (or run live extraction from `ph0igg-jv.myshopify.com`).
3. **Step 3:** Run the batch compression engine to generate all WebP/AVIF assets in an `optimized/` folder.
4. **Step 4:** Build the clean Shopify UI (Dashboard showing: Total Images, MBs Saved, Speed Score Boost, and a 1-Click "Optimize All" button).
5. **Step 5:** Test on the old store by creating a draft duplicate theme first to guarantee 0% risk.
