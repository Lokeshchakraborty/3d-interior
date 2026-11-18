import React, { useRef } from 'react';
import { Upload, X, Sliders, CheckCircle2, ArrowRight, Loader2, Sparkles, Wand2 } from 'lucide-react';

const STYLES = [
  { id: 'scandinavian', name: 'Scandinavian', color: '#10b981', prompt: 'Scandinavian living room with light oak furniture, minimalist decor, neutral linen couch, warm ambient lighting, 8k photo' },
  { id: 'japandi', name: 'Japandi', color: '#f59e0b', prompt: 'Japandi living room, clean wabi-sabi aesthetics, low profile wood furniture, paper lantern lamp, warm ambient light, 8k' },
  { id: 'modern_luxury', name: 'Modern Luxury', color: '#3b82f6', prompt: 'Modern luxury living room, marble coffee table, emerald velvet sofa, brushed gold lighting, high-end editorial, 8k' },
  { id: 'bohemian', name: 'Bohemian', color: '#f43f5e', prompt: 'Cozy bohemian living room, textured Moroccan shag rug, rattan cane sofa, terracotta rust tones, lush indoor plants, 8k' },
  { id: 'industrial', name: 'Industrial Loft', color: '#8b5cf6', prompt: 'Urban industrial loft, exposed brick wall, matte black steel, distressed cognac leather sofa, vintage Edison lighting, 8k' }
];

const PRESETS = [
  { name: 'Compact', l: 12, w: 10, h: 8.5 },
  { name: 'Standard', l: 16, w: 14, h: 9.5 },
  { name: 'Spacious', l: 22, w: 18, h: 10.5 }
];

