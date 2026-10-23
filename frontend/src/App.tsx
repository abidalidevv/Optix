import React, { useState, useEffect, useRef } from 'react';
import { Gauge, Layers, ShieldCheck, Zap } from 'lucide-react';
import { Header } from './components/Header';
import { SpeedAuditHero } from './components/SpeedAuditHero';
import { ImageTable } from './components/ImageTable';
import { ImageComparatorModal } from './components/ImageComparatorModal';
import { ThemeSafetyCard } from './components/ThemeSafetyCard';
import { FreemiumComparisonModal } from './components/FreemiumComparisonModal';
import { SettingsModal } from './components/SettingsModal';
import type { StoreAuditReport, OptimizationProgress, ImageAuditItem, SettingsConfig } from './types';
import { optixApi } from './api';

export const App: React.FC = () => {
  const [report, setReport] = useState<StoreAuditReport | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [activePlan, setActivePlan] = useState<'free' | 'pro'>('free');
  const [activeTab, setActiveTab] = useState<'cockpit' | 'inventory' | 'theme' | 'pricing'>('cockpit');

  // Modals state
  const [inspectImage, setInspectImage] = useState<ImageAuditItem | null>(null);
  const [showThemeGuard, setShowThemeGuard] = useState(false);
  const [showPricing, setShowPricing] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // Settings & Core Web Vitals Standard
  const [config, setConfig] = useState<SettingsConfig>({
    shop: 'ph0igg-jv.myshopify.com',
    quality_webp: 82,
    quality_avif: 74,
    strip_metadata: true,
    inject_lazy_loading: true,
    inject_async_decoding: true,
    inject_fetchpriority_hero: true,
    enforce_cls_dimensions: true,
    auto_generate_alt_tags: true,
    normalize_seo_slugs: true,
    max_width_banner: 1600,
    max_width_product: 1200,
    sandbox_theme_guard: true
  });

  // Optimization Progress State
  const [progress, setProgress] = useState<OptimizationProgress>({
    is_running: false,
    current_step: 'idle',
    total_images: 0,
    processed_images: 0,
    failed_images: 0,
    total_bytes_saved: 0,
    percent_complete: 0,
    status_message: 'Ready'
  });

  const pollIntervalRef = useRef<any>(null);

  // Initial Data Fetch
  const loadAuditData = async (forceRefresh: boolean = false) => {
    try {
      if (forceRefresh) setIsRefreshing(true);
      const data = await optixApi.getAudit(forceRefresh);
      setReport(data);
    } catch (e) {
      console.error('Error fetching audit data:', e);
    } finally {
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadAuditData();
  }, []);

  // Poll progress while optimizing
  useEffect(() => {
    if (progress.is_running) {
      pollIntervalRef.current = setInterval(async () => {
        try {
          const prog = await optixApi.getProgress();
          setProgress(prog);
          if (!prog.is_running && prog.current_step === 'completed') {
            clearInterval(pollIntervalRef.current);
            loadAuditData(true);
          }
        } catch (err) {
          console.error(err);
        }
      }, 750);
    } else {
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    }

    return () => {
      if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
    };
  }, [progress.is_running]);

  const handleStartOptimization = async (format?: string, level?: string) => {
    try {
      const targetCount = activePlan === 'pro' ? 1000 : 500;
      const res = await optixApi.startOptimization(targetCount);
      if (res.status === 'started') {
        const fmtTag = format ? format.toUpperCase() : 'DUAL AVIF+WEBP';
        const lvlTag = level ? level.toUpperCase() : 'BALANCED';
        setProgress(prev => ({
          ...prev,
          is_running: true,
          current_step: 'scanning',
          status_message: `Starting batch optimization (${fmtTag} &bull; ${lvlTag})...`,
          percent_complete: 5
        }));
      }
    } catch (e) {
      console.error('Failed to trigger optimization:', e);
    }
  };

  return (
    <div className="app-shell">
      {/* 1. App Header (Clonix Polaris Top Bar) */}
      <Header
        storeDomain={report?.shop || config.shop}
        onOpenSettings={() => setShowSettings(true)}
        onOpenPricing={() => setShowPricing(true)}
        onOpenThemeGuard={() => setActiveTab('theme')}
        onRefreshAudit={() => loadAuditData(true)}
        isRefreshing={isRefreshing}
        activePlan={activePlan}
      />

      {/* 2. Navigation Tabs (Industrial Micro-SaaS Pill Style) */}
      <nav className="main-nav">
        <button
          onClick={() => setActiveTab('cockpit')}
          className={`nav-tab ${activeTab === 'cockpit' ? 'active' : ''}`}
        >
          <Gauge size={15} />
          <span>Speed Cockpit</span>
        </button>

        <button
          onClick={() => setActiveTab('inventory')}
          className={`nav-tab ${activeTab === 'inventory' ? 'active' : ''}`}
        >
          <Layers size={15} />
          <span>Image Catalog ({report?.total_images_count || report?.images?.length || 528})</span>
        </button>

        <button
          onClick={() => setActiveTab('theme')}
          className={`nav-tab ${activeTab === 'theme' ? 'active' : ''}`}
        >
          <ShieldCheck size={15} />
          <span>Theme Sandbox Guard</span>
        </button>

        <button
          onClick={() => setActiveTab('pricing')}
          className={`nav-tab ${activeTab === 'pricing' ? 'active' : ''}`}
        >
          <Zap size={15} />
          <span>Plans &amp; Upgrade ($9/mo)</span>
        </button>
      </nav>

      {/* 5. Main Tab Content */}
      {activeTab === 'cockpit' && (
        <>
          <SpeedAuditHero
            report={report}
            progress={progress}
            onStartOptimization={handleStartOptimization}
            isOptimizing={progress.is_running}
          />

          {/* Quick Assets Table Preview */}
          {report && (
            <div style={{ marginTop: '24px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                <h3 style={{ fontSize: '15px', fontWeight: 700, fontFamily: 'Archivo, sans-serif' }}>
                  Unoptimized Store Media ({report.images?.length || 528} Files Detected)
                </h3>
                <button
                  onClick={() => setActiveTab('inventory')}
                  className="btn btn-secondary"
                  style={{ fontSize: '12px', padding: '5px 10px' }}
                >
                  View Full Inventory &rarr;
                </button>
              </div>
              <ImageTable
                images={report.images.slice(0, 8)}
                onCompareImage={(img) => setInspectImage(img)}
              />
            </div>
          )}
        </>
      )}

      {activeTab === 'inventory' && report && (
        <ImageTable
          images={report.images}
          onCompareImage={(img) => setInspectImage(img)}
        />
      )}

      {activeTab === 'theme' && (
        <ThemeSafetyCard onClose={() => setActiveTab('cockpit')} />
      )}

      {activeTab === 'pricing' && (
        <FreemiumComparisonModal
          isEmbedded={true}
          currentPlan={activePlan}
          onSelectPlan={(plan) => setActivePlan(plan)}
        />
      )}

      {/* Theme Safety Guard Modal (if opened separately) */}
      {showThemeGuard && (
        <div className="modal-overlay">
          <div className="modal-content" style={{ maxWidth: '820px' }}>
            <ThemeSafetyCard onClose={() => setShowThemeGuard(false)} />
          </div>
        </div>
      )}

      {/* Before / After Comparator Modal */}
      {inspectImage && (
        <ImageComparatorModal
          image={inspectImage}
          onClose={() => setInspectImage(null)}
        />
      )}

      {/* Freemium & Pricing Modal */}
      {showPricing && (
        <FreemiumComparisonModal
          isEmbedded={false}
          onClose={() => setShowPricing(false)}
          onSelectPlan={(plan) => {
            setActivePlan(plan);
            setShowPricing(false);
          }}
          currentPlan={activePlan}
        />
      )}

      {/* Settings Modal */}
      {showSettings && (
        <SettingsModal
          onClose={() => setShowSettings(false)}
          config={config}
          onSaveConfig={(newCfg) => setConfig(newCfg)}
        />
      )}
    </div>
  );
};

export default App;
