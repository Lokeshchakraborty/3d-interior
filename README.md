# AI 3D Interior Redesign Studio

An end-to-end **Agentic AI Interior Design System** powered by multimodal spatial reasoning (Google Gemini 3.8 Flash), real-world B2C furniture catalog lookup (Amazon, Flipkart, IKEA), and fine-tuned diffusion models (FLUX.2 Klein / Stable Diffusion) via Hugging Face ZeroGPU inference.

Unlike conventional generative interior apps that hallucinate random, unpurchasable furniture, this system operates with an **Agent Brain & Modular Toolset**:
1. **Spatial Depth & Clearance Tool**: Estimates real physical room dimensions ($W \times D \times H$ in feet and inches) and enforces ergonomic walkway clearance rules (minimum 30–36 inch corridors).
2. **B2C Dimension-Verified Catalog Tool**: Queries an inventory of authentic products from **Amazon India, Flipkart, and IKEA** with verified dimensions, prices in INR (₹), materials, and store buy links.
3. **Conditioned Architectural Prompt Synthesizer**: Injects exact visual attributes, textures, and geometry of curated products into the FLUX LoRA trigger (`modern_interior`).
4. **ZeroGPU Visual Synthesis API**: Renders the redesign on high-speed A100 GPUs without deploying extra models or incurring disk clutter.
5. **Interactive Hotspot Mapping & Bill of Materials (BOM)**: Overlays interactive 2D perspective pins onto the redesigned photo and renders direct store purchase cards.

---

## Architecture Overview

```
                                  +------------------------------+
                                  |     User Room Photo Upload   |
                                  |  + Length, Width, Height (ft)|
                                  +--------------+---------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |           LangGraph StateGraph v1.2 Engine         |
                       | Node 1: Spatial Perception (Gemini 3.8 Flash)      |
                       |         - Ground-truth calibration (L x W x H)     |
                       |         - Walkway clearance corridors (>= 32")     |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       | Node 2: Simultaneous Playwright Crawler & Catalog  |
                       |         - Headless Chromium crawls Amazon.in &     |
                       |           Flipkart simultaneously in async pool    |
                       |         - Scrapes live prices, packshots & specs   |
                       |         - Backfills with verified B2C catalog      |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       | Node 3: Conditioned Architectural Prompt Synthesizer|
                       |         - Injects exact shapes, colors, scale      |
                       |         - Retains LoRA trigger 'modern_interior'   |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       | Node 4: ZeroGPU FLUX A100 Visual Synthesis API     |
                       |         - (lokesh006/room-design-api endpoint)     |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       | Node 5: Exact Product Perspective Compositing      |
                       |         - Transforms actual packshots onto floor   |
                       |         - Renders elliptical ambient drop-shadows  |
                       |         - Generates 'Exact Product Match' view     |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |             FastAPI Serverless Streaming           |
                       | - In-memory Base64 data URL (Zero-disk footprint)  |
                       | - Bill of Materials (BOM) with Live Store Badges   |
                       | - Interactive 2D Perspective Hotspot Pins          |
                       +----------------------------------------------------+
```

---

## Features

- **Modern React & Three.js 3D WebGL Frontend (`frontend/`)**: Modular, clean, and functional React UI built with Vite, Lucide icons, and an interactive Three.js 3D WebGL stager supporting OrbitControls, directional lighting, soft shadow planes, model drag-and-drop across the floor plan, 45° rotation, and synchronized hover pins.
- **LangGraph StateGraph v1.2**: 5-node autonomous pipeline with conditional state routing and error fallbacks.
- **Simultaneous Playwright Crawler**: Live, concurrent headless browser navigation across **Amazon India** and **Flipkart** to extract real-time prices, specifications, and packshots.
- **Ground-Truth Dimensional Calibration**: Input room Length, Width, and Ceiling Height (ft) to eliminate scale hallucinations and preserve 32" circulation walkways.
- **Exact Product Perspective Compositing**: Projects real e-commerce packshots directly into the redesigned floor zone with realistic elliptical ambient drop-shadows.
- **Shape & Color Precision**: Every product explicitly defines geometric shape (rectangular, curved cantilever, etc.) and color palette.
- **5 Aesthetic Styles**: Scandinavian, Japandi, Modern Luxury, Bohemian, and Industrial.
- **Interactive Hotspot Pins**: Click or hover over pins on the rendered image to highlight the corresponding product card in the Bill of Materials.
- **Direct Buy Links**: One-click direct shopping links for Amazon.in, Flipkart, and IKEA India.
- **Zero Disk Footprint**: In-memory Base64 image streaming ensures no temporary images accumulate on the server disk.
- **FastAPI Backend with Swagger**: Interactive documentation accessible at `/docs` and `/redoc`.