export default function RoomInput({
  roomFile,
  setRoomFile,
  roomPreview,
  setRoomPreview,
  length,
  setLength,
  width,
  setWidth,
  height,
  setHeight,
  selectedStyle,
  setSelectedStyle,
  prompt,
  setPrompt,
  isLoading,
  loadingStage,
  onSubmit
}) {
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setRoomFile(file);
      const reader = new FileReader();
      reader.onload = (event) => setRoomPreview(event.target.result);
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('image/')) {
      setRoomFile(file);
      const reader = new FileReader();
      reader.onload = (event) => setRoomPreview(event.target.result);
      reader.readAsDataURL(file);
    }
  };

  const applyPreset = (preset) => {
    setLength(preset.l);
    setWidth(preset.w);
    setHeight(preset.h);
  };

  const applyStyle = (styleObj) => {
    setSelectedStyle(styleObj.id);
    setPrompt(styleObj.prompt);
  };

  return (
    <div className="input-card">
      <div className="section-header">
        <h2 className="section-title">Design Parameters</h2>
        <span className="section-badge">Step 1</span>
      </div>

      <form onSubmit={onSubmit} className="form-stack">
        {/* 1. Room Photo Upload */}
        <div className="control-group">
          <label className="control-label">
            <span>1. Upload Room Photo</span>
            <span className="req-pill">Required</span>
          </label>

          {!roomPreview ? (
            <div
              className="dropzone"
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                className="hidden"
              />
              <div className="dropzone-inner">
                <div className="upload-circle">
                  <Upload size={22} className="text-cyan-400" />
                </div>
                <p className="drop-title"><strong>Click to upload</strong> or drag & drop</p>
                <p className="drop-sub">JPG, PNG, WEBP (Max 15MB)</p>
              </div>
            </div>
          ) : (
            <div className="preview-wrap">
              <img src={roomPreview} alt="Selected Room" className="preview-image" />
              <button
                type="button"
                className="remove-btn"
                onClick={() => {
                  setRoomFile(null);
                  setRoomPreview(null);
                }}
                title="Remove Photo"
              >
                <X size={16} />
              </button>
              <div className="preview-badge">Room Photo Loaded</div>
            </div>
          )}
        </div>

        {/* 2. Room Dimensions */}
        <div className="control-group">
          <div className="label-row">
            <label className="control-label">
              <span>2. Room Dimensions (L × W × H)</span>
              <span className="precision-pill">Anti-Hallucination</span>
            </label>
            <span className="unit-pill">Feet (ft)</span>
          </div>

          <div className="dims-grid">
            <div className="dim-field">
              <span className="dim-tag">Length</span>
              <div className="dim-input-box">
                <input
                  type="number"
                  min="6"
                  max="100"
                  step="0.5"
                  value={length}
                  onChange={(e) => setLength(parseFloat(e.target.value) || '')}
                  placeholder="16.0"
                />
                <span className="dim-sub">ft</span>
              </div>
            </div>

            <div className="dim-field">
              <span className="dim-tag">Width</span>
              <div className="dim-input-box">
                <input
                  type="number"
                  min="6"
                  max="100"
                  step="0.5"
                  value={width}
                  onChange={(e) => setWidth(parseFloat(e.target.value) || '')}
                  placeholder="14.0"
                />
                <span className="dim-sub">ft</span>
              </div>
            </div>

            <div className="dim-field">
              <span className="dim-tag">Ceiling</span>
              <div className="dim-input-box">
                <input
                  type="number"
                  min="7"
                  max="30"
                  step="0.5"
                  value={height}
                  onChange={(e) => setHeight(parseFloat(e.target.value) || '')}
                  placeholder="9.5"
                />
                <span className="dim-sub">ft</span>
              </div>
            </div>
          </div>

          <div className="preset-row">
            <span className="preset-label">Quick Presets:</span>
            {PRESETS.map((p) => (
              <button
                key={p.name}
                type="button"
                className={`preset-btn ${length === p.l && width === p.w ? 'active' : ''}`}
                onClick={() => applyPreset(p)}
              >
                {p.name} ({p.l}×{p.w}')
              </button>
            ))}
          </div>
        </div>

        {/* 3. Aesthetic Style Selector */}
        <div className="control-group">
          <label className="control-label">
            <span>3. Aesthetic Style & Catalog Alignment</span>
          </label>
          <div className="styles-grid">
            {STYLES.map((st) => (
              <button
                key={st.id}
                type="button"
                className={`style-card ${selectedStyle === st.id ? 'active' : ''}`}
                onClick={() => applyStyle(st)}
              >
                <span className="style-dot" style={{ backgroundColor: st.color }}></span>
                <span className="style-name">{st.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* 4. Custom Design Prompt Feature (Define What You Want) */}
        <div className="control-group">
          <div className="label-row">
            <label className="control-label">
              <span>4. Custom Design Prompt</span>
              <span className="precision-pill">What You Want</span>
            </label>
            <span className="unit-pill">Personalized Vision</span>
          </div>
          <p className="control-hint">
            Define colors, materials, furniture items, or mood. The AI will curate matching verified furniture and render your vision:
          </p>

          <div className="prompt-box-wrap">
            <textarea
              className="prompt-textarea"
              rows={3}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="e.g. Scandinavian living room with light oak coffee table, neutral linen couch, olive green cushions, indoor plants, and warm 2700K ambient lighting..."
            />
          </div>

          {/* Quick-Add Suggestion Chips */}
          <div className="prompt-chips-row">
            <span className="chips-title">Quick Add:</span>
            {[
              '🌿 Indoor Plants',
              '🕯️ Warm 2700K Lighting',
              '🪵 Natural Oak Wood',
              '✨ Brass Accents',
              '🛋️ Velvet Cushions',
              '📚 Reading Nook'
            ].map((chip) => (
              <button
                key={chip}
                type="button"
                className="prompt-chip-btn"
                onClick={() => {
                  const clean = chip.replace(/^[^\w\s]+\s*/, '');
                  if (!prompt.toLowerCase().includes(clean.toLowerCase())) {
                    setPrompt((prev) => (prev ? `${prev.trim()}, with ${clean}` : clean));
                  }
                }}
              >
                {chip}
              </button>
            ))}
          </div>
        </div>

        {/* 5. Submit Action */}
        <button
          type="submit"
          disabled={isLoading || !roomFile}
          className={`submit-btn ${isLoading ? 'loading' : ''}`}
        >
          {isLoading ? (
            <div className="btn-loading-content">
              <Loader2 size={18} className="spinner" />
              <span>{loadingStage || 'Synthesizing Architecture...'}</span>
            </div>
          ) : (
            <div className="btn-content">
              <Sparkles size={18} />
              <span>Execute Precision Redesign</span>
              <ArrowRight size={16} />
            </div>
          )}
        </button>
      </form>
    </div>
  );
}

