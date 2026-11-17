"""
Agentic Interior Redesign Orchestrator powered by LangGraph StateGraph
Coordinates spatial reasoning, catalog query, prompt conditioning, ZeroGPU visual synthesis,
and exact product packshot perspective compositing.
"""

import os
import tempfile
from typing import Dict, Any, List, Optional
from langgraph_agent import langgraph_app

class AgentService:
    def __init__(self, gradio_client_getter=None):
        self.gradio_client_getter = gradio_client_getter
        self.graph = langgraph_app

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
        Executes the LangGraph Redesign State Machine:
        1. Spatial Perception Node
        2. Catalog Curation Node
        3. Conditioned Prompt Synthesizer Node
        4. ZeroGPU Generative Node
        5. Exact Product Perspective Matching Node
        """
        temp_input_path = None
        zerogpu_result_path = None

        try:
            temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            temp_input_path = temp_file.name
            temp_file.close()

            with open(temp_input_path, "wb") as f:
                f.write(image_bytes)

            if not self.gradio_client_getter:
                raise RuntimeError("ZeroGPU client getter is not configured.")
            gradio_client = self.gradio_client_getter()

            user_dimensions = {}
            if room_length and room_length > 0:
                user_dimensions["length_ft"] = float(room_length)
            if room_width and room_width > 0:
                user_dimensions["width_ft"] = float(room_width)
            if room_height and room_height > 0:
                user_dimensions["height_ft"] = float(room_height)

            style = preferred_style or self.detect_style_from_prompt(user_prompt)

            initial_state = {
                "image_bytes": image_bytes,
                "temp_input_path": temp_input_path,
                "user_prompt": user_prompt,
                "preferred_style": style,
                "max_budget_inr": max_budget_inr,
                "room_length": room_length,
                "room_width": room_width,
                "room_height": room_height,
                "user_dimensions": user_dimensions,
                "gradio_client": gradio_client
            }

            print("[AgentService] Triggering LangGraph State Machine execution...")
            final_state = self.graph.invoke(initial_state)

            zerogpu_result_path = final_state.get("zerogpu_result_path")

            return {
                "success": True,
                "image_url": final_state.get("image_url"),
                "matched_image_url": final_state.get("matched_image_url"),
                "spatial_plan": final_state.get("spatial_plan"),
                "detected_style": style,
                "conditioned_prompt": final_state.get("conditioned_prompt"),
                "products": final_state.get("products", []),
                "total_estimated_cost_inr": final_state.get("total_estimated_cost_inr", 0),
                "total_products_count": final_state.get("total_products_count", 0),
                "agent_engine": final_state.get("agent_engine", "gemini-3.8-flash"),
                "dimension_source": final_state.get("dimension_source", "aspect_ratio_estimation"),
                "is_ground_truth_dimensions": final_state.get("is_ground_truth_dimensions", False),
                "orchestration_framework": "LangGraph v1.2 StateGraph"
            }

        finally:
            if temp_input_path and os.path.exists(temp_input_path):
                try:
                    os.remove(temp_input_path)
                except Exception:
                    pass
            if zerogpu_result_path and os.path.exists(zerogpu_result_path):
                try:
                    os.remove(zerogpu_result_path)
                except Exception:
                    pass
