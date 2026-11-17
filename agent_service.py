"""
Agentic Interior Redesign Orchestrator
Coordinates spatial reasoning, catalog query, prompt conditioning, ZeroGPU visual synthesis,
and interactive product hotspot mapping.
"""

import os
import re
import io
import base64
import tempfile
from typing import Dict, Any, List, Optional
from PIL import Image

from catalog_service import catalog_service
from spatial_tool import spatial_tool

class AgentService:
    def __init__(self, gradio_client_getter=None):
        self.gradio_client_getter = gradio_client_getter

    def detect_style_from_prompt(self, user_prompt: str) -> str:
        prompt_lower = (user_prompt or "").lower()
        if any(w in prompt_lower for w in ["japandi", "japanese", "wabi-sabi", "wabi sabi", "zen"]):
            return "japandi"
        elif any(w in prompt_lower for w in ["luxury", "modern luxury", "glam", "penthouse", "marble", "velvet", "gold"]):
            return "modern_luxury"
        elif any(w in prompt_lower for w in ["boho", "bohemian", "rattan", "macrame", "rustic warm"]):
            return "bohemian"
        elif any(w in prompt_lower for w in ["industrial", "loft", "brick", "cast iron", "distressed"]):
            return "industrial"
        else:
            return "scandinavian"

    def synthesize_conditioned_prompt(
        self,
        base_user_prompt: str,
        style: str,
        curated_products: List[Dict[str, Any]],
        spatial_plan: Dict[str, Any]
    ) -> str:
        """
        Synthesize a photorealistic visual prompt for the FLUX LoRA model that precisely describes
        the real products selected from the catalog so the generated image matches the purchasable items.
        """
        # Always maintain the required FLUX LoRA trigger word
        trigger = "modern_interior"
        
        # Extract visual descriptions of all selected products
        product_descriptions = []
        for p in curated_products:
            desc = p.get("visual_description")
            if desc:
                product_descriptions.append(desc)

        # Style descriptor
        style_title = style.replace("_", " ").title()
        room_type = spatial_plan.get("room_type", "living room").replace("_", " ")

        if product_descriptions:
            items_text = ", ".join(product_descriptions)
            prompt = (
                f"{trigger}, {style_title} {room_type} designed with architectural scale and harmony. "
                f"Featuring {items_text}. "
                f"Natural daylight flowing from {spatial_plan.get('natural_light_source', 'window')}, "
                f"photorealistic interior photography, architectural digest quality, high-end textures, 8k resolution"
            )
        else:
            # Fallback to base prompt with trigger preserved
            clean_base = base_user_prompt.strip()
            if not clean_base.startswith(trigger):
                prompt = f"{trigger}, {clean_base}"
            else:
                prompt = clean_base

        return prompt

    def run_redesign_pipeline(
        self,
        image_bytes: bytes,
        user_prompt: str = "",
        preferred_style: Optional[str] = None,
        max_budget_inr: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Executes the end-to-end Agentic Redesign Pipeline:
        1. Spatial Perception (Room dimensions, zones, clearances)
        2. Catalog Selection (Real products with dimensions fitting the space)
        3. Prompt Synthesis (Conditioned prompt describing real products)
        4. ZeroGPU Visual Synthesis (ZeroGPU FLUX model generation)
        5. Hotspot & Bill of Materials Alignment (Interactive metadata)
        """
        temp_input_path = None
        zerogpu_result = None

        try:
            # Save uploaded image to temp file for spatial analysis and ZeroGPU
            temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            temp_input_path = temp_file.name
            temp_file.close()

            with open(temp_input_path, "wb") as f:
                f.write(image_bytes)

            # ----------------------------------------------------
            # Step 1: Spatial Perception Tool
            # ----------------------------------------------------
            spatial_plan = spatial_tool.analyze_room(temp_input_path, user_prompt)
            spatial_zones = spatial_plan.get("zones", {})

            # ----------------------------------------------------
            # Step 2: B2C Product Catalog Tool
            # ----------------------------------------------------
            style = preferred_style or self.detect_style_from_prompt(user_prompt)
            curated_products = catalog_service.curate_room_products(
                style=style,
                spatial_zones=spatial_zones,
                max_budget_inr=max_budget_inr
            )

            # Map spatial hotspot coordinates onto each curated product
            category_to_zone_key = {
                "sofa": "seating_zone",
                "coffee_table": "table_zone",
                "accent_chair": "accent_zone",
                "floor_lamp": "lamp_zone",
                "rug": "rug_zone"
            }

            products_with_hotspots = []
            total_cost_inr = 0

            for p in curated_products:
                cat = p.get("category")
                zone_key = category_to_zone_key.get(cat, "seating_zone")
                zone_info = spatial_zones.get(zone_key, {})

                # Enrich product with 2D perspective normalized hotspot
                p_copy = dict(p)
                p_copy["hotspot"] = {
                    "x_pct": zone_info.get("hotspot_x_pct", 50.0),
                    "y_pct": zone_info.get("hotspot_y_pct", 50.0),
                    "zone_name": zone_info.get("zone_name", zone_key),
                    "label": f"{p['store']} - {p['title'][:25]}..."
                }
                products_with_hotspots.append(p_copy)
                total_cost_inr += p.get("price_inr", 0)

            # ----------------------------------------------------
            # Step 3: Conditioned Architectural Prompt Synthesis
            # ----------------------------------------------------
            conditioned_prompt = self.synthesize_conditioned_prompt(
                base_user_prompt=user_prompt,
                style=style,
                curated_products=curated_products,
                spatial_plan=spatial_plan
            )

            # ----------------------------------------------------
            # Step 4: ZeroGPU Visual Synthesis Tool
            # ----------------------------------------------------
            if not self.gradio_client_getter:
                raise RuntimeError("ZeroGPU client getter is not configured.")

            from gradio_client import handle_file
            gradio_client = self.gradio_client_getter()

            print(f"[Agent] Submitting synthesized prompt to ZeroGPU...")
            print(f"[Agent] Prompt: {conditioned_prompt}")

            zerogpu_result = gradio_client.predict(
                room_image=handle_file(temp_input_path),
                prompt=conditioned_prompt,
                api_name="/redesign"
            )

            # Convert result into Base64 data URL
            buffer = io.BytesIO()
            with Image.open(zerogpu_result) as img:
                img.convert("RGB").save(buffer, format="JPEG", quality=95)
            buffer.seek(0)
            base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
            image_data_url = f"data:image/jpeg;base64,{base64_data}"

            # ----------------------------------------------------
            # Step 5: Bill of Materials & Final Payload
            # ----------------------------------------------------
            return {
                "success": True,
                "image_url": image_data_url,
                "spatial_plan": spatial_plan,
                "detected_style": style,
                "conditioned_prompt": conditioned_prompt,
                "products": products_with_hotspots,
                "total_estimated_cost_inr": total_cost_inr,
                "total_products_count": len(products_with_hotspots),
                "agent_engine": spatial_plan.get("analysis_engine", "gemini-3.8-flash")
            }

        finally:
            if temp_input_path and os.path.exists(temp_input_path):
                try:
                    os.remove(temp_input_path)
                except Exception:
                    pass
            if zerogpu_result and os.path.exists(zerogpu_result):
                try:
                    os.remove(zerogpu_result)
                except Exception:
                    pass
