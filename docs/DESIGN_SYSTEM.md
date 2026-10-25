# ⚡ OPTIX DESIGN SYSTEM SPECIFICATION
### High-Fidelity Optical Engineering & PageSpeed Booster UI
> **Aesthetic Philosophy:** Industrial Luxury / High-Performance Micro-SaaS.  
> **Inspired by:** Linear, Raycast, Vercel, Clonify, and Shopify Polaris v12.  
> **Anti-AI Slop Rule:** Zero generic purple gradients (`#8B5CF6`), zero fuzzy 40px drop-shadows, zero tacky AI sparkles (`✨`), zero generic Bootstrap feel. Everything is razor-sharp, hairline-bordered, and precision-engineered.

---

## 1. 🎯 Visual Identity & Design Principles

1. **Surgical Precision:** Hairline 1px borders (`rgba(255,255,255,0.08)` in dark mode, `#E4E7EB` in light mode).
2. **Speed-First Visual Metaphor:** Tachometers, optical lenses, laser-focus rings, and real-time streaming byte counters.
3. **High-Contrast Data Density:** Clean typography hierarchy with monospaced metrics for file sizes, LCP scores, and compression ratios.
4. **Tactile Micro-Interactions:** Subtle hover lifts (`translateY(-1px)`), crisp focus rings, and living pulse indicators.

---

## 2. 🔤 Typography Hierarchy

| Role | Font Family | Weights | Letter Spacing | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Display / Hero** | **`Archivo`** | 600, 700, 800 | `-0.03em` | Main titles, hero speed metrics, modal headers |
| **Dashboard UI & Body** | **`Geist`** or **`Inter`** | 400, 500, 600 | `-0.01em` | Labels, tables, tooltips, buttons, form controls |
| **Numbers & Counters** | **`JetBrains Mono`** | 500, 700 | `normal` (tabular) | Speed scores (`98`), sizes (`4.2 MB -> 410 KB`), percentages (`-89.4%`) |
| **Hero Speed Badges** | **`Anton`** / Display Mono | 400 | `normal` | Giant Core Web Vitals numbers (e.g. `98 / 100`) |

### Google Fonts Import
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800&family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

---

## 3. 🎨 Color Tokens & Palette

### Dark Mode (Primary Professional SaaS Theme)
```css
:root {
  /* Surfaces */
  --optix-bg-canvas: #09090B;          /* Deepest obsidian canvas */
  --optix-bg-card: #121215;            /* Solid matte surface card */
  --optix-bg-subtle: #18181B;          /* Inner wells, input fields, pill backgrounds */
  --optix-border-hairline: rgba(255, 255, 255, 0.08); /* Surgical 1px border */
  --optix-border-hover: rgba(255, 255, 255, 0.16);

  /* Performance Accents */
  --optix-speed-emerald: #10B981;      /* 90-100 Score, AVIF verified, LCP good */
  --optix-speed-emerald-glow: rgba(16, 185, 129, 0.15);
  --optix-laser-cyan: #06B6D4;         /* Optical scanner, active lens, image remapper */
  --optix-laser-cyan-glow: rgba(6, 182, 212, 0.15);
  --optix-warning-amber: #F59E0B;      /* 50-89 Score, pending compression */
  --optix-critical-rose: #F43F5E;      /* 0-49 Score, uncompressed 10MB+ images */
  
  /* Text */
  --optix-text-primary: #FAFAFA;
  --optix-text-secondary: #A1A1AA;
  --optix-text-muted: #71717A;
}
```

### Light Mode (Shopify Admin Native Embedded Theme)
```css
.theme-light {
  --optix-bg-canvas: #F8F9FA;
  --optix-bg-card: #FFFFFF;
  --optix-bg-subtle: #F1F3F5;
  --optix-border-hairline: #E4E7EB;
  --optix-border-hover: #D1D5DB;
  --optix-text-primary: #0F172A;
  --optix-text-secondary: #475569;
  --optix-text-muted: #94A3B8;
}
```

---

## 4. 🧩 Core Component Specifications

### A. The "Before vs After" Speed Score Tachometer Card
Instead of boring plain text, present speed transformation as a split cockpit gauge:

```tsx
<div className="grid grid-cols-2 gap-4 p-6 bg-[#121215] border border-white/10 rounded-xl">
  {/* Before State */}
  <div className="p-4 rounded-lg bg-red-500/5 border border-red-500/20">
    <div className="text-xs uppercase tracking-wider text-red-400 font-mono">Current Store State</div>
    <div className="mt-2 flex items-baseline gap-2">
      <span className="font-mono text-4xl font-bold text-red-400">38</span>
      <span className="text-xs text-red-400/80">/ 100 (Slow)</span>
    </div>
    <div className="mt-3 text-xs text-zinc-400 space-y-1 font-mono">
      <div>LCP: <span className="text-red-300 font-semibold">4.8s</span></div>
      <div>Image Weight: <span className="text-red-300">184.2 MB</span></div>
    </div>
  </div>

  {/* After Optix AVIF State */}
  <div className="p-4 rounded-lg bg-emerald-500/5 border border-emerald-500/30 relative overflow-hidden">
    <div className="text-xs uppercase tracking-wider text-emerald-400 font-mono flex items-center gap-1.5">
      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
      With Optix AVIF Engine
    </div>
    <div className="mt-2 flex items-baseline gap-2">
      <span className="font-mono text-4xl font-bold text-emerald-400">97</span>
      <span className="text-xs text-emerald-400/80">/ 100 (Instant)</span>
    </div>
    <div className="mt-3 text-xs text-zinc-400 space-y-1 font-mono">
      <div>LCP: <span className="text-emerald-300 font-semibold">0.9s (-81%)</span></div>
      <div>Image Weight: <span className="text-emerald-300">14.1 MB (-92%)</span></div>
    </div>
  </div>
</div>
```

