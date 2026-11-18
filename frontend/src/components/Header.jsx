import React from 'react';
import { Sparkles, Box, Compass, Cpu } from 'lucide-react';

export default function Header({ status }) {
  return (
    <header className="app-header">
      <div className="header-brand">
        <div className="logo-icon-wrap">
          <Sparkles className="logo-icon text-cyan-400" size={24} />
        </div>
        <div>
          <h1 className="brand-title">SpaceCraft AI</h1>
          <p className="brand-subtitle">Precision Interior Architecture with Real Amazon, Flipkart & IKEA Furniture</p>
        </div>
      </div>

      <div className="header-status-pills">
        <div className="status-pill">
          <span className="pill-dot dot-emerald"></span>
          <span className="pill-label">ZeroGPU FLUX</span>
        </div>
        <div className="status-pill">
          <span className="pill-dot dot-cyan"></span>
          <span className="pill-label">{status?.spatial_engine || 'Spatial AI'}</span>
        </div>
        <div className="status-pill">
          <span className="pill-dot dot-amber"></span>
          <span className="pill-label">⚡ Live Playwright Active</span>
        </div>
      </div>
    </header>
  );
}
