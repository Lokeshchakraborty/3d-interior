"""
LangGraph Multi-Agent State Machine for AI Interior Architecture
Orchestrates:
1. Spatial Perception Node (Gemini 3.8 Flash Vision / Architectural clearance)
2. Catalog RAG Node (Amazon, Flipkart, IKEA dimension-filtered curation)
3. Conditioned Prompt Synthesizer Node (Anti-hallucination shape, color, dimension injection)
4. ZeroGPU Generative Node (Serverless FLUX diffusion synthesis)
5. Exact Product Matcher Node (Real product packshot perspective compositing)
6. Bill of Materials Assembly Node (Hotspot mapping, costs, and buy links)
"""

import io
import os
import re
import base64
import tempfile
from typing import Dict, Any, List, Optional, TypedDict
from PIL import Image

from langgraph.graph import StateGraph, END
from catalog_service import catalog_service
from spatial_tool import spatial_tool
from product_matcher import product_matcher

class RedesignState(TypedDict):
    # Input parameters
    image_bytes: bytes
    temp_input_path: str
    user_prompt: str
    preferred_style: str
    max_budget_inr: Optional[int]
    room_length: Optional[float]
    room_width: Optional[float]
    room_height: Optional[float]
    user_dimensions: Dict[str, float]
    gradio_client: Any

    # Node state outputs
    spatial_plan: Dict[str, Any]
    curated_products: List[Dict[str, Any]]
    conditioned_prompt: str
    zerogpu_result_path: Optional[str]
    image_url: str
    matched_image_url: str
    products: List[Dict[str, Any]]
    total_estimated_cost_inr: int
    total_products_count: int
    agent_engine: str
    dimension_source: str
    is_ground_truth_dimensions: bool
    error: Optional[str]

# ==================== LANGGRAPH NODES ====================

def spatial_perception_node(state: RedesignState) -> Dict[str, Any]:
    """Node 1: Computes physical room dimensions, zones, and clearances."""
    print("[LangGraph: Node 1] Executing Spatial Perception & Clearance Analysis...")
    plan = spatial_tool.analyze_room(
        image_path=state["temp_input_path"],
        user_hint=state["user_prompt"],
        user_dimensions=state["user_dimensions"]
    )
    return {
        "spatial_plan": plan,
        "agent_engine": plan.get("analysis_engine", "gemini-3.8-flash"),
        "dimension_source": plan.get("dimension_source", "aspect_ratio_estimation"),
        "is_ground_truth_dimensions": plan.get("is_ground_truth_dimensions", False)
    }

def catalog_curation_node(state: RedesignState) -> Dict[str, Any]:
    """Node 2: Curates real B2C products from Amazon, Flipkart, and IKEA fitting zone boundaries."""
    print("[LangGraph: Node 2] Querying B2C Product Catalog with Physical Dimensional Bounds...")
    style = state["preferred_style"] or "scandinavian"
    spatial_zones = state["spatial_plan"].get("zones", {})

    curated = catalog_service.curate_room_products(
        style=style,
        spatial_zones=spatial_zones,
        max_budget_inr=state.get("max_budget_inr")
    )
    return {"curated_products": curated}

def prompt_synthesis_node(state: RedesignState) -> Dict[str, Any]:
    """Node 3: Synthesizes conditioned LoRA prompt enforcing exact shapes, colors, and room scale."""
    print("[LangGraph: Node 3] Synthesizing Anti-Hallucination Architectural Prompt...")
    trigger = "modern_interior"
    style = state["preferred_style"]
    style_title = style.replace("_", " ").title()
    spatial_plan = state["spatial_plan"]
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

    product_descriptions = []
    for p in state["curated_products"]:
        desc = p.get("visual_description", "")
        shape = p.get("shape", "")
        color = p.get("color", "")
        if desc:
            shape_words = [w for w in re.findall(r'\b[a-zA-Z-]+\b', shape.lower()) if len(w) > 3]
            has_shape = any(w in desc.lower() for w in shape_words) if shape_words else False

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

    if product_descriptions:
        items_text = ", ".join(product_descriptions)
        prompt = (
            f"{trigger}, {style_title} {room_type} {dim_scale_str}designed with architectural scale and harmony. "
            f"Featuring {items_text}. "
            f"Natural daylight flowing from {spatial_plan.get('natural_light_source', 'window')}, "
            f"photorealistic interior photography, architectural digest quality, correct physical scale and perspective, realistic furniture proportions, high-end textures, 8k resolution"
        )
    else:
        clean_base = state["user_prompt"].strip()
        prompt = f"{trigger}, {clean_base}" if not clean_base.startswith(trigger) else clean_base

    return {"conditioned_prompt": prompt}

