import os
import io
import base64
import tempfile
import uvicorn
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from gradio_client import Client, handle_file
from PIL import Image

from catalog_service import catalog_service
from agent_service import AgentService
from spatial_tool import spatial_tool
from mesh_generator import mesh_generator
from embedding_service import embedding_service

# Initialize FastAPI app
app = FastAPI(
    title="AI Agentic Room Redesign Studio",
    description="Agentic Interior Architecture with ZeroGPU and Dimension-Verified B2C Products"
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount React frontend static assets if built
if os.path.exists("frontend/dist/assets"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="frontend-assets")

# Configuration
SPACE_NAME = "lokesh006/room-design-api"

# Load environment variables from .env file
if os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("'\"")
                    if key:
                        os.environ[key] = val
    except Exception as e:
        print(f"Notice: Failed to parse .env file: {e}")

HF_TOKEN = os.getenv("HF_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

client = None

def get_client():
    global client
    if client is None:
        print(f"Connecting to Hugging Face Space ({SPACE_NAME})...")
        client = Client(SPACE_NAME, token=HF_TOKEN, httpx_kwargs={"timeout": 180.0})
        print("Connected successfully to ZeroGPU Space!")
    return client

# Initialize Agent Service with ZeroGPU client getter
agent_service = AgentService(gradio_client_getter=get_client)

@app.get("/", response_class=HTMLResponse)
def index():
    """Serves the modern React SPA if built in frontend/dist, else falls back to templates/index.html."""
    if os.path.exists("frontend/dist/index.html"):
        return FileResponse("frontend/dist/index.html")
    return FileResponse("templates/index.html")

@app.get("/legacy", response_class=HTMLResponse)
def legacy_index():
    """Serves the legacy HTML/Vanilla JS interface for backwards compatibility."""
    return FileResponse("templates/index.html")

@app.get("/api/catalog")
def get_catalog():
    """Returns the list of verified real B2C products available in the catalog."""
    products = catalog_service.get_all_products()
    return JSONResponse(content={
        "success": True,
        "count": len(products),
        "products": products
    })

@app.get("/api/model_3d/{product_id}")
def get_product_3d_model(product_id: str):
    """
    Returns the binary GLB 3D model for the specified product ID.
    Used by Three.js GLTFLoader for real-time 3D WebGL spatial staging.
    """
    product = catalog_service.get_product_by_id(product_id)
    if not product:
        # Fallback for dynamic live-crawled products
        product = {
            "id": product_id,
            "category": "coffee_table",
            "shape": "oval curved",
            "dimensions": {"width_in": 36.0, "depth_in": 24.0, "height_in": 18.0}
        }
    glb_bytes = mesh_generator.get_or_generate_glb(product)
    return Response(content=glb_bytes, media_type="model/gltf-binary")

@app.get("/api/status")
def get_status():
    """Returns system status including ZeroGPU connection, Gemini AI, and CLIP ViT embedding engine."""
    has_gemini = bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
    return JSONResponse(content={
        "zerogpu_space": SPACE_NAME,
        "has_hf_token": bool(HF_TOKEN),
        "has_gemini_key": has_gemini,
        "spatial_engine": "gemini-3.8-flash" if has_gemini else "deterministic_spatial_heuristics",
        "visual_embedding_engine": embedding_service.model_engine
    })

@app.post("/api/redesign_agentic")
async def redesign_agentic(
    room_image: UploadFile = File(...),
    prompt: str = Form("Scandinavian living room with light oak furniture, minimalist decor, neutral linen couch"),
    style: Optional[str] = Form(None),
    budget: Optional[int] = Form(None),
    room_length: Optional[float] = Form(None),
    room_width: Optional[float] = Form(None),
    room_height: Optional[float] = Form(None),
    enable_live_crawl: Optional[str] = Form("false")
):
    """
    Agentic redesign endpoint with Ground-Truth Dimensional Calibration & Custom Prompt Conditioning:
    1. Runs spatial perception & room dimension calculation using user Length, Width, Height.
    2. Curates real dimension-verified products from Amazon/Flipkart/IKEA matching user prompt keywords and visual harmony.
    3. Synthesizes an architectural prompt enforcing exact user desires and verified product shapes/colors.
    4. Calls ZeroGPU visual generation API with automatic graceful fallback.
    5. Returns redesigned image with bill of materials and interactive hotspots.
    """
    try:
        if not room_image.filename:
            return JSONResponse(status_code=400, content={"success": False, "error": "No image file selected"})

        image_bytes = await room_image.read()
        if not image_bytes:
            return JSONResponse(status_code=400, content={"success": False, "error": "Image file is empty"})

        is_live_crawl = False
        print(f"[Agentic Redesign] Initiating pipeline for: {room_image.filename} (L={room_length}, W={room_width}, H={room_height}, Prompt='{prompt[:40]}...')")
        result = agent_service.run_redesign_pipeline(
            image_bytes=image_bytes,
            user_prompt=prompt,
            preferred_style=style,
            max_budget_inr=budget,
            room_length=room_length,
            room_width=room_width,
            room_height=room_height,
            enable_live_crawl=is_live_crawl
        )
        return JSONResponse(content=result)

    except Exception as e:
        print(f"[Agentic Redesign Error]: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/redesign")
def redesign_direct(
    room_image: UploadFile = File(...),
    prompt: str = Form("modern_interior, luxury Scandinavian living room with beige linen couch")
):
    """
    Direct redesign endpoint (Legacy fallback without product dimension alignment).
    """
    temp_input_path = None
    result = None
    try:
        if not room_image.filename:
            return JSONResponse(status_code=400, content={"success": False, "error": "No image file selected"})

        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        temp_input_path = temp_file.name
        temp_file.close()

        image = Image.open(room_image.file).convert("RGB")
        image.save(temp_input_path, "JPEG", quality=95)

        gradio_client = get_client()
        result = gradio_client.predict(
            room_image=handle_file(temp_input_path),
            prompt=prompt.strip(),
            api_name="/redesign"
        )

        buffer = io.BytesIO()
        with Image.open(result) as img:
            img.convert("RGB").save(buffer, format="JPEG", quality=95)
        buffer.seek(0)
        base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_data_url = f"data:image/jpeg;base64,{base64_data}"

        return JSONResponse(content={
            "success": True,
            "image_url": image_data_url
        })

    except Exception as e:
        print(f"Error during redesign: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

    finally:
        if temp_input_path and os.path.exists(temp_input_path):
            try:
                os.remove(temp_input_path)
            except Exception:
                pass
        if result and os.path.exists(result):
            try:
                os.remove(result)
            except Exception:
                pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Agentic Room Redesign UI at http://127.0.0.1:{port}")
    try:
        get_client()
    except Exception as e:
        print(f"Warning: Could not pre-connect to Space: {e}")
    uvicorn.run(app, host="0.0.0.0", port=port)
