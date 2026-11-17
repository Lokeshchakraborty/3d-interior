"""
Spatial Perception & Room Dimension Estimator Tool
Performs multimodal spatial reasoning to extract physical room dimensions,
clearance boundaries, and furniture placement zones.
Supports user ground-truth dimensions (Length x Width x Height) to eliminate
perspective hallucinations and ground furniture selection in exact room scale.
"""

import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from PIL import Image

class ZoneBoundary(BaseModel):
    zone_name: str = Field(..., description="Name of the placement zone, e.g. seating_zone, table_zone")
    max_width_in: float = Field(..., description="Maximum allowable width in inches for physical clearance")
    max_depth_in: float = Field(..., description="Maximum allowable depth in inches")
    max_height_in: float = Field(..., description="Maximum allowable height in inches")
    suggested_category: str = Field(..., description="Category suited for this zone, e.g. sofa, coffee_table, accent_chair")
    hotspot_x_pct: float = Field(..., description="Normalized X coordinate (0-100%) in the image perspective")
    hotspot_y_pct: float = Field(..., description="Normalized Y coordinate (0-100%) in the image perspective")
    description: str = Field(..., description="Rationale for furniture placement in this zone")

class RoomSpatialAnalysis(BaseModel):
    room_type: str = Field(..., description="Type of room: living_room, bedroom, dining_room, home_office")
    room_dimensions_ft: Dict[str, float] = Field(
        ...,
        description="Physical room dimensions in feet: width_ft, length_ft, ceiling_height_ft"
    )
    floor_area_sqft: float = Field(..., description="Total floor area in square feet")
    natural_light_source: str = Field(..., description="Position of primary windows/light: left, right, rear, frontal")
    existing_flooring: str = Field(..., description="Detected floor material: hardwood, tile, concrete, carpet")
    primary_focal_wall: str = Field(..., description="Position of the main focal wall: center, left, right")
    circulation_clearance_in: float = Field(..., description="Required minimum walkway circulation clearance in inches (typically 30-36 in)")
    zones: Dict[str, ZoneBoundary] = Field(
        ...,
        description="Zoned physical placement envelopes for furniture items"
    )
    design_recommendation: str = Field(..., description="Architectural recommendations for scale and proportion")
    is_ground_truth_dimensions: bool = Field(default=False, description="Whether dimensions are confirmed by user measurements")

