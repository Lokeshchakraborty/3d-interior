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
  
  const outputPlaceholder = document.getElementById('output-placeholder');
  const outputLoading = document.getElementById('output-loading');
  const outputResult = document.getElementById('output-result');
  const outputImage = document.getElementById('output-image');
  const downloadBtn = document.getElementById('download-btn');
  const fullscreenBtn = document.getElementById('fullscreen-btn');
  const outputBadge = document.getElementById('output-badge');
  const presetChips = document.querySelectorAll('.preset-chip');

  // 1. File Upload & Drag-and-Drop
  dropZone.addEventListener('click', (e) => {
    if (e.target !== changeImgBtn) {
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
      inputPreview.src = e.target.result;
      dropZonePrompt.classList.add('hidden');
      previewContainer.classList.remove('hidden');
      clearStatus();
    };
    reader.readAsDataURL(file);
  }

  // 2. Preset Style Chips
  presetChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const stylePrompt = chip.getAttribute('data-prompt');
      promptInput.value = stylePrompt;
      promptInput.focus();
    });
  });

  // 3. Form Submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!fileInput.files || fileInput.files.length === 0) {
      showStatus('Please upload an image of your room first.', 'error');
      dropZone.scrollIntoView({ behavior: 'smooth' });
      return;
    }

    const promptText = promptInput.value.trim();
    if (!promptText) {
      showStatus('Please enter an interior design prompt.', 'error');
      promptInput.focus();
      return;
    }

    // Set UI to loading state
    setLoadingState(true);
    clearStatus();

    const formData = new FormData();
    formData.append('room_image', fileInput.files[0]);
    formData.append('prompt', promptText);

    try {
      const response = await fetch('/api/redesign', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Failed to redesign room. Please check backend logs.');
      }

      // Display the generated image
      outputImage.src = data.image_url;
      downloadBtn.href = data.image_url;
      downloadBtn.setAttribute('download', `redesigned_${Date.now()}.jpg`);

      outputPlaceholder.classList.add('hidden');
      outputLoading.classList.add('hidden');
      outputResult.classList.remove('hidden');
      
      outputBadge.textContent = 'Completed';
      outputBadge.classList.add('active');

      showStatus('Interior redesign completed successfully!', 'success');
    } catch (err) {
      console.error(err);
      showStatus(err.message, 'error');
      outputLoading.classList.add('hidden');
      outputPlaceholder.classList.remove('hidden');
      outputBadge.textContent = 'Failed';
      outputBadge.classList.remove('active');
    } finally {
      setLoadingState(false);
    }
  });

  // 4. Fullscreen image viewer
  fullscreenBtn.addEventListener('click', () => {
    if (!outputImage.src) return;
    if (outputImage.requestFullscreen) {
      outputImage.requestFullscreen();
    } else {
      const newWin = window.open('');
      if (newWin) {
        newWin.document.write(`<body style="margin:0;background:#0f172a;display:flex;align-items:center;justify-content:center;height:100vh;"><img src="${outputImage.src}" style="max-width:100%;max-height:100%;object-fit:contain;"></body>`);
      }
    }
  });

  // Helper functions
  function setLoadingState(isLoading) {
    submitBtn.disabled = isLoading;
    if (isLoading) {
      btnSpinner.classList.remove('hidden');
      btnText.textContent = 'Redesigning Room...';
      outputPlaceholder.classList.add('hidden');
      outputResult.classList.add('hidden');
      outputLoading.classList.remove('hidden');
      outputBadge.textContent = 'Processing';
      outputBadge.classList.add('active');
    } else {
      btnSpinner.classList.add('hidden');
      btnText.textContent = 'Redesign Room';
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

