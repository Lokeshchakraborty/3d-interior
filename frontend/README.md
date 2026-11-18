# React + Vite + Three.js Interior Redesign Frontend

A clean, modern, and functional React web application for the **Agentic AI Interior Redesign Studio**.

## Architecture & Components

- **`src/components/Header.jsx`**: Studio navigation header with real-time operational status pills (ZeroGPU FLUX space, Spatial Perception Engine, Playwright Live Crawler).
- **`src/components/RoomInput.jsx`**: Room photo dropzone with instant preview, length/width/height dimension inputs with anti-hallucination presets, 5 architectural style cards, and live Playwright crawler toggle.
- **`src/components/VisualStage.jsx`**: Viewport switcher for **Exact Match (100% Real)**, **3D WebGL Stager**, **AI Ambiance**, and **Side-by-Side (Before & After)** with hover-synchronized hotspot pins.
- **`src/components/ThreeStage.jsx`**: Interactive Three.js WebGL 3D staging canvas with OrbitControls, directional sun lighting, soft ground shadow receiver, click-and-drag floor placement, and 45° rotation.
- **`src/components/SpatialCard.jsx`**: Ergonomic breakdown of room area (sq.ft), ceiling clearance, 32" circulation walkways, and natural light intake.
- **`src/components/ProductList.jsx`**: Purchasable furniture Bill of Materials (BOM) featuring real cutout packshots, store badges (Amazon, Flipkart, IKEA), live scraped badges, dimensions, shapes, colors, and direct store buy links.

## Quickstart

### Development Mode (with Live Reload)
```bash
npm install
npm run dev
```
Runs at `http://localhost:3000`. API requests to `/api` are automatically proxied to `http://127.0.0.1:5000`.

### Production Build
```bash
npm run build
```
Generates production assets in `dist/`. When `server.py` is executed, FastAPI serves `dist/index.html` at `http://127.0.0.1:5000`.