class SpatialTool:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("Gemini Client initialized for Spatial Vision Analysis.")
            except Exception as e:
                print(f"Notice: Failed to initialize Gemini Client: {e}")

    def analyze_room(
        self,
        image_path: str,
        user_hint: Optional[str] = None,
        user_dimensions: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Analyze the room image to extract physical dimensions, clearances, and placement zones.
        Incorporates user-provided Length, Width, and Height as ground truth anchors when available.
        """
        user_dims = user_dimensions or {}
        has_user_dims = any(user_dims.get(k) for k in ["length_ft", "width_ft", "height_ft"])

        # 1. Attempt Gemini Multimodal Vision Reasoning if client is available
        if self.client:
            try:
                result = self._analyze_with_gemini(image_path, user_hint, user_dims)
                if result:
                    result["analysis_engine"] = "gemini-3.8-flash"
                    result["dimension_source"] = "User Ground-Truth" if has_user_dims else "Gemini Multimodal Estimation"
                    result["is_ground_truth_dimensions"] = has_user_dims
                    return result
            except Exception as e:
                print(f"Gemini spatial analysis encountered error, falling back to deterministic engine: {e}")

        # 2. Deterministic Architectural Fallback
        fallback = self._deterministic_spatial_analysis(image_path, user_hint, user_dims)
        fallback["analysis_engine"] = "deterministic_spatial_heuristics"
        fallback["dimension_source"] = "User Ground-Truth" if has_user_dims else "Aspect-Ratio Estimation"
        fallback["is_ground_truth_dimensions"] = has_user_dims
        return fallback

    def _analyze_with_gemini(
        self,
        image_path: str,
        user_hint: Optional[str] = None,
        user_dims: Optional[Dict[str, float]] = None
    ) -> Optional[Dict[str, Any]]:
        from google.genai import types

        img = Image.open(image_path).convert("RGB")
        dims = user_dims or {}
        user_w = dims.get("width_ft")
        user_l = dims.get("length_ft")
        user_h = dims.get("height_ft")

        ground_truth_directive = ""
        if user_w or user_l or user_h:
            ground_truth_directive = f"""
CRITICAL GROUND-TRUTH MEASUREMENTS (PROVIDED BY USER):
- Width: {user_w if user_w else 'Estimate from photo'} ft
- Length: {user_l if user_l else 'Estimate from photo'} ft
- Ceiling Height: {user_h if user_h else 'Estimate from photo'} ft
DO NOT invent conflicting dimensions. You MUST use these exact ground-truth measurements as the physical envelope.
Ensure every placement zone bounding box (max_width_in, max_depth_in, max_height_in) strictly respects these physical boundaries, leaving at least 32 inches for circulation walkways.
"""

        prompt = f"""You are an expert architectural spatial analyst and interior surveyor.
Examine this photograph of an interior space.
{ground_truth_directive}
Determine the physical dimensions, ceiling height, and floor clearance boundaries in feet and inches.
Identify 5 specific placement zones for furniture that respect architectural circulation walkways (minimum 30-36 inches walkway clearance).

For each zone, specify:
1. Zone name: 'seating_zone' (main sofa), 'table_zone' (coffee table), 'accent_zone' (accent/armchair), 'lamp_zone' (floor lamp), 'rug_zone' (area rug).
2. Maximum physical bounding box (max_width_in, max_depth_in, max_height_in) in inches so furniture physically fits without overcrowding.
3. 2D perspective normalized hotspot coordinates (hotspot_x_pct from 0 to 100, hotspot_y_pct from 0 to 100) where that furniture piece will sit in the image.
4. Rationale for placement.

User hint / design goal: {user_hint or 'Modern interior redesign'}
"""

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[img, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_json_schema=RoomSpatialAnalysis.model_json_schema(),
                temperature=0.1,
            )
        )

        if response and response.text:
            data = json.loads(response.text)
            # Enforce user dimensions if provided
            if user_w:
                data.setdefault("room_dimensions_ft", {})["width_ft"] = float(user_w)
            if user_l:
                data.setdefault("room_dimensions_ft", {})["length_ft"] = float(user_l)
            if user_h:
                data.setdefault("room_dimensions_ft", {})["ceiling_height_ft"] = float(user_h)
            
            w = data["room_dimensions_ft"].get("width_ft", 14.0)
            l = data["room_dimensions_ft"].get("length_ft", 16.0)
            data["floor_area_sqft"] = round(w * l, 1)
            return data
        return None

    def _deterministic_spatial_analysis(
        self,
        image_path: str,
        user_hint: Optional[str] = None,
        user_dims: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Intelligent deterministic spatial calculation using user ground-truth measurements
        with mathematical ergonomic zoning formulas.
        """
        dims = user_dims or {}
        user_w = dims.get("width_ft")
        user_l = dims.get("length_ft")
        user_h = dims.get("height_ft")

        # Fallback estimation from image aspect ratio if user did not provide all values
        width, height = 800, 600
        aspect_ratio = 1.33
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    aspect_ratio = width / height if height > 0 else 1.33
            except Exception:
                pass

        if aspect_ratio >= 1.4:
            est_w, est_l, est_h = 16.0, 18.0, 9.5
        elif aspect_ratio >= 1.1:
            est_w, est_l, est_h = 14.0, 15.5, 9.0
        else:
            est_w, est_l, est_h = 12.0, 14.0, 8.5

        # Merge user ground truth with sensible defaults
        width_ft = float(user_w) if user_w and user_w > 0 else est_w
        length_ft = float(user_l) if user_l and user_l > 0 else est_l
        ceiling_ft = float(user_h) if user_h and user_h > 0 else est_h

        sqft = round(width_ft * length_ft, 1)

        # Smaller dimension represents the transverse wall clearance
        min_dim_in = min(width_ft, length_ft) * 12
        max_dim_in = max(width_ft, length_ft) * 12
        ceiling_in = ceiling_ft * 12

        # 1. Seating Zone: Main sofa occupies up to 55% of the transverse axis, leaving 30"+ walkways
        sofa_max_width = round(min(96.0, min_dim_in * 0.55), 1)
        sofa_max_depth = round(min(42.0, max_dim_in * 0.22), 1)
        sofa_max_height = round(min(38.0, ceiling_in * 0.35), 1)

        # 2. Coffee Table: Typically 55-65% of sofa width, with 18" reach clearance
        table_max_width = round(min(48.0, sofa_max_width * 0.60), 1)
        table_max_depth = round(min(30.0, sofa_max_depth * 0.75), 1)
        table_max_height = 20.0

        # 3. Accent Chair: Sits angled in the perimeter zone
        accent_max_width = round(min(36.0, min_dim_in * 0.25), 1)
        accent_max_depth = round(min(36.0, max_dim_in * 0.22), 1)
        accent_max_height = round(min(40.0, ceiling_in * 0.38), 1)

        # 4. Floor Lamp: Bounded by ceiling height (leaving 18" headroom minimum)
        lamp_max_height = round(min(84.0, ceiling_in - 18.0), 1)

        # 5. Area Rug: Bounds 70% of floor area to anchor furniture grouping
        rug_max_width = round(min(120.0, min_dim_in * 0.75), 1)
        rug_max_depth = round(min(144.0, max_dim_in * 0.65), 1)

        zones = {
            "seating_zone": {
                "zone_name": "seating_zone",
                "max_width_in": sofa_max_width,
                "max_depth_in": sofa_max_depth,
                "max_height_in": sofa_max_height,
                "suggested_category": "sofa",
                "hotspot_x_pct": 48.0,
                "hotspot_y_pct": 62.0,
                "description": f"Main seating zone sized up to {sofa_max_width}\"W to maintain minimum 32\" perimeter walkway across the {width_ft}' wall."
            },
            "table_zone": {
                "zone_name": "table_zone",
                "max_width_in": table_max_width,
                "max_depth_in": table_max_depth,
                "max_height_in": table_max_height,
                "suggested_category": "coffee_table",
                "hotspot_x_pct": 50.0,
                "hotspot_y_pct": 76.0,
                "description": f"Central coffee table bounded to {table_max_width}\"W preserving 18\" reach buffer from sofa."
            },
            "accent_zone": {
                "zone_name": "accent_zone",
                "max_width_in": accent_max_width,
                "max_depth_in": accent_max_depth,
                "max_height_in": accent_max_height,
                "suggested_category": "accent_chair",
                "hotspot_x_pct": 22.0,
                "hotspot_y_pct": 68.0,
                "description": f"Accent seating corner bounded to {accent_max_width}\"W for natural conversational flow."
            },
            "lamp_zone": {
                "zone_name": "lamp_zone",
                "max_width_in": 22.0,
                "max_depth_in": 22.0,
                "max_height_in": lamp_max_height,
                "suggested_category": "floor_lamp",
                "hotspot_x_pct": 82.0,
                "hotspot_y_pct": 52.0,
                "description": f"Vertical lighting corner tailored to {ceiling_ft}' ceiling height (max {lamp_max_height}\"H)."
            },
            "rug_zone": {
                "zone_name": "rug_zone",
                "max_width_in": rug_max_width,
                "max_depth_in": rug_max_depth,
                "max_height_in": 1.5,
                "suggested_category": "rug",
                "hotspot_x_pct": 50.0,
                "hotspot_y_pct": 84.0,
                "description": f"Proportioned area rug ({rug_max_width}\"W x {rug_max_depth}\"D) anchoring the seating island on the {sqft} sq.ft floor."
            }
        }

        dim_status = "user-verified measurements" if (user_w or user_l or user_h) else "photometric aspect-ratio estimation"

        return {
            "room_type": "living_room",
            "room_dimensions_ft": {
                "width_ft": width_ft,
                "length_ft": length_ft,
                "ceiling_height_ft": ceiling_ft
            },
            "floor_area_sqft": sqft,
            "natural_light_source": "lateral window intake",
            "existing_flooring": "neutral architectural substrate",
            "primary_focal_wall": "center wall elevation",
            "circulation_clearance_in": 32.0,
            "zones": zones,
            "design_recommendation": f"Calibrated for {width_ft}' Length x {length_ft}' Width ({sqft} sq.ft) with {ceiling_ft}' ceiling based on {dim_status}. Maintains 32-inch unobstructed circulation corridors."
        }

# Singleton instance
spatial_tool = SpatialTool()
