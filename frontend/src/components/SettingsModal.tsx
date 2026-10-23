import React, { useState } from 'react';
import { X, Sliders, Save, Check } from 'lucide-react';
import type { SettingsConfig } from '../types';

interface SettingsModalProps {
  onClose: () => void;
  config: SettingsConfig;
  onSaveConfig: (newConfig: SettingsConfig) => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  onClose,
  config,
  onSaveConfig
}) => {
  const [localConfig, setLocalConfig] = useState<SettingsConfig>({ ...config });
  const [saved, setSaved] = useState(false);

  const applyPreset = (preset: 'balanced' | 'lossless' | 'aggressive') => {
    if (preset === 'lossless') {
      setLocalConfig(prev => ({ ...prev, quality_webp: 90, quality_avif: 85 }));
    } else if (preset === 'balanced') {
      setLocalConfig(prev => ({ ...prev, quality_webp: 82, quality_avif: 74 }));
    } else if (preset === 'aggressive') {
      setLocalConfig(prev => ({ ...prev, quality_webp: 74, quality_avif: 65 }));
    }
  };

  const handleSave = () => {
    onSaveConfig(localConfig);
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      onClose();
    }, 500);
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: '640px' }}>
        {/* Header */}
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: 'var(--radius-sm)',
              background: 'var(--tint-cyan-bg)',
              color: 'var(--tint-cyan-text)',
              border: '1px solid var(--tint-cyan-border)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Sliders size={18} />
            </div>
            <div>
              <h3 className="modal-title" style={{ fontSize: '16px' }}>
                Optical Engineering &amp; Core Web Vitals Settings
              </h3>
              <p className="modal-subtitle">
                Configure next-gen image encoders, LCP network priority, and SEO metadata.
              </p>
            </div>
          </div>

          <button onClick={onClose} className="modal-close-btn" title="Close">
            <X size={16} />
          </button>
        </div>

        {/* Compression Presets Bar */}
        <div style={{
          background: 'var(--bg-subtle)',
          border: '1px solid var(--border-hairline)',
          borderRadius: 'var(--radius-sm)',
          padding: '12px 16px',
          marginBottom: '16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '10px'
        }}>
          <div>
            <strong style={{ fontSize: '12.5px', color: 'var(--fg-primary)' }}>Quick Quality Presets</strong>
            <p style={{ fontSize: '11px', color: 'var(--fg-secondary)', marginTop: '2px' }}>
              Select an industry standard profile or fine-tune below.
            </p>
          </div>
          <div style={{ display: 'flex', gap: '6px' }}>
            <button
              type="button"
              onClick={() => applyPreset('lossless')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '4px 8px' }}
            >
              Lossless (Low)
            </button>
            <button
              type="button"
              onClick={() => applyPreset('balanced')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '4px 8px', borderColor: 'var(--p-green)', color: 'var(--p-green)', fontWeight: 700 }}
            >
              Balanced (Shopify Std)
            </button>
            <button
              type="button"
              onClick={() => applyPreset('aggressive')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '4px 8px' }}
            >
              Aggressive (Speed 95+)
            </button>
          </div>
        </div>

        {/* Sliders Group */}
        <div className="settings-form-group">
          {/* WebP Slider */}
          <div className="slider-container" style={{ marginBottom: '16px' }}>
            <div className="slider-header">
              <span style={{ fontWeight: 600, fontSize: '12.5px', color: 'var(--fg-primary)' }}>
                Universal WebP Quality (Catalog Products)
              </span>
              <span className="container-badge badge-emerald" style={{ fontSize: '11px' }}>
                {localConfig.quality_webp}%
              </span>
            </div>
            <input
              type="range"
              min="70"
              max="95"
              value={localConfig.quality_webp}
              onChange={(e) => setLocalConfig({ ...localConfig, quality_webp: Number(e.target.value) })}
              className="slider-input"
            />
            <div style={{ fontSize: '11px', color: 'var(--fg-secondary)' }}>
              Standard: 82 delivers ~85% reduction with 99.96% SSIM perceptual parity.
            </div>
          </div>

          {/* AVIF Slider */}
          <div className="slider-container">
            <div className="slider-header">
              <span style={{ fontWeight: 600, fontSize: '12.5px', color: 'var(--fg-primary)' }}>
                Next-Gen AVIF Quality (Hero Banners &amp; Large Photos)
              </span>
              <span className="container-badge badge-cyan" style={{ fontSize: '11px' }}>
                {localConfig.quality_avif}%
              </span>
            </div>
            <input
              type="range"
              min="65"
              max="90"
              value={localConfig.quality_avif}
              onChange={(e) => setLocalConfig({ ...localConfig, quality_avif: Number(e.target.value) })}
              className="slider-input"
            />
            <div style={{ fontSize: '11px', color: 'var(--fg-secondary)' }}>
              Standard: 74 delivers ~92% reduction. Optimal for Chrome, Safari &amp; Firefox.
            </div>
          </div>
        </div>

        {/* Core Web Vitals Toggles */}
        <div className="settings-form-group">
          <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--fg-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em', marginBottom: '8px' }}>
            Core Web Vitals &amp; SEO Automation
          </div>

          {/* LCP fetchpriority */}
          <div className="toggle-row">
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--fg-primary)' }}>
                Hero Banner LCP Booster (fetchpriority="high")
              </div>
              <div style={{ fontSize: '11.5px', color: 'var(--fg-secondary)', marginTop: '2px' }}>
                Removes lazy-load from above-the-fold hero banners and requests early network fetch.
              </div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={localConfig.inject_fetchpriority_hero}
                onChange={(e) => setLocalConfig({ ...localConfig, inject_fetchpriority_hero: e.target.checked })}
              />
              <span className="toggle-slider" />
            </label>
          </div>

          {/* Native Lazy Loading */}
          <div className="toggle-row">
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--fg-primary)' }}>
                Native Lazy-Loading (loading="lazy")
              </div>
              <div style={{ fontSize: '11.5px', color: 'var(--fg-secondary)', marginTop: '2px' }}>
                Defers offscreen catalog images until customer scrolls near viewport.
              </div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={localConfig.inject_lazy_loading}
                onChange={(e) => setLocalConfig({ ...localConfig, inject_lazy_loading: e.target.checked })}
              />
              <span className="toggle-slider" />
            </label>
          </div>

          {/* Async Image Decoding */}
          <div className="toggle-row">
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--fg-primary)' }}>
                Async Image Decoding (decoding="async")
              </div>
              <div style={{ fontSize: '11.5px', color: 'var(--fg-secondary)', marginTop: '2px' }}>
                Frees main thread while images decompress, improving Interaction to Next Paint (INP).
              </div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={localConfig.inject_async_decoding}
                onChange={(e) => setLocalConfig({ ...localConfig, inject_async_decoding: e.target.checked })}
              />
              <span className="toggle-slider" />
            </label>
          </div>

          {/* CLS Dimensions */}
          <div className="toggle-row">
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--fg-primary)' }}>
                Enforce Layout Shift Dimensions (width &amp; height)
              </div>
              <div style={{ fontSize: '11.5px', color: 'var(--fg-secondary)', marginTop: '2px' }}>
                Reserves aspect ratio space on page render to eliminate CLS layout jank.
              </div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={localConfig.enforce_cls_dimensions}
                onChange={(e) => setLocalConfig({ ...localConfig, enforce_cls_dimensions: e.target.checked })}
              />
              <span className="toggle-slider" />
            </label>
          </div>

          {/* SEO Alt Tags */}
          <div className="toggle-row">
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--fg-primary)' }}>
                Auto-Generate Alt Tags &amp; SEO Slugs
              </div>
              <div style={{ fontSize: '11.5px', color: 'var(--fg-secondary)', marginTop: '2px' }}>
                Synthesizes keyword-rich descriptive alt attributes from product titles for Google Images.
              </div>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={localConfig.auto_generate_alt_tags}
                onChange={(e) => setLocalConfig({ ...localConfig, auto_generate_alt_tags: e.target.checked })}
              />
              <span className="toggle-slider" />
            </label>
          </div>
        </div>

        {/* Modal Actions */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
          <button onClick={onClose} className="btn btn-secondary">
            Cancel
          </button>
          <button onClick={handleSave} className="btn btn-green">
            {saved ? <Check size={16} /> : <Save size={16} />}
            {saved ? 'Saved Successfully!' : 'Save Settings'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal;
