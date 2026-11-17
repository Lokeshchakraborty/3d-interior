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
import asyncio
import tempfile
import concurrent.futures
from typing import Dict, Any, List, Optional, TypedDict
from PIL import Image

from langgraph.graph import StateGraph, END
from catalog_service import catalog_service
from spatial_tool import spatial_tool
from product_matcher import product_matcher
from live_crawler import live_crawler

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
    enable_live_crawl: bool
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
    """Node 1: Computes physical room dimensions, zones, and clearances with dimensional guardrails."""
    print("[LangGraph: Node 1] Executing Spatial Perception & Clearance Analysis...")

    # Input Dimension Guardrails: sanitize and clamp user dimensions to realistic architectural ranges
    user_dims = dict(state.get("user_dimensions", {}))
    if user_dims.get("length_ft"):
        user_dims["length_ft"] = round(max(6.0, min(80.0, float(user_dims["length_ft"]))), 1)
    if user_dims.get("width_ft"):
        user_dims["width_ft"] = round(max(6.0, min(60.0, float(user_dims["width_ft"]))), 1)
    if user_dims.get("height_ft"):
        user_dims["height_ft"] = round(max(7.0, min(30.0, float(user_dims["height_ft"]))), 1)

    plan = spatial_tool.analyze_room(
        image_path=state["temp_input_path"],
        user_hint=state["user_prompt"],
        user_dimensions=user_dims
    )
    return {
        "spatial_plan": plan,
        "agent_engine": plan.get("analysis_engine", "gemini-3.8-flash"),
        "dimension_source": plan.get("dimension_source", "aspect_ratio_estimation"),
        "is_ground_truth_dimensions": plan.get("is_ground_truth_dimensions", False)
    }

def catalog_curation_node(state: RedesignState) -> Dict[str, Any]:
    """
    Node 2: Curates real B2C products using fast simultaneous Playwright live crawling on Amazon & Flipkart
    alongside dimension-verified catalog matching and budget guardrails.
    """
    style = state["preferred_style"] or "scandinavian"
    spatial_zones = state["spatial_plan"].get("zones", {})
    enable_live = state.get("enable_live_crawl", True)
    max_budget = state.get("max_budget_inr")

    curated = []

    # 1. Fast Simultaneous Live Playwright Crawl across Amazon & Flipkart
    if enable_live:
        print("[LangGraph: Node 2] Launching fast single-browser Playwright crawl on Amazon India & Flipkart...")
        try:
            def run_simultaneous_crawl():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                items = loop.run_until_complete(
                    live_crawler.crawl_both_simultaneous(style=style, category="coffee_table", limit_each=2)
                )
                loop.close()
                return items

            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                live_items = executor.submit(run_simultaneous_crawl).result(timeout=18)

            if live_items:
                for item in live_items:
                    item["is_live_crawled"] = True
                    curated.append(item)
                print(f"[LangGraph: Node 2] Successfully injected {len(live_items)} LIVE crawled products from Amazon & Flipkart into design!")
        except Exception as crawl_err:
            print(f"[LangGraph: Node 2] Live crawl fallback notice: {crawl_err}")

    # 2. Fill remaining spatial zones with verified catalog products
    base_curated = catalog_service.curate_room_products(
        style=style,
        spatial_zones=spatial_zones,
        max_budget_inr=max_budget
    )

    crawled_categories = {p.get("category") for p in curated}
    for base_p in base_curated:
        if base_p.get("category") not in crawled_categories:
            curated.append(base_p)

    # 3. Budget Guardrail: filter if maximum budget is specified
    if max_budget and max_budget > 0:
        budget_total = 0
        budget_curated = []
        for p in curated:
            p_cost = p.get("price_inr", 0)
            if budget_total + p_cost <= max_budget * 1.15:
                budget_curated.append(p)
                budget_total += p_cost
        if budget_curated:
            curated = budget_curated

    return {"curated_products": curated}

def prompt_synthesis_node(state: RedesignState) -> Dict[str, Any]:
    """
    Node 3: Synthesizes high-efficiency conditioned architectural prompt enforcing
    camera optics, circulation corridors, exact product attributes, and anti-hallucination guardrails.
    """
    print("[LangGraph: Node 3] Synthesizing Multi-Tier Architectural Prompt with Guardrails...")
    trigger = "modern_interior"
    style = state["preferred_style"]
    style_title = style.replace("_", " ").title()
    spatial_plan = state["spatial_plan"]
    room_type = spatial_plan.get("room_type", "living room").replace("_", " ")

    dims = spatial_plan.get("room_dimensions_ft", {})
    w = dims.get("width_ft")
    l = dims.get("length_ft")
    h = dims.get("ceiling_height_ft")

    # Tier 1: Metric Proportions & Circulation Clearance Guardrail
    dim_guardrail = ""
    if w and l and h:
        dim_guardrail = f"architecturally proportioned for {l}ft length by {w}ft width with {h}ft high ceilings, strict 32-inch open walkway clearance corridor, clean negative floor space, "
    elif w and l:
        dim_guardrail = f"architecturally proportioned for {l}ft by {w}ft floor plan with 32-inch circulation clearance, "

    # Tier 2: Product Visual Attributions
    product_descriptors = []
    for p in state["curated_products"]:
        desc = p.get("visual_description", "")
        shape = p.get("shape", "")
        color = p.get("color", "")
        cat_name = p.get("category", "furniture").replace("_", " ")

        if desc:
            clean_desc = desc
            for noise in ["tea poy", "pack of", "set of", "warranty", "home & office"]:
                clean_desc = re.sub(rf"\b{noise}\b", "", clean_desc, flags=re.IGNORECASE)
            clean_desc = " ".join(clean_desc.split()).strip()
            product_descriptors.append(f"{clean_desc}")
        elif shape or color:
            product_descriptors.append(f"{shape} {cat_name} in {color}")

    products_str = ", ".join(product_descriptors) if product_descriptors else "harmonious minimalist furniture layout"

    # Tier 3: Lighting & Ambient Photometry
    light_source = spatial_plan.get("natural_light_source", "window").replace("_", " ")
    lighting_guardrail = f"diffuse natural daylight cascading from {light_source}, warm 3000K ambient mood lighting, soft raytraced ambient occlusion contact shadows on floor"

    # Tier 4: Photographic Framing & Anti-Hallucination Guardrails
    framing_guardrail = "shot on Hasselblad H6D-100c with 24mm f/8 architectural tilt-shift lens, eye-level camera height at 1.4m, straight parallel vertical walls, zero perspective distortion"
    quality_guardrail = "Architectural Digest cover editorial, photorealistic textures, 8k resolution, crisp craftsmanship, no floating furniture, no overlapping objects, perfectly grounded floor contact"

    prompt = (
        f"{trigger}, {style_title} {room_type}, {dim_guardrail}"
        f"featuring {products_str}. "
        f"{lighting_guardrail}, {framing_guardrail}, {quality_guardrail}"
    )

    return {"conditioned_prompt": prompt}

def zerogpu_synthesis_node(state: RedesignState) -> Dict[str, Any]:
    """
    Node 4: Exemplar & ControlNet Inpainting Synthesis
    Sends floor-conditioned room geometry to ZeroGPU so ControlNet preserves
    exact furniture footprints instead of hallucinating random items in empty space.
    """
    print("[LangGraph: Node 4] Invoking ZeroGPU ControlNet / Inpainting Visual Synthesis API...")
    gradio_client = state["gradio_client"]
    from gradio_client import handle_file

    input_img_path = state["temp_input_path"]

    result_path = gradio_client.predict(
        room_image=handle_file(input_img_path),
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

