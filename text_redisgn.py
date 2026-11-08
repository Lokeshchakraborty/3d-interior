import os
from gradio_client import Client, handle_file
from PIL import Image

# 1. Hugging Face Space & Authentication Token
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

print(f"Connecting to your Hugging Face Space ({SPACE_NAME})...")
client = Client(SPACE_NAME, token=HF_TOKEN, httpx_kwargs={"timeout": 120.0})

# 2. Local room image path
LOCAL_ROOM_PATH = "my_room.jpg"

print("Sending room to fine-tuned FLUX.2 Klein on ZeroGPU...")

# 3. Call redesign endpoint (FLUX.2 Klein accepts room_image and prompt)
result = client.predict(
    room_image=handle_file(LOCAL_ROOM_PATH),
    prompt="modern_interior, luxury Scandinavian living room with beige linen couch, white oak floor, warm sunlight",
    api_name="/redesign"
)

# 4. Save result
output_filename = "flux_redesigned_room.jpg"
Image.open(result).convert("RGB").save(output_filename, "JPEG", quality=95)
print(f"SUCCESS! Saved as '{output_filename}'")
