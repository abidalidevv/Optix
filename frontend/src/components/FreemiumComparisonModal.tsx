import React from 'react';
import { X, Check, ShieldCheck, Sparkles } from 'lucide-react';

interface FreemiumComparisonModalProps {
  onClose?: () => void;
  onSelectPlan: (plan: 'free' | 'pro') => void;
  currentPlan: 'free' | 'pro';
  isEmbedded?: boolean;
}

export const FreemiumComparisonModal: React.FC<FreemiumComparisonModalProps> = ({
  onClose,
  onSelectPlan,
  currentPlan,
  isEmbedded = false
}) => {
  const content = (
    <div className={isEmbedded ? "card-container" : "modal-content"} style={isEmbedded ? { margin: 0 } : { maxWidth: '940px' }}>
      {/* Header */}
      <div className="modal-header">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
            <span className="container-badge badge-emerald">
              DISRUPTIVE FREEMIUM ARCHITECTURE
            </span>
            <span className="container-badge badge-cyan">
              SHOPIFY APP STORE TEARDOWN
            </span>
          </div>
          <h2 className="modal-title">
            Optix vs Legacy Shopify Optimizers
          </h2>
          <p className="modal-subtitle">
            10x higher free tier quota than TinyIMG with enterprise-grade AVIF + WebP dual format pipeline.
          </p>
        </div>

        {onClose && !isEmbedded && (
          <button onClick={onClose} className="modal-close-btn" title="Close">
            <X size={16} />
          </button>
        )}
      </div>

      {/* Pricing Cards Grid */}
      <div className="pricing-grid">
        {/* Free Forever */}
        <div className="pricing-card">
          <div className="pricing-card-header">
            <div className="pricing-tier-tag" style={{ color: 'var(--fg-secondary)' }}>
              DISRUPTIVE FREE TIER
            </div>
            <div className="pricing-price">
              $0 <small>/ forever</small>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--fg-secondary)', marginTop: '4px' }}>
              For emerging stores that want enterprise PageSpeed with zero recurring cost.
            </p>
          </div>

          <ul className="pricing-features-list">
            <li className="pricing-feature-item">
              <Check size={16} />
              <span><strong>500 Images 100% Free</strong> (TinyIMG gives only 50)</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Universal WebP Conversion (Quality 82)</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Instant Core Web Vitals Audit</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Native Lazy-Loading &amp; Async Decoding Injection</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Zero-Risk Theme Sandbox Duplicate</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>1-Click Safe Rollback Backup</span>
            </li>
          </ul>

          <button
            onClick={() => {
              onSelectPlan('free');
              if (onClose) onClose();
            }}
            className="btn btn-secondary"
            style={{ width: '100%', padding: '10px' }}
          >
            {currentPlan === 'free' ? '✓ Currently Active Plan' : 'Select Free Forever'}
          </button>
        </div>

        {/* Pro Unlimited */}
        <div className="pricing-card featured">
          <div style={{
            position: 'absolute',
            top: '-12px',
            right: '20px',
            background: 'var(--p-green)',
            color: '#ffffff',
            fontSize: '11px',
            fontWeight: 700,
            padding: '3px 10px',
            borderRadius: '999px',
            boxShadow: '0 2px 6px rgba(0, 128, 96, 0.3)',
            display: 'flex',
            alignItems: 'center',
            gap: '4px'
          }}>
            <Sparkles size={12} />
            MOST POPULAR FOR SHOPIFY
          </div>

          <div className="pricing-card-header">
            <div className="pricing-tier-tag" style={{ color: 'var(--p-green)' }}>
              PRO UNLIMITED COCKPIT
            </div>
            <div className="pricing-price">
              $9 <small>/ month</small>
            </div>
            <p style={{ fontSize: '12px', color: 'var(--fg-secondary)', marginTop: '4px' }}>
              Full store catalog optimization with next-gen AVIF and priority delivery.
            </p>
          </div>

          <ul className="pricing-features-list">
            <li className="pricing-feature-item">
              <Check size={16} />
              <span><strong>Unlimited Store Media Catalog</strong> (No caps)</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span><strong>Dual Format Engine:</strong> Next-Gen AVIF + WebP Fallback</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span><strong>Hero Banner LCP Accelerator:</strong> fetchpriority="high"</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>SSIM &gt; 0.9996 Perceptual Lossless Guarantee</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Automated Theme Liquid Remapper (Zero 404s)</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Automated SEO Alt-Tag &amp; Slug Synthesizer</span>
            </li>
            <li className="pricing-feature-item">
              <Check size={16} />
              <span>Unlimited Snapshot Vault &amp; Emergency Rollbacks</span>
            </li>
          </ul>

          <button
            onClick={() => {
              onSelectPlan('pro');
              if (onClose) onClose();
            }}
            className="btn btn-green"
            style={{ width: '100%', padding: '10px' }}
          >
            {currentPlan === 'pro' ? '✓ Currently Active Plan' : 'Upgrade to Pro Unlimited ($9/mo)'}
          </button>
        </div>
      </div>

      {/* Competitor Teardown Comparison Matrix */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--fg-primary)' }}>
            Feature Comparison: Optix vs Shopify Market Alternatives
          </h3>
          <span style={{ fontSize: '11px', color: 'var(--fg-secondary)', fontFamily: 'JetBrains Mono, monospace' }}>
            Verified Oct 2026 Telemetry
          </span>
        </div>

        <div className="teardown-table-wrapper">
          <table className="teardown-table">
            <thead>
              <tr>
                <th>Capability / Guarantee</th>
                <th style={{ color: 'var(--p-green)', fontWeight: 800 }}>Optix ($9/mo)</th>
                <th>TinyIMG ($14/mo)</th>
                <th>Crush.pics ($19.99/mo)</th>
                <th>Compresso</th>
                <th>Booster ($29/mo)</th>
              </tr>
            </thead>
            <tbody>
              <tr className="highlight-row">
                <td><strong>Free Tier Allowance</strong></td>
                <td><strong style={{ color: 'var(--p-green)' }}>500 Images</strong></td>
                <td>50 Images</td>
                <td>25 MB (~15 imgs)</td>
                <td>100 Images</td>
                <td>0 Images</td>
              </tr>
              <tr>
                <td><strong>Next-Gen AVIF Support</strong></td>
                <td><span className="container-badge badge-emerald">✓ Included ($9)</span></td>
                <td>$28/mo plan</td>
                <td>$19.99/mo</td>
                <td style={{ color: 'var(--fg-muted)' }}>Skips 326 files</td>
                <td style={{ color: 'var(--fg-muted)' }}>None</td>
              </tr>
              <tr>
                <td><strong>Dual Fallback (AVIF + WebP)</strong></td>
                <td><span className="container-badge badge-emerald">✓ Automated</span></td>
                <td style={{ color: 'var(--fg-muted)' }}>WebP only</td>
                <td style={{ color: 'var(--fg-muted)' }}>WebP only</td>
                <td style={{ color: 'var(--fg-muted)' }}>None</td>
                <td style={{ color: 'var(--fg-muted)' }}>WebP only</td>
              </tr>
              <tr>
                <td><strong>Compression Modes</strong></td>
                <td><span className="container-badge badge-cyan">Low, Med, High</span></td>
                <td>Basic</td>
                <td>Lossless / Balanced</td>
                <td>Aggressive only</td>
                <td>Single mode</td>
              </tr>
              <tr>
                <td><strong>Theme Sandbox Guard</strong></td>
                <td><span className="container-badge badge-emerald">✓ Isolated Sandbox</span></td>
                <td style={{ color: 'var(--tint-rose-text)' }}>Live Overwrite</td>
                <td style={{ color: 'var(--tint-rose-text)' }}>Live Overwrite</td>
                <td style={{ color: 'var(--tint-rose-text)' }}>Live Overwrite</td>
                <td style={{ color: 'var(--tint-rose-text)' }}>Live Overwrite</td>
              </tr>
              <tr>
                <td><strong>LCP fetchpriority Booster</strong></td>
                <td><span className="container-badge badge-emerald">✓ Automated</span></td>
                <td style={{ color: 'var(--fg-muted)' }}>Manual</td>
                <td style={{ color: 'var(--fg-muted)' }}>None</td>
                <td style={{ color: 'var(--fg-muted)' }}>None</td>
                <td style={{ color: 'var(--fg-muted)' }}>None</td>
              </tr>
              <tr>
                <td><strong>Offline Rollback Vault</strong></td>
                <td><span className="container-badge badge-emerald">✓ 100% Offline Vault</span></td>
                <td>30 days</td>
                <td>30 days</td>
                <td style={{ color: 'var(--fg-muted)' }}>None</td>
                <td>14 days</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Safety Notice Footer */}
      <div style={{
        marginTop: '18px',
        padding: '12px 16px',
        background: 'var(--bg-subtle)',
        border: '1px solid var(--border-hairline)',
        borderRadius: 'var(--radius-sm)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '12px',
        color: 'var(--fg-secondary)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ShieldCheck size={16} color="#008060" />
          <span>Billed securely through native Shopify App Billing API &bull; Cancel anytime with 1 click.</span>
        </div>
        <span style={{ fontWeight: 600, color: 'var(--fg-primary)' }}>
          14-Day Money Back Guarantee
        </span>
      </div>
    </div>
  );

  if (isEmbedded) {
    return content;
  }

  return (
    <div className="modal-overlay">
      {content}
    </div>
  );
};

export default FreemiumComparisonModal;
