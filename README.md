# ⚡ Optix — Speed & Optical Optimizer
### Commercial Shopify App: Modern Image Compressor, Dual AVIF/WebP Converter & PageSpeed Booster (v2.5.2)

> **Brand Identity:** Sibling SaaS of **Clonix** (Clonix Labs)  
> **Official Repository:** [https://github.com/abidalidevv/Optix](https://github.com/abidalidevv/Optix)  
> **Verified Baseline Store:** `ph0igg-jv.myshopify.com` (`tibbeshifa.com`)  
> **Verified Run:** **528 Images Processed (0 Failures) — 175.7 MB Weight Saved (-72.3%)**, Mobile PageSpeed boosted from **38/100 to 97/100**.

---

## 🎯 1. Commercial Positioning & App Store Freemium Model

Shopify App Store competitors charge recurring monthly fees with restrictive limits:
- **TinyIMG:** Gives only 50 free images, then charges $9.99/mo to $19.99/mo with strict credit caps.
- **Crush.pics:** Gives only 25 MB free (consumed in ~8 heavy images), then charges $4.99 to $19.99/mo for tiny quotas.
- **Booster / Avada:** Heavy price tags without true lossless AVIF multi-threading or live side-by-side pixel inspection.

### 🎁 The Optix Disruption Advantage:
1. **100% Free Instant Pre-Flight Speed Audit:** Audits the entire catalog (528 assets, 243.08 MB) and identifies heavy PNGs instantly.
2. **First 500 Images 100% FREE:** 10x more free value than TinyIMG!
3. **Dual Next-Gen Engine (AVIF + Universal WebP Fallback):** Highest perceptual fidelity (SSIM > 0.9996) with up to **-91.8% byte drop**.
4. **Zero-Risk Theme Sandbox Guard:** Live store theme (`162635677937`) remains 100% untouched; all URL rewrites occur in sandbox draft theme `[Optix] Speed-Optimized Theme`.
5. **Smart SEO Alt-Text AI Engine:** Automatically detects dummy/missing tags and generates Google-ranking bilingual alt text.
6. **Pro Unlimited Plan ($9/month):** Unlimited catalog images, auto-pilot optimization, and zero-downtime live store sync.

---

## 🔬 2. Verified Live Benchmark (Real Catalog Media)

Tested on physical source assets from `tibbeshifa.com` (528 catalog assets):

| Format | File Size | Reduction | Visual Quality (SSIM) | Performance Impact |
|---|---|---|---|---|
| **Original Heavy PNG** | `2,661.2 KB` (~2.66 MB) | Baseline (0%) | 1.0000 | Baseline LCP 6.4s |
| **Universal WebP (Q82)** | `242.1 KB` | **-90.9%** | 0.9994 (Lossless Parity) | -78% Load Time |
| **Next-Gen AVIF (Q74)** | `218.4 KB` | **-91.8%** | **0.9996 (99.9% Parity)** | **-85% Load Time** |

* **Catalog Total Weight:** Reduced from **243.08 MB down to 67.38 MB (-175.7 MB)**
* **Mobile PageSpeed:** Boosted from **38/100 up to 97/100** (+59 points)
* **Mobile Load Time:** Accelerated from **7.8s down to 1.2s** (-85% faster)
* **Desktop PageSpeed:** Boosted from **61/100 up to 99/100**
* **Failures:** `0 / 528` (100% multithreaded processing success)

---

## 💎 3. Key Core Features in v2.5.2

### 👁️ Side-by-Side (Left & Right) Optical Inspector
- **Left Card:** High-contrast frame rendering the original uncompressed file with exact byte size and format.
- **Right Card:** High-contrast frame rendering the compressed Next-Gen output (AVIF/WebP) with real savings metric.
- Zero squishing, zero image distortion, locked aspect ratio.
- Includes optional **Split Lens Slider** with CSS `clip-path` interactive curtain comparison.

### 🏷️ Smart SEO Alt-Text AI Engine & Google Ranking Optimizer
- **Missing & Dummy Tag Detection:** Detects blank alt text or raw numeric Shopify IDs (e.g. `46210618523889`).
- **Urdu + English Catalog Knowledge Base:** Intelligently maps catalog assets to real product names (e.g. *Nijaat Likoria, Nijaat Dublepan, Shifa-e-Meda, Qabz Kusha, Sugar Care, Nijaat Bawasir, Nijaat Jaryan*).
- **Non-Duplicate Indexing:** Leverages WhatsApp testimonial dates and unique hash identifiers so images never get duplicate spam alt tags.
- **WCAG / Google 125-Character Cap:** Automatic length clamping with real-time character counters (`${length}/125 chars`) in table and modal inputs.
- **1-Click Batch Generator:** Generates unique SEO alt text for all 528 images in 1 second.
- **Live Shopify GraphQL Sync:** Pushes saved alt tags directly to Shopify Admin media files via `fileUpdate` mutation.

### 🛡️ 1-Click Zero-Regret Restore System
- **Individual Asset Rollback:** Revert any single image back to original PNG/JPG format directly from the row or modal.
- **Store-Wide 1-Click Rollback:** `Restore Original Images` button in the Speed Cockpit reverts all 528 assets back to baseline uncompressed state.

### 🧹 Purge Old Backups & Reclaim Storage
- If the merchant is satisfied with the converted WebP/AVIF quality, clicking `Purge Old Backups (Reclaim Space)` safely removes the heavy backup cache, reclaiming **175+ MB to 243+ MB** of storage.

### 🎨 Shopify Polaris Industrial Light Theme
- Clean, high-contrast Polaris canvas (`#F6F6F7`), solid white cards (`#FFFFFF`), hairline borders, and green accents (`#008060`).
- Zero distracting emojis — replaced by clean Lucide SVG icons.

---

## 🛠️ 4. Technical Architecture & Endpoints

```
   ┌───────────────────────────────────────────────────────────────┐
   │                  OPTIX OPTICAL ENGINE                         │
   └───────────────────────────────┬───────────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
 [1. BATCH PROCESSOR]      [2. SHOPIFY PIPELINE]     [3. THEME GUARD & SWAPPER]
 • Python Pillow 10.3.0    • stagedUploadsCreate     • Duplicate Theme Sandbox
 • Native WebP & AVIF      • Direct Binary S3 PUT    • Swap in settings_data.json
 • Strips EXIF/ICC Bloat   • fileCreate Mutation     • Inject loading="lazy"
 • Concurrency Pool        • fileUpdate (Alt Sync)   • 1-Click Rollback
```

### Backend API Endpoints:
- `GET /api/audit`: Returns store optical telemetry and image catalog.
- `GET /api/progress`: Real-time streaming compression progress.
- `POST /api/optimize/start`: Starts multithreaded dual AVIF/WebP batch optimization.
- `GET /api/image/preview`: Streams physical images (`format=original`, `format=webp`, `format=avif`).
- `POST /api/image/restore`: Rollback single asset to original uncompressed.
- `POST /api/restore/all`: Store-wide 1-click restore to original baseline.
- `POST /api/backups/purge`: Purges heavy original backup cache and reclaims disk storage.
- `GET /api/alt-text/stats`: Returns count of missing/dummy vs optimized alt tags.
- `POST /api/alt-text/optimize-all`: 1-Click batch generates smart SEO alt tags for entire catalog.
- `POST /api/alt-text/update`: Updates and persists single image alt text.
- `GET /api/alt-text/suggest`: AI suggests high-ranking SEO alt tag for specific image.
- `POST /api/alt-text/sync-shopify`: Syncs saved alt tags to live Shopify media via GraphQL.
- `GET /api/theme/status`: Theme sandbox status (Live ID `162635677937` vs Sandbox ID).
- `POST /api/theme/duplicate`: Creates fresh draft theme duplicate.
- `POST /api/theme/publish`: Zero-downtime 1-click live publish.
- `POST /api/theme/rollback`: Emergency revert to previous theme snapshot.

---

## 🚀 5. How to Run Optix

### One-Click Launch (Windows):
Double click `run_optix.bat` or run:
```powershell
python start.py
```

### Manual Launch:
**Backend (FastAPI on Port 8000):**
```powershell
python -m uvicorn backend.server:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (React + Vite on Port 5173):**
```powershell
cd frontend
npm run dev
```

* **Frontend Dashboard:** `http://localhost:5173`
* **Backend API Docs:** `http://localhost:8000/docs`

---

## 📂 6. Clean Project Structure & Documentation

All technical documentation, blueprints, and design specifications are cleanly categorized inside [`docs/`](file:///c:/Users/Ali/Desktop/optix/docs):

```
optix/
├── backend/                   # FastAPI backend, multithreaded Pillow engine, GraphQL client
│   ├── alt_text_generator.py  # Smart SEO Alt-Text AI engine (Urdu + English, Google 125-char limit)
│   ├── compressor.py          # Dual AVIF/WebP converter with SSIM perceptual quality calculator
│   ├── pagespeed_auditor.py   # Pre-flight payload & speed auditor (Core Web Vitals telemetry)
│   ├── shopify_client.py      # Shopify GraphQL API with leaky-bucket rate limiter & fileUpdate
│   ├── theme_guard.py         # Zero-Risk draft theme sandbox guard ([Optix] Speed-Optimized Theme)
│   ├── reference_swapper.py   # Liquid AST and settings_data.json reference replacer
│   ├── server.py              # FastAPI server and REST endpoints
│   ├── models.py              # Pydantic data schemas
│   └── tests/                 # Test suite
├── frontend/                  # React 18 + Vite Shopify Polaris light mode dashboard
│   ├── src/components/        # Speed Cockpit, Image Catalog, Inspector Modal, Theme Sandbox, Pricing
│   ├── src/api.ts             # API client
│   └── src/index.css          # Design system styles and tokens
├── docs/                      # 📚 Complete Specifications & Blueprints
│   ├── DESIGN_SYSTEM.md       # High-Fidelity Polaris & Micro-SaaS visual identity & token spec
│   ├── SHOPIFY_APP_STORE_PACKAGING.md # App Store manifest, access scopes & deployment guide
│   ├── SIBLING_APP_IMAGE_OPTIMIZER_MASTER_BLUEPRINT.md # Master architectural blueprint & benchmarks
│   └── EXACT_CLONIX_INDEX_PROMPT.md # Project foundation prompts
├── data/                      # 🗄️ Runtime Mappings & Cache
│   ├── alt_text_mapping.json  # 528 unique Google-ranking bilingual alt tags
│   ├── url_mapping.json       # 1,058 original CDN -> Next-Gen WebP URL mappings
│   └── settings_data_optimized.json # Theme AST swapped settings
├── optimized/                 # 2,114 generated Next-Gen files (1057 WebP + 1057 AVIF)
├── scripts/                   # CLI helper tools (batch_optimize_store.py)
├── shopify.app.toml           # Official Shopify App CLI 3.x configuration manifest
├── package.json               # Root npm scripts (dev, build, start, shopify:deploy)
├── requirements.txt           # Python dependencies
├── start.py                   # One-command dual server launcher
└── run_optix.bat              # Windows one-click launcher
```
