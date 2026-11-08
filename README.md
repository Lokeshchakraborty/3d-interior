# AI 3D Interior Redesign Studio

An end-to-end AI interior design platform powered by Stable Diffusion, custom LoRA fine-tuning, and Hugging Face ZeroGPU inference. Features an interactive web UI for uploading room photos, selecting aesthetics, and generating photorealistic redesigns on-demand.

## Features

- **Interactive Web UI**: Drag-and-drop room image upload, instant preview, and live generation.
- **Custom LoRA Fine-Tuning**: Trained on high-resolution room design pairs (`modern_interior` trigger).
- **Hugging Face ZeroGPU Backend**: Serverless GPU acceleration with automated memory cleanup and base64 streaming.
- **Preset Design Styles**: Japandi, Scandinavian, Modern Luxury, Bohemian, and Industrial.

## Quickstart

### 1. Install Dependencies
```bash
pip install -r requirements.txt # or uv pip install flask gradio_client pillow
```

### 2. Configure Token (Optional for Private Spaces)
Create a `.env` file (copied from `.env.example`):
```bash
HF_TOKEN=your_huggingface_token_here
```

### 3. Run the Web Application
```bash
python server.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

### 4. CLI Redesign Script
```bash
python text_redisgn.py
```

## Project Structure

```
├── server.py              # Flask backend server connecting to HF ZeroGPU Space
├── text_redisgn.py        # Standalone Python CLI script for generation
├── prepare_dataset.py     # LoRA dataset preparation script
├── templates/             # HTML templates (Web UI)
├── static/                # CSS and client-side JavaScript
├── .env.example           # Example configuration template
└── README.md
```
