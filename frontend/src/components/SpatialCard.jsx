import React from 'react';
import { Compass, CheckCircle2, Sun, Maximize, ShieldCheck } from 'lucide-react';

export default function SpatialCard({ spatialPlan, agentEngine }) {
  if (!spatialPlan) return null;

  const dims = spatialPlan.room_dimensions_ft || {};
  const length = dims.length_ft || 16;
  const width = dims.width_ft || 14;
  const height = dims.ceiling_height_ft || 9.5;
  const area = spatialPlan.floor_area_sqft || Math.round(length * width);
  const clearance = spatialPlan.circulation_clearance_in || 32;
  const light = spatialPlan.natural_light_source || 'Lateral Window Daylight';

  return (
    <div className="spatial-card">
      <div className="spatial-header">
        <div className="spatial-title-group">
          <Compass className="text-cyan-400" size={18} />
          <h3 className="spatial-title">Spatial Dimension & Ergonomics Analysis</h3>
        </div>
        <span className="spatial-engine-badge">
          <ShieldCheck size={12} className="text-emerald-400" />
          Engine: {agentEngine || 'Gemini 3.8 Flash'}
        </span>
      </div>

      <div className="spatial-metrics-grid">
        <div className="metric-box">
          <span className="metric-label">Estimated Dimensions</span>
          <strong className="metric-value">{length}' L × {width}' W ({area} sq.ft)</strong>
        </div>

        <div className="metric-box">
          <span className="metric-label">Ceiling Height</span>
          <strong className="metric-value">{height} ft Vertical Clearance</strong>
        </div>

        <div className="metric-box">
          <span className="metric-label">Circulation Walkway</span>
          <strong className="metric-value text-emerald-400">
            <CheckCircle2 size={13} className="inline mr-1" />
            {clearance}" Unobstructed
          </strong>
        </div>

        <div className="metric-box">
          <span className="metric-label">Natural Lighting</span>
          <strong className="metric-value capitalize">{light.replace(/_/g, ' ')}</strong>
        </div>
      </div>

      {spatialPlan.design_recommendation && (
        <p className="spatial-notes">{spatialPlan.design_recommendation}</p>
      )}
    </div>
  );
}

