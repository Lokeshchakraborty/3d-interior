"""
Spatial Perception & Room Dimension Estimator Tool
Performs multimodal spatial reasoning to extract physical room dimensions,
clearance boundaries, and furniture placement zones.
Uses Google Gemini 3.8 Flash when GEMINI_API_KEY is available, with an intelligent
deterministic architectural fallback.
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
        description="Estimated physical room dimensions in feet: width_ft, length_ft, ceiling_height_ft"
    )
    floor_area_sqft: float = Field(..., description="Total estimated floor area in square feet")
    natural_light_source: str = Field(..., description="Position of primary windows/light: left, right, rear, frontal")
    existing_flooring: str = Field(..., description="Detected floor material: hardwood, tile, concrete, carpet")
    primary_focal_wall: str = Field(..., description="Position of the main focal wall: center, left, right")
    circulation_clearance_in: float = Field(..., description="Required minimum walkway circulation clearance in inches (typically 30-36 in)")
    zones: Dict[str, ZoneBoundary] = Field(
        ...,
        description="Zoned physical placement envelopes for furniture items"
    )
    design_recommendation: str = Field(..., description="Architectural recommendations for scale and proportion")

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

    def analyze_room(self, image_path: str, user_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the room image to extract physical dimensions, clearances, and placement zones.
        """
        # 1. Check if Gemini Client is active and API key provided
        if self.client:
            try:
                result = self._analyze_with_gemini(image_path, user_hint)
                if result:
                    result["analysis_engine"] = "gemini-3.8-flash"
                    return result
            except Exception as e:
                print(f"Gemini spatial analysis encountered error, falling back to deterministic engine: {e}")

        # 2. Deterministic Architectural Fallback
        fallback = self._deterministic_spatial_analysis(image_path, user_hint)
        fallback["analysis_engine"] = "deterministic_spatial_heuristics"
        return fallback

    def _analyze_with_gemini(self, image_path: str, user_hint: Optional[str] = None) -> Optional[Dict[str, Any]]:
        from google.genai import types

        img = Image.open(image_path).convert("RGB")

        prompt = f"""You are an expert architectural spatial analyst and interior surveyor.
Examine this photograph of an interior space.
Estimate the real-world physical dimensions, ceiling height, and floor clearance boundaries in feet and inches.
Identify 5 specific placement zones for furniture that respect architectural circulation walkways (minimum 30 inches walkway clearance).

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
                temperature=0.2,
            )
        )

        if response and response.text:
            data = json.loads(response.text)
            return data
        return None

    def _deterministic_spatial_analysis(self, image_path: str, user_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Intelligent deterministic spatial calculation based on image aspect ratio and standard architectural clearance standards.
        """
        width, height = 800, 600
        aspect_ratio = 1.33
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    aspect_ratio = width / height if height > 0 else 1.33
            except Exception:
                pass

        # Calculate estimated room dimensions based on standard residential scale
        # Wide angle lens vs portrait perspective
        if aspect_ratio >= 1.4:
            width_ft, length_ft, ceiling_ft = 16.0, 18.0, 9.5
        elif aspect_ratio >= 1.1:
            width_ft, length_ft, ceiling_ft = 14.0, 15.5, 9.0
        else:
            width_ft, length_ft, ceiling_ft = 12.0, 14.0, 8.5

        sqft = round(width_ft * length_ft, 1)

        # Standard ergonomic zoning with normalized 2D perspective hotspots
        zones = {
            "seating_zone": {
                "zone_name": "seating_zone",
                "max_width_in": min(92.0, (width_ft * 12) * 0.55),
                "max_depth_in": 40.0,
                "max_height_in": 36.0,
                "suggested_category": "sofa",
                "hotspot_x_pct": 48.0,
                "hotspot_y_pct": 62.0,
                "description": "Primary central seating focal zone positioned opposite the main visual axis with 34-inch front clearance."
            },
            "table_zone": {
                "zone_name": "table_zone",
                "max_width_in": 46.0,
                "max_depth_in": 28.0,
                "max_height_in": 20.0,
                "suggested_category": "coffee_table",
                "hotspot_x_pct": 50.0,
                "hotspot_y_pct": 76.0,
                "description": "Central low-profile coffee table zone maintaining 18-inch reach buffer from main sofa."
            },
            "accent_zone": {
                "zone_name": "accent_zone",
                "max_width_in": 34.0,
                "max_depth_in": 34.0,
                "max_height_in": 38.0,
                "suggested_category": "accent_chair",
                "hotspot_x_pct": 22.0,
                "hotspot_y_pct": 68.0,
                "description": "Angled conversational accent seating corner positioned near natural light intake."
            },
            "lamp_zone": {
                "zone_name": "lamp_zone",
                "max_width_in": 22.0,
                "max_depth_in": 22.0,
                "max_height_in": 78.0,
                "suggested_category": "floor_lamp",
                "hotspot_x_pct": 82.0,
                "hotspot_y_pct": 52.0,
                "description": "Vertical ambient lighting corner illuminating room peripheral shadow without obstructing circulation."
            },
            "rug_zone": {
                "zone_name": "rug_zone",
                "max_width_in": min(108.0, (width_ft * 12) * 0.70),
                "max_depth_in": min(132.0, (length_ft * 12) * 0.65),
                "max_height_in": 1.5,
                "suggested_category": "rug",
                "hotspot_x_pct": 50.0,
                "hotspot_y_pct": 84.0,
                "description": "Acoustic and spatial anchoring area rug extending at least 8 inches beyond front legs of all seating."
            }
        }

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
            "design_recommendation": f"Scale furniture proportionally for an estimated {width_ft}' x {length_ft}' ({sqft} sq.ft) space. Maintain a minimum 32-inch unobstructed circulation corridor from entryway."
        }

# Singleton instance
spatial_tool = SpatialTool()
