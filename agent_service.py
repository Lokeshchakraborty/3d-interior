"""
Agentic Interior Redesign Orchestrator
Coordinates spatial reasoning, catalog query, prompt conditioning, ZeroGPU visual synthesis,
and interactive product hotspot mapping.
Grounds visual generation in user-specified Length x Width x Height to prevent perspective hallucinations.
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
        Synthesize an architectural prompt for the FLUX LoRA model that precisely describes
        the real products and exact room dimensions ($L \times W \times H$) to prevent scaling hallucinations.
        """
        trigger = "modern_interior"
        
        # Extract visual descriptions of all selected products, guaranteeing explicit shape and color
        product_descriptions = []
        for p in curated_products:
            desc = p.get("visual_description", "")
            shape = p.get("shape", "")
            color = p.get("color", "")
            if desc:
                # Check if shape keywords are already in desc
                shape_words = [w for w in re.findall(r'\b[a-zA-Z-]+\b', shape.lower()) if len(w) > 3]
                has_shape = any(w in desc.lower() for w in shape_words) if shape_words else False

                # Check if color keywords are already in desc
                color_words = [w for w in re.findall(r'\b[a-zA-Z-]+\b', color.lower()) if len(w) > 3]
                has_color = any(w in desc.lower() for w in color_words) if color_words else False

                if not has_shape and shape:
                    desc = f"{shape}-shaped {desc}"
                if not has_color and color:
                    desc = f"{desc} in {color}"
                product_descriptions.append(desc)
            elif shape or color:
                cat = p.get("category", "furniture")
                product_descriptions.append(f"{shape} {color} {cat}")

        style_title = style.replace("_", " ").title()
        room_type = spatial_plan.get("room_type", "living room").replace("_", " ")

        dims = spatial_plan.get("room_dimensions_ft", {})
        w = dims.get("width_ft")
        l = dims.get("length_ft")
        h = dims.get("ceiling_height_ft")

        dim_scale_str = ""
        if w and l and h:
            dim_scale_str = f"accurately proportioned for a {l}ft length by {w}ft width space with {h}ft high ceilings and 32-inch circulation walkways, "
        elif w and l:
            dim_scale_str = f"accurately proportioned for a {l}ft by {w}ft floor plan, "

        if product_descriptions:
            items_text = ", ".join(product_descriptions)
            prompt = (
                f"{trigger}, {style_title} {room_type} {dim_scale_str}designed with architectural scale and harmony. "
                f"Featuring {items_text}. "
                f"Natural daylight flowing from {spatial_plan.get('natural_light_source', 'window')}, "
                f"photorealistic interior photography, architectural digest quality, correct physical scale and perspective, realistic furniture proportions, high-end textures, 8k resolution"
            )
        else:
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
        max_budget_inr: Optional[int] = None,
        room_length: Optional[float] = None,
        room_width: Optional[float] = None,
        room_height: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Executes the end-to-end Agentic Redesign Pipeline with Ground-Truth Dimensional Guidance:
        1. Spatial Perception (anchored by user length, width, height)
        2. Catalog Selection (real products sized specifically for the user's room bounds)
        3. Dimension-Conditioned Prompt Synthesis (eliminates hallucinations)
        4. ZeroGPU Visual Synthesis (ZeroGPU FLUX model generation)
        5. Hotspot & Bill of Materials Alignment (Interactive metadata)
        """
        temp_input_path = None
        zerogpu_result = None

        try:
            temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            temp_input_path = temp_file.name
            temp_file.close()

            with open(temp_input_path, "wb") as f:
                f.write(image_bytes)

            # Build user dimensions payload
            user_dimensions = {}
            if room_length and room_length > 0:
                user_dimensions["length_ft"] = float(room_length)
            if room_width and room_width > 0:
                user_dimensions["width_ft"] = float(room_width)
            if room_height and room_height > 0:
                user_dimensions["height_ft"] = float(room_height)

            # ----------------------------------------------------
            # Step 1: Spatial Perception Tool (Anchored by Dimensions)
            # ----------------------------------------------------
            spatial_plan = spatial_tool.analyze_room(
                image_path=temp_input_path,
                user_hint=user_prompt,
                user_dimensions=user_dimensions
            )
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

            print(f"[Agent] Submitting dimension-grounded prompt to ZeroGPU...")
            print(f"[Agent] Prompt: {conditioned_prompt}")

            zerogpu_result = gradio_client.predict(
                room_image=handle_file(temp_input_path),
                prompt=conditioned_prompt,
                api_name="/redesign"
            )

            buffer = io.BytesIO()
            with Image.open(zerogpu_result) as img:
                img.convert("RGB").save(buffer, format="JPEG", quality=95)
            buffer.seek(0)
            base64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
            image_data_url = f"data:image/jpeg;base64,{base64_data}"

            # ----------------------------------------------------
            # Step 5: Final Response Payload
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
                "agent_engine": spatial_plan.get("analysis_engine", "gemini-3.8-flash"),
                "dimension_source": spatial_plan.get("dimension_source", "aspect_ratio_estimation"),
                "is_ground_truth_dimensions": spatial_plan.get("is_ground_truth_dimensions", False)
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
