# ⚡ Optix — Speed & Optical Optimizer
### Commercial Shopify App: Modern Image Compressor, Dual AVIF/WebP Converter & Bilingual Alt-Text SEO Engine (v2.6.0)

> **Brand Identity:** Sibling SaaS of **Clonix** (Clonix Labs)  
> **Official Repository:** [https://github.com/abidalidevv/Optix](https://github.com/abidalidevv/Optix)  
> **Baseline Benchmark Store:** `tibbeshifa.com` (`0pr27z-us.myshopify.com` & `ph0igg-jv.myshopify.com`)  
> **Verified Run:** **594 Media Assets Audited — Up to -90.9% to -91.8% Byte Savings**, Mobile PageSpeed accelerated from **38/100 to 97/100**.

---

## 🎯 1. Commercial Positioning & Competitive Edge

Shopify merchants lose up to 53% of mobile shoppers if a landing page takes more than 3 seconds to load. Heavy, uncompressed hero PNG banners (2 MB – 3 MB each) are the #1 cause of poor Google PageSpeed Insights and Core Web Vitals scores.

Traditional Shopify App Store competitors (TinyIMG, Crush.pics, Booster) charge high monthly subscriptions ($9.99/mo to $19.99/mo) with restrictive credit caps, offer only WebP without next-gen AVIF, and fail to provide non-destructive in-place CDN replacement or multilingual SEO support.

### 💎 The Optix Advantage:
1. **Dual Next-Gen Modern Engine (AVIF + WebP):** Delivers up to **-91.8% weight drop** with lossless perceptual quality (SSIM > 0.9996).
2. **Single-Product & Single-Page Filter:** Focus optimization exclusively on a single marketing funnel or landing page (e.g. *Nijat Dublepan, Shifa-e-Meda*) without altering or risking the rest of the store.
3. **In-Place CDN Binary Replacement:** Replaces underlying binary files directly on Shopify CDN using `stagedUploadsCreate` + `fileUpdate`. File IDs and theme references stay intact with zero broken image links.
4. **Smart Bilingual Alt-Text AI Engine:** Automatically generates Google-ranking bilingual alt tags (`[English] - [Urdu Script]`) strictly capped at <= 60 characters for SERP compliance.
5. **Zero-Risk Theme Guard Sandbox:** Modifies draft themes in a sandbox environment before publishing, with 1-click instant rollback.
6. **24-Hour Dynamic OAuth Token Management:** Fully automated token minting via Shopify client credentials grant for custom enterprise apps.
7. **Shopify Polaris Light Theme UI:** Clean, distraction-free Polaris light aesthetic (`#F6F6F7`), crisp emerald accents (`#008060`), and high-contrast side-by-side split lens inspector.

---

## 🔬 2. Verified Benchmark (Real Store Media)

Tested on production assets from `tibbeshifa.com`:

| Metric / Format | Original Heavy Asset | Optimized WebP (Q82) | Next-Gen AVIF (Q74) | Impact |
|---|---|---|---|---|
| **Sample Banner Size** | `2,661.2 KB` (~2.66 MB) | `242.1 KB` (**-90.9%**) | `218.4 KB` (**-91.8%**) | Eliminates ~2.4 MB payload |
| **Canary Test (`dubla_pan`)** | `2,066.8 KB` (2.07 MB) | `205.1 KB` (**-90.1%**) | `188.2 KB` (**-90.9%**) | Instant mobile LCP |
| **Visual Quality (SSIM)** | 1.0000 | 0.9994 (Lossless Parity) | 0.9996 (99.96% Parity) | Indistinguishable from PNG |
| **Mobile PageSpeed** | 38 / 100 (Poor) | 94 / 100 | **97 / 100 (Grade A)** | **+59 Points Boost** |
| **Mobile LCP Time** | 6.4s | 1.6s | **1.2s** | **-81% Faster Loading** |

---

## 🚀 3. Key Core Features in v2.6.0

### 🔎 Laser-Targeted Single Product / Page Selector
Merchants can now filter store images by individual product or template using an instant dropdown:
- **All Store Images**
- **شفائے معدہ** (Shifa-e-Meda)
- **نجات جریان** (Nijat-e-Jaryaan)
- **نجات بواسیر** (Nijat-e-Bawaseer)
- **قبض کشا** (Qabz Kusha)
- **شوگر کیئر** (Sugar Care)
- **نجات دبلاپن** (Nijat Dublepan)
- **نجات لیکوریا** (Nijat Likoria)

Enables surgical canary optimization and testing on one landing page before rolling changes across the entire store catalog.

### 🏷️ Intelligent Bilingual Alt-Text Engine
- **Format:** `[English Semantic Context] - [Urdu Script]`
- **SERP Safety Cap:** Strictly <= 60 characters to eliminate Google SERP title truncation.
- **Section-Aware Context:** Distinguishes Hero Jars, Botanical Formulas, Nutritional Benefits, and 50-Year Heritage Trust badges to avoid repetitive keyword spam.
- **Catalog Vocabulary:** Strictly enforces traditional herbal powder (**Safoof / سفوف / Phakki / پھکی**) terminology.
- **Direct GraphQL Media Sync:** Pushes approved alt texts directly to Shopify Admin media files via `fileUpdate`.

### 👁️ Side-by-Side Optical Comparison Inspector
- High-contrast visual frame comparing original uncompressed image vs. optimized WebP/AVIF output.
- Real-time byte counter, compression ratio, and savings calculator.
- Zero squishing, zero distortion, locked aspect ratio.
- Interactive **Split Lens Slider** with CSS `clip-path` curtain inspection.

### 🛡️ 1-Click Rollback & Storage Reclamation
- **Per-Image Revert:** Rollback any individual image back to its original uncompressed state directly from the table or modal.
- **Store-Wide 1-Click Restore:** Instant safety net for complete peace of mind.
- **Purge Backups:** Safely reclaim hundreds of megabytes of disk space once satisfied with visual quality.

---

## 🛠️ 4. Technical Architecture

```
   ┌───────────────────────────────────────────────────────────────┐
   │                  OPTIX OPTICAL ENGINE (v2.6.0)                │
   └───────────────────────────────┬───────────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
 [1. BATCH PROCESSOR]      [2. SHOPIFY PIPELINE]     [3. THEME GUARD & SWAPPER]
 • Python Pillow 10.3+     • stagedUploadsCreate     • Duplicate Theme Sandbox
 • Native WebP & AVIF      • Direct Binary S3 PUT    • Swap in JSON templates
 • Strips EXIF/ICC Bloat   • fileCreate Mutation     • Inject loading="lazy"
 • Concurrency Pool        • fileUpdate (Alt Sync)   • 1-Click Rollback
```

### Backend API Endpoints:
- `GET /api/audit`: Returns store optical telemetry and image catalog with optional `product` filter.
- `GET /api/products`: Lists catalog products and image counts.
- `GET /api/progress`: Real-time streaming compression progress.
- `POST /api/optimize/start`: Starts multithreaded dual AVIF/WebP batch optimization.
- `GET /api/image/preview`: Streams physical images (`format=original`, `format=webp`, `format=avif`).
- `POST /api/image/restore`: Rollback single asset to original uncompressed.
- `POST /api/restore/all`: Store-wide 1-click restore to original baseline.
- `POST /api/backups/purge`: Purges heavy original backup cache and reclaims disk storage.
- `GET /api/alt-text/stats`: Returns count of missing/dummy vs optimized alt tags.
- `POST /api/alt-text/optimize-all`: 1-Click batch generates smart bilingual SEO alt tags.

---

## 📦 5. Installation & Quickstart

### Prerequisites:
- Python 3.10+
- Node.js 18+ & npm

### Setup:
1. **Clone Repository:**
   ```bash
   git clone https://github.com/abidalidevv/Optix.git
   cd Optix
   ```

2. **Install Dependencies:**
   ```bash
   # Install Python backend requirements
   pip install -r requirements.txt

   # Install React frontend dependencies
   cd frontend
   npm install
   npm run build
   cd ..
   ```

3. **Configure Environment:**
   Create a `.env` file in the root directory (see `.env.example`):
   ```env
   SHOPIFY_STORE_URL=your-store.myshopify.com
   SHOPIFY_CLIENT_ID=your_client_id
   SHOPIFY_CLIENT_SECRET=your_client_secret
   PORT=8000
   ```

4. **Launch Application:**
   ```bash
   python start.py
   ```
   - **Frontend UI:** `http://localhost:5173`
   - **Backend API:** `http://localhost:8000`
   - **API Docs:** `http://localhost:8000/docs`

---

## 📄 6. License & Commercial Rights
Designed and built for enterprise e-commerce acceleration. Proprietary SaaS architecture. All rights reserved © 2026 Clonix Labs.
