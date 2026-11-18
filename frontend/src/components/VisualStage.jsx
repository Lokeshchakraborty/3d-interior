import React, { useState } from 'react';
import { Target, Box, Sparkles, Columns, Download, Maximize2, ShoppingCart } from 'lucide-react';
import ThreeStage from './ThreeStage';

export default function VisualStage({
  data,
  beforeImage,
  hoveredProductId,
  setHoveredProductId,
  onSelectProduct
}) {
  const [activeTab, setActiveTab] = useState('matched'); // 'matched' | '3d' | 'after' | 'split'

  const matchedUrl = data?.matched_image_url;
  const afterUrl = data?.image_url;
  const products = data?.products || [];

  const handleDownload = () => {
    const src = activeTab === 'matched' ? matchedUrl : afterUrl;
    if (!src) return;
    const a = document.createElement('a');
    a.href = src;
    a.download = `redesign_${activeTab}_${Date.now()}.jpg`;
    a.click();
  };

  const handleFullscreen = () => {
    const el = document.getElementById('visual-viewport-container');
    if (el?.requestFullscreen) el.requestFullscreen();
  };

  return (
    <div className="visual-stage-card">
      {/* View Switcher Tabs Header */}
      <div className="stage-header">
        <div className="tab-pill-group">
          <button
            type="button"
            className={`tab-pill ${activeTab === 'matched' ? 'active' : ''}`}
            onClick={() => setActiveTab('matched')}
          >
            <Target size={14} className="text-cyan-400" />
            <span>Exact Match (100% Real)</span>
          </button>

          <button
            type="button"
            className={`tab-pill ${activeTab === '3d' ? 'active' : ''}`}
            onClick={() => setActiveTab('3d')}
          >
            <Box size={14} className="text-emerald-400" />
            <span>3D WebGL Stager</span>
          </button>

          <button
            type="button"
            className={`tab-pill ${activeTab === 'after' ? 'active' : ''}`}
            onClick={() => setActiveTab('after')}
          >
            <Sparkles size={14} className="text-amber-400" />
            <span>AI Ambiance</span>
          </button>

          <button
            type="button"
            className={`tab-pill ${activeTab === 'split' ? 'active' : ''}`}
            onClick={() => setActiveTab('split')}
          >
            <Columns size={14} />
            <span>Side-by-Side</span>
          </button>
        </div>

        <div className="stage-actions">
          <button type="button" onClick={handleDownload} className="action-icon-btn" title="Download Image">
            <Download size={16} />
          </button>
          <button type="button" onClick={handleFullscreen} className="action-icon-btn" title="Fullscreen">
            <Maximize2 size={16} />
          </button>
        </div>
      </div>

      {/* Main Visual Viewport */}
      <div className="visual-viewport" id="visual-viewport-container">
        {/* 1. Exact Match View */}
        {activeTab === 'matched' && (
          <div className="image-viewport">
            <img src={matchedUrl || afterUrl} alt="Exact Match Room" className="stage-image" />
            {/* Hotspot Pins */}
            <div className="hotspot-layer">
              {products.map((prod, idx) => {
                const hs = prod.hotspot || {};
                const x = Math.min(Math.max(hs.x_pct || 50, 10), 90);
                const y = Math.min(Math.max(hs.y_pct || 50, 15), 90);
                const isHovered = hoveredProductId === prod.id;

                return (
                  <div
                    key={prod.id}
                    className={`hotspot-pin ${isHovered ? 'active' : ''}`}
                    style={{ left: `${x}%`, top: `${y}%` }}
                    onMouseEnter={() => setHoveredProductId(prod.id)}
                    onMouseLeave={() => setHoveredProductId(null)}
                    onClick={() => onSelectProduct?.(prod)}
                  >
                    <div className="pin-circle">
                      <span>{idx + 1}</span>
                      <span className="pin-glow"></span>
                    </div>
                    <div className="pin-popup">
                      <strong>{prod.store} · {prod.title?.slice(0, 24)}...</strong>
                      <span className="popup-specs">₹{prod.price_inr?.toLocaleString('en-IN')} · {prod.dimensions?.width_in}"W × {prod.dimensions?.depth_in}"D</span>
                    </div>
                  </div>
                );
              })}
            </div>
            <div className="viewport-badge badge-matched">Exact B2C Match (Real Packshots)</div>
          </div>
        )}

        {/* 2. Three.js 3D WebGL Viewport */}
        {activeTab === '3d' && (
          <ThreeStage
            products={products}
            roomImage={beforeImage}
            onSelectProduct={onSelectProduct}
          />
        )}

        {/* 3. AI Diffusion Ambiance View */}
        {activeTab === 'after' && (
          <div className="image-viewport">
            <img src={afterUrl} alt="AI Diffusion Ambiance" className="stage-image" />
            <div className="viewport-badge badge-diffusion">FLUX AI Concept Ambiance</div>
          </div>
        )}

        {/* 4. Side-by-Side Split View */}
        {activeTab === 'split' && (
          <div className="split-viewport">
            <div className="split-half">
              <span className="split-tag">Before (Original)</span>
              <img src={beforeImage} alt="Before" className="split-img" />
            </div>
            <div className="split-half">
              <span className="split-tag">After (Precision Redesign)</span>
              <img src={matchedUrl || afterUrl} alt="After" className="split-img" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
