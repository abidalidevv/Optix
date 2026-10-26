import React, { useState, useMemo } from 'react';
import { Search, AlertCircle, Eye, RotateCcw, Check, Sparkles, Edit2, Save, X, UploadCloud } from 'lucide-react';
import type { ImageAuditItem } from '../types';
import { optixApi } from '../api';

interface ImageTableProps {
  images: ImageAuditItem[];
  onCompareImage: (image: ImageAuditItem) => void;
  onRefresh?: () => void;
}

export const ImageTable: React.FC<ImageTableProps> = ({ images, onCompareImage, onRefresh }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFormat, setSelectedFormat] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedProduct, setSelectedProduct] = useState<string>('all');
  const [heavyOnly, setHeavyOnly] = useState(false);
  const [altFilter, setAltFilter] = useState<'all' | 'dummy' | 'optimized'>('all');
  const [sortBy, setSortBy] = useState<'size' | 'savings' | 'name'>('size');
  const [page, setPage] = useState(1);
  const [restoredImages, setRestoredImages] = useState<Set<string>>(new Set());

  // Alt Text Management State
  const [altOverrides, setAltOverrides] = useState<Record<string, string>>({});
  const [editingFilename, setEditingFilename] = useState<string | null>(null);
  const [editValue, setEditValue] = useState<string>('');
  const [isBatchOptimizingAlt, setIsBatchOptimizingAlt] = useState<boolean>(false);
  const [altBannerMessage, setAltBannerMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const pageSize = 15;

  // Helper to determine if an alt tag is dummy or missing
  const isDummyAlt = (alt?: string, filename?: string) => {
    if (!alt || !alt.trim()) return true;
    const clean = alt.trim().toLowerCase();
    if (/^\d+[\s\-_]*(tibbe[\s\-_]*shifa)?$/.test(clean)) return true;
    if (filename && (clean === filename.toLowerCase() || clean === filename.split('.')[0].toLowerCase())) return true;
    if (/\.(png|jpg|jpeg|webp|avif|gif)$/i.test(clean)) return true;
    return false;
  };

  const handleRowRestore = async (filename: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await optixApi.restoreSingleImage(filename);
      setRestoredImages(prev => new Set(prev).add(filename));
    } catch (err) {
      console.error('Failed to restore image:', err);
    }
  };

  // 1-Click Batch Auto-Generate SEO Alt Tags for All Images (Instant O(1) Mapping)
  const handleBatchOptimizeAlt = async () => {
    try {
      setIsBatchOptimizingAlt(true);
      setAltBannerMessage(null);
      const res = await optixApi.optimizeAllAltTexts();
      
      // Update local state overrides instantly without N+1 HTTP loop
      if (res.mapping) {
        setAltOverrides(prev => ({ ...prev, ...res.mapping }));
      }
      setAltBannerMessage({
        type: 'success',
        text: `✓ Successfully generated unique Google SEO Alt Tags for ${res.optimized_count || images.length} images!`
      });
      if (onRefresh) onRefresh();
    } catch (err: any) {
      setAltBannerMessage({
        type: 'error',
        text: 'Failed to auto-generate alt texts: ' + (err.message || 'Error')
      });
    } finally {
      setIsBatchOptimizingAlt(false);
    }
  };

  const [isSyncingShopify, setIsSyncingShopify] = useState(false);

  // Sync saved Alt Tags directly to Shopify Live store media via GraphQL
  const handleSyncShopify = async () => {
    try {
      setIsSyncingShopify(true);
      setAltBannerMessage(null);
      const res = await optixApi.syncAltTextsToShopify();
      setAltBannerMessage({
        type: res.success ? 'success' : 'error',
        text: res.message
      });
    } catch (err: any) {
      setAltBannerMessage({
        type: 'error',
        text: 'Failed to sync to Shopify: ' + (err.message || 'Error')
      });
    } finally {
      setIsSyncingShopify(false);
    }
  };

  // Quick 1-Image AI Suggestion
  const handleQuickSuggest = async (filename: string, category: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const res = await optixApi.suggestAltText(filename, category);
      if (res?.suggested_alt) {
        await optixApi.updateAltText(filename, res.suggested_alt);
        setAltOverrides(prev => ({ ...prev, [filename]: res.suggested_alt }));
      }
    } catch (err) {
      console.error('Failed to suggest alt text:', err);
    }
  };

  // Save Inline Edit
  const handleSaveInlineAlt = async (filename: string) => {
    if (!editValue.trim()) return;
    try {
      await optixApi.updateAltText(filename, editValue.trim());
      setAltOverrides(prev => ({ ...prev, [filename]: editValue.trim() }));
      setEditingFilename(null);
    } catch (err) {
      console.error('Failed to save alt text:', err);
    }
  };

  // Calculate dummy count
  const dummyAltCount = useMemo(() => {
    return images.filter(img => isDummyAlt(altOverrides[img.filename] ?? img.alt_text, img.filename)).length;
  }, [images, altOverrides]);

  // Filter & Sort Logic
  const PRODUCT_KEYWORDS: Record<string, string[]> = {
    meda: ["meda", "sm1", "sm2", "sm3", "196ff892", "a76c6123", "a69130e8", "9ff0bcf4", "2c58f670", "55b477cc", "7d2fa1e4", "1f10d7e1", "bba3c5fe", "04d35db1", "d758073d", "117bca03", "e8c3fe90", "83c5d0bf", "e6404290", "3fcd2585", "images_2", "46348965"],
    jaryan: ["jaryan", "nj1", "nj2", "nj3", "d054e9bd", "46348949", "46210583855345"],
    bawasir: ["bawasir", "bawaseer", "piles", "c54401f7", "46348966", "46210583888113"],
    qabz: ["qabz", "constipation", "46210607", "46348957", "46348961", "46210583953649"],
    sugar: ["sugar", "87b6d299", "46348963", "46210593", "46210583920881"],
    dublepan: ["dublepan", "dublapun", "1c01e1d5", "46348964", "46210584", "46210583986417"],
    likoria: ["likoria", "c9fd6a39", "46348951", "46348952", "46210618"]
  };

  const filteredImages = useMemo(() => {
    return images.filter(img => {
      const currentAlt = altOverrides[img.filename] ?? img.alt_text;
      
      if (searchTerm) {
        const term = searchTerm.toLowerCase();
        const matchName = img.filename.toLowerCase().includes(term);
        const matchAlt = (currentAlt || '').toLowerCase().includes(term);
        if (!matchName && !matchAlt) return false;
      }
      if (selectedProduct !== 'all') {
        const kws = PRODUCT_KEYWORDS[selectedProduct] || [];
        const fn = img.filename.toLowerCase();
        const url = (img.url || '').toLowerCase();
        const id = (img.id || '').toLowerCase();
        const matches = kws.some(kw => fn.includes(kw) || url.includes(kw) || id.includes(kw));
        if (!matches) return false;
      }
      if (selectedFormat !== 'all') {
        const ext = img.filename.split('.').pop()?.toLowerCase();
        if (selectedFormat === 'png' && ext !== 'png') return false;
        if (selectedFormat === 'jpg' && ext !== 'jpg' && ext !== 'jpeg') return false;
        if (selectedFormat === 'webp' && ext !== 'webp') return false;
        if (selectedFormat === 'avif' && ext !== 'avif') return false;
      }
      if (selectedCategory !== 'all' && img.category.toLowerCase() !== selectedCategory.toLowerCase()) {
        return false;
      }
      if (heavyOnly && !img.is_heavy) {
        return false;
      }
      if (altFilter === 'dummy' && !isDummyAlt(currentAlt, img.filename)) {
        return false;
      }
      if (altFilter === 'optimized' && isDummyAlt(currentAlt, img.filename)) {
        return false;
      }
      return true;
    }).sort((a, b) => {
      if (sortBy === 'size') {
        return b.original_size_bytes - a.original_size_bytes;
      } else if (sortBy === 'savings') {
        return b.estimated_savings_pct - a.estimated_savings_pct;
      } else {
        return a.filename.localeCompare(b.filename);
      }
    });
  }, [images, searchTerm, selectedProduct, selectedFormat, selectedCategory, heavyOnly, altFilter, sortBy, altOverrides]);

  const totalPages = Math.ceil(filteredImages.length / pageSize) || 1;
  const paginatedImages = filteredImages.slice((page - 1) * pageSize, page * pageSize);

  const getFormatBadge = (filename: string) => {
    const ext = filename.split('.').pop()?.toUpperCase() || 'IMG';
    if (ext === 'PNG') return <span className="container-badge badge-rose" style={{ fontSize: '10px' }}>PNG</span>;
    if (ext === 'WEBP') return <span className="container-badge badge-cyan" style={{ fontSize: '10px' }}>WEBP</span>;
    if (ext === 'AVIF') return <span className="container-badge badge-emerald" style={{ fontSize: '10px' }}>AVIF</span>;
    return <span className="container-badge badge-amber" style={{ fontSize: '10px' }}>{ext}</span>;
  };

  return (
    <div className="card-container" style={{ padding: '0', overflow: 'hidden' }}>
      {/* Table Top Bar */}
      <div style={{
        padding: '16px 20px',
        borderBottom: '1px solid var(--border-hairline)',
        background: 'var(--bg-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '12px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span className="status-pulse" />
          <span style={{ fontFamily: 'Archivo, sans-serif', fontWeight: 700, fontSize: '15px', color: 'var(--fg-primary)' }}>
            Store Media Assets &bull; Universal Catalog
          </span>
        </div>

        {/* 1-Click SEO Alt-Text Batch Optimizer Button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <button
            onClick={handleBatchOptimizeAlt}
            disabled={isBatchOptimizingAlt}
            className="btn btn-green"
            style={{ padding: '7px 14px', fontSize: '12.5px' }}
            title="Auto-generate Google SEO alt text for all images with missing or dummy alt tags"
          >
            <Sparkles size={14} />
            {isBatchOptimizingAlt
              ? 'Generating SEO Alt Tags...'
              : `Auto-Generate SEO Alt Tags (${dummyAltCount} Dummy Detected)`}
          </button>

          <button
            onClick={handleSyncShopify}
            disabled={isSyncingShopify}
            className="btn btn-secondary"
            style={{ padding: '7px 12px', fontSize: '12.5px', display: 'flex', alignItems: 'center', gap: '6px' }}
            title="Push saved SEO Alt Tags directly to Shopify Admin (Live store media)"
          >
            <UploadCloud size={14} color="#008060" />
            {isSyncingShopify ? 'Syncing to Shopify...' : 'Sync to Shopify Live'}
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontFamily: 'JetBrains Mono, monospace', color: 'var(--fg-secondary)' }}>
            <span>{images.length} Files Total</span>
            <span>&bull;</span>
            <span>{filteredImages.length} Matches</span>
          </div>
        </div>
      </div>

      {/* Notification Banner */}
      {altBannerMessage && (
        <div style={{
          padding: '10px 18px',
          background: altBannerMessage.type === 'success' ? '#e4f8f0' : '#fef2f2',
          borderBottom: `1px solid ${altBannerMessage.type === 'success' ? '#a7f3d0' : '#fecaca'}`,
          color: altBannerMessage.type === 'success' ? '#008060' : '#dc2626',
          fontSize: '12px',
          fontFamily: 'JetBrains Mono, monospace',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <span>{altBannerMessage.text}</span>
          <button
            onClick={() => setAltBannerMessage(null)}
            style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'inherit', fontWeight: 'bold' }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Filter and Search Bar (Crush.pics Style Search) */}
      <div style={{
        padding: '12px 18px',
        borderBottom: '1px solid var(--border-subdued)',
        background: 'var(--bg-surface)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '10px'
      }}>
        {/* Search */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          background: 'var(--bg-hover)',
          border: '1px solid var(--border-hairline)',
          borderRadius: 'var(--radius-sm)',
          padding: '6px 12px',
          minWidth: '260px'
        }}>
          <Search size={14} color="var(--fg-secondary)" />
          <input
            type="text"
            placeholder="Search images or alt text..."
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); setPage(1); }}
            style={{
              background: 'transparent',
              border: 'none',
              outline: 'none',
              fontSize: '12px',
              fontFamily: 'JetBrains Mono, monospace',
              color: 'var(--fg-primary)',
              width: '100%'
            }}
          />
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}>
          {/* Single Page / Product Filter */}
          <select
            value={selectedProduct}
            onChange={(e) => { setSelectedProduct(e.target.value); setPage(1); }}
            style={{
              background: selectedProduct !== 'all' ? '#e4f8f0' : 'var(--bg-surface)',
              border: `1px solid ${selectedProduct !== 'all' ? '#008060' : 'var(--border-hairline)'}`,
              color: selectedProduct !== 'all' ? '#008060' : 'var(--fg-primary)',
              fontWeight: selectedProduct !== 'all' ? 700 : 500,
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              outline: 'none',
              cursor: 'pointer'
            }}
          >
            <option value="all">📦 All Store Images</option>
            <option value="meda">🥣 شفائے معدہ (Shifa-e-Medda)</option>
            <option value="jaryan">⚡ نجات جریان (Nijat-e-Jaryaan)</option>
            <option value="bawasir">🌿 نجات بواسیر (Nijat-e-Bawaseer)</option>
            <option value="qabz">🍃 قبض کشا (Qabz Kusha)</option>
            <option value="sugar">🩸 شوگر کیئر (Sugar Care)</option>
            <option value="dublepan">💪 نجات دبلپن (Nijat Dublepan)</option>
            <option value="likoria">🌸 نجات لیکوریا (Nijat Likoria)</option>
          </select>

          <select
            value={selectedFormat}
            onChange={(e) => { setSelectedFormat(e.target.value); setPage(1); }}
            style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-hairline)',
              color: 'var(--fg-primary)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              outline: 'none'
            }}
          >
            <option value="all">All Formats</option>
            <option value="png">PNG (Heavy)</option>
            <option value="jpg">JPG</option>
            <option value="webp">WebP</option>
            <option value="avif">AVIF</option>
          </select>

          <select
            value={selectedCategory}
            onChange={(e) => { setSelectedCategory(e.target.value); setPage(1); }}
            style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-hairline)',
              color: 'var(--fg-primary)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              outline: 'none'
            }}
          >
            <option value="all">All Categories</option>
            <option value="files">Hero Files</option>
            <option value="products">Products</option>
            <option value="collections">Collections</option>
            <option value="theme-assets">Theme Assets</option>
          </select>

          {/* SEO Alt Text Status Filter */}
          <select
            value={altFilter}
            onChange={(e) => { setAltFilter(e.target.value as any); setPage(1); }}
            style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-hairline)',
              color: 'var(--fg-primary)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              outline: 'none'
            }}
          >
            <option value="all">All Alt Tags</option>
            <option value="dummy">Dummy / Missing ({dummyAltCount})</option>
            <option value="optimized">SEO Optimized</option>
          </select>

          <button
            onClick={() => { setHeavyOnly(!heavyOnly); setPage(1); }}
            className={`btn ${heavyOnly ? 'badge-rose' : 'btn-secondary'}`}
            style={{ padding: '6px 10px', fontSize: '11px' }}
          >
            <AlertCircle size={13} />
            Heavy (&gt;700KB)
          </button>

          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            style={{
              background: 'var(--bg-surface)',
              border: '1px solid var(--border-hairline)',
              color: 'var(--fg-primary)',
              borderRadius: 'var(--radius-sm)',
              padding: '6px 10px',
              outline: 'none'
            }}
          >
            <option value="size">Sort: Heaviest First</option>
            <option value="savings">Sort: Highest Savings %</option>
            <option value="name">Sort: Filename</option>
          </select>
        </div>
      </div>

      {/* Images Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '13px' }}>
          <thead>
            <tr style={{
              background: 'var(--bg-subtle)',
              borderBottom: '1px solid var(--border-hairline)',
              color: 'var(--fg-secondary)',
              fontSize: '11px',
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
              fontFamily: 'JetBrains Mono, monospace'
            }}>
              <th style={{ padding: '12px 18px' }}>Asset &bull; Resolution</th>
              <th style={{ padding: '12px 16px', minWidth: '220px' }}>SEO Alt Tag (Google Ranking)</th>
              <th style={{ padding: '12px 16px' }}>Original</th>
              <th style={{ padding: '12px 16px' }}>AVIF (Projected)</th>
              <th style={{ padding: '12px 16px' }}>Savings</th>
              <th style={{ padding: '12px 18px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {paginatedImages.map((img) => {
              const currentAlt = altOverrides[img.filename] ?? img.alt_text;
              const isDummy = isDummyAlt(currentAlt, img.filename);
              const isEditing = editingFilename === img.filename;

              return (
                <tr
                  key={img.id}
                  style={{
                    borderBottom: '1px solid var(--border-subdued)',
                    transition: 'background 0.15s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = 'var(--bg-hover)'}
                  onMouseLeave={(e) => e.currentTarget.style.background = 'transparent'}
                >
                  {/* Asset Column */}
                  <td style={{ padding: '12px 18px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div style={{
                        width: '42px',
                        height: '42px',
                        borderRadius: 'var(--radius-sm)',
                        background: '#09090b',
                        border: '1px solid var(--border-hairline)',
                        overflow: 'hidden',
                        flexShrink: 0,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        <img
                          src={optixApi.getImagePreviewUrl(img.filename, 'original', img.id)}
                          alt={currentAlt || img.filename}
                          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          onError={(e) => {
                            (e.target as HTMLElement).style.display = 'none';
                          }}
                        />
                      </div>

                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontWeight: 600, color: 'var(--fg-primary)' }}>
                          <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '12px' }}>
                            {img.filename}
                          </span>
                          {img.is_heavy && (
                            <span className="container-badge badge-rose" style={{ fontSize: '9px', padding: '1px 4px' }}>
                              HEAVY
                            </span>
                          )}
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '3px' }}>
                          {getFormatBadge(img.filename)}
                          <span style={{ fontSize: '11px', color: 'var(--fg-secondary)', fontFamily: 'JetBrains Mono, monospace' }}>
                            {img.dimensions || '1200x1200'} &bull; {img.category}
                          </span>
                        </div>
                      </div>
                    </div>
                  </td>

                  {/* SEO Alt Text Column (Interactive Inline AI Engine) */}
                  <td style={{ padding: '12px 16px', maxWidth: '260px' }}>
                    {isEditing ? (
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                          <input
                            type="text"
                            value={editValue}
                            onChange={(e) => setEditValue(e.target.value)}
                            onKeyDown={(e) => { if (e.key === 'Enter') handleSaveInlineAlt(img.filename); }}
                            autoFocus
                            style={{
                              width: '100%',
                              background: 'var(--bg-subtle)',
                              border: `1px solid ${editValue.length > 125 ? '#ef4444' : 'var(--p-green)'}`,
                              borderRadius: 'var(--radius-sm)',
                              padding: '4px 8px',
                              fontSize: '11.5px',
                              fontFamily: 'JetBrains Mono, monospace',
                              color: 'var(--fg-primary)',
                              outline: 'none'
                            }}
                          />
                          <button
                            onClick={() => handleSaveInlineAlt(img.filename)}
                            className="btn btn-green"
                            style={{ padding: '4px 6px', fontSize: '10px' }}
                            title="Save Alt Text"
                          >
                            <Save size={11} />
                          </button>
                          <button
                            onClick={() => setEditingFilename(null)}
                            className="btn btn-secondary"
                            style={{ padding: '4px 6px', fontSize: '10px' }}
                            title="Cancel"
                          >
                            <X size={11} />
                          </button>
                        </div>
                        <div style={{
                          display: 'flex',
                          justifyContent: 'flex-end',
                          marginTop: '2px',
                          fontSize: '10px',
                          color: editValue.length > 125 ? '#ef4444' : 'var(--fg-muted)',
                          fontFamily: 'JetBrains Mono, monospace'
                        }}>
                          {editValue.length}/125 chars {editValue.length > 125 ? '(WCAG warning)' : ''}
                        </div>
                      </div>
                    ) : (
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '6px' }}>
                        <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', fontSize: '11.5px' }}>
                          {isDummy ? (
                            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '5px' }}>
                              <span style={{
                                background: '#fef3c7',
                                color: '#92400e',
                                border: '1px solid #fde68a',
                                borderRadius: '3px',
                                padding: '1px 5px',
                                fontSize: '9px',
                                fontWeight: 700,
                                fontFamily: 'JetBrains Mono, monospace'
                              }}>
                                DUMMY
                              </span>
                              <span style={{ color: 'var(--fg-muted)' }}>{currentAlt || 'Missing Alt Text'}</span>
                            </span>
                          ) : (
                            <span style={{ color: 'var(--fg-primary)', fontWeight: 500 }} title={currentAlt}>
                              {currentAlt}
                            </span>
                          )}
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '3px', flexShrink: 0 }}>
                          <button
                            onClick={(e) => handleQuickSuggest(img.filename, img.category, e)}
                            className="btn btn-secondary"
                            style={{ padding: '3px 6px', fontSize: '10px' }}
                            title="AI Auto-Generate SEO Alt Tag for this image"
                          >
                            <Sparkles size={11} color="#008060" />
                          </button>
                          <button
                            onClick={() => { setEditingFilename(img.filename); setEditValue(currentAlt || ''); }}
                            className="btn btn-secondary"
                            style={{ padding: '3px 6px', fontSize: '10px' }}
                            title="Edit Alt Text"
                          >
                            <Edit2 size={11} />
                          </button>
                        </div>
                      </div>
                    )}
                  </td>

                  {/* Original Size Column */}
                  <td style={{ padding: '12px 16px', color: 'var(--fg-secondary)' }}>
                    <span style={{ color: img.is_heavy ? 'var(--tint-rose-text)' : 'inherit', fontWeight: img.is_heavy ? 700 : 500 }}>
                      {img.original_size_kb >= 1024
                        ? `${(img.original_size_kb / 1024).toFixed(2)} MB`
                        : `${img.original_size_kb.toLocaleString()} KB`}
                    </span>
                  </td>

                  {/* Converted AVIF Column */}
                  <td style={{ padding: '12px 16px', color: 'var(--tint-emerald-text)', fontWeight: 700 }}>
                    {img.estimated_avif_kb >= 1024
                      ? `${(img.estimated_avif_kb / 1024).toFixed(2)} MB`
                      : `${img.estimated_avif_kb.toLocaleString()} KB`}{' '}
                    <span style={{ fontSize: '10px', color: 'var(--fg-secondary)', fontWeight: 400 }}>AVIF</span>
                  </td>

                  {/* Savings Column */}
                  <td style={{ padding: '12px 16px' }}>
                    <span className="container-badge badge-emerald" style={{ fontWeight: 700 }}>
                      -{img.estimated_savings_pct}%
                    </span>
                  </td>

                  {/* Action Column */}
                  <td style={{ padding: '12px 18px', textAlign: 'right' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '6px' }}>
                      <button
                        onClick={() => onCompareImage(img)}
                        className="btn btn-secondary"
                        style={{ padding: '5px 10px', fontSize: '11px' }}
                        title="Inspect side-by-side with optical slider"
                      >
                        <Eye size={12} color="#008060" />
                        Inspect ⟷
                      </button>
                      <button
                        onClick={(e) => handleRowRestore(img.filename, e)}
                        disabled={restoredImages.has(img.filename)}
                        className="btn btn-secondary"
                        style={{
                          padding: '5px 8px',
                          fontSize: '11px',
                          color: restoredImages.has(img.filename) ? '#008060' : 'var(--fg-secondary)',
                          borderColor: restoredImages.has(img.filename) ? '#a7f3d0' : undefined
                        }}
                        title="Revert this individual image back to original uncompressed asset"
                      >
                        {restoredImages.has(img.filename) ? <Check size={12} /> : <RotateCcw size={12} />}
                        {restoredImages.has(img.filename) ? 'Restored' : 'Restore'}
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div style={{
        padding: '12px 20px',
        borderTop: '1px solid var(--border-hairline)',
        background: 'var(--bg-subtle)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '12px',
        fontFamily: 'JetBrains Mono, monospace',
        color: 'var(--fg-secondary)'
      }}>
        <div>
          Showing {(page - 1) * pageSize + 1} &ndash; {Math.min(page * pageSize, filteredImages.length)} of {filteredImages.length} images
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="btn btn-secondary"
            style={{ padding: '4px 8px', fontSize: '11px' }}
          >
            Previous
          </button>
          <span style={{ display: 'flex', alignItems: 'center', padding: '0 8px' }}>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="btn btn-secondary"
            style={{ padding: '4px 8px', fontSize: '11px' }}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default ImageTable;
