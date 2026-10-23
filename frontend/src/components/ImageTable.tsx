import React, { useState, useMemo } from 'react';
import { Search, AlertCircle, Eye, Image as ImageIcon, RotateCcw, Check } from 'lucide-react';
import type { ImageAuditItem } from '../types';
import { optixApi } from '../api';

interface ImageTableProps {
  images: ImageAuditItem[];
  onCompareImage: (image: ImageAuditItem) => void;
}

export const ImageTable: React.FC<ImageTableProps> = ({ images, onCompareImage }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFormat, setSelectedFormat] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [heavyOnly, setHeavyOnly] = useState(false);
  const [sortBy, setSortBy] = useState<'size' | 'savings' | 'name'>('size');
  const [page, setPage] = useState(1);
  const [restoredImages, setRestoredImages] = useState<Set<string>>(new Set());
  const pageSize = 15;

  const handleRowRestore = async (filename: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      await optixApi.restoreSingleImage(filename);
      setRestoredImages(prev => new Set(prev).add(filename));
    } catch (err) {
      console.error('Failed to restore image:', err);
    }
  };

  // Filter & Sort Logic
  const filteredImages = useMemo(() => {
    return images.filter(img => {
      if (searchTerm && !img.filename.toLowerCase().includes(searchTerm.toLowerCase())) {
        return false;
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
  }, [images, searchTerm, selectedFormat, selectedCategory, heavyOnly, sortBy]);

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
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontFamily: 'JetBrains Mono, monospace', color: 'var(--fg-secondary)' }}>
          <span>{images.length} Files Total</span>
          <span>&bull;</span>
          <span>{filteredImages.length} Matches</span>
        </div>
      </div>

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
            <option value="size">Largest Size First</option>
            <option value="savings">Highest Savings First</option>
            <option value="name">Filename A-Z</option>
          </select>
        </div>
      </div>

      {/* Crush.pics Style Media Table */}
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '12px', fontFamily: 'JetBrains Mono, monospace' }}>
          <thead>
            <tr style={{ background: 'var(--bg-subtle)', borderBottom: '1px solid var(--border-hairline)', color: 'var(--fg-secondary)' }}>
              <th style={{ padding: '10px 16px', fontWeight: 600 }}>FILE</th>
              <th style={{ padding: '10px 16px', fontWeight: 600 }}>ALT TEXT</th>
              <th style={{ padding: '10px 16px', fontWeight: 600 }}>ORIGINAL SIZE</th>
              <th style={{ padding: '10px 16px', fontWeight: 600 }}>OPTIMIZED (AVIF)</th>
              <th style={{ padding: '10px 16px', fontWeight: 600 }}>SAVINGS</th>
              <th style={{ padding: '10px 16px', fontWeight: 600, textAlign: 'right' }}>ACTION</th>
            </tr>
          </thead>
          <tbody>
            {paginatedImages.map((img) => (
              <tr key={img.id} style={{ borderBottom: '1px solid var(--border-subdued)', transition: 'background 0.15s' }}>
                
                {/* File Column (Crush.pics Style with Thumbnail + Format tag under name) */}
                <td style={{ padding: '12px 16px', fontFamily: 'Geist, sans-serif' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {/* Thumbnail */}
                    <div style={{
                      width: '42px',
                      height: '42px',
                      borderRadius: 'var(--radius-sm)',
                      background: 'var(--bg-subtle)',
                      border: '1px solid var(--border-hairline)',
                      overflow: 'hidden',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      {img.url ? (
                        <img
                          src={img.url}
                          alt={img.alt_text || img.filename}
                          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          onError={(e) => {
                            (e.target as HTMLElement).style.display = 'none';
                          }}
                        />
                      ) : (
                        <ImageIcon size={18} color="var(--fg-muted)" />
                      )}
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

                {/* Alt Text Column (Crush.pics Style) */}
                <td style={{ padding: '12px 16px', color: 'var(--fg-secondary)', maxWidth: '180px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {img.alt_text ? (
                    <span style={{ color: 'var(--fg-primary)' }}>{img.alt_text}</span>
                  ) : (
                    <span style={{ color: 'var(--fg-muted)' }}>—</span>
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
                <td style={{ padding: '12px 16px', textAlign: 'right' }}>
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
            ))}
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
            style={{ padding: '4px 10px', fontSize: '11px' }}
          >
            Prev
          </button>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="btn btn-secondary"
            style={{ padding: '4px 10px', fontSize: '11px' }}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};