def zerogpu_synthesis_node(state: RedesignState) -> Dict[str, Any]:
    """Node 4: Generates photorealistic room redesign using ZeroGPU API endpoint."""
    print("[LangGraph: Node 4] Invoking ZeroGPU FLUX Visual Synthesis API...")
    gradio_client = state["gradio_client"]
    from gradio_client import handle_file

    result_path = gradio_client.predict(
        room_image=handle_file(state["temp_input_path"]),
        prompt=state["conditioned_prompt"],
        api_name="/redesign"
    )

    buffer = io.BytesIO()
    with Image.open(result_path) as img:
        img.convert("RGB").save(buffer, format="JPEG", quality=95)
    buffer.seek(0)
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")
    image_url = f"data:image/jpeg;base64,{b64_data}"

    return {
        "zerogpu_result_path": result_path,
        "image_url": image_url
    }

def exact_product_matching_node(state: RedesignState) -> Dict[str, Any]:
    """
    Node 5: Solves the visual discrepancy by compositing the verified retail product packshots
    directly onto the room image perspective zones.
    """
    print("[LangGraph: Node 5] Performing Exact Product Perspective Compositing & Visual Matching...")
    category_to_zone_key = {
        "sofa": "seating_zone",
        "coffee_table": "table_zone",
        "accent_chair": "accent_zone",
        "floor_lamp": "lamp_zone",
        "rug": "rug_zone"
    }

    spatial_zones = state["spatial_plan"].get("zones", {})
    products_with_hotspots = []
    total_cost = 0

    for p in state["curated_products"]:
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
        total_cost += p.get("price_inr", 0)

    # Read bytes of the generated redesign
    with open(state["zerogpu_result_path"], "rb") as f:
        rendered_bytes = f.read()

    # Generate exact product placement composite
    matched_image_url = product_matcher.composite_products_onto_room(
        room_image_bytes=rendered_bytes,
        products=products_with_hotspots,
        spatial_plan=state["spatial_plan"]
    )

    # Compute match metrics
    enriched_products = product_matcher.compute_match_metrics(products_with_hotspots, state["spatial_plan"])

    return {
        "products": enriched_products,
        "matched_image_url": matched_image_url,
        "total_estimated_cost_inr": total_cost,
        "total_products_count": len(enriched_products)
    }

# ==================== COMPILE LANGGRAPH STATE MACHINE ====================

def build_redesign_graph():
    workflow = StateGraph(RedesignState)

    workflow.add_node("spatial_perception", spatial_perception_node)
    workflow.add_node("catalog_curation", catalog_curation_node)
    workflow.add_node("prompt_synthesis", prompt_synthesis_node)
    workflow.add_node("zerogpu_synthesis", zerogpu_synthesis_node)
    workflow.add_node("exact_product_matching", exact_product_matching_node)

    workflow.set_entry_point("spatial_perception")
    workflow.add_edge("spatial_perception", "catalog_curation")
    workflow.add_edge("catalog_curation", "prompt_synthesis")
    workflow.add_edge("prompt_synthesis", "zerogpu_synthesis")
    workflow.add_edge("zerogpu_synthesis", "exact_product_matching")
    workflow.add_edge("exact_product_matching", END)

    return workflow.compile()

# Singleton compiled LangGraph instance
langgraph_app = build_redesign_graph()