---

### B. Optical Interactive Image Compare Slider (Lens Viewer)
Allows the merchant to slide between **Original JPEG** and **Optix AVIF** to visually verify that quality is 100% identical while file size dropped 85%:

```tsx
<div className="relative overflow-hidden rounded-xl border border-white/10 bg-black aspect-video group">
  {/* Left: Original Label */}
  <div className="absolute top-3 left-3 z-20 px-2.5 py-1 rounded bg-black/75 backdrop-blur text-xs font-mono text-zinc-300 border border-white/10">
    Original JPEG • 4.2 MB
  </div>

  {/* Right: Optix AVIF Label */}
  <div className="absolute top-3 right-3 z-20 px-2.5 py-1 rounded bg-emerald-950/80 backdrop-blur text-xs font-mono text-emerald-400 border border-emerald-500/30">
    Optix AVIF • 385 KB (-91%)
  </div>

  {/* Center divider bar with lens icon */}
  <div className="absolute inset-y-0 left-1/2 w-0.5 bg-cyan-400 shadow-[0_0_12px_#06b6d4] z-10 flex items-center justify-center">
    <div className="w-7 h-7 rounded-full bg-[#121215] border border-cyan-400 text-cyan-400 flex items-center justify-center shadow-lg text-[10px] font-mono">
      ⟷
    </div>
  </div>
</div>
```

---

### C. Live Compression Pipeline Stream (Data Table)
Clean, tabular, monospaced rows without clumsy borders:

```tsx
<div className="border border-white/10 rounded-xl overflow-hidden bg-[#121215]">
  <div className="px-5 py-3.5 border-b border-white/10 bg-white/[0.02] flex items-center justify-between">
    <div className="flex items-center gap-2">
      <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping"></span>
      <span className="font-medium text-sm text-zinc-200">Active Optical Optimization Pipeline</span>
    </div>
    <span className="text-xs font-mono text-zinc-400">533 Files Detected</span>
  </div>

  <table className="w-full text-left text-xs font-mono">
    <thead className="bg-white/[0.01] text-zinc-400 border-b border-white/5">
      <tr>
        <th className="py-2.5 px-4 font-normal">ASSET NAME</th>
        <th className="py-2.5 px-4 font-normal">ORIGINAL</th>
        <th className="py-2.5 px-4 font-normal">CONVERTED (AVIF)</th>
        <th className="py-2.5 px-4 font-normal">SAVINGS</th>
        <th className="py-2.5 px-4 font-normal text-right">STATUS</th>
      </tr>
    </thead>
    <tbody className="divide-y divide-white/5 text-zinc-300">
      <tr className="hover:bg-white/[0.02] transition-colors">
        <td className="py-3 px-4 font-sans font-medium text-zinc-100 flex items-center gap-2">
          <span className="text-cyan-400">🖼️</span> hero_banner_urdu_desktop.png
        </td>
        <td className="py-3 px-4 text-zinc-400">3.8 MB (PNG)</td>
        <td className="py-3 px-4 text-emerald-400 font-semibold">284 KB (AVIF)</td>
        <td className="py-3 px-4">
          <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-bold border border-emerald-500/20">
            -92.5%
          </span>
        </td>
        <td className="py-3 px-4 text-right">
          <span className="inline-flex items-center gap-1 text-emerald-400">
            ✓ REPLACED IN THEME
          </span>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

---

### D. Zero-Leak Liquid Rewriter Status Card
Assures the merchant that Optix doesn't just convert files, it rewrites the store's code to automatically point to AVIF:

```tsx
<div className="p-4 rounded-xl border border-cyan-500/20 bg-cyan-950/10 flex items-start gap-3.5">
  <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
    ⚡
  </div>
  <div>
    <h4 className="text-sm font-semibold text-zinc-100">Automated Theme Liquid & HTML Remapper Active</h4>
    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">
      All <code>product.images</code>, <code>settings_data.json</code>, collection hero banners, and inline HTML <code>&lt;img&gt;</code> tags are automatically updated to point to the new high-performance AVIF endpoints with zero 404 broken images.
    </p>
  </div>
</div>
```

---

## 5. 🛠️ Tailwind CSS Configuration Snippet (Ready to Paste)

Add this to `tailwind.config.js` in Optix:

```js
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        optix: {
          canvas: '#09090B',
          card: '#121215',
          subtle: '#18181B',
          hairline: 'rgba(255, 255, 255, 0.08)',
          emerald: '#10B981',
          cyan: '#06B6D4',
          amber: '#F59E0B',
          rose: '#F43F5E',
        }
      },
      fontFamily: {
        display: ['Archivo', 'sans-serif'],
        sans: ['Geist', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    }
  }
}
```

---

## 6. 🚫 What to Avoid (The Anti-Slop Checklist)

- ❌ **NO Big Glowing Gradient Buttons:** Avoid `bg-gradient-to-r from-purple-500 to-indigo-600 shadow-purple-500/50`. Use solid `#10B981` with clean hover `#059669` or solid dark `#FAFAFA` with black text.
- ❌ **NO Cartoon AI Icons:** Replace random stars (`✨`, `🌟`) with mechanical performance icons (`⚡`, `🔍`, `📊`, `🎯`, `⟷`).
- ❌ **NO Fuzzy Card Outlines:** Use exact `border border-white/10` or hairline `1px solid rgba(255,255,255,0.08)`.
- ❌ **NO Low-Density Spacing:** Do not leave giant empty 100px gaps. Micro-SaaS tools thrive on high-density, legible data tables with compact monospaced telemetry.
