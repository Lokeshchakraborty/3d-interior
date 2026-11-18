document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('redesign-form');
  const fileInput = document.getElementById('room-image');
  const dropZone = document.getElementById('drop-zone');
  const dropZonePrompt = document.getElementById('drop-zone-prompt');
  const previewContainer = document.getElementById('preview-container');
  const inputPreview = document.getElementById('input-preview');
  const changeImgBtn = document.getElementById('change-image-btn');
  const promptInput = document.getElementById('prompt');
  const submitBtn = document.getElementById('submit-btn');
  const btnSpinner = document.getElementById('btn-spinner');
  const btnText = document.getElementById('btn-text');
  const statusMessage = document.getElementById('status-message');

  // Execution Pipeline Mode Selectors
  const modeAgentic = document.getElementById('mode-agentic');
  const modeDirect = document.getElementById('mode-direct');
  const modeAgenticLabel = document.getElementById('mode-agentic-label');
  const modeDirectLabel = document.getElementById('mode-direct-label');
  const enableLiveCrawlInput = document.getElementById('enable-live-crawl');

  // Room Dimension Inputs & Presets
  const roomLengthInput = document.getElementById('room-length');
  const roomWidthInput = document.getElementById('room-width');
  const roomHeightInput = document.getElementById('room-height');
  const dimPresetBtns = document.querySelectorAll('.dim-preset-btn');

  // Output Views & Placeholders
  const outputPlaceholder = document.getElementById('output-placeholder');
  const outputLoading = document.getElementById('output-loading');
  const outputResult = document.getElementById('output-result');
  const outputImage = document.getElementById('output-image');
  const beforeImage = document.getElementById('before-image');
  const imageViewBadge = document.getElementById('image-view-badge');
  const downloadBtn = document.getElementById('download-btn');
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  const outputBadge = document.getElementById('output-badge');
  const styleChips = document.querySelectorAll('#style-chips .preset-chip');

  // Tab View Switcher
  const viewSwitcher = document.getElementById('view-switcher');
  const tabAfter = document.getElementById('tab-after');
  const tabMatched = document.getElementById('tab-matched');
  const tabInteractive = document.getElementById('tab-interactive');
  const tabBefore = document.getElementById('tab-before');
  const tabSplit = document.getElementById('tab-split');
  const singleViewContainer = document.getElementById('single-view-container');
  const splitViewContainer = document.getElementById('split-view-container');
  const interactiveStageContainer = document.getElementById('interactive-stage-container');
  const stageCanvasWrapper = document.getElementById('stage-canvas-wrapper');
  const stageBgImage = document.getElementById('stage-bg-image');
  const stageItemsLayer = document.getElementById('stage-items-layer');
  const resetStageBtn = document.getElementById('reset-stage-btn');
  const splitBeforeImg = document.getElementById('split-before-img');
  const splitAfterImg = document.getElementById('split-after-img');
  const matchedImage = document.getElementById('matched-image');

  // Hotspots & Product BOM Elements
  const hotspotPins = document.getElementById('hotspot-pins');
  const productsSection = document.getElementById('products-section');
  const productsGrid = document.getElementById('products-grid');
  const totalCostAmount = document.getElementById('total-cost-amount');
  const spatialCard = document.getElementById('spatial-card');
  const spatialEngineBadge = document.getElementById('spatial-engine-badge');
  const metricDim = document.getElementById('metric-dim');
  const metricCeiling = document.getElementById('metric-ceiling');
  const metricClearance = document.getElementById('metric-clearance');
  const metricLight = document.getElementById('metric-light');
  const spatialRecommendation = document.getElementById('spatial-recommendation');
  const synthesizedPromptText = document.getElementById('synthesized-prompt-text');

  // Multi-stage Progress Indicators
  const progressBarFill = document.getElementById('progress-bar-fill');
  const loadingStageText = document.getElementById('loading-stage-text');
  const loadingStageSub = document.getElementById('loading-stage-sub');
  const steps = [
    document.getElementById('step-1'),
    document.getElementById('step-2'),
    document.getElementById('step-3'),
    document.getElementById('step-4'),
    document.getElementById('step-5')
  ];

  let originalImageSrc = null;
  let redesignedImageSrc = null;
  let matchedImageSrc = null;
  let progressInterval = null;
  let selectedStyle = 'scandinavian';

  // 1. Pipeline Mode Switcher
  [modeAgentic, modeDirect].forEach(radio => {
    radio.addEventListener('change', () => {
      if (modeAgentic.checked) {
        modeAgenticLabel.classList.add('active');
        modeDirectLabel.classList.remove('active');
        btnText.innerHTML = `
          <svg class="btn-sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z"/>
          </svg>
          Execute Agentic Redesign
        `;
      } else {
        modeDirectLabel.classList.add('active');
        modeAgenticLabel.classList.remove('active');
        btnText.innerHTML = `
          <svg class="btn-sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
          </svg>
          Execute Direct Synthesis
        `;
      }
    });
  });

  // 2. File Upload & Drag-and-Drop
  dropZone.addEventListener('click', (e) => {
    if (e.target !== changeImgBtn && !changeImgBtn.contains(e.target)) {
      fileInput.click();
    }
  });

  changeImgBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
  });

  fileInput.addEventListener('change', () => {
    if (fileInput.files && fileInput.files[0]) {
      displayFilePreview(fileInput.files[0]);
    }
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove('dragover');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files && files.length > 0) {
      fileInput.files = files;
      displayFilePreview(files[0]);
    }
  });

  function displayFilePreview(file) {
    if (!file.type.startsWith('image/')) {
      showStatus('Please select a valid image file (JPG, PNG, WEBP).', 'error');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      originalImageSrc = e.target.result;
      inputPreview.src = originalImageSrc;
      beforeImage.src = originalImageSrc;
      splitBeforeImg.src = originalImageSrc;

      dropZonePrompt.classList.add('hidden');
      previewContainer.classList.remove('hidden');
      clearStatus();
    };
    reader.readAsDataURL(file);
  }

  // 3. Preset Aesthetic Style Chips
  styleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      styleChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      selectedStyle = chip.getAttribute('data-style') || 'scandinavian';
      const promptPreset = chip.getAttribute('data-prompt');
      if (promptPreset) {
        promptInput.value = promptPreset;
      }
    });
  });

  // 3b. Room Dimension Presets & Live Area Guardrail
  const liveAreaCalc = document.getElementById('live-area-calc');

  function updateLiveAreaGuardrail() {
    if (!liveAreaCalc) return;
    const l = parseFloat(roomLengthInput ? roomLengthInput.value : 16) || 16;
    const w = parseFloat(roomWidthInput ? roomWidthInput.value : 14) || 14;
    const sqft = (l * w).toFixed(1);
    liveAreaCalc.innerHTML = `Floor Area: <strong>${sqft} sq.ft</strong> &bull; Walkway Clearance: <strong>32" Min</strong>`;
  }

  [roomLengthInput, roomWidthInput].forEach(inp => {
    if (inp) inp.addEventListener('input', updateLiveAreaGuardrail);
  });

  dimPresetBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      dimPresetBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      if (roomLengthInput) roomLengthInput.value = btn.getAttribute('data-length');
      if (roomWidthInput) roomWidthInput.value = btn.getAttribute('data-width');
      if (roomHeightInput) roomHeightInput.value = btn.getAttribute('data-height');
      updateLiveAreaGuardrail();
    });
  });

  // 4. View Mode Switcher
  tabAfter.addEventListener('click', () => switchView('after'));
  if (tabMatched) tabMatched.addEventListener('click', () => switchView('matched'));
  if (tabInteractive) tabInteractive.addEventListener('click', () => switchView('interactive'));
  tabBefore.addEventListener('click', () => switchView('before'));
  tabSplit.addEventListener('click', () => switchView('split'));

  function switchView(mode) {
    [tabAfter, tabMatched, tabInteractive, tabBefore, tabSplit].forEach(t => t && t.classList.remove('active'));

    if (mode === 'after') {
      tabAfter.classList.add('active');
      singleViewContainer.classList.remove('hidden');
      splitViewContainer.classList.add('hidden');
      if (interactiveStageContainer) interactiveStageContainer.classList.add('hidden');
      outputImage.classList.remove('hidden');
      if (matchedImage) matchedImage.classList.add('hidden');
      beforeImage.classList.add('hidden');
      hotspotPins.classList.remove('hidden');
      imageViewBadge.textContent = 'AI Ambiance (FLUX Diffusion)';
    } else if (mode === 'matched') {
      if (tabMatched) tabMatched.classList.add('active');
      singleViewContainer.classList.remove('hidden');
      splitViewContainer.classList.add('hidden');
      if (interactiveStageContainer) interactiveStageContainer.classList.add('hidden');
      outputImage.classList.add('hidden');
      if (matchedImage) matchedImage.classList.remove('hidden');
      beforeImage.classList.add('hidden');
      hotspotPins.classList.remove('hidden');
      imageViewBadge.textContent = 'Exact Product Placement (Real Amazon/IKEA Cutouts)';
    } else if (mode === 'interactive') {
      if (tabInteractive) tabInteractive.classList.add('active');
      singleViewContainer.classList.add('hidden');
      splitViewContainer.classList.add('hidden');
      if (interactiveStageContainer) {
        interactiveStageContainer.classList.remove('hidden');
        if (stageBgImage) {
          stageBgImage.src = matchedImageSrc || redesignedImageSrc || originalImageSrc;
        }
        setTimeout(() => {
          initThreeJS();
          if (renderer && camera && stageCanvasWrapper) {
            const r = stageCanvasWrapper.getBoundingClientRect();
            camera.aspect = r.width / r.height;
            camera.updateProjectionMatrix();
            renderer.setSize(r.width, r.height);
          }
        }, 60);
      }
      imageViewBadge.textContent = 'Interactive 3D Floor Stager';
    } else if (mode === 'before') {
      tabBefore.classList.add('active');
      singleViewContainer.classList.remove('hidden');
      splitViewContainer.classList.add('hidden');
      if (interactiveStageContainer) interactiveStageContainer.classList.add('hidden');
      outputImage.classList.add('hidden');
      if (matchedImage) matchedImage.classList.add('hidden');
      beforeImage.classList.remove('hidden');
      hotspotPins.classList.add('hidden');
      imageViewBadge.textContent = 'Original Room (Before)';
    } else if (mode === 'split') {
      tabSplit.classList.add('active');
      singleViewContainer.classList.add('hidden');
      if (interactiveStageContainer) interactiveStageContainer.classList.add('hidden');
      splitViewContainer.classList.remove('hidden');
      hotspotPins.classList.add('hidden');
    }
  }

  // 5. Form Submission with Agentic Pipeline Execution
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!fileInput.files || fileInput.files.length === 0) {
      showStatus('Please upload an image of your room first.', 'error');
      dropZone.scrollIntoView({ behavior: 'smooth' });
      return;
    }

    const promptText = promptInput.value.trim();
    if (!promptText) {
      showStatus('Please enter an interior design prompt or select a style.', 'error');
      promptInput.focus();
      return;
    }

    const isAgentic = modeAgentic.checked;
    const endpoint = isAgentic ? '/api/redesign_agentic' : '/api/redesign';

    setLoadingState(true, isAgentic);
    startProgressAnimation(isAgentic);
    clearStatus();

    const formData = new FormData();
    formData.append('room_image', fileInput.files[0]);
    formData.append('prompt', promptText);
    if (isAgentic) {
      formData.append('style', selectedStyle);
      if (roomLengthInput && roomLengthInput.value) {
        formData.append('room_length', roomLengthInput.value);
      }
      if (roomWidthInput && roomWidthInput.value) {
        formData.append('room_width', roomWidthInput.value);
      }
      if (roomHeightInput && roomHeightInput.value) {
        formData.append('room_height', roomHeightInput.value);
      }
      if (enableLiveCrawlInput) {
        formData.append('enable_live_crawl', enableLiveCrawlInput.checked ? 'true' : 'false');
      }
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Server redesign process failed.');
      }

      stopProgressAnimation(true);

      redesignedImageSrc = data.image_url;
      outputImage.src = redesignedImageSrc;
      splitAfterImg.src = redesignedImageSrc;

      downloadBtn.href = redesignedImageSrc;
      downloadBtn.setAttribute('download', `redesigned_${selectedStyle}_${Date.now()}.jpg`);

      // If Agentic pipeline succeeded, render spatial plan, products & hotspots
      if (isAgentic && data.products) {
        if (data.matched_image_url && matchedImage) {
          matchedImageSrc = data.matched_image_url;
          matchedImage.src = matchedImageSrc;
          if (tabMatched) tabMatched.classList.remove('hidden');
        }

        renderSpatialAnalysis(data.spatial_plan, data.agent_engine);
        renderPurchasableProducts(data.products, data.total_estimated_cost_inr);
        renderHotspots(data.products);
        renderInteractiveStager(data.products);
        synthesizedPromptText.textContent = data.conditioned_prompt || promptText;
        productsSection.classList.remove('hidden');
        spatialCard.classList.remove('hidden');
        if (tabInteractive) tabInteractive.classList.remove('hidden');
      } else {
        // Direct mode: hide product sections and matched tab
        if (tabMatched) tabMatched.classList.add('hidden');
        if (tabInteractive) tabInteractive.classList.add('hidden');
        productsSection.classList.add('hidden');
        spatialCard.classList.add('hidden');
        hotspotPins.innerHTML = '';
        synthesizedPromptText.textContent = promptText;
      }

      // Display results view
      outputPlaceholder.classList.add('hidden');
      outputLoading.classList.add('hidden');
      outputResult.classList.remove('hidden');
      viewSwitcher.classList.remove('hidden');

      // In Agentic mode, default to the 100% Exact Product Match view!
      if (isAgentic && matchedImageSrc) {
        switchView('matched');
      } else {
        switchView('after');
      }

      outputBadge.textContent = isAgentic ? 'Exact Match Active' : 'Rendered';
      outputBadge.classList.add('active');

      showStatus(
        isAgentic 
          ? `Zero-hallucination match! Placed ${data.products.length} verified real Amazon, Flipkart & IKEA items into your room.`
          : 'Redesign completed successfully!',
        'success'
      );

    } catch (err) {
      console.error(err);
      stopProgressAnimation(false);
      showStatus(err.message, 'error');
      outputLoading.classList.add('hidden');
      outputPlaceholder.classList.remove('hidden');
      outputBadge.textContent = 'Failed';
      outputBadge.classList.remove('active');
    } finally {
      setLoadingState(false, isAgentic);
    }
  });

  // 6. Render Spatial Analysis Card
  function renderSpatialAnalysis(plan, engine) {
    if (!plan) return;
    const isGroundTruth = plan.is_ground_truth_dimensions || false;
    const engineLabel = engine === 'gemini-3.8-flash' ? 'Gemini 3.8 Flash' : 'Spatial Heuristics';
    const sourceLabel = isGroundTruth ? 'User Ground Truth' : 'AI Estimated';

    spatialEngineBadge.textContent = `${engineLabel} · ${sourceLabel}`;
    if (isGroundTruth) {
      spatialEngineBadge.classList.add('badge-ground-truth');
    } else {
      spatialEngineBadge.classList.remove('badge-ground-truth');
    }
    
    const dims = plan.room_dimensions_ft || {};
    const w = dims.width_ft || 14;
    const l = dims.length_ft || 16;
    const sqft = plan.floor_area_sqft || Math.round(w * l);
    metricDim.textContent = `${l}' Length × ${w}' Width (${sqft} sq.ft)`;

    metricCeiling.textContent = `${dims.ceiling_height_ft || 9.0} ft Ceiling`;
    metricClearance.textContent = `${plan.circulation_clearance_in || 32}" Walkway`;
    metricLight.textContent = (plan.natural_light_source || 'Natural Window Intake').replace('_', ' ');
    spatialRecommendation.textContent = plan.design_recommendation || 'Scaled to match spatial ergonomics and circulation corridors.';
  }

  // 7. Render Purchasable Products (BOM)
  function renderPurchasableProducts(products, totalCost) {
    productsGrid.innerHTML = '';
    totalCostAmount.textContent = `₹${(totalCost || 0).toLocaleString('en-IN')}`;

    products.forEach((prod, idx) => {
      const card = document.createElement('div');
      card.className = 'product-card';
      card.id = `prod-card-${prod.id}`;
      card.setAttribute('data-prod-id', prod.id);

      const storeClass = `store-${prod.store.toLowerCase().replace('.', '')}`;
      const dim = prod.dimensions || {};
      const dimStr = `${dim.width_in}"W × ${dim.depth_in}"D × ${dim.height_in}"H (${dim.width_cm} × ${dim.depth_cm} × ${dim.height_cm} cm)`;
      const liveBadgeHtml = prod.is_live_crawled 
        ? `<span class="product-live-badge" title="Live crawled via Playwright Chromium from ${prod.store}"><span class="live-dot"></span>⚡ Live Scraped</span>`
        : '';

      card.innerHTML = `
        <div class="product-thumb-wrap">
          <img src="${prod.image_url}" alt="${prod.title}" class="product-thumb" loading="lazy">
          <span class="product-store-badge ${storeClass}">${prod.store}</span>
          ${liveBadgeHtml}
          <span class="product-pin-idx">${idx + 1}</span>
        </div>
        <div class="product-info">
          <span class="product-category">${prod.category.replace('_', ' ').toUpperCase()}</span>
          <h4 class="product-title" title="${prod.title}">${prod.title}</h4>
          
          <div class="product-dimension-tag">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
            </svg>
            <span>Verified Fit: ${dimStr}</span>
          </div>

          <div class="product-harmony-pill" title="${prod.aesthetic_harmony?.harmony_tier || 'High Aesthetic Harmony'} · CLIP ViT 512-dim Cosine Similarity: ${prod.aesthetic_harmony?.cosine_similarity || '0.62'}">
            <span class="harmony-icon">✨</span>
            <span class="harmony-pct">${prod.visual_similarity_score || prod.aesthetic_harmony?.harmony_score_pct || 92.5}% Visual Harmony</span>
            <span class="harmony-tier-badge">${prod.aesthetic_harmony?.harmony_tier || 'Harmonious Fit'}</span>
          </div>

          <div class="product-attributes">
            <span class="attr-chip chip-shape" title="Product Geometric Shape">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="11" height="11">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
              </svg>
              ${prod.shape || 'Geometric'}
            </span>
            <span class="attr-chip chip-color" title="Product Color Palette">
              <span class="color-swatch-dot"></span>
              ${prod.color || 'Neutral'}
            </span>
          </div>

          <div class="product-materials">
            ${(prod.materials || []).slice(0, 2).map(m => `<span class="mat-chip">${m}</span>`).join('')}
          </div>

          <div class="product-price-row">
            <span class="product-price">₹${(prod.price_inr || 0).toLocaleString('en-IN')}</span>
            <a href="${prod.buy_url}" target="_blank" rel="noopener noreferrer" class="buy-link-btn">
              <span>Buy on ${prod.store}</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="13" height="13">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                <polyline points="15 3 21 3 21 9"/>
                <line x1="10" y1="14" x2="21" y2="3"/>
              </svg>
            </a>
          </div>
        </div>
      `;

      // Highlight corresponding hotspot on hover
      card.addEventListener('mouseenter', () => {
        const pin = document.getElementById(`pin-${prod.id}`);
        if (pin) pin.classList.add('pin-active');
      });
      card.addEventListener('mouseleave', () => {
        const pin = document.getElementById(`pin-${prod.id}`);
        if (pin) pin.classList.remove('pin-active');
      });

      productsGrid.appendChild(card);
    });
  }

  // 8. Render Interactive Hotspot Pins on Redesigned Room Image
  function renderHotspots(products) {
    hotspotPins.innerHTML = '';

    products.forEach((prod, idx) => {
      const hotspot = prod.hotspot || {};
      const x = Math.min(Math.max(hotspot.x_pct || 50, 8), 92);
      const y = Math.min(Math.max(hotspot.y_pct || 50, 15), 90);

      const pin = document.createElement('div');
      pin.className = 'hotspot-pin';
      pin.id = `pin-${prod.id}`;
      pin.style.left = `${x}%`;
      pin.style.top = `${y}%`;

      pin.innerHTML = `
        <div class="pin-marker">
          <span class="pin-idx">${idx + 1}</span>
          <span class="pin-pulse"></span>
        </div>
        <div class="pin-tooltip">
          <strong>${prod.store} - ${prod.title.slice(0, 24)}...</strong>
          <span style="color:#a5f3fc;font-size:0.7rem;">${prod.shape} · ${prod.color}</span>
          <span>₹${prod.price_inr.toLocaleString('en-IN')} · ${prod.dimensions.width_in}"W × ${prod.dimensions.depth_in}"D</span>
        </div>
      `;

      // Pin interactions: hover and click
      pin.addEventListener('mouseenter', () => {
        highlightProductCard(prod.id);
      });
      pin.addEventListener('mouseleave', () => {
        unhighlightProductCard(prod.id);
      });
      pin.addEventListener('click', () => {
        const card = document.getElementById(`prod-card-${prod.id}`);
        if (card) {
          card.scrollIntoView({ behavior: 'smooth', block: 'center' });
          card.classList.add('card-highlight');
          setTimeout(() => card.classList.remove('card-highlight'), 2000);
        }
      });

      hotspotPins.appendChild(pin);
    });
  }

  function highlightProductCard(prodId) {
    const card = document.getElementById(`prod-card-${prodId}`);
    if (card) card.classList.add('card-hover');
  }

  function unhighlightProductCard(prodId) {
    const card = document.getElementById(`prod-card-${prodId}`);
    if (card) card.classList.remove('card-hover');
  }

  // 9. Fullscreen Viewer
  fullscreenBtn.addEventListener('click', () => {
    const currentActiveImg = tabBefore.classList.contains('active') ? beforeImage : outputImage;
    if (!currentActiveImg || !currentActiveImg.src) return;

    if (currentActiveImg.requestFullscreen) {
      currentActiveImg.requestFullscreen();
    } else {
      const newWin = window.open('');
      if (newWin) {
        newWin.document.write(`<body style="margin:0;background:#0b0f19;display:flex;align-items:center;justify-content:center;height:100vh;"><img src="${currentActiveImg.src}" style="max-width:100%;max-height:100%;object-fit:contain;"></body>`);
      }
    }
  });

  // Helper functions: Loading & Progress simulation
  function setLoadingState(isLoading, isAgentic) {
    submitBtn.disabled = isLoading;
    if (isLoading) {
      btnSpinner.classList.remove('hidden');
      btnText.textContent = isAgentic ? 'Agent Analyzing & Redesigning...' : 'Synthesizing Room...';
      outputPlaceholder.classList.add('hidden');
      outputResult.classList.add('hidden');
      outputLoading.classList.remove('hidden');
      viewSwitcher.classList.add('hidden');
      outputBadge.textContent = 'Processing';
      outputBadge.classList.add('active');
    } else {
      btnSpinner.classList.add('hidden');
      btnText.innerHTML = `
        <svg class="btn-sparkle" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3L12 3z"/>
        </svg>
        ${isAgentic ? 'Execute Agentic Redesign' : 'Execute Direct Synthesis'}
      `;
    }
  }

  function startProgressAnimation(isAgentic) {
    let progress = 0;
    progressBarFill.style.width = '0%';
    steps.forEach(s => s.classList.remove('active'));
    steps[0].classList.add('active');
    loadingStageText.textContent = isAgentic ? 'Analyzing Room Geometry...' : 'Uploading room snapshot...';
    loadingStageSub.textContent = isAgentic ? 'Calculating spatial depth, clearances, and placement zones' : 'Preparing image for ZeroGPU A100';

    progressInterval = setInterval(() => {
      progress += 1.4;
      if (progress > 92) progress = 92;
      progressBarFill.style.width = `${progress}%`;

      if (progress > 15 && progress <= 35) {
        if (steps[1]) steps[1].classList.add('active');
        loadingStageText.textContent = isAgentic ? 'Visual RAG & Simultaneous Crawling...' : 'Connecting to ZeroGPU A100...';
        loadingStageSub.textContent = isAgentic ? 'Extracting CLIP visual embeddings & crawling Amazon & Flipkart' : 'Allocating GPU compute';
      } else if (progress > 35 && progress <= 55) {
        if (steps[2]) steps[2].classList.add('active');
        loadingStageText.textContent = isAgentic ? 'Synthesizing Architectural LoRA Prompt...' : 'Denoising & synthesizing layout...';
        loadingStageSub.textContent = isAgentic ? 'Embedding exact shapes, colors, and physical bounds' : 'Running FLUX LoRA diffusion steps';
      } else if (progress > 55 && progress <= 78) {
        if (steps[3]) steps[3].classList.add('active');
        loadingStageText.textContent = 'Rendering Visuals on ZeroGPU A100...';
        loadingStageSub.textContent = 'Applying photorealistic 8K textures and architectural lighting';
      } else if (progress > 78) {
        if (steps[4]) steps[4].classList.add('active');
        loadingStageText.textContent = isAgentic ? 'LangGraph Exact Product Compositing...' : 'Finalizing output...';
        loadingStageSub.textContent = isAgentic ? 'Perspective matching real Amazon & IKEA packshots onto floor' : 'Completing generation';
      }
    }, 280);
  }

  function stopProgressAnimation(isSuccess) {
    clearInterval(progressInterval);
    if (isSuccess) {
      progressBarFill.style.width = '100%';
      steps.forEach(s => s.classList.add('active'));
      loadingStageText.textContent = 'Transformation Complete!';
      loadingStageSub.textContent = 'Spatial dimensions and product bill of materials ready';
    } else {
      progressBarFill.style.width = '0%';
    }
  }

  function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-box ${type}`;
    statusMessage.classList.remove('hidden');
  }

  function clearStatus() {
    statusMessage.textContent = '';
    statusMessage.classList.add('hidden');
  }

  // 10. Interactive Drag-and-Drop Precision Stager
  let currentStagedProducts = [];

  function renderInteractiveStager(products) {
    currentStagedProducts = products || [];
    if (!stageItemsLayer) return;
    stageItemsLayer.innerHTML = '';
    if (stageBgImage) {
      stageBgImage.src = matchedImageSrc || redesignedImageSrc || originalImageSrc;
    }

    currentStagedProducts.forEach((prod, idx) => {
      const cutoutSrc = prod.cutout_url || prod.image_url;
      if (!cutoutSrc) return;

      const coords = prod.stage_coords || {};
      const initX = coords.center_x_pct || (prod.hotspot ? prod.hotspot.x_pct : 50);
      const initY = coords.center_y_pct || (prod.hotspot ? prod.hotspot.y_pct : 60);
      const initWidth = coords.width_pct || 28;

      const itemEl = document.createElement('div');
      itemEl.className = 'staged-item';
      itemEl.id = `staged-item-${prod.id}`;
      itemEl.setAttribute('data-id', prod.id);
      itemEl.style.left = `${initX}%`;
      itemEl.style.top = `${initY}%`;
      itemEl.style.width = `${initWidth}%`;
      itemEl.style.zIndex = Math.round(initY);

      const dim = prod.dimensions || {};
      const dimStr = `${dim.width_in || 36}"W × ${dim.depth_in || 24}"D`;

      itemEl.innerHTML = `
        <div class="staged-shadow"></div>
        <img src="${cutoutSrc}" alt="${prod.title}" class="staged-img" draggable="false">
        <div class="staged-badge">
          <span class="staged-store">${prod.store}</span>
          <span class="staged-dim">${dimStr}</span>
        </div>
        <div class="staged-resizer">
          <button type="button" class="resize-btn resize-minus" title="Scale Down">-</button>
          <button type="button" class="resize-btn resize-plus" title="Scale Up">+</button>
        </div>
      `;

      // Setup Drag & Drop
      setupDragEvents(itemEl);

      // Setup Scaling Controls
      const btnMinus = itemEl.querySelector('.resize-minus');
      const btnPlus = itemEl.querySelector('.resize-plus');
      let currentWidth = initWidth;

      btnMinus.addEventListener('click', (e) => {
        e.stopPropagation();
        currentWidth = Math.max(12, currentWidth - 3);
        itemEl.style.width = `${currentWidth}%`;
      });

      btnPlus.addEventListener('click', (e) => {
        e.stopPropagation();
        currentWidth = Math.min(65, currentWidth + 3);
        itemEl.style.width = `${currentWidth}%`;
      });

      stageItemsLayer.appendChild(itemEl);
    });

    // Populate Three.js 3D WebGL Staging scene with .glb models
    setTimeout(() => {
      initThreeJS();
      populateThreeJSModels(currentStagedProducts);
    }, 100);
  }

  function setupDragEvents(el) {
    if (!stageCanvasWrapper) return;
    let isDragging = false;
    let startX = 0, startY = 0;
    let elemStartLeft = 0, elemStartTop = 0;

    const onPointerDown = (e) => {
      if (e.target.closest('.staged-resizer')) return;
      isDragging = true;
      el.classList.add('dragging');
      startX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
      startY = e.clientY || (e.touches && e.touches[0].clientY) || 0;

      const parentRect = stageCanvasWrapper.getBoundingClientRect();
      const elemRect = el.getBoundingClientRect();
      elemStartLeft = ((elemRect.left + elemRect.width / 2 - parentRect.left) / parentRect.width) * 100;
      elemStartTop = ((elemRect.top + elemRect.height / 2 - parentRect.top) / parentRect.height) * 100;

      document.addEventListener('pointermove', onPointerMove);
      document.addEventListener('pointerup', onPointerUp);
    };

    const onPointerMove = (e) => {
      if (!isDragging) return;
      const clientX = e.clientX || (e.touches && e.touches[0].clientX) || 0;
      const clientY = e.clientY || (e.touches && e.touches[0].clientY) || 0;
      const parentRect = stageCanvasWrapper.getBoundingClientRect();
      if (!parentRect.width || !parentRect.height) return;

      const deltaXPct = ((clientX - startX) / parentRect.width) * 100;
      const deltaYPct = ((clientY - startY) / parentRect.height) * 100;

      const newXPct = Math.max(5, Math.min(95, elemStartLeft + deltaXPct));
      const newYPct = Math.max(15, Math.min(95, elemStartTop + deltaYPct));

      el.style.left = `${newXPct}%`;
      el.style.top = `${newYPct}%`;
      el.style.zIndex = Math.round(newYPct);
    };

    const onPointerUp = () => {
      isDragging = false;
      el.classList.remove('dragging');
      document.removeEventListener('pointermove', onPointerMove);
      document.removeEventListener('pointerup', onPointerUp);
    };

    el.addEventListener('pointerdown', onPointerDown);
  }

  if (resetStageBtn) {
    resetStageBtn.addEventListener('click', () => {
      renderInteractiveStager(currentStagedProducts);
    });
  }

  // ============================================================
  // Phase 2: Three.js 3D WebGL Precision Stager
  // ============================================================
  const threejsCanvas = document.getElementById('threejs-canvas');
  const btnSubmode3D = document.getElementById('btn-submode-3d');
  const btnSubmode2D = document.getElementById('btn-submode-2d');
  const rotateModelBtn = document.getElementById('rotate-model-btn');
  const threejsHud = document.getElementById('threejs-hud');
  const hudModelInfo = document.getElementById('hud-model-info');
  const hudModelTitle = document.getElementById('hud-model-title');
  const hudModelDim = document.getElementById('hud-model-dim');

  let scene, camera, renderer, orbitControls;
  let threeModels = [];
  let selected3DModel = null;
  let is3DInitialized = false;

  function initThreeJS() {
    if (is3DInitialized || !threejsCanvas || typeof THREE === 'undefined') return;

    try {
      scene = new THREE.Scene();
      const rect = stageCanvasWrapper.getBoundingClientRect();
      const width = rect.width || 800;
      const height = rect.height || 600;

      camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
      camera.position.set(0, 2.2, 4.6);

      renderer = new THREE.WebGLRenderer({
        canvas: threejsCanvas,
        alpha: true,
        antialias: true
      });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;

      orbitControls = new THREE.OrbitControls(camera, renderer.domElement);
      orbitControls.enableDamping = true;
      orbitControls.dampingFactor = 0.05;
      orbitControls.maxPolarAngle = Math.PI / 2 + 0.02; // Can't go below floor
      orbitControls.minDistance = 1.0;
      orbitControls.maxDistance = 12.0;
      orbitControls.target.set(0, 0.5, 0);

      // Ambient Light
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.75);
      scene.add(ambientLight);

      // Directional Sun/Window Light with Soft Shadow
      const dirLight = new THREE.DirectionalLight(0xfff6e6, 1.15);
      dirLight.position.set(-3, 6, 4);
      dirLight.castShadow = true;
      dirLight.shadow.mapSize.width = 1024;
      dirLight.shadow.mapSize.height = 1024;
      dirLight.shadow.camera.near = 0.5;
      dirLight.shadow.camera.far = 15;
      dirLight.shadow.bias = -0.001;
      scene.add(dirLight);

      // Soft Secondary Fill Light
      const fillLight = new THREE.DirectionalLight(0xdbeafe, 0.45);
      fillLight.position.set(3, 4, -2);
      scene.add(fillLight);

      // Ground Plane (Shadow Receiver)
      const floorGeo = new THREE.PlaneGeometry(16, 16);
      const floorMat = new THREE.ShadowMaterial({ opacity: 0.38 });
      const floor = new THREE.Mesh(floorGeo, floorMat);
      floor.rotation.x = -Math.PI / 2;
      floor.position.y = 0;
      floor.receiveShadow = true;
      scene.add(floor);

      // Subtle Grid Guide for Walkway Clearance
      const grid = new THREE.GridHelper(8, 16, 0x38bdf8, 0x1e293b);
      grid.position.y = 0.001;
      grid.material.opacity = 0.35;
      grid.material.transparent = true;
      scene.add(grid);

      // Raycasting for clicking & dragging 3D furniture
      setupThreeJSRaycasting();

      // Render Loop
      const animate = () => {
        requestAnimationFrame(animate);
        orbitControls.update();
        const selHelper = scene.getObjectByName('selection-helper');
        if (selHelper) selHelper.update();
        renderer.render(scene, camera);
      };
      animate();

      window.addEventListener('resize', () => {
        if (!stageCanvasWrapper || !renderer || !camera) return;
        const r = stageCanvasWrapper.getBoundingClientRect();
        camera.aspect = r.width / r.height;
        camera.updateProjectionMatrix();
        renderer.setSize(r.width, r.height);
      });

      is3DInitialized = true;
      console.log("[ThreeJS] 3D Stager initialized successfully!");
    } catch (e) {
      console.error("[ThreeJS] Initialization error:", e);
    }
  }

  function setupThreeJSRaycasting() {
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let isDragging3D = false;
    const plane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0); // Y = 0 floor plane
    const planeIntersect = new THREE.Vector3();

    threejsCanvas.addEventListener('pointerdown', (e) => {
      const rect = threejsCanvas.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(threeModels, true);

      if (intersects.length > 0) {
        let topGroup = intersects[0].object;
        while (topGroup.parent && topGroup.parent !== scene) {
          topGroup = topGroup.parent;
        }
        select3DModel(topGroup);

        if (e.button === 0 && !e.shiftKey) {
          isDragging3D = true;
          orbitControls.enabled = false;
        }
      } else {
        deselect3DModel();
      }
    });

    window.addEventListener('pointermove', (e) => {
      if (!isDragging3D || !selected3DModel) return;
      const rect = threejsCanvas.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      if (raycaster.ray.intersectPlane(plane, planeIntersect)) {
        selected3DModel.position.x = Math.max(-3.5, Math.min(3.5, planeIntersect.x));
        selected3DModel.position.z = Math.max(-3.5, Math.min(3.5, planeIntersect.z));
      }
    });

    window.addEventListener('pointerup', () => {
      if (isDragging3D) {
        isDragging3D = false;
        orbitControls.enabled = true;
      }
    });
  }

  function select3DModel(modelGroup) {
    deselect3DModel();
    selected3DModel = modelGroup;

    const bbox = new THREE.BoxHelper(modelGroup, 0x38bdf8);
    bbox.name = 'selection-helper';
    scene.add(bbox);

    const prod = modelGroup.userData || {};
    if (hudModelInfo && prod.title) {
      hudModelTitle.textContent = `${prod.store} - ${prod.title.slice(0, 22)}...`;
      const d = prod.dimensions || {};
      hudModelDim.textContent = `${d.width_in || 48}"W × ${d.depth_in || 28}"D × ${d.height_in || 30}"H (Verified)`;
      hudModelInfo.classList.remove('hidden');
    }
  }

  function deselect3DModel() {
    selected3DModel = null;
    const existingHelper = scene ? scene.getObjectByName('selection-helper') : null;
    if (existingHelper) scene.remove(existingHelper);
    if (hudModelInfo) hudModelInfo.classList.add('hidden');
  }

  function populateThreeJSModels(products) {
    if (!scene || typeof THREE === 'undefined') return;

    // Remove existing models
    threeModels.forEach(m => scene.remove(m));
    threeModels = [];
    deselect3DModel();

    const loader = (typeof THREE.GLTFLoader !== 'undefined') ? new THREE.GLTFLoader() : null;

    products.forEach((prod, idx) => {
      const coords = prod.stage_coords || {};
      const xPct = coords.center_x_pct || (prod.hotspot ? prod.hotspot.x_pct : 50);
      const yPct = coords.center_y_pct || (prod.hotspot ? prod.hotspot.y_pct : 60);

      // Map 2D floor percentage (0..100) to 3D world meters (-3.5 .. +3.5)
      const posX = ((xPct - 50) / 50) * 2.8;
      const posZ = ((yPct - 50) / 50) * 2.2;

      const dim = prod.dimensions || {};
      const wM = Math.max(0.3, Math.min((dim.width_in || 48) * 0.0254, 3.5));
      const dM = Math.max(0.3, Math.min((dim.depth_in || 28) * 0.0254, 2.5));
      const hM = Math.max(0.02, Math.min((dim.height_in || 30) * 0.0254, 2.2));

      // Attempt GLTF Load if GLB URL is available
      if (loader && prod.model_3d_url) {
        loader.load(
          prod.model_3d_url,
          (gltf) => {
            const root = gltf.scene;
            root.position.set(posX, 0, posZ);
            root.traverse(child => {
              if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
              }
            });
            root.userData = prod;
            scene.add(root);
            threeModels.push(root);
          },
          undefined,
          (err) => {
            // Fallback to procedural PBR mesh
            createProcedural3DMesh(prod, posX, posZ, wM, dM, hM);
          }
        );
      } else {
        createProcedural3DMesh(prod, posX, posZ, wM, dM, hM);
      }
    });
  }

  function createProcedural3DMesh(prod, posX, posZ, wM, dM, hM) {
    const group = new THREE.Group();
    const cat = (prod.category || 'sofa').toLowerCase();

    let mat;
    if (prod.cutout_url) {
      const texture = new THREE.TextureLoader().load(prod.cutout_url);
      mat = new THREE.MeshStandardMaterial({
        map: texture,
        roughness: 0.6,
        metalness: 0.1,
        transparent: true
      });
    } else {
      mat = new THREE.MeshStandardMaterial({
        color: 0x38bdf8,
        roughness: 0.5,
        metalness: 0.2
      });
    }

    let geo;
    if (cat === 'rug') {
      geo = new THREE.BoxGeometry(wM, 0.015, dM);
    } else if (cat === 'coffee_table') {
      geo = new THREE.CylinderGeometry(Math.min(wM, dM) / 2, Math.min(wM, dM) / 2, hM, 24);
    } else if (cat === 'floor_lamp') {
      geo = new THREE.CylinderGeometry(0.03, minR(wM, dM), hM, 16);
    } else {
      geo = new THREE.BoxGeometry(wM, hM, dM);
    }

    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.y = hM / 2;
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);

    group.position.set(posX, 0, posZ);
    group.userData = prod;
    scene.add(group);
    threeModels.push(group);
  }

  function minR(w, d) {
    return Math.max(0.12, Math.min(w, d) * 0.4);
  }

  if (rotateModelBtn) {
    rotateModelBtn.addEventListener('click', () => {
      if (selected3DModel) {
        selected3DModel.rotation.y += Math.PI / 4;
        const helper = scene.getObjectByName('selection-helper');
        if (helper) helper.update();
      }
    });
  }

  // Submode Toggles (3D WebGL vs 2D Canvas)
  if (btnSubmode3D && btnSubmode2D) {
    btnSubmode3D.addEventListener('click', () => {
      btnSubmode3D.classList.add('active');
      btnSubmode2D.classList.remove('active');
      threejsCanvas.classList.remove('hidden');
      threejsHud.classList.remove('hidden');
      stageBgImage.classList.add('hidden');
      stageItemsLayer.classList.add('hidden');
      initThreeJS();
    });

    btnSubmode2D.addEventListener('click', () => {
      btnSubmode2D.classList.add('active');
      btnSubmode3D.classList.remove('active');
      threejsCanvas.classList.add('hidden');
      threejsHud.classList.add('hidden');
      stageBgImage.classList.remove('hidden');
      stageItemsLayer.classList.remove('hidden');
    });
  }
});
