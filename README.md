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
                                  +--------------+---------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |       Gemini 3.8 Flash Spatial Reasoning Tool      |
                       | - Physical Room Dimensions (W x D x H)             |
                       | - Zoned Placement Clearance (Walkways >= 32")     |
                       | - Natural Light Direction & Perspective Hotspots   |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |           B2C Product Catalog Tool                 |
                       | - Queries Amazon.in, Flipkart, and IKEA            |
                       | - Matches verified dimensions to spatial zones     |
                       | - Filters by aesthetic style (Scandi, Japandi, etc)|
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |     Conditioned Architectural Prompt Synthesizer   |
                       | - Injects exact product materials, colors, forms   |
                       | - Retains LoRA trigger 'modern_interior'           |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |             ZeroGPU FLUX A100 Tool                 |
                       | (lokesh006/room-design-api endpoint)               |
                       +-------------------------+--------------------------+
                                                 |
                                                 v
                       +----------------------------------------------------+
                       |             FastAPI Serverless Streaming           |
                       | - In-memory Base64 data URL (Zero-disk footprint)  |
                       | - Bill of Materials (BOM) with Prices & Buy Links  |
                       | - Interactive 2D Perspective Hotspot Pins          |
                       +----------------------------------------------------+
```

---

## Features

- **Agentic vs. Direct Modes**: Choose between full Agentic product dimension alignment or direct visual diffusion.
- **5 Aesthetic Styles**: Scandinavian, Japandi, Modern Luxury, Bohemian, and Industrial.
- **Interactive Hotspot Pins**: Click or hover over pins on the rendered image to highlight the corresponding product card in the Bill of Materials.
- **Direct Buy Links**: One-click direct shopping links for Amazon.in, Flipkart, and IKEA India.
- **Spatial Breakdown Card**: Displays calculated room dimensions, ceiling height, and circulation walkway clearances.
- **Zero Disk Footprint**: In-memory Base64 image streaming ensures no temporary images accumulate on the server disk.
- **FastAPI Backend with Swagger**: Interactive documentation accessible at `/docs` and `/redoc`.

---

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Or with uv: `uv pip install -r requirements.txt`)*

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
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## Clean Project Structure

```
├── server.py                              # FastAPI server with Agentic & Direct endpoints
├── agent_service.py                       # Agent orchestrator coordinating tools and ZeroGPU
├── spatial_tool.py                        # Spatial perception & room dimension calculation tool
├── catalog_service.py                     # B2C furniture catalog tool (Amazon, Flipkart, IKEA)
├── templates/
│   └── index.html                         # Modern UI with interactive hotspots & BOM cards
├── static/
│   ├── style.css                          # Modern dark architectural UI styling
│   └── app.js                             # Client-side agentic pipeline & hotspot interaction
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
