import os
import io
import base64
import tempfile
from flask import Flask, render_template, request, jsonify
from gradio_client import Client, handle_file
from PIL import Image

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Configuration
SPACE_NAME = "lokesh006/room-design-api"

# Load HF_TOKEN from environment or local .env file
if not os.getenv("HF_TOKEN") and os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("HF_TOKEN="):
                    os.environ["HF_TOKEN"] = line.strip().split("=", 1)[1].strip()
    except Exception:
        pass

HF_TOKEN = os.getenv("HF_TOKEN")

client = None

def get_client():
    global client
    if client is None:
        print(f"Connecting to Hugging Face Space ({SPACE_NAME})...")
        client = Client(SPACE_NAME, token=HF_TOKEN, httpx_kwargs={"timeout": 180.0})
        print("Connected successfully!")
    return client

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/redesign", methods=["POST"])
def redesign():
    temp_input_path = None
    result = None
    try:
        # 1. Validate inputs
        if "room_image" not in request.files:
            return jsonify({"success": False, "error": "No image uploaded"}), 400

        file = request.files["room_image"]
        if file.filename == "":
            return jsonify({"success": False, "error": "No image file selected"}), 400

        prompt = request.form.get("prompt", "modern_interior, luxury Scandinavian living room").strip()

        # 2. Save temporary uploaded image to temporary directory (auto-deleted after prediction)
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        temp_input_path = temp_file.name
        temp_file.close()

        image = Image.open(file.stream).convert("RGB")
        image.save(temp_input_path, "JPEG", quality=95)

        # 3. Call Hugging Face ZeroGPU Space
        gradio_client = get_client()
        print(f"Submitting prediction to {SPACE_NAME}...")
        result = gradio_client.predict(
            room_image=handle_file(temp_input_path),
            prompt=prompt,
            api_name="/redesign"
        )
        print(f"ZeroGPU generation complete! Temp file: {result}")

        # 4. Convert result into in-memory base64 Data URL (no files saved to project disk)
        buffer = io.BytesIO()
        with Image.open(result) as img:
            img.convert("RGB").save(buffer, format="JPEG", quality=95)
        buffer.seek(0)
        base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_data_url = f"data:image/jpeg;base64,{base64_data}"

        # Return in-memory image directly to the browser
        return jsonify({
            "success": True,
            "image_url": image_data_url
        })

    except Exception as e:
        print(f"Error during redesign: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

    finally:
        # Clean up temporary input and output files immediately
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
    print(f"Starting Room Redesign UI at http://127.0.0.1:{port}")
    try:
        get_client()
    except Exception as e:
        print(f"Warning: Could not pre-connect to Space: {e}")
    app.run(host="0.0.0.0", port=port, debug=False)
