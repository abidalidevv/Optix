import React from 'react';
import { ShieldCheck, Settings, RefreshCw, Zap } from 'lucide-react';

interface HeaderProps {
  storeDomain: string;
  onOpenSettings: () => void;
  onOpenPricing: () => void;
  onOpenThemeGuard: () => void;
  onRefreshAudit: () => void;
  isRefreshing: boolean;
  activePlan: 'free' | 'pro';
}

export const Header: React.FC<HeaderProps> = ({
  storeDomain,
  onOpenSettings,
  onOpenPricing,
  onOpenThemeGuard,
  onRefreshAudit,
  isRefreshing,
  activePlan
}) => {
  return (
    <header className="top-header">
      {/* Brand Logo & Telemetry Tag */}
      <div className="brand-group">
        <div className="logo-badge">
          OP
        </div>

        <div>
          <div className="page-title">
            <span>Optix</span>
            <span className="brand-version-pill">
              v2.4.0
            </span>
            <span className="container-badge badge-cyan" style={{ fontSize: '11px', textTransform: 'uppercase' }}>
              AVIF Engine
            </span>
          </div>
          <p className="page-subtitle">
            Shopify High-Performance Optical Image Compressor &amp; PageSpeed Booster
          </p>
        </div>
      </div>

      {/* Store Context & Controls */}
      <div className="top-actions">
        {/* Active Store */}
        <div className="store-pill">
          <span className="status-pulse" />
          <span style={{ color: 'var(--fg-secondary)' }}>Store:</span>
          <span>{storeDomain}</span>
        </div>

        {/* Plan Pill */}
        <button
          onClick={onOpenPricing}
          className={`btn ${activePlan === 'pro' ? 'badge-emerald' : 'badge-amber'}`}
          style={{ padding: '6px 12px', fontSize: '11px', fontFamily: 'JetBrains Mono, monospace', borderRadius: 'var(--radius-sm)', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
        >
          <Zap size={12} />
          <span>{activePlan === 'pro' ? 'PRO UNLIMITED ($9/MO)' : 'FREE TIER (500 IMAGES)'}</span>
        </button>

        {/* Theme Safety Guard */}
        <button
          onClick={onOpenThemeGuard}
          className="btn btn-secondary"
          style={{ padding: '6px 12px', fontSize: '12px' }}
        >
          <ShieldCheck size={14} color="#008060" />
          Theme Sandbox
        </button>

        {/* Refresh Audit */}
        <button
          onClick={onRefreshAudit}
          disabled={isRefreshing}
          className="btn btn-secondary"
          style={{ padding: '7px 10px' }}
          title="Re-run PageSpeed Telemetry"
        >
          <RefreshCw size={14} style={{ animation: isRefreshing ? 'spin 1s linear infinite' : 'none' }} />
        </button>

        {/* Settings */}
        <button
          onClick={onOpenSettings}
          className="btn btn-secondary"
          style={{ padding: '7px 10px' }}
          title="Optical Engine Standards"
        >
          <Settings size={14} />
        </button>
      </div>
    </header>
  );
};
