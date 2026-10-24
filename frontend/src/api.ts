import type { StoreAuditReport, OptimizationProgress, ThemeSafetyStatus } from './types';

const API_BASE = 'http://localhost:8000/api';

export const optixApi = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },

  async getAudit(refresh: boolean = false): Promise<StoreAuditReport> {
    const res = await fetch(`${API_BASE}/audit?refresh=${refresh}`);
    if (!res.ok) throw new Error('Failed to fetch audit report');
    return res.json();
  },

  async getProgress(): Promise<OptimizationProgress> {
    const res = await fetch(`${API_BASE}/progress`);
    if (!res.ok) throw new Error('Failed to fetch progress');
    return res.json();
  },

  async startOptimization(count: number = 500): Promise<{ status: string; target_images: number }> {
    const res = await fetch(`${API_BASE}/optimize/start?count=${count}`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Failed to trigger optimization');
    return res.json();
  },

  async getThemeStatus(): Promise<ThemeSafetyStatus> {
    const res = await fetch(`${API_BASE}/theme/status`);
    if (!res.ok) throw new Error('Failed to fetch theme status');
    return res.json();
  },

  async duplicateTheme(): Promise<any> {
    const res = await fetch(`${API_BASE}/theme/duplicate`, { method: 'POST' });
    return res.json();
  },

  async publishTheme(): Promise<any> {
    const res = await fetch(`${API_BASE}/theme/publish`, { method: 'POST' });
    return res.json();
  },

  async rollbackTheme(): Promise<any> {
    const res = await fetch(`${API_BASE}/theme/rollback`, { method: 'POST' });
    return res.json();
  },

  getImageFileUrl(path: string): string {
    return `${API_BASE}/image/file?path=${encodeURIComponent(path)}`;
  },

  getImagePreviewUrl(filename: string, format: 'original' | 'webp' | 'avif', imgId?: string): string {
    const idParam = imgId ? `&img_id=${encodeURIComponent(imgId)}` : '';
    return `${API_BASE}/image/preview?filename=${encodeURIComponent(filename)}&format=${format}${idParam}`;
  },

  async restoreSingleImage(filename: string): Promise<any> {
    const res = await fetch(`${API_BASE}/image/restore?filename=${encodeURIComponent(filename)}`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to restore image');
    return res.json();
  },

  async restoreAllImages(): Promise<any> {
    const res = await fetch(`${API_BASE}/restore/all`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to restore all images');
    return res.json();
  },

  async purgeBackups(): Promise<{ success: boolean; reclaimed_mb: number; message: string }> {
    const res = await fetch(`${API_BASE}/backups/purge`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to purge backups');
    return res.json();
  },

  async getAltTextStats(): Promise<{ total_images: number; dummy_or_missing: number; optimized: number }> {
    const res = await fetch(`${API_BASE}/alt-text/stats`);
    if (!res.ok) throw new Error('Failed to fetch alt text stats');
    return res.json();
  },

  async optimizeAllAltTexts(): Promise<{ success: boolean; total_images: number; optimized_count: number; message: string }> {
    const res = await fetch(`${API_BASE}/alt-text/optimize-all`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to optimize all alt texts');
    return res.json();
  },

  async updateAltText(filename: string, altText: string): Promise<{ success: boolean; filename: string; alt_text: string; message: string }> {
    const res = await fetch(`${API_BASE}/alt-text/update`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename, alt_text: altText })
    });
    if (!res.ok) throw new Error('Failed to update alt text');
    return res.json();
  },

  async suggestAltText(filename: string, category: string = 'files'): Promise<{ filename: string; suggested_alt: string }> {
    const res = await fetch(`${API_BASE}/alt-text/suggest?filename=${encodeURIComponent(filename)}&category=${encodeURIComponent(category)}`);
    if (!res.ok) throw new Error('Failed to get alt text suggestion');
    return res.json();
  }
};
