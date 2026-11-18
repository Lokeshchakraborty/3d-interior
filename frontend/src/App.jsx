import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import RoomInput from './components/RoomInput';
import VisualStage from './components/VisualStage';
import SpatialCard from './components/SpatialCard';
import ProductList from './components/ProductList';
import { Sparkles, Layers, Image as ImageIcon } from 'lucide-react';
import './App.css';

export default function App() {
  const [status, setStatus] = useState(null);
  const [roomFile, setRoomFile] = useState(null);
  const [roomPreview, setRoomPreview] = useState(null);
  const [length, setLength] = useState(16.0);
  const [width, setWidth] = useState(14.0);
  const [height, setHeight] = useState(9.5);
  const [selectedStyle, setSelectedStyle] = useState('scandinavian');
  const [prompt, setPrompt] = useState(
    'Scandinavian living room with light oak coffee table, neutral linen sofa, olive green accents, and warm 2700K ambient lighting'
  );

  const [isLoading, setIsLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [resultData, setResultData] = useState(null);
  const [hoveredProductId, setHoveredProductId] = useState(null);
  const [toastMessage, setToastMessage] = useState(null);

  // Fetch status on mount
  useEffect(() => {
    fetch('/api/status')
      .then((res) => res.json())
      .then((data) => setStatus(data))
      .catch((err) => console.log('Notice: status fetch fallback:', err));
  }, []);

  const showToast = (msg, type = 'info') => {
    setToastMessage({ text: msg, type });
    setTimeout(() => setToastMessage(null), 4000);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!roomFile) {
      showToast('Please upload a room image first.', 'error');
      return;
    }

    setIsLoading(true);
    setLoadingStage('Analyzing Room Geometry & Ergonomics...');

    const stages = [
      'Analyzing Room Geometry & Ergonomics...',
      'Matching Verified Furniture to Your Custom Prompt...',
      'Synthesizing Architectural Conditioning...',
      'Rendering Photorealistic Visuals on ZeroGPU...',
      'Compositing Exact Product Packshots...'
    ];

    let stageIdx = 0;
    const interval = setInterval(() => {
      stageIdx++;
      if (stageIdx < stages.length) {
        setLoadingStage(stages[stageIdx]);
      }
    }, 4500);

    const formData = new FormData();
    formData.append('room_image', roomFile);
    formData.append('prompt', prompt);
    formData.append('style', selectedStyle);
    formData.append('room_length', length.toString());
    formData.append('room_width', width.toString());
    formData.append('room_height', height.toString());

    try {
      const response = await fetch('/api/redesign_agentic', {
        method: 'POST',
        body: formData
      });

      clearInterval(interval);

      if (!response.ok) {
        let errMsg = `Server returned status ${response.status}`;
        try {
          const errData = await response.json();
          if (errData.error) errMsg = errData.error;
        } catch (_) {
          errMsg = 'Cannot connect to backend server. Make sure "python server.py" is running on port 5000.';
        }
        throw new Error(errMsg);
      }

      const data = await response.json();
      if (!data.success) {
        throw new Error(data.error || 'Server redesign process failed.');
      }

      setResultData(data);
      if (data.zerogpu_notice) {
        showToast(
          `Placed ${data.products?.length || 0} real products! Note: ${data.zerogpu_notice}`,
          'warning'
        );
      } else {
        showToast(
          `Precision redesign ready! Placed ${data.products?.length || 0} real dimension-verified products.`,
          'success'
        );
      }
    } catch (err) {
      clearInterval(interval);
      console.error(err);
      showToast(err.message, 'error');
    } finally {
      setIsLoading(false);
      setLoadingStage('');
    }
  };

  return (
    <div className="app-shell">
      <Header status={status} />

      {toastMessage && (
        <div className={`toast-notification toast-${toastMessage.type}`}>
          {toastMessage.text}
        </div>
      )}

      <main className="main-content-layout">
        {/* Left Column: Input Form */}
        <div className="left-column">
          <RoomInput
            roomFile={roomFile}
            setRoomFile={setRoomFile}
            roomPreview={roomPreview}
            setRoomPreview={setRoomPreview}
            length={length}
            setLength={setLength}
            width={width}
            setWidth={setWidth}
            height={height}
            setHeight={setHeight}
            selectedStyle={selectedStyle}
            setSelectedStyle={setSelectedStyle}
            prompt={prompt}
            setPrompt={setPrompt}
            isLoading={isLoading}
            loadingStage={loadingStage}
            onSubmit={handleSubmit}
          />
        </div>

        {/* Right Column: Visual Stage & Staging Results */}
        <div className="right-column">
          {resultData ? (
            <div className="results-container">
              <VisualStage
                data={resultData}
                beforeImage={roomPreview}
                hoveredProductId={hoveredProductId}
                setHoveredProductId={setHoveredProductId}
                onSelectProduct={(prod) => {
                  const card = document.getElementById(`card-${prod.id}`);
                  card?.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }}
              />

              <SpatialCard
                spatialPlan={resultData.spatial_plan}
                agentEngine={resultData.agent_engine}
              />

              <ProductList
                products={resultData.products}
                totalCost={resultData.total_estimated_cost_inr}
                hoveredProductId={hoveredProductId}
                setHoveredProductId={setHoveredProductId}
              />
            </div>
          ) : (
            <div className="empty-placeholder-card">
              <div className="placeholder-icon-bubble">
                <ImageIcon size={36} className="text-cyan-400 opacity-60" />
              </div>
              <h3 className="placeholder-heading">No Room Redesigned Yet</h3>
              <p className="placeholder-sub">
                Upload your room photo on the left. The agent will calculate spatial depth,
                clearances, scrape real products from Amazon India & Flipkart, and stage your room with 100% precision.
              </p>
              <div className="placeholder-features">
                <div className="feat-pill">
                  <span className="dot dot-cyan"></span>
                  <span>100% Real Packshots</span>
                </div>
                <div className="feat-pill">
                  <span className="dot dot-emerald"></span>
                  <span>Interactive 3D WebGL</span>
                </div>
                <div className="feat-pill">
                  <span className="dot dot-amber"></span>
                  <span>Live Store Links</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
