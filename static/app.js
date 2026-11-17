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
  const tabBefore = document.getElementById('tab-before');
  const tabSplit = document.getElementById('tab-split');
  const singleViewContainer = document.getElementById('single-view-container');
  const splitViewContainer = document.getElementById('split-view-container');
  const splitBeforeImg = document.getElementById('split-before-img');
  const splitAfterImg = document.getElementById('split-after-img');

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
    document.getElementById('step-4')
  ];

  let originalImageSrc = null;
  let redesignedImageSrc = null;
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

  // 4. View Mode Switcher
  tabAfter.addEventListener('click', () => switchView('after'));
  tabBefore.addEventListener('click', () => switchView('before'));
  tabSplit.addEventListener('click', () => switchView('split'));

  function switchView(mode) {
    [tabAfter, tabBefore, tabSplit].forEach(t => t.classList.remove('active'));

    if (mode === 'after') {
      tabAfter.classList.add('active');
      singleViewContainer.classList.remove('hidden');
      splitViewContainer.classList.add('hidden');
      outputImage.classList.remove('hidden');
      beforeImage.classList.add('hidden');
      hotspotPins.classList.remove('hidden');
      imageViewBadge.textContent = 'Redesigned (AI)';
    } else if (mode === 'before') {
      tabBefore.classList.add('active');
      singleViewContainer.classList.remove('hidden');
      splitViewContainer.classList.add('hidden');
      outputImage.classList.add('hidden');
      beforeImage.classList.remove('hidden');
      hotspotPins.classList.add('hidden');
      imageViewBadge.textContent = 'Original Room (Before)';
    } else if (mode === 'split') {
      tabSplit.classList.add('active');
      singleViewContainer.classList.add('hidden');
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
        renderSpatialAnalysis(data.spatial_plan, data.agent_engine);
        renderPurchasableProducts(data.products, data.total_estimated_cost_inr);
        renderHotspots(data.products);
        synthesizedPromptText.textContent = data.conditioned_prompt || promptText;
        productsSection.classList.remove('hidden');
        spatialCard.classList.remove('hidden');
      } else {
        // Direct mode: hide product sections
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

      switchView('after');
      outputBadge.textContent = isAgentic ? 'Agentic Complete' : 'Rendered';
      outputBadge.classList.add('active');

      showStatus(
        isAgentic 
          ? `Spatial analysis complete! Curated ${data.products.length} dimension-verified items from Amazon, Flipkart & IKEA.`
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
    spatialEngineBadge.textContent = engine === 'gemini-3.8-flash' ? 'Engine: Gemini 3.8 Flash Vision' : 'Engine: Architectural Spatial Heuristics';
    
    const dims = plan.room_dimensions_ft || {};
    const w = dims.width_ft || 14;
    const l = dims.length_ft || 16;
    const sqft = plan.floor_area_sqft || Math.round(w * l);
    metricDim.textContent = `${w}' × ${l}' (${sqft} sq.ft)`;

    metricCeiling.textContent = `${dims.ceiling_height_ft || 9.0} ft`;
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

      card.innerHTML = `
        <div class="product-thumb-wrap">
          <img src="${prod.image_url}" alt="${prod.title}" class="product-thumb" loading="lazy">
          <span class="product-store-badge ${storeClass}">${prod.store}</span>
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

      if (progress > 20 && progress <= 45) {
        steps[1].classList.add('active');
        loadingStageText.textContent = isAgentic ? 'Curating B2C Catalog Products...' : 'Connecting to ZeroGPU A100...';
        loadingStageSub.textContent = isAgentic ? 'Filtering Amazon, Flipkart & IKEA items fitting room dimensions' : 'Allocating GPU compute';
      } else if (progress > 45 && progress <= 70) {
        steps[2].classList.add('active');
        loadingStageText.textContent = isAgentic ? 'Synthesizing Architectural LoRA Prompt...' : 'Denoising & synthesizing layout...';
        loadingStageSub.textContent = isAgentic ? 'Embedding real materials, textures, and geometry' : 'Running FLUX LoRA diffusion steps';
      } else if (progress > 70) {
        steps[3].classList.add('active');
        loadingStageText.textContent = 'Rendering Visuals on ZeroGPU A100...';
        loadingStageSub.textContent = 'Applying photorealistic 8K textures and architectural lighting';
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
});
