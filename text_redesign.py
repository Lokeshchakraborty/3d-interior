import os
import argparse
from gradio_client import Client, handle_file
from PIL import Image

SPACE_NAME = "lokesh006/room-design-api"

def get_token():
    if not os.getenv("HF_TOKEN") and os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("HF_TOKEN="):
                        os.environ["HF_TOKEN"] = line.strip().split("=", 1)[1].strip()
        except Exception:
            pass
    return os.getenv("HF_TOKEN")

def redesign_room(
    image_path: str = "my_room.jpg",
    prompt: str = "modern_interior, luxury Scandinavian living room with beige linen couch, white oak floor, warm sunlight",
    output_path: str = "flux_redesigned_room.jpg",
    agentic: bool = True,
    style: str = "scandinavian",
    length_ft: float = 16.0,
    width_ft: float = 14.0,
    height_ft: float = 9.5
):
    token = get_token()

    if agentic:
        from spatial_tool import spatial_tool
        from catalog_service import catalog_service
        from agent_service import AgentService

        user_dimensions = {"length_ft": length_ft, "width_ft": width_ft, "height_ft": height_ft}
        print(f"[Agentic Mode] Analyzing spatial dimensions for L={length_ft}ft, W={width_ft}ft, H={height_ft}ft...")
        spatial_plan = spatial_tool.analyze_room(image_path, prompt, user_dimensions=user_dimensions)
        print(f"-> Room Dimensions: {spatial_plan.get('room_dimensions_ft')} ({spatial_plan.get('floor_area_sqft')} sq.ft)")

        print(f"[Agentic Mode] Curating B2C products from Amazon, Flipkart, IKEA...")
        products = catalog_service.curate_room_products(style=style, spatial_zones=spatial_plan.get("zones"))
        total_inr = sum(p.get("price_inr", 0) for p in products)
        print(f"-> Curated {len(products)} products (Total: ₹{total_inr:,}):")
        for p in products:
            dim = p['dimensions']
            print(f"   * [{p['store']}] {p['title'][:35]}... ({dim['width_in']}\"W x {dim['depth_in']}\"D) - ₹{p['price_inr']:,}")

        agent = AgentService()
        prompt = agent.synthesize_conditioned_prompt(prompt, style, products, spatial_plan)
        print(f"[Agentic Mode] Synthesized LoRA Prompt:\n{prompt}\n")

    print(f"Connecting to Hugging Face Space ({SPACE_NAME})...")
    client = Client(SPACE_NAME, token=token, httpx_kwargs={"timeout": 180.0})

    print("Sending room to fine-tuned FLUX model on ZeroGPU...")
    result = client.predict(
        room_image=handle_file(image_path),
        prompt=prompt,
        api_name="/redesign"
    )

    Image.open(result).convert("RGB").save(output_path, "JPEG", quality=95)
    print(f"SUCCESS! Saved redesigned room to '{output_path}'")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Interior Redesign CLI")
    parser.add_argument("--image", default="my_room.jpg", help="Path to room image")
    parser.add_argument("--prompt", default="modern_interior, luxury Scandinavian living room", help="Prompt")
    parser.add_argument("--style", default="scandinavian", help="Style: scandinavian, japandi, modern_luxury, bohemian, industrial")
    parser.add_argument("--length", type=float, default=16.0, help="Room length in feet")
    parser.add_argument("--width", type=float, default=14.0, help="Room width in feet")
    parser.add_argument("--height", type=float, default=9.5, help="Room ceiling height in feet")
    parser.add_argument("--direct", action="store_true", help="Run direct diffusion instead of agentic mode")
    parser.add_argument("--output", default="flux_redesigned_room.jpg", help="Output path")
    args = parser.parse_args()

    redesign_room(
        image_path=args.image,
        prompt=args.prompt,
        output_path=args.output,
        agentic=not args.direct,
        style=args.style,
        length_ft=args.length,
        width_ft=args.width,
        height_ft=args.height
    )
