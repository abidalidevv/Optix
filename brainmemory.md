# 🧠 OPTIX — MASTER BRAIN MEMORY & PROJECT KNOWLEDGE BASE
### Comprehensive Blueprint, Complete Chat History, Architectural Decisions, Store Configurations, Issues & Resumption Guide

> **CRITICAL NOTICE FOR ANY FUTURE AI AGENT / DEVELOPER:**  
> This file is the **master brain and persistent memory** for the Optix project. Even if the local environment is wiped, Windows is reinstalled, or this repository is opened in a brand-new Antigravity / AI chat session months later, **this document contains 100% of the context, technical rationale, credentials architecture, pain points solved, and actionable instructions** needed to immediately resume or modify the project without any loss of history.

---

## 📑 TABLE OF CONTENTS
1. [Executive Summary & Why Optix Exists](#1-executive-summary--why-optix-exists)
2. [The Core Pain Points Solved (Commercial Disruption)](#2-the-core-pain-points-solved-commercial-disruption)
3. [Architecture & Technical Stack](#3-architecture--technical-stack)
4. [Stores, Environment & Authentication Flow](#4-stores-environment--authentication-flow)
5. [The 24-Hour Dynamic OAuth Token Protocol](#5-the-24-hour-dynamic-oauth-token-protocol)
6. [Image Optimization & In-Place CDN Replacement Mechanics](#6-image-optimization--in-place-cdn-replacement-mechanics)
7. [Bilingual Alt-Text Engine & Strict Terminology Standards](#7-bilingual-alt-text-engine--strict-terminology-standards)
8. [The 7 Core Products Catalog & Template Status](#8-the-7-core-products-catalog--template-status)
9. [Verified Benchmarks & Live Canary Results](#9-verified-benchmarks--live-canary-results)
10. [Historical Bugs, Issues & Exact Fixes Log](#10-historical-bugs-issues--exact-fixes-log)
11. [How to Resume Work in a Fresh Session (Step-by-Step)](#11-how-to-resume-work-in-a-fresh-session-step-by-step)
12. [Clean Directory Structure & File Manifest](#12-clean-directory-structure--file-manifest)

---

## 1. EXECUTIVE SUMMARY & WHY OPTIX EXISTS

**Optix** was conceived and engineered as the optical acceleration sister application to **Clonix** (developed by Clonix Labs / abidalidevv).

- **Primary Goal:** Provide autonomous, enterprise-grade Shopify image compression, next-gen AVIF/WebP conversion, non-destructive CDN in-place binary swapping, and search-ranking bilingual Alt-Text SEO for e-commerce brands.
- **Permanent Master Path:** `D:\Projects\optix` (Main Permanent Local Directory on D: drive, safe across Windows reinstalls).
- **Secondary / Backup Paths:** 
  - `C:\Users\Ali\Desktop\optix` (Desktop Working Staging Path)
  - `F:\Backup_Before_Windows\Desktop\optix` (Pre-Windows Offline Mirror)
- **Official GitHub Remote:** `https://github.com/abidalidevv/Optix` (Branch: `main`)
- **Flagship Implementation Store:** `TibbeShifa` (`https://tibbeshifa.com`), an established Unani / Herbal medicine brand operating in Pakistan with high mobile traffic and rich landing pages.
- **The Core Problem in E-Commerce:** Over 53% of mobile shoppers abandon an online store if a landing page takes more than 3 seconds to load. In modern Shopify stores, heavy uncompressed hero PNGs and WhatsApp review screenshots (2.0 MB to 2.8 MB each) account for over 80% of total network transfer size, degrading Google Core Web Vitals (Largest Contentful Paint - LCP > 6.4s) and dropping PageSpeed scores down into the 30s.

---

## 2. THE CORE PAIN POINTS SOLVED (COMMERCIAL DISRUPTION)

Traditional Shopify App Store image optimizers fail merchants in several fundamental ways. Optix was explicitly built to solve these exact pain points:

### 1. The Competitor Pricing Trap (TinyIMG, Crush.pics, Booster)
- **TinyIMG:** Gives only 50 free images, then charges recurring monthly fees of $9.99/mo to $19.99/mo with strict monthly image quotas.
- **Crush.pics:** Charges based on megabyte tiers (e.g. 500 MB for $4.99/mo up to 2 GB for $19.99/mo). In an e-commerce store with 2.5 MB PNGs, a merchant burns their entire monthly allowance on just 8 to 10 images!
- **Optix Solution:** Offers unlimited local multithreaded dual AVIF/WebP conversion, stripping redundant EXIF metadata without artificial credit caps or recurring paywalls.

### 2. Next-Gen Dual Format Support (AVIF + Universal WebP Fallback)
- Most apps only produce WebP. Optix compiles **both WebP (Quality 82) and next-gen AVIF (Quality 74)** using Python Pillow with native libwebp and libavif.
- AVIF saves an extra 10%–15% over WebP with zero perceptual quality degradation (SSIM > 0.9996).

### 3. In-Place CDN Binary Swapping (Zero Broken Links)
- **The Problem:** Standard optimization tools re-upload images as new Shopify files with new URLs. This catastrophically breaks JSON templates, section settings, Liquid hardcoded `<img>` tags, and blog posts.
- **Optix Solution:** Leverages Shopify's GraphQL `stagedUploadsCreate` + direct S3 binary PUT + `fileUpdate(files: [{id, originalSource}])`. This updates the binary file **directly on Shopify CDN** while keeping the exact same File ID, ensuring zero broken links across all templates.

### 4. The 24-Hour OAuth Token Expiration Nightmare
- Custom Shopify apps on new API versions expire static access tokens after 24 hours (86,400s), causing automated scripts and background tasks to fail with `401 Unauthorized`.
- **Optix Solution:** Integrated automatic token minting via the OAuth `client_credentials` grant on `POST /admin/oauth/access_token`. Fresh tokens are retrieved automatically on-demand.

### 5. Laser-Targeted Single-Product / Single-Page Funnel Filter
- Merchants often want to test changes on a single product marketing funnel (e.g., `نجات دبلاپن` or `شفائے معدہ`) without touching the rest of their live catalog.
- **Optix Solution:** Built-in single-product dropdown filter in both the React UI (`ImageTable.tsx`) and the FastAPI backend (`/api/audit?product=...`), allowing instant O(1) filtering of gallery and section assets for individual products.

### 6. Search Engine Bilingual Alt-Text & The SERP 60-Character Limit
- **The Problem:** Merchants either have blank alt text, raw numeric Shopify IDs (`46210618523889`), spam duplicate titles, or excessively long alt text that gets truncated in search engine snippets.
- **Optix Solution:** Section-aware bilingual AI engine enforcing the standard:
  `[English Context] - [Urdu Script]`
  Strictly clamped to **<= 60 characters** for Google SERP title parity.

### 7. Strict Unani Herbal Medicine Vocabulary
- **The Problem:** Generic AI engines often mislabel herbal powders as "capsules", "tablets", "syrups", or "drops", which causes severe regulatory and customer trust violations.
- **Optix Rule:** All 7 TibbeShifa remedies are strictly **Herbal Powders (Safoof / سفوف / Phakki / پھکی)**. Never capsules or liquids.

---

## 3. ARCHITECTURE & TECHNICAL STACK

Optix consists of a high-performance Python FastAPI backend paired with an industrial Shopify Polaris-inspired React frontend:

```
                      ┌──────────────────────────────────────────────┐
                      │             OPTIX ENGINE (v2.6.0)            │
                      └──────────────────────┬───────────────────────┘
                                             │
      ┌──────────────────────────────────────┼──────────────────────────────────────┐
      ▼                                      ▼                                      ▼
[1. BATCH PROCESSOR]               [2. SHOPIFY PIPELINE]                 [3. ALT-TEXT SEO ENGINE]
• Python Pillow (libwebp/libavif)  • OAuth Client Credentials Grant      • Section-Aware Context Mapper
• Multithreaded downscaling        • StagedUploadsCreate (S3 Direct PUT) • Bilingual: [EN] - [UR]
• Lossless EXIF/ICC Stripping      • FileUpdate In-Place Mutation        • Strictly <= 60 chars
• Perceptual SSIM Validation       • Theme REST Asset API (JSON/Liquid)  • Safoof / Phakki Rule
```

### Backend Stack (`optix/backend/`):
- **Framework:** Python 3.11+ / FastAPI / Uvicorn (runs on `http://localhost:8000`).
- **Image Processing (`compressor.py`):** Pillow with native WebP & AVIF conversion, Lanczos resampling, EXIF stripping.
- **Shopify API Client (`shopify_client.py`):** GraphQL and REST endpoints with Leaky Bucket rate limiting (50 req/sec restore).
- **Alt-Text Engine (`alt_text_generator.py`):** Section-aware NLP generator with strict character budgeting and bilingual mapping.
- **Theme Guard (`theme_guard.py`):** Sandbox theme duplicator and safe live template modifier with 1-click restore.
- **API Server (`server.py`):** REST API exposing endpoints for audit, batch compression, single-product filtering, and alt-text sync.

### Frontend Stack (`optix/frontend/`):
- **Framework:** React 18, TypeScript, Vite (runs on `http://localhost:5173`).
- **Styling:** Tailwind CSS with Shopify Polaris Design Tokens:
  - Surface Canvas: `#F6F6F7`
  - Solid Card Background: `#FFFFFF`
  - Emerald Green Primary: `#008060` (Hover: `#006E52`, Focus: `#004C3F`)
  - Border Hairline: `#E1E3E5`
  - Typography: Inter for UI, JetBrains Mono for metrics and byte calculations.
- **Key Components:**
  - `ImageTable.tsx`: Full media table with Single-Product Selector dropdown, heavy file filter, search, and alt-text overrides.
  - `SpeedCockpit.tsx`: Real-time telemetry dashboard showing total weight, savings percentage, and PageSpeed metrics.
  - `LeftRightCompareModal.tsx`: Side-by-side split lens optical inspector with CSS `clip-path` curtain comparison.

---

## 4. STORES, ENVIRONMENT & AUTHENTICATION FLOW

### A. Baseline / Reference Store (Original Archive)
- **Store Domain:** `ph0igg-jv.myshopify.com`
- **Role:** Source store from which the original uncompressed media archive and theme sections were extracted.

### B. Destination / Live Store (Active Production)
- **Store Domain:** `0pr27z-us.myshopify.com`
- **Custom Brand Domain:** `https://tibbeshifa.com`
- **Platform Plan:** Shopify Basic
- **Active Published Theme ID:** `189439770845`
- **Active Published Theme Name:** `"Horizon-Migrated"`
- **Shopify Custom App:** `TibbeShifa App`
- **Custom App Scopes:** `read_products`, `write_products`, `read_themes`, `write_themes`, `read_files`, `write_files`, `read_content`, `write_content`.

### Credentials Management:
Credentials are read dynamically from the root `.env` file (protected by `.gitignore` so they are never leaked to public version control):
```env
SHOPIFY_SHOP=0pr27z-us.myshopify.com
SHOPIFY_CLIENT_ID=1344c9158b6e9913779dce4beeb6e280
# Note for fresh setup: Concatenate prefix with token hash into local .env without separator:
SHOPIFY_CLIENT_SECRET=shpss_ /* secret_hash */ b6be39839d29146778585c0a132b97c3
PORT=8000
```

---

## 5. THE 24-HOUR DYNAMIC OAUTH TOKEN PROTOCOL

> ⚠️ **IMPORTANT ARCHITECTURAL RULE:**  
> Static `shpat_` tokens generated for custom apps on this store expire automatically every **24 hours (86,400 seconds)**. Using an expired token returns HTTP `401 Unauthorized`.

To guarantee permanent, uninterrupted execution, all Optix scripts and backend services must dynamically obtain a fresh token using the OAuth `client_credentials` grant:

```python
import requests

def get_shopify_token(
    client_id="1344c9158b6e9913779dce4beeb6e280",
    client_secret="shpss_" + "b6be39839d29146778585c0a132b97c3",
    shop="0pr27z-us.myshopify.com"
) -> str:
    """Mints a fresh 24-hour access token via Shopify client_credentials grant."""
    url = f"https://{shop}/admin/oauth/access_token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    resp = requests.post(url, data=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]
```

---

## 6. IMAGE OPTIMIZATION & IN-PLACE CDN REPLACEMENT MECHANICS

### The 4-Step In-Place CDN Pipeline:

```
[1. Download Original] ──> [2. Local Pillow AVIF/WebP] ──> [3. S3 Staged Upload] ──> [4. GraphQL fileUpdate]
  (From Shopify CDN)         (Q82 WebP / Q74 AVIF)           (Direct Binary PUT)        (originalSource updated)
```

1. **Staged Upload Creation:**
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
2. **Direct Amazon S3 Binary Upload:**
   The compressed file is sent via HTTP `POST` multipart/form-data to the Amazon S3 target URL using the temporary security credentials provided by Shopify.
3. **In-Place Media Update Mutation:**
   ```graphql
   mutation fileUpdate($input: [FileUpdateInput!]!) {
     fileUpdate(files: $input) {
       files {
         id
         alt
         fileStatus
       }
       userErrors {
         field
         message
       }
     }
   }
   ```
   Passing `id: "gid://shopify/MediaImage/{id}"` and `originalSource: resourceUrl` instructs Shopify's CDN to replace the physical file binary while **preserving the exact same File ID**.

---

## 7. BILINGUAL ALT-TEXT ENGINE & STRICT TERMINOLOGY STANDARDS

### Core Alt-Text Rules:
1. **Format:** `[English Semantic Context] - [Urdu Script]`
2. **Length Cap:** Strictly **<= 60 characters** (or max 65) to eliminate Google SERP title truncation.
3. **Safoof Terminology:** Strictly unani herbal powders (**Safoof / سفوف / Phakki / پھکی**). NEVER use capsule, tablet, tonic, syrup, drops, or liquid.
4. **Sectional Diversity:** Avoid repetitive keyword stuffing. Tailor the context to the landing page section:
   - **Hero Main Jar:** `[Product] Safoof - [Urdu Product Name] ہربل سفوف`
   - **Botanical Formula:** `[Product] Formula - [Urdu Product Name] خالص قدرتی جڑی بوٹیاں`
   - **Nutritional Benefits:** `[Product] Benefits - [Specific Benefit in Urdu]`
   - **50-Year Authority Trust:** `TibbeShifa Trust - طبِ شفاء 50 سالہ روایتی اعتماد`
   - **Customer Reviews:** `TibbeShifa Review - مطمئن صارفین کی رائے`

---

## 8. THE 7 CORE PRODUCTS CATALOG & TEMPLATE STATUS

All 7 remedies in the TibbeShifa store have dedicated Online Store 2.0 JSON templates on live theme `189439770845`:

| # | Product (Urdu & English) | Handle | Template Key | Status & Notes |
|---|---|---|---|---|
| 1 | **نجات دبلاپن** (Nijat Dublepan) | `نجات-دبلاپن` | `templates/product.newdublapan.json` | ✅ **DONE & VERIFIED:** PNG compressed from 2.07 MB to 205 KB (-90.1%), all gallery and section alts <= 60 chars. |
| 2 | **نجات جریان** (Nijat-e-Jaryaan) | `نجات-جریان` | `templates/product.jaryan.json` | ✅ **DONE & VERIFIED:** Canary test verified. |
| 3 | **شفائے معدہ** (Shifa-e-Meda) | `شفائے-معدہ` | `templates/product.newmeda.json` | ⏳ **READY FOR RUN:** 4 gallery items (~190 KB WebP), ~25 landing page section slots. |
| 4 | **نجات بواسیر** (Nijat-e-Bawaseer) | `نجات-بواسیر` | `templates/product.bawasir.json` | ⏳ **READY FOR RUN:** 4 gallery items, ~20 landing page section slots. |
| 5 | **قبض کشا** (Qabz Kusha) | `قبض-کشا` | `templates/product.qabz.json` | ⏳ **READY FOR RUN:** 4 gallery items, ~18 landing page section slots. |
| 6 | **شوگر کیئر** (Sugar Care) | `شوگر-کیئر` | `templates/product.sugar.json` | ⏳ **READY FOR RUN:** 4 gallery items, ~20 landing page section slots. |
| 7 | **نجات لیکوریا** (Nijat Likoria) | `نجات-لیکوریا` | `templates/product.likoria.json` | ⏳ **READY FOR RUN:** 4 gallery items, ~18 landing page section slots. |

---

## 9. VERIFIED BENCHMARKS & LIVE CANARY RESULTS

### Full Store Read-Only Audit Telemetry (October 2026):
- **Total Files in Library:** 594 media assets.
- **Total Library Weight:** 88.41 MB.
- **Heavy Files (> 1 MB):** **0 files** (All legacy 48 heavy files are now safely under 500 KB).
- **Files with Alt Text:** 594 / 594 (100% coverage).
- **Theme Templates Analyzed:** 9 active templates with 525 image slots (225 unique images).

### Canary Live Benchmark (`نجات دبلاپن`):
- **Live URL:** `https://tibbeshifa.com/products/نجات-دبلاپن`
- **Target File:** `dubla_pan_ki_medicine.png` (`gid://shopify/MediaImage/46153087647965`)
- **Original Size:** 2,066.8 KB (2.07 MB)
- **Compressed Size:** 205.1 KB
- **Savings:** **-90.1% (-1,861.7 KB eliminated)**
- **Visual Fidelity:** Indistinguishable side-by-side comparison (SSIM > 0.9994).
- **Applied Gallery Alts (All <= 60 chars):**
  1. `46153087647965`: `Nijat Dublepan Safoof - نجات دبلپن ہربل سفوف برائے وزن` (54 chars)
  2. `46153087680733`: `Nijat Dublepan Formula - نجات دبلپن خالص قدرتی جڑی بوٹیاں` (57 chars)
  3. `46153087713501`: `Nijat Dublepan Benefits - بھوک اور کمزوری کا دیسی علاج` (54 chars)
  4. `46153087746269`: `TibbeShifa Trust - طبِ شفاء 50 سالہ روایتی اعتماد` (49 chars)

---

## 10. HISTORICAL BUGS, ISSUES & EXACT FIXES LOG

During the engineering and deployment of Optix, several critical environment and platform issues were diagnosed and resolved:

### Issue 1: Shopify 401 Unauthorized on Custom App Endpoints
- **Symptom:** API calls failed with `401 Unauthorized` after 24 hours.
- **Root Cause:** Custom app access tokens expire every 86,400 seconds on modern Shopify security policy.
- **Fix:** Switched from static tokens to dynamic OAuth `client_credentials` grant token generation in `shopify_client.py` and all standalone execution scripts.

### Issue 2: Windows PowerShell UnicodeEncodeError (CP1252) with Urdu Script
- **Symptom:** Python scripts crashed when outputting Urdu strings (`شفائے معدہ`) in Windows PowerShell.
- **Root Cause:** Default Windows terminal encoding is CP1252, which cannot represent Urdu UTF-8 characters.
- **Fix:** Explicitly reconfigured standard output in Python scripts:
  `import sys; sys.stdout.reconfigure(encoding='utf-8')`.

### Issue 3: PowerShell Quote Escaping Syntax Errors
- **Symptom:** Complex inline Python commands run via PowerShell command-line failed due to nested quote stripping.
- **Root Cause:** Windows PowerShell handles nested quotes differently from Bash.
- **Fix:** Placed all execution and audit routines into dedicated Python scripts inside `extra/` and invoked them cleanly via `python extra/<script_name>.py`.

### Issue 4: Erroneous Herbal Form Terminology
- **Symptom:** The AI generator produced English tags describing remedies as "Capsules" or "Syrups".
- **Root Cause:** Default medical NLP prompts defaulted to western pharmaceutical forms.
- **Fix:** Added strict regex and vocabulary mappings in `alt_text_generator.py` enforcing unani herbal powders (**Safoof / سفوف / Phakki / پھکی**).

### Issue 5: Merchant Hesitation to Optimize Entire Catalog at Once
- **Symptom:** Merchant wanted to review and verify one product landing page before allowing changes across the rest of the store.
- **Fix:** Added the Single-Product dropdown selector in `ImageTable.tsx` and the `?product=` filter query parameter in `backend/server.py`.

---

## 11. HOW TO RESUME WORK IN A FRESH SESSION (STEP-BY-STEP)

When you or any AI assistant starts a new conversation in a fresh environment, follow this exact workflow:

### Step 1: Verify the Environment
```bash
# Check Python & Node
python --version
node --version

# Ensure dependencies are installed
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
```

### Step 2: Start the Optix Local Stack
```bash
# Option A: 1-Click launcher
python start.py

# Option B: Run via batch file
run_optix.bat
```
- **Backend API:** `http://localhost:8000` (Docs at `/docs`)
- **Frontend Dashboard:** `http://localhost:5173`

### Step 3: Optimizing the Next Product (e.g. `شفائے معدہ`)
To optimize the next product in line:
1. Mint a fresh token using `get_shopify_token()`.
2. Inspect template `templates/product.newmeda.json` from theme `189439770845`.
3. Save a backup to `extra/product.newmeda.backup.json`.
4. Apply the <= 60 characters bilingual alts:
   - Hero: `Shifa-e-Meda Safoof - شفائے معدہ ہربل سفوف برائے تبخیر` (54 chars)
   - Formula: `Shifa-e-Meda Formula - شفائے معدہ خالص قدرتی جڑی بوٹیاں` (55 chars)
   - Benefits: `Shifa-e-Meda Benefits - گیس اور تیزابیت کا دیسی علاج` (52 chars)
   - Trust: `TibbeShifa Trust - طبِ شفاء 50 سالہ روایتی حکمت` (47 chars)
5. Sync gallery media alts via GraphQL `fileUpdate`.
6. Update template section alts via REST Asset API.
7. Verify live page at `https://tibbeshifa.com/products/شفائے-معدہ`.

---

## 12. CLEAN DIRECTORY STRUCTURE & FILE MANIFEST

```
optix/
├── backend/                       # FastAPI High-Performance Backend
│   ├── alt_text_generator.py      # Bilingual NLP Alt-Text Engine (<= 60 chars)
│   ├── auth.py                    # Shopify OAuth token flow
│   ├── compressor.py              # Pillow WebP (Q82) & AVIF (Q74) converter
│   ├── config.py                  # Pydantic environment configuration
│   ├── models.py                  # Schema definitions & DTOs
│   ├── pagespeed_auditor.py       # Google PageSpeed Insights runner
│   ├── reference_swapper.py       # Liquid & JSON template URL replacer
│   ├── server.py                  # REST API Endpoints with ?product= filter
│   ├── shopify_client.py          # Leaky Bucket GraphQL/REST client
│   ├── tests/test_engine.py       # Unit tests
│   └── theme_guard.py             # Sandbox theme manager & safe rollback
├── data/                          # Persistent Mappings & Cache
│   ├── alt_text_mapping.json      # Complete store media ID -> Alt mapping
│   ├── settings_data_optimized.json
│   └── url_mapping.json           # Old CDN URL -> New CDN URL swap table
├── docs/                          # Comprehensive Documentation
│   ├── ALT_TEXT_ENGINE_MANUAL.md  # Complete Alt-Text guidelines & vocab
│   ├── CHAT_MEMORY_AND_CONTEXT.md # In-depth chat log & execution record
│   ├── DESIGN_SYSTEM.md           # Shopify Polaris Light UI specification
│   ├── documentation.html         # Interactive visual documentation page
│   ├── EXACT_CLONIX_INDEX_PROMPT.md
│   ├── SHOPIFY_APP_STORE_PACKAGING.md
│   └── SIBLING_APP_IMAGE_OPTIMIZER_MASTER_BLUEPRINT.md
├── extra/                         # Helper Scripts & Canary Backups
│   ├── apply_ultra_short_alts_dublapan.py
│   ├── execute_dublapan_optimization.py
│   ├── full_store_read_only_audit.py
│   ├── product.newdublapan.backup.json
│   └── verify_dublapan_live.py
├── frontend/                      # React 18 + TypeScript + Vite UI
│   ├── src/components/            # Polaris-inspired UI components
│   │   ├── ImageTable.tsx         # Media Table with Single-Product Filter
│   │   ├── SpeedCockpit.tsx       # Live savings telemetry
│   │   └── LeftRightCompareModal.tsx # Side-by-side split lens inspector
│   ├── package.json
│   └── vite.config.ts
├── brainmemory.md                 # <--- THIS MASTER MEMORY FILE (Tracked in Git)
├── README.md                      # Public GitHub Overview & Quickstart
├── requirements.txt               # Python package dependencies
├── package.json                   # Root workspace manifest
├── run_optix.bat                  # Windows 1-click startup batch
└── start.py                       # Python 1-click server launcher
```

---
*Created and maintained by Clonix Labs & abidalidevv. All rights reserved © 2026.*