---

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```
*(Or with uv: `uv pip install -r requirements.txt && uv run playwright install chromium`)*

### 2. Configure Tokens (.env)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Populate the keys:
```env
# Hugging Face Access Token (for ZeroGPU Space access)
HF_TOKEN=your_huggingface_token_here

# Google Gemini API Key (for Live Gemini 3.8 Flash Vision Spatial Perception)
# Free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If `GEMINI_API_KEY` is not provided, the system automatically uses the built-in deterministic architectural heuristics engine without crashing).*

### 3. Run the Server
```bash
python server.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser. The compiled React UI from `frontend/dist` is served automatically. (The legacy interface remains accessible at `/legacy`).

### 4. Optional: Frontend Development (React + Vite)
If you wish to modify or develop the React interface with hot module reloading (HMR):
```bash
cd frontend
npm install
npm run dev
```
Open **[http://localhost:3000](http://localhost:3000)** (API requests are automatically proxied to FastAPI on port 5000). To rebuild for production:
```bash
npm run build
```

---

## Clean Project Structure

```
├── frontend/                              # Modern React + Vite + Three.js application
│   ├── src/
│   │   ├── components/                    # Modular UI components (Header, RoomInput, VisualStage, ThreeStage, SpatialCard, ProductList)
│   │   ├── App.jsx                        # Master state & layout orchestrator
│   │   ├── App.css                        # Modern architectural UI styling
│   │   └── main.jsx                       # React entry point
│   ├── dist/                              # Production build served by FastAPI at http://localhost:5000
│   ├── package.json                       # React dependencies (three, lucide-react)
│   └── vite.config.js                     # Vite configuration with /api proxy to FastAPI
├── server.py                              # FastAPI server with React SPA & Agentic endpoints
├── langgraph_agent.py                     # Compiled LangGraph StateGraph (5 nodes)
├── live_crawler.py                        # Simultaneous Playwright crawler (Amazon & Flipkart)
├── agent_service.py                       # High-level orchestrator calling LangGraph StateGraph
├── spatial_tool.py                        # Spatial perception & ground-truth room calculation
├── catalog_service.py                     # B2C furniture catalog (Amazon, Flipkart, IKEA)
├── product_matcher.py                     # Perspective compositor with elliptical drop shadows
├── mesh_generator.py                      # 3D GLB mesh generation for Three.js WebGL stager
├── templates/
│   └── index.html                         # Legacy HTML template (available at /legacy)
├── static/
│   ├── style.css                          # Legacy UI styling
│   └── app.js                             # Legacy client script
├── text_redesign.py                       # Standalone Python CLI script for generation
├── prepare_dataset.py                     # LoRA dataset preparation & cropping pipeline
├── generate_project_pdf.py                # Academic project report PDF generator
├── AI_Interior_Redesign_Project_Report.pdf# Technical report & architectural evaluation
├── pytorch_lora_weights.safetensors       # Trained LoRA fine-tuning weights
├── interior_lora_dataset/                 # Curated interior image-caption pairs
├── my_room.jpg                            # Sample room image for verification
├── requirements.txt                       # Project dependencies
├── .env.example                           # Template for environment configuration
└── README.md                              # Project documentation
```
