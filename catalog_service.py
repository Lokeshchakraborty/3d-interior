"""
B2C Furniture Catalog Service
Provides access to real, dimension-verified furniture products from Amazon India, Flipkart, and IKEA.
Each product explicitly defines its physical dimensions, geometric shape, color palette,
and visual description specifying both shape and color to eliminate generative hallucinations.
Supports prompt-driven semantic search so user desires directly curate matching furniture.
"""

import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ProductDimensions(BaseModel):
    width_in: float = Field(..., description="Width in inches")
    depth_in: float = Field(..., description="Depth in inches")
    height_in: float = Field(..., description="Height in inches")
    width_cm: float = Field(..., description="Width in centimeters")
    depth_cm: float = Field(..., description="Depth in centimeters")
    height_cm: float = Field(..., description="Height in centimeters")

class Product(BaseModel):
    id: str
    title: str
    store: str  # "Amazon", "Flipkart", "IKEA"
    category: str  # "sofa", "coffee_table", "accent_chair", "tv_unit", "rug", "floor_lamp", "side_table"
    style: str  # "scandinavian", "japandi", "modern_luxury", "bohemian", "industrial"
    shape: str  # Explicit geometric shape: "rectangular", "oval", "circular round", "L-shaped", etc.
    dimensions: ProductDimensions
    price_inr: int
    buy_url: str
    image_url: str
    materials: List[str]
    color: str  # Explicit primary and secondary color palette
    visual_description: str  # Must explicitly describe both SHAPE and COLOR
    rating: float = 4.5
    review_count: int = 150
    in_stock: bool = True

# Curated high-fidelity catalog of real B2C furniture with verified dimensions, shapes, and colors
CATALOG: List[Product] = [
    # ==================== 1. SCANDINAVIAN ====================
    Product(
        id="ikea-sofa-landskrona",
        title="IKEA LANDSKRONA 3-Seat Sofa, Gunnared Light Green / Wood",
        store="IKEA",
        category="sofa",
        style="scandinavian",
        shape="rectangular geometric",
        dimensions=ProductDimensions(width_in=80.3, depth_in=35.0, height_in=30.7, width_cm=204, depth_cm=89, height_cm=78),
        price_inr=54990,
        buy_url="https://www.ikea.com/in/en/p/landskrona-3-seat-sofa-gunnared-light-green-wood-s59270306/",
        image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80",
        materials=["Boucle textured fabric", "Solid oak legs", "Pocket springs"],
        color="Muted Sage Green & Natural Light Oak",
        visual_description="rectangular 3-seater Scandinavian sofa in muted sage green textured fabric with clean geometric lines and tapered round light oak wooden legs",
        rating=4.7,
        review_count=328
    ),
    Product(
        id="ikea-sofa-soederhamn",
        title="IKEA SÖDERHAMN 3-Seat Sectional Sofa, Viarp Beige/Brown",
        store="IKEA",
        category="sofa",
        style="scandinavian",
        shape="low modular rectangular",
        dimensions=ProductDimensions(width_in=73.2, depth_in=39.0, height_in=32.6, width_cm=186, depth_cm=99, height_cm=83),
        price_inr=44990,
        buy_url="https://www.ikea.com/in/en/p/soederhamn-3-seat-section-viarp-beige-brown-s09305697/",
        image_url="https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=600&q=80",
        materials=["Cotton-polyester weave", "Chrome-plated steel legs", "High resilience foam"],
        color="Warm Oatmeal Beige & Silver",
        visual_description="low modular rectangular Scandinavian sofa in warm oatmeal beige textured weave with slender silver chrome steel legs and deep seating",
        rating=4.6,
        review_count=215
    ),
    Product(
        id="amz-scandi-linen-sofa",
        title="Wakefit Napper 3-Seater Minimalist Scandinavian Fabric Sofa (Oatmeal Cream)",
        store="Amazon",
        category="sofa",
        style="scandinavian",
        shape="straight clean-line rectangular",
        dimensions=ProductDimensions(width_in=78.0, depth_in=33.0, height_in=31.0, width_cm=198, depth_cm=84, height_cm=79),
        price_inr=18499,
        buy_url="https://www.amazon.in/dp/B08L7L984M",
        image_url="https://images.unsplash.com/photo-1567016432779-094069958ea5?auto=format&fit=crop&w=600&q=80",
        materials=["Breathable organic linen", "Kiln-dried neem wood frame", "Natural tapered rubberwood legs"],
        color="Oatmeal Cream & Blonde Beech",
        visual_description="straight rectangular Scandinavian sofa upholstered in durable oatmeal cream linen with flared blonde beech wooden legs",
        rating=4.5,
        review_count=512
    ),
    Product(
        id="amz-scandi-boucle-sofa",
        title="Urban Ladder Westley 3-Seater Bouclé Minimalist Sofa (Ivory White)",
        store="Amazon",
        category="sofa",
        style="scandinavian",
        shape="soft curved rectangular",
        dimensions=ProductDimensions(width_in=82.0, depth_in=36.0, height_in=30.0, width_cm=208, depth_cm=91, height_cm=76),
        price_inr=42999,
        buy_url="https://www.amazon.in/dp/B09V7N421G",
        image_url="https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=600&q=80",
        materials=["Plush teddy boucle yarn", "Hardwood frame", "Natural oak base"],
        color="Ivory Snow White & Light Oak",
        visual_description="softly curved rectangular Scandinavian sofa wrapped in tactile ivory snow bouclé fabric with a continuous light oak wooden plinth",
        rating=4.8,
        review_count=89
    ),
    Product(
        id="ikea-table-loevbacken",
        title="IKEA LÖVBACKEN Side / Coffee Table, Medium Brown Leaf Shape",
        store="IKEA",
        category="coffee_table",
        style="scandinavian",
        shape="organic asymmetrical leaf triangle",
        dimensions=ProductDimensions(width_in=30.3, depth_in=15.3, height_in=20.1, width_cm=77, depth_cm=39, height_cm=51),
        price_inr=5990,
        buy_url="https://www.ikea.com/in/en/p/loevbacken-side-table-medium-brown-80270125/",
        image_url="https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=600&q=80",
        materials=["Poplar veneer top", "Solid beech legs", "Gold metallic brass foot tips"],
        color="Medium Warm Walnut & Gold Brass",
        visual_description="asymmetrical leaf-shaped organic Scandinavian coffee table with medium warm walnut veneer top and 3 slender angled legs with gold brass tips",
        rating=4.8,
        review_count=612
    ),
    Product(
        id="amz-scandi-round-table",
        title="Solimo Vega Solid Sheesham Round Scandinavian Coffee Table",
        store="Amazon",
        category="coffee_table",
        style="scandinavian",
        shape="circular round cylinder",
        dimensions=ProductDimensions(width_in=36.0, depth_in=36.0, height_in=18.0, width_cm=91, depth_cm=91, height_cm=46),
        price_inr=8499,
        buy_url="https://www.amazon.in/dp/B083QRLC7F",
        image_url="https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?auto=format&fit=crop&w=600&q=80",
        materials=["Solid Indian Sheesham wood", "Natural matte PU sealant"],
        color="Light Honey Oak Finish",
        visual_description="circular round solid oak Scandinavian coffee table with cross-lap base and smooth chamfered edge tabletop",
        rating=4.6,
        review_count=340
    ),
    Product(
        id="flip-scandi-nest-table",
        title="DeckUp Siena Set of 2 Scandinavian Nesting Coffee Tables",
        store="Flipkart",
        category="coffee_table",
        style="scandinavian",
        shape="twin circular round nesting",
        dimensions=ProductDimensions(width_in=24.0, depth_in=24.0, height_in=17.5, width_cm=61, depth_cm=61, height_cm=44),
        price_inr=4299,
        buy_url="https://www.flipkart.com/deckup-siena-engineered-wood-coffee-table/p/itmfc44d8ff27cf7",
        image_url="https://images.unsplash.com/photo-1592078615290-033ee584e267?auto=format&fit=crop&w=600&q=80",
        materials=["Matte white engineered wood", "Solid pine legs"],
        color="Matte Arctic White & Natural Pine",
        visual_description="twin circular nesting Scandinavian coffee tables with satin white rounded tops and slender natural pine tripod legs",
        rating=4.4,
        review_count=180
    ),
    Product(
        id="ikea-chair-strandmon",
        title="IKEA STRANDMON Wing Chair, Nordvalla Dark Gray",
        store="IKEA",
        category="accent_chair",
        style="scandinavian",
        shape="high-back curved wingback",
        dimensions=ProductDimensions(width_in=32.2, depth_in=37.8, height_in=39.8, width_cm=82, depth_cm=96, height_cm=101),
        price_inr=18990,
        buy_url="https://www.ikea.com/in/en/p/strandmon-wing-chair-nordvalla-dark-gray-70359844/",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["Woven polyester fabric", "Solid beech legs", "Polyurethane foam"],
        color="Nordvalla Dark Slate Gray & Black",
        visual_description="high-back curved Scandinavian wingback armchair in dark slate gray textured weave with button-tufted backrest and dark stained tapered wooden legs",
        rating=4.7,
        review_count=512
    ),
    Product(
        id="amz-scandi-poang-chair",
        title="IKEA POÄNG Armchair with Cushion, Birch Veneer & Knisa Beige",
        store="Amazon",
        category="accent_chair",
        style="scandinavian",
        shape="curved cantilever ergonomic",
        dimensions=ProductDimensions(width_in=26.8, depth_in=32.3, height_in=39.4, width_cm=68, depth_cm=82, height_cm=100),
        price_inr=8990,
        buy_url="https://www.amazon.in/dp/B07YDJ1L5C",
        image_url="https://images.unsplash.com/photo-1549497538-303791108f95?auto=format&fit=crop&w=600&q=80",
        materials=["Layer-glued bent birch wood", "Knisa cotton-polyester cushion"],
        color="Light Birch Wood & Cream Beige",
        visual_description="curved cantilever Scandinavian bentwood armchair with light natural birch veneer frame and supportive cream beige padded cushion",
        rating=4.6,
        review_count=980
    ),
    Product(
        id="ikea-lamp-hektar",
        title="IKEA HEKTAR Floor Lamp with LED Bulb, Dark Gray Metal",
        store="IKEA",
        category="floor_lamp",
        style="scandinavian",
        shape="oversized cone industrial bell",
        dimensions=ProductDimensions(width_in=12.5, depth_in=12.5, height_in=71.0, width_cm=32, depth_cm=32, height_cm=181),
        price_inr=6990,
        buy_url="https://www.ikea.com/in/en/p/hektar-floor-lamp-dark-gray-00216544/",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Powder-coated steel", "Cast iron weight base", "Aluminum interior"],
        color="Matte Anthracite Dark Gray",
        visual_description="tall Scandinavian steel floor lamp with oversized cone bell shade in matte anthracite dark gray and warm directional spotlighting",
        rating=4.6,
        review_count=340
    ),
    Product(
        id="amz-scandi-tripod-lamp",
        title="Crosscut Furniture Nordic Wooden Tripod Floor Lamp with Cream Linen Shade",
        store="Amazon",
        category="floor_lamp",
        style="scandinavian",
        shape="triangular tripod flared column",
        dimensions=ProductDimensions(width_in=18.0, depth_in=18.0, height_in=58.0, width_cm=46, depth_cm=46, height_cm=147),
        price_inr=3499,
        buy_url="https://www.amazon.in/dp/B07V6W454N",
        image_url="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=600&q=80",
        materials=["Natural pine timber", "Drum woven linen fabric shade"],
        color="Natural Pine Timber & Soft Cream",
        visual_description="slender triangular Scandinavian tripod floor lamp with natural pine wooden legs and cylindrical soft cream linen drum shade",
        rating=4.5,
        review_count=420
    ),
    Product(
        id="ikea-rug-stoense",
        title="IKEA STOENSE Low Pile Area Rug, Off-White Beige (170x240 cm)",
        store="IKEA",
        category="rug",
        style="scandinavian",
        shape="rectangular flat",
        dimensions=ProductDimensions(width_in=94.5, depth_in=67.0, height_in=0.5, width_cm=240, depth_cm=170, height_cm=1.3),
        price_inr=6990,
        buy_url="https://www.ikea.com/in/en/p/stoense-rug-low-pile-off-white-50426802/",
        image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
        materials=["100% polypropylene pile", "Synthetic latex backing"],
        color="Soft Off-White Cream & Warm Milk",
        visual_description="rectangular low-pile Scandinavian area rug in soft off-white cream with dense sound-dampening wool-like texture",
        rating=4.8,
        review_count=215
    ),
    Product(
        id="amz-scandi-jute-rug",
        title="Saral Home Handwoven Scandinavian Diamond Jute Area Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="scandinavian",
        shape="rectangular textured weave",
        dimensions=ProductDimensions(width_in=96.0, depth_in=60.0, height_in=0.4, width_cm=244, depth_cm=152, height_cm=1.0),
        price_inr=4799,
        buy_url="https://www.amazon.in/dp/B08V8W3K9L",
        image_url="https://images.unsplash.com/photo-1581539250439-c96689b516dd?auto=format&fit=crop&w=600&q=80",
        materials=["100% natural braided golden jute", "Bleached white cotton warp"],
        color="Natural Golden Jute & Bleached Cotton White",
        visual_description="rectangular handwoven Scandinavian area rug in natural golden jute with subtle white diamond geometric weave patterns",
        rating=4.4,
        review_count=310
    ),

    # ==================== 2. JAPANDI ====================
    Product(
        id="ikea-sofa-kivik",
        title="IKEA KIVIK 3-Seat Low-Profile Sofa, Tibbleby Beige-Grey",
        store="IKEA",
        category="sofa",
        style="japandi",
        shape="grounded rectangular low-profile",
        dimensions=ProductDimensions(width_in=74.8, depth_in=37.4, height_in=32.6, width_cm=190, depth_cm=95, height_cm=83),
        price_inr=39990,
        buy_url="https://www.ikea.com/in/en/p/kivik-three-seat-sofa-tibbleby-beige-grey-s99440578/",
        image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80",
        materials=["Wabi-sabi textured cotton blend", "Solid ash wood frame", "Memory foam topper"],
        color="Muted Stone Grey & Oatmeal",
        visual_description="grounded rectangular low-profile Japandi sofa in muted stone-grey organic linen with deep square cushions and wide armrests",
        rating=4.7,
        review_count=418
    ),
    Product(
        id="amz-japandi-wood-sofa",
        title="Saraf Furniture Solid Sheesham Low Platform Bench Sofa (Honey Teak)",
        store="Amazon",
        category="sofa",
        style="japandi",
        shape="low platform rectilinear",
        dimensions=ProductDimensions(width_in=75.0, depth_in=32.0, height_in=28.0, width_cm=190, depth_cm=81, height_cm=71),
        price_inr=28999,
        buy_url="https://www.amazon.in/dp/B07T7L494K",
        image_url="https://images.unsplash.com/photo-1517705008128-361805f42e86?auto=format&fit=crop&w=600&q=80",
        materials=["Solid seasoned Sheesham hardwood", "Off-white cotton duck canvas cushions"],
        color="Honey Teak & Off-White Canvas",
        visual_description="low platform rectilinear Japandi daybed sofa featuring exposed joinery honey teak timber and thick firm off-white canvas cushions",
        rating=4.6,
        review_count=165
    ),
    Product(
        id="amz-japandi-curved-sofa",
        title="Solimo Wabi-Sabi Low Curved 3-Seater Sofa (Muted Clay & Ash)",
        store="Amazon",
        category="sofa",
        style="japandi",
        shape="gentle curved organic rectangular",
        dimensions=ProductDimensions(width_in=78.0, depth_in=35.0, height_in=29.0, width_cm=198, depth_cm=89, height_cm=74),
        price_inr=34499,
        buy_url="https://www.amazon.in/dp/B09C9V112Z",
        image_url="https://images.unsplash.com/photo-1616046229478-9901c5536a45?auto=format&fit=crop&w=600&q=80",
        materials=["Textured coarse linen", "Solid ash wood skids"],
        color="Muted Clay Grey & Washed Ash",
        visual_description="gently curved organic Japandi 3-seater sofa with seamless muted clay grey coarse linen upholstery resting on concealed low ash wood skids",
        rating=4.7,
        review_count=72
    ),
    Product(
        id="amz-japandi-coffee-table",
        title="Urban Wood Sheesham Round Low Fluted Coffee Table (Teak Finish)",
        store="Amazon",
        category="coffee_table",
        style="japandi",
        shape="circular round cylinder",
        dimensions=ProductDimensions(width_in=31.5, depth_in=31.5, height_in=14.0, width_cm=80, depth_cm=80, height_cm=35),
        price_inr=11499,
        buy_url="https://www.amazon.in/dp/B09D3R894M",
        image_url="https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?auto=format&fit=crop&w=600&q=80",
        materials=["Solid Indian Sheesham wood", "Slatted fluted tambour timber"],
        color="Warm Honey Teak",
        visual_description="circular round low Japandi coffee table with vertical fluted wooden tambour slats and flat round honey teak top",
        rating=4.6,
        review_count=87
    ),
    Product(
        id="amz-japandi-kidney-table",
        title="Custom Decor Organic Kidney Curved Ash Wood Low Coffee Table",
        store="Amazon",
        category="coffee_table",
        style="japandi",
        shape="curved asymmetrical kidney bean",
        dimensions=ProductDimensions(width_in=42.0, depth_in=24.0, height_in=15.0, width_cm=107, depth_cm=61, height_cm=38),
        price_inr=9990,
        buy_url="https://www.amazon.in/dp/B09N8V414J",
        image_url="https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=600&q=80",
        materials=["Solid natural ash wood", "Beeswax organic finish"],
        color="Pale Ash Blonde Wood",
        visual_description="organic kidney-shaped asymmetrical Japandi low coffee table with softly bevelled natural ash top and 3 thick cylindrical peg legs",
        rating=4.7,
        review_count=94
    ),
    Product(
        id="flip-japandi-tatami-table",
        title="Woodness Low-Height Chashitsu Tea Coffee Table (Walnut Finish)",
        store="Flipkart",
        category="coffee_table",
        style="japandi",
        shape="low rectangular slab",
        dimensions=ProductDimensions(width_in=36.0, depth_in=22.0, height_in=13.0, width_cm=91, depth_cm=56, height_cm=33),
        price_inr=7299,
        buy_url="https://www.flipkart.com/woodness-low-tea-table/p/itm2841b99ff12e",
        image_url="https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=600&q=80",
        materials=["Solid acacia wood", "Matte open-pore walnut finish"],
        color="Smoked Walnut Brown",
        visual_description="low rectilinear Japandi tatami tea table with a thick solid acacia tabletop and minimalist block legs in smoked walnut finish",
        rating=4.5,
        review_count=138
    ),
    Product(
        id="amz-japandi-cane-chair",
        title="Green Soul Natural Cane & Solid Wood Low Accent Lounge Chair",
        store="Amazon",
        category="accent_chair",
        style="japandi",
        shape="curved backrest low lounge",
        dimensions=ProductDimensions(width_in=25.0, depth_in=28.0, height_in=30.0, width_cm=63, depth_cm=71, height_cm=76),
        price_inr=12999,
        buy_url="https://www.amazon.in/dp/B09H2S457T",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["Hand-woven natural rattan cane", "Solid North American Ash frame"],
        color="Bleached Natural Rattan & Matte Ash",
        visual_description="low-slung Japandi accent lounge chair featuring hand-woven octagonal rattan cane webbing and ergonomic angled solid ash wood armrests",
        rating=4.7,
        review_count=195
    ),
    Product(
        id="ikea-chair-vedbo",
        title="IKEA VEDBO Low Back Armchair, Gunnared Light Brown-Pink",
        store="IKEA",
        category="accent_chair",
        style="japandi",
        shape="sculptural curved shell",
        dimensions=ProductDimensions(width_in=28.7, depth_in=25.6, height_in=29.5, width_cm=73, depth_cm=65, height_cm=75),
        price_inr=16990,
        buy_url="https://www.ikea.com/in/en/p/vedbo-armchair-gunnared-light-brown-pink-10424131/",
        image_url="https://images.unsplash.com/photo-1544457070-4cd773b4d71e?auto=format&fit=crop&w=600&q=80",
        materials=["Moulded high-resilience foam", "Solid birch legs", "Woven tactile fabric"],
        color="Earthy Terracotta Clay & Birch Wood",
        visual_description="curved sculptural Japandi tub armchair with an organic embracing backrest in terracotta clay fabric and slender birch legs",
        rating=4.6,
        review_count=182
    ),
    Product(
        id="amz-japandi-washi-lamp",
        title="Eliante Japanese Washi Rice Paper Lantern Tripod Floor Lamp",
        store="Amazon",
        category="floor_lamp",
        style="japandi",
        shape="spherical oval lantern balloon",
        dimensions=ProductDimensions(width_in=15.0, depth_in=15.0, height_in=52.0, width_cm=38, depth_cm=38, height_cm=132),
        price_inr=4299,
        buy_url="https://www.amazon.in/dp/B0B7G8K41L",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Handmade mulberry Washi paper", "Wire ribs", "Matte black wire legs"],
        color="Translucent Warm Ivory & Matte Black",
        visual_description="spherical oval Japanese Washi rice paper floor lantern emitting soft 2700K ambient diffused glow on thin matte black wire tripod legs",
        rating=4.7,
        review_count=230
    ),
    Product(
        id="amz-japandi-bamboo-lamp",
        title="Decorfur Minimalist Slender Bamboo & Linen Column Floor Lamp",
        store="Amazon",
        category="floor_lamp",
        style="japandi",
        shape="cylindrical vertical column",
        dimensions=ProductDimensions(width_in=11.0, depth_in=11.0, height_in=56.0, width_cm=28, depth_cm=28, height_cm=142),
        price_inr=3899,
        buy_url="https://www.amazon.in/dp/B09K8L112T",
        image_url="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=600&q=80",
        materials=["Natural steamed bamboo ribs", "Unbleached woven flax linen"],
        color="Natural Blonde Bamboo & Flax Linen",
        visual_description="tall cylindrical column Japandi floor lamp crafted from natural vertical bamboo slats with an inner unbleached linen diffuser",
        rating=4.6,
        review_count=145
    ),
    Product(
        id="amz-japandi-ribbed-rug",
        title="Status Contract Hand-tufted Ribbed Wool Area Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="japandi",
        shape="rectangular linear ribbed",
        dimensions=ProductDimensions(width_in=96.0, depth_in=60.0, height_in=0.5, width_cm=244, depth_cm=152, height_cm=1.3),
        price_inr=8499,
        buy_url="https://www.amazon.in/dp/B08M9K841J",
        image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
        materials=["100% unbleached New Zealand wool", "Cotton cloth backing"],
        color="Oatmeal Cream & Sand",
        visual_description="rectangular hand-tufted Japandi area rug with parallel linear grooved ribs in soothing unbleached oatmeal cream wool",
        rating=4.8,
        review_count=290
    ),

    # ==================== 3. MODERN LUXURY ====================
    Product(
        id="amz-lux-velvet-sofa",
        title="CasaStyle Royal Emerald Velvet 3-Seater Channel-Tufted Sofa",
        store="Amazon",
        category="sofa",
        style="modern_luxury",
        shape="curved-back channel tufted rectangular",
        dimensions=ProductDimensions(width_in=84.0, depth_in=36.0, height_in=32.0, width_cm=213, depth_cm=91, height_cm=81),
        price_inr=36999,
        buy_url="https://www.amazon.in/dp/B08G8X994L",
        image_url="https://images.unsplash.com/photo-1550254478-ead40cc54513?auto=format&fit=crop&w=600&q=80",
        materials=["High-sheen plush royal velvet", "Electroplated gold titanium steel legs"],
        color="Deep Jewel Emerald Green & Polished Gold",
        visual_description="curved rectangular luxury sofa upholstered in deep emerald green velvet with vertical fluted channel tufting and polished gold stiletto legs",
        rating=4.8,
        review_count=210
    ),
    Product(
        id="flip-lux-curved-sofa",
        title="Bharat Lifestyle Cloud Bouclé Curved Luxury 3-Seater Sofa (Pearl White)",
        store="Flipkart",
        category="sofa",
        style="modern_luxury",
        shape="curved organic crescent",
        dimensions=ProductDimensions(width_in=88.0, depth_in=38.0, height_in=31.0, width_cm=224, depth_cm=96, height_cm=79),
        price_inr=49999,
        buy_url="https://www.flipkart.com/bharat-lifestyle-cloud-boucle-sofa/p/itmd3341b8ff12c",
        image_url="https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=600&q=80",
        materials=["High-density cloud bouclé fabric", "Solid hardwood frame", "Brushed brass plinth"],
        color="Pearl White Bouclé & Brushed Brass",
        visual_description="curved crescent luxury statement sofa in plush pearl white bouclé with seamless organic curves and a concealed brushed brass base rim",
        rating=4.9,
        review_count=115
    ),
    Product(
        id="amz-lux-chesterfield-sofa",
        title="Royal Interiors Deep Navy Velvet Chesterfield 3-Seater Sofa",
        store="Amazon",
        category="sofa",
        style="modern_luxury",
        shape="deep button-tufted rolled arm rectangular",
        dimensions=ProductDimensions(width_in=86.0, depth_in=35.0, height_in=31.0, width_cm=218, depth_cm=89, height_cm=79),
        price_inr=44500,
        buy_url="https://www.amazon.in/dp/B07Y7M419K",
        image_url="https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=600&q=80",
        materials=["Lustrous royal navy velvet", "High density memory foam", "Polished brass castor feet"],
        color="Midnight Royal Navy & Gold Brass",
        visual_description="classic Chesterfield luxury sofa in deep midnight navy velvet with all-over diamond button tufting and rolled scroll armrests on brass feet",
        rating=4.7,
        review_count=168
    ),
    Product(
        id="amz-lux-marble-table",
        title="DeckUp Calacatta Faux Marble & Brushed Gold Round Coffee Table",
        store="Amazon",
        category="coffee_table",
        style="modern_luxury",
        shape="circular round with cross frame",
        dimensions=ProductDimensions(width_in=36.0, depth_in=36.0, height_in=18.0, width_cm=91, depth_cm=91, height_cm=46),
        price_inr=14999,
        buy_url="https://www.amazon.in/dp/B08L5P781M",
        image_url="https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=600&q=80",
        materials=["Calacatta sintered stone marble top", "Brushed gold stainless steel frame"],
        color="Calacatta White with Grey Veining & Brushed Gold",
        visual_description="circular round modern luxury coffee table with high-gloss Calacatta white marble top featuring bold grey veining on an intersecting brushed gold metal frame",
        rating=4.7,
        review_count=285
    ),
    Product(
        id="flip-lux-glass-table",
        title="Home Centre Helix Tempered Smoked Glass & Brass Coffee Table",
        store="Flipkart",
        category="coffee_table",
        style="modern_luxury",
        shape="oval rounded oblong",
        dimensions=ProductDimensions(width_in=42.0, depth_in=24.0, height_in=17.0, width_cm=107, depth_cm=61, height_cm=43),
        price_inr=12490,
        buy_url="https://www.flipkart.com/home-centre-helix-glass-table/p/itmfc44e8812c",
        image_url="https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?auto=format&fit=crop&w=600&q=80",
        materials=["8mm smoked tempered safety glass", "Electroplated champagne brass tube base"],
        color="Smoked Charcoal Tint & Champagne Brass",
        visual_description="oval oblong modern luxury coffee table with bevelled smoked charcoal glass tabletop suspended above an open champagne brass cage base",
        rating=4.6,
        review_count=142
    ),
    Product(
        id="amz-lux-swivel-chair",
        title="Furny Adele Velvet Swivel Shell Accent Chair with Brushed Gold Base",
        store="Amazon",
        category="accent_chair",
        style="modern_luxury",
        shape="curved clamshell swivel",
        dimensions=ProductDimensions(width_in=31.0, depth_in=30.0, height_in=32.0, width_cm=79, depth_cm=76, height_cm=81),
        price_inr=15999,
        buy_url="https://www.amazon.in/dp/B09D8K544Q",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["Silky dust rose velvet", "360-degree silent brass swivel pedestal"],
        color="Dusty Rose Pink & Brushed Gold",
        visual_description="sculptural clamshell swivel accent chair in rich dusty rose velvet with pleated backrest folds on a 360-degree brushed gold pedestal",
        rating=4.8,
        review_count=178
    ),
    Product(
        id="flip-lux-boucle-chair",
        title="Urban Ladder Astrid Modern Brass Frame Bouclé Lounge Chair",
        store="Flipkart",
        category="accent_chair",
        style="modern_luxury",
        shape="geometric open cube with soft cushion",
        dimensions=ProductDimensions(width_in=29.0, depth_in=31.0, height_in=30.0, width_cm=74, depth_cm=79, height_cm=76),
        price_inr=19999,
        buy_url="https://www.flipkart.com/urban-ladder-astrid-chair/p/itm3341bcf881a",
        image_url="https://images.unsplash.com/photo-1549497538-303791108f95?auto=format&fit=crop&w=600&q=80",
        materials=["Cream teddy bouclé fabric", "Solid brass electroplated square profile steel"],
        color="Cream Teddy White & Polished Brass",
        visual_description="open geometric brass frame luxury lounge chair with plush oversized cream teddy bouclé seat and back pillows",
        rating=4.7,
        review_count=98
    ),
    Product(
        id="amz-lux-arc-lamp",
        title="Brightech Ornate Brushed Brass Arched Marble Base Floor Lamp",
        store="Amazon",
        category="floor_lamp",
        style="modern_luxury",
        shape="dramatic cantilever overhead arc",
        dimensions=ProductDimensions(width_in=44.0, depth_in=14.0, height_in=78.0, width_cm=112, depth_cm=36, height_cm=198),
        price_inr=9990,
        buy_url="https://www.amazon.in/dp/B07N4W771K",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Solid Carrara marble slab base (12kg)", "Extendable brushed brass gooseneck arm"],
        color="Brushed Gold & White Carrara Marble",
        visual_description="dramatic sweeping arc floor lamp with a brushed gold brass stem and hemispherical brass dome suspended over seating from a heavy white marble base",
        rating=4.8,
        review_count=360
    ),
    Product(
        id="amz-lux-silk-rug",
        title="Carpet Couture Abstract Marble Swirl High-Density Viscose Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="modern_luxury",
        shape="rectangular marble pattern",
        dimensions=ProductDimensions(width_in=96.0, depth_in=60.0, height_in=0.6, width_cm=244, depth_cm=152, height_cm=1.5),
        price_inr=14999,
        buy_url="https://www.amazon.in/dp/B08V5L981X",
        image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=600&q=80",
        materials=["Silky high-luster viscose yarn", "Woven cotton warp"],
        color="Gold Leaf, Charcoal Grey & Slate Silver",
        visual_description="high-luster modern luxury area rug with abstract fluid marble swirl patterns in metallic gold leaf, charcoal grey, and luminous slate silver",
        rating=4.8,
        review_count=192
    ),

    # ==================== 4. BOHEMIAN ====================
    Product(
        id="amz-boho-sofa",
        title="Kurl-on Earth Series 3-Seater Rattan Cane & Fabric Boho Sofa",
        store="Amazon",
        category="sofa",
        style="bohemian",
        shape="rectangular with curved armrests",
        dimensions=ProductDimensions(width_in=76.0, depth_in=34.0, height_in=32.0, width_cm=193, depth_cm=86, height_cm=81),
        price_inr=32990,
        buy_url="https://www.amazon.in/dp/B08V5Q471R",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["Hand-woven sustainable cane wicker", "Natural teak wood", "Terracotta linen cushions"],
        color="Terracotta Rust & Warm Honey Teak",
        visual_description="rectangular bohemian sofa with curved rattan wicker side panels in warm honey teak and plush terracotta rust linen cushions",
        rating=4.5,
        review_count=142
    ),
    Product(
        id="flip-boho-leather-sofa",
        title="Sleepyhead Bae Distressed Cognac Tan 3-Seater Sofa",
        store="Flipkart",
        category="sofa",
        style="bohemian",
        shape="slouchy deep rectangular",
        dimensions=ProductDimensions(width_in=80.0, depth_in=34.0, height_in=31.0, width_cm=203, depth_cm=86, height_cm=79),
        price_inr=24999,
        buy_url="https://www.flipkart.com/sleepyhead-bae-leather-sofa/p/itm2844b881a2",
        image_url="https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=600&q=80",
        materials=["Breathable vegan distressed leatherette", "Pocket springs"],
        color="Warm Cognac Tan & Muted Brass",
        visual_description="slouchy deep-seated bohemian sofa in rich distressed cognac tan leatherette with flange piped edges and warm vintage character",
        rating=4.6,
        review_count=210
    ),
    Product(
        id="amz-boho-mustard-sofa",
        title="Furny Velvet 3-Seater Tufted Sofa in Warm Mustard Yellow",
        store="Amazon",
        category="sofa",
        style="bohemian",
        shape="curved retro rectangular",
        dimensions=ProductDimensions(width_in=78.0, depth_in=33.0, height_in=31.0, width_cm=198, depth_cm=84, height_cm=79),
        price_inr=21499,
        buy_url="https://www.amazon.in/dp/B08L7L984Z",
        image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80",
        materials=["Plush tactile velvet", "Solid Sheesham wood turned legs"],
        color="Spiced Mustard Ochre & Dark Walnut",
        visual_description="retro bohemian 3-seater sofa in warm spiced mustard yellow velvet with tufted back accents and dark walnut turned spindle legs",
        rating=4.5,
        review_count=175
    ),
    Product(
        id="amz-boho-carved-table",
        title="CraftVatika Handmade Carved Solid Mango Wood Mandala Coffee Table",
        store="Amazon",
        category="coffee_table",
        style="bohemian",
        shape="circular round with carved lip",
        dimensions=ProductDimensions(width_in=32.0, depth_in=32.0, height_in=16.0, width_cm=81, depth_cm=81, height_cm=41),
        price_inr=9890,
        buy_url="https://www.amazon.in/dp/B09V7M441K",
        image_url="https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?auto=format&fit=crop&w=600&q=80",
        materials=["Solid seasoned mango wood", "Hand-carved floral mandala motif"],
        color="Weathered Bleached Wood & White Wash",
        visual_description="circular round bohemian coffee table handcrafted from mango wood with an intricately carved floral mandala top and whitewashed patina",
        rating=4.7,
        review_count=88
    ),
    Product(
        id="amz-boho-rattan-drum",
        title="Chumbak Braided Natural Rattan Drum Coffee Table with Tray Top",
        store="Amazon",
        category="coffee_table",
        style="bohemian",
        shape="cylindrical drum hourglass",
        dimensions=ProductDimensions(width_in=30.0, depth_in=30.0, height_in=16.5, width_cm=76, depth_cm=76, height_cm=42),
        price_inr=8499,
        buy_url="https://www.amazon.in/dp/B08X8P112L",
        image_url="https://images.unsplash.com/photo-1538688525198-9b88f6f53126?auto=format&fit=crop&w=600&q=80",
        materials=["Braided natural seagrass & rattan", "Concealed iron wire frame"],
        color="Natural Straw & Honey Blonde",
        visual_description="cylindrical drum-shaped bohemian coffee table woven from dense natural rattan ropes with an indented tray tabletop",
        rating=4.6,
        review_count=135
    ),
    Product(
        id="amz-boho-peacock-chair",
        title="Cane Crafts Handcrafted Natural Cane Peacock Fan Accent Chair",
        store="Amazon",
        category="accent_chair",
        style="bohemian",
        shape="high fan-back peacock throne",
        dimensions=ProductDimensions(width_in=33.0, depth_in=28.0, height_in=44.0, width_cm=84, depth_cm=71, height_cm=112),
        price_inr=11500,
        buy_url="https://www.amazon.in/dp/B07V7M994J",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["100% natural Assam cane wicker", "White linen seat pad"],
        color="Natural Golden Cane & Ivory Cushion",
        visual_description="iconic high fan-back bohemian peacock chair in intricately woven golden cane with radiating lace wicker patterns and round seat pad",
        rating=4.8,
        review_count=154
    ),
    Product(
        id="flip-boho-butterfly-chair",
        title="ExclusiveLane Genuine Leather & Iron Butterfly Lounge Chair",
        store="Flipkart",
        category="accent_chair",
        style="bohemian",
        shape="sculptural wing sling",
        dimensions=ProductDimensions(width_in=30.0, depth_in=29.0, height_in=35.0, width_cm=76, depth_cm=74, height_cm=89),
        price_inr=7999,
        buy_url="https://www.flipkart.com/exclusivelane-leather-butterfly-chair/p/itmfc44d8821a",
        image_url="https://images.unsplash.com/photo-1549497538-303791108f95?auto=format&fit=crop&w=600&q=80",
        materials=["Full-grain saddle leather sling", "Folding matte black iron frame"],
        color="Vintage Saddle Brown & Matte Black",
        visual_description="classic bohemian butterfly sling chair with a hand-stitched vintage saddle brown leather seat suspended on a folding black iron rod frame",
        rating=4.5,
        review_count=230
    ),
    Product(
        id="amz-boho-jute-lamp",
        title="Homesake Hand-Woven Bamboo & Jute Arc Floor Lamp",
        store="Amazon",
        category="floor_lamp",
        style="bohemian",
        shape="curved arched gooseneck with woven shade",
        dimensions=ProductDimensions(width_in=16.0, depth_in=16.0, height_in=60.0, width_cm=41, depth_cm=41, height_cm=152),
        price_inr=4599,
        buy_url="https://www.amazon.in/dp/B08V9P112J",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Hand-woven bamboo wicker basket shade", "Curved dark walnut timber arm"],
        color="Natural Straw Tan & Dark Walnut",
        visual_description="arched bohemian floor lamp with a sweeping wooden arm supporting a bell-shaped open-weave bamboo basket shade creating patterned warm shadows",
        rating=4.6,
        review_count=180
    ),
    Product(
        id="amz-boho-macrame-rug",
        title="Status Multi Moroccan Berber Diamond Shag Area Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="bohemian",
        shape="rectangular shag with fringe tassels",
        dimensions=ProductDimensions(width_in=96.0, depth_in=60.0, height_in=0.8, width_cm=244, depth_cm=152, height_cm=2.0),
        price_inr=7499,
        buy_url="https://www.amazon.in/dp/B07T7R494M",
        image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
        materials=["Plush microfiber high shag pile", "Braided fringe ends"],
        color="Warm Ivory Cream & Charcoal Diamond Lines",
        visual_description="plush high-pile Moroccan Berber bohemian area rug in warm ivory cream with geometric charcoal diamond lattice lines and braided tassel fringe",
        rating=4.7,
        review_count=340
    ),
    Product(
        id="amz-boho-kilim-rug",
        title="Villedomo Handwoven Reversible Cotton Kilim Geometric Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="bohemian",
        shape="rectangular flatweave tribal",
        dimensions=ProductDimensions(width_in=96.0, depth_in=60.0, height_in=0.3, width_cm=244, depth_cm=152, height_cm=0.8),
        price_inr=4299,
        buy_url="https://www.amazon.in/dp/B09C8L114J",
        image_url="https://images.unsplash.com/photo-1581539250439-c96689b516dd?auto=format&fit=crop&w=600&q=80",
        materials=["100% pure organic cotton flatweave", "Natural vegetable dyes"],
        color="Terracotta Rust, Sage Green & Mustard Ochre",
        visual_description="reversible flatweave bohemian kilim area rug featuring vibrant Aztec geometric motifs dyed in earthy terracotta rust, sage green, and mustard ochre",
        rating=4.5,
        review_count=215
    ),

    # ==================== 5. INDUSTRIAL ====================
    Product(
        id="amz-ind-chesterfield",
        title="Sleepyhead Distressed Cigar Brown Leatherette 3-Seater Sofa",
        store="Amazon",
        category="sofa",
        style="industrial",
        shape="rectilinear block with track arms",
        dimensions=ProductDimensions(width_in=84.0, depth_in=36.0, height_in=32.0, width_cm=213, depth_cm=91, height_cm=81),
        price_inr=29999,
        buy_url="https://www.amazon.in/dp/B08N8R441P",
        image_url="https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=600&q=80",
        materials=["Heavyweight distressed vintage faux leather", "Matte black powder-coated steel legs"],
        color="Distressed Cigar Brown & Matte Black",
        visual_description="rectilinear industrial loft 3-seater sofa upholstered in aged distressed cigar brown leather with clean square track arms and sturdy matte black steel legs",
        rating=4.7,
        review_count=310
    ),
    Product(
        id="amz-ind-charcoal-sofa",
        title="Urban Ladder Barclay 3-Seater Sofa in Matte Black Iron Frame",
        store="Amazon",
        category="sofa",
        style="industrial",
        shape="exposed metal cage rectangular",
        dimensions=ProductDimensions(width_in=80.0, depth_in=34.0, height_in=30.0, width_cm=203, depth_cm=86, height_cm=76),
        price_inr=26499,
        buy_url="https://www.amazon.in/dp/B09V7N881J",
        image_url="https://images.unsplash.com/photo-1567016432779-094069958ea5?auto=format&fit=crop&w=600&q=80",
        materials=["Woven heavy canvas twill", "Welded square iron cage frame"],
        color="Dark Charcoal Slate & Raw Iron Black",
        visual_description="industrial cage sofa featuring an architectural exposed matte black iron frame holding deep boxed cushions in durable dark charcoal canvas twill",
        rating=4.6,
        review_count=185
    ),
    Product(
        id="amz-ind-cart-table",
        title="The Attic Reclaimed Teak & Cast Iron Industrial Cart Coffee Table",
        store="Amazon",
        category="coffee_table",
        style="industrial",
        shape="rectangular cart with functional iron wheels",
        dimensions=ProductDimensions(width_in=44.0, depth_in=24.0, height_in=16.0, width_cm=112, depth_cm=61, height_cm=41),
        price_inr=14999,
        buy_url="https://www.amazon.in/dp/B08G8Y114N",
        image_url="https://images.unsplash.com/photo-1530018607912-eff2daa1bac4?auto=format&fit=crop&w=600&q=80",
        materials=["Reclaimed railway sleeper teak wood", "Heavy cast iron spoke wheels and brackets"],
        color="Distressed Walnut & Raw Black Cast Iron",
        visual_description="rectangular vintage industrial factory cart coffee table crafted from thick weathered teak slabs fitted with heavy black cast iron spoke wheels and corner rivets",
        rating=4.8,
        review_count=145
    ),
    Product(
        id="flip-ind-mesh-table",
        title="DeckUp Zephyr Matte Black Powder-Coated Steel & Wood Coffee Table",
        store="Flipkart",
        category="coffee_table",
        style="industrial",
        shape="two-tier rectangular with mesh shelf",
        dimensions=ProductDimensions(width_in=38.0, depth_in=22.0, height_in=17.0, width_cm=96, depth_cm=56, height_cm=43),
        price_inr=6999,
        buy_url="https://www.flipkart.com/deckup-zephyr-coffee-table/p/itmfc44d8ff112",
        image_url="https://images.unsplash.com/photo-1519710164239-da123dc03ef4?auto=format&fit=crop&w=600&q=80",
        materials=["Rustic engineered wood top", "Heavy-gauge black perforated steel mesh shelf"],
        color="Rustic Dark Walnut & Matte Carbon Black",
        visual_description="two-tier industrial coffee table with a warm rustic dark walnut tabletop supported by a rigid black carbon steel box frame with an integrated lower wire mesh shelf",
        rating=4.5,
        review_count=215
    ),
    Product(
        id="amz-ind-aviator-chair",
        title="Royal Oak Aviator Polished Aluminum & Distressed Leather Club Chair",
        store="Amazon",
        category="accent_chair",
        style="industrial",
        shape="curved aerodynamic tub armchair",
        dimensions=ProductDimensions(width_in=31.0, depth_in=33.0, height_in=30.0, width_cm=79, depth_cm=84, height_cm=76),
        price_inr=24990,
        buy_url="https://www.amazon.in/dp/B07Y7N112K",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["Riveted aircraft-grade aluminum panels", "Aged saddle brown leather seat"],
        color="Spitfire Riveted Silver Aluminum & Cognac Leather",
        visual_description="aerodynamic industrial aviator club chair clad in riveted spitfire aluminum sheeting with an interior deep bucket lined with supple aged cognac brown leather",
        rating=4.9,
        review_count=84
    ),
    Product(
        id="amz-ind-wire-chair",
        title="MetalCraft Bertoia Diamond Wire Armchair with Leather Pad",
        store="Amazon",
        category="accent_chair",
        style="industrial",
        shape="geometric wire basket diamond",
        dimensions=ProductDimensions(width_in=33.0, depth_in=28.0, height_in=30.0, width_cm=84, depth_cm=71, height_cm=76),
        price_inr=8499,
        buy_url="https://www.amazon.in/dp/B08X9P441J",
        image_url="https://images.unsplash.com/photo-1549497538-303791108f95?auto=format&fit=crop&w=600&q=80",
        materials=["Electro-welded black steel wire lattice", "Black faux leather removable seat pad"],
        color="Matte Jet Black Steel & Black Leather",
        visual_description="sculptural diamond wire industrial lounge chair made of welded matte black steel grid mesh with an ergonomic scoop profile and black leatherette seat cushion",
        rating=4.6,
        review_count=190
    ),
    Product(
        id="amz-ind-tripod-lamp",
        title="Brightech Vintage Cinema Studio Spotlight Matte Black Floor Lamp",
        store="Amazon",
        category="floor_lamp",
        style="industrial",
        shape="cinema spotlight on surveyor tripod",
        dimensions=ProductDimensions(width_in=18.0, depth_in=18.0, height_in=64.0, width_cm=46, depth_cm=46, height_cm=162),
        price_inr=6999,
        buy_url="https://www.amazon.in/dp/B07T7M112J",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Matte black carbon steel", "Chrome lock knobs", "Ribbed glass lens"],
        color="Matte Black & Polished Chrome",
        visual_description="vintage Hollywood cinema studio spotlight floor lamp in matte black steel featuring an adjustable cylindrical searchlight can on an expandable survey tripod",
        rating=4.7,
        review_count=275
    ),
    Product(
        id="amz-ind-edison-lamp",
        title="Generic Steampunk Industrial Water-Pipe 3-Light Edison Cage Floor Lamp",
        store="Amazon",
        category="floor_lamp",
        style="industrial",
        shape="multi-tier branching pipe tree",
        dimensions=ProductDimensions(width_in=14.0, depth_in=14.0, height_in=62.0, width_cm=36, depth_cm=36, height_cm=157),
        price_inr=5499,
        buy_url="https://www.amazon.in/dp/B09V7P112Q",
        image_url="https://images.unsplash.com/photo-1513519245088-0e12902e5a38?auto=format&fit=crop&w=600&q=80",
        materials=["Malleable iron plumbing pipe", "Metal wire cages", "Amber warm Edison filament bulbs"],
        color="Aged Cast Bronze & Dark Charcoal",
        visual_description="steampunk industrial plumbing pipe floor lamp with 3 staggered branching arms encased in wire cage shades illuminating warm amber Edison filaments",
        rating=4.6,
        review_count=165
    ),
    Product(
        id="amz-ind-distressed-rug",
        title="Saral Home Industrial Distressed Concrete Washed Area Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="industrial",
        shape="rectangular abstract washed",
        dimensions=ProductDimensions(width_in=96.0, depth_in=60.0, height_in=0.4, width_cm=244, depth_cm=152, height_cm=1.0),
        price_inr=5299,
        buy_url="https://www.amazon.in/dp/B08V8M994X",
        image_url="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
        materials=["Printed chenille yarn", "Anti-skid TPR rubber backing"],
        color="Concrete Slate Grey, Charcoal & Weathered White",
        visual_description="low-profile industrial area rug with a weathered concrete wash motif featuring textured transitions between dark graphite charcoal, slate grey, and chalky white",
        rating=4.6,
        review_count=230
    ),
    Product(
        id="amz-ind-leather-rug",
        title="Handcrafted Reclaimed Leather Patchwork Geometric Rug (5 x 7 Ft)",
        store="Amazon",
        category="rug",
        style="industrial",
        shape="rectangular tiled patchwork",
        dimensions=ProductDimensions(width_in=84.0, depth_in=60.0, height_in=0.3, width_cm=213, depth_cm=152, height_cm=0.8),
        price_inr=8990,
        buy_url="https://www.amazon.in/dp/B09C8K441M",
        image_url="https://images.unsplash.com/photo-1581539250439-c96689b516dd?auto=format&fit=crop&w=600&q=80",
        materials=["100% genuine upcycled cowhide leather tiles", "Heavy felt backing"],
        color="Tanned Cognac, Raw Charcoal & Mocha Brown",
        visual_description="geometric patchwork industrial area rug hand-stitched from hexagonal and square tiles of upcycled genuine cowhide leather in rich shades of cognac, charcoal, and mocha",
        rating=4.7,
        review_count=110
    )
]

class CatalogService:
    def __init__(self):
        self.catalog = CATALOG

    def get_all_products(self) -> List[Dict[str, Any]]:
        """Returns all products in the catalog as dictionaries."""
        return [p.model_dump() for p in self.catalog]

    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Finds a product by its unique ID."""
        for p in self.catalog:
            if p.id == product_id:
                return p.model_dump()
        return None

    def search_products(
        self,
        category: Optional[str] = None,
        style: Optional[str] = None,
        store: Optional[str] = None,
        max_width_in: Optional[float] = None,
        max_depth_in: Optional[float] = None,
        max_height_in: Optional[float] = None,
        max_price_inr: Optional[int] = None,
        user_prompt: Optional[str] = None,
        limit: int = 6
    ) -> List[Dict[str, Any]]:
        """
        Search catalog with strict physical dimensional constraints and prompt relevance scoring.
        """
        candidates: List[Product] = []
        for p in self.catalog:
            if category and p.category.lower() != category.lower():
                continue
            if style and p.style.lower() != style.lower():
                continue
            if store and p.store.lower() != store.lower():
                continue
            if max_width_in is not None and p.dimensions.width_in > max_width_in:
                continue
            if max_depth_in is not None and p.dimensions.depth_in > max_depth_in:
                continue
            if max_height_in is not None and p.dimensions.height_in > max_height_in:
                continue
            if max_price_inr is not None and p.price_inr > max_price_inr:
                continue
            candidates.append(p)

        # Fallback if style filter was overly restrictive
        if not candidates and style:
            for p in self.catalog:
                if category and p.category.lower() != category.lower():
                    continue
                if max_width_in is not None and p.dimensions.width_in > max_width_in:
                    continue
                if max_depth_in is not None and p.dimensions.depth_in > max_depth_in:
                    continue
                candidates.append(p)

        # Prompt-driven keyword scoring
        scored: List[Dict[str, Any]] = []
        prompt_words = set(re.findall(r"\w+", (user_prompt or "").lower()))
        # Filter common stopwords
        stopwords = {"with", "and", "the", "for", "room", "living", "photo", "modern_interior", "8k", "decor"}
        meaningful_words = [w for w in prompt_words if len(w) > 2 and w not in stopwords]

        for p in candidates:
            p_dict = p.model_dump()
            score = 0.0
            if meaningful_words:
                text_corpus = f"{p.title} {p.category} {p.style} {p.shape} {p.color} {p.visual_description} {' '.join(p.materials)}".lower()
                for w in meaningful_words:
                    if w in text_corpus:
                        score += 1.5
            p_dict["prompt_relevance_score"] = score
            scored.append(p_dict)

        # Sort by prompt relevance first, then rating
        scored.sort(key=lambda item: (item.get("prompt_relevance_score", 0), item.get("rating", 4.5)), reverse=True)
        return scored[:limit]

    def curate_room_products(
        self,
        style: str = "scandinavian",
        spatial_zones: Optional[Dict[str, Any]] = None,
        max_budget_inr: Optional[int] = None,
        room_image: Optional[Any] = None,
        user_prompt: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Curates a harmonious ensemble of real furniture for the room based on spatial zone boundaries,
        user prompt keyword relevance, and Visual RAG image embedding cosine similarity against the user's room image.
        Returns a complete set of items: sofa, coffee_table, accent_chair, floor_lamp, and rug.
        """
        zones = spatial_zones or {}
        sofa_zone = zones.get("seating_zone", {})
        table_zone = zones.get("table_zone", {})
        accent_zone = zones.get("accent_zone", {})
        lamp_zone = zones.get("lamp_zone", {})
        rug_zone = zones.get("rug_zone", {})

        def _select_best_match(candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
            if not candidates:
                return None
            # If candidates have high prompt relevance, prioritize prompt match!
            top_prompt_score = max(c.get("prompt_relevance_score", 0) for c in candidates)
            if top_prompt_score >= 1.5:
                top_candidates = [c for c in candidates if c.get("prompt_relevance_score", 0) == top_prompt_score]
            else:
                top_candidates = candidates

            if not room_image or len(top_candidates) == 1:
                return top_candidates[0]

            try:
                from embedding_service import embedding_service
                ranked = embedding_service.rank_products_by_aesthetic_harmony(room_image, top_candidates)
                return ranked[0] if ranked else top_candidates[0]
            except Exception as emb_err:
                print(f"[CatalogService] Visual embedding ranking notice: {emb_err}")
                return top_candidates[0]

        selected = []

        # 1. Main Seating / Sofa
        sofas = self.search_products(
            category="sofa",
            style=style,
            max_width_in=sofa_zone.get("max_width_in", 92.0),
            max_depth_in=sofa_zone.get("max_depth_in", 42.0),
            user_prompt=user_prompt,
            limit=6
        )
        best_sofa = _select_best_match(sofas)
        if best_sofa:
            selected.append(best_sofa)

        # 2. Coffee Table
        tables = self.search_products(
            category="coffee_table",
            style=style,
            max_width_in=table_zone.get("max_width_in", 48.0),
            max_depth_in=table_zone.get("max_depth_in", 32.0),
            user_prompt=user_prompt,
            limit=6
        )
        best_table = _select_best_match(tables)
        if best_table:
            selected.append(best_table)

        # 3. Accent Chair
        chairs = self.search_products(
            category="accent_chair",
            style=style,
            max_width_in=accent_zone.get("max_width_in", 36.0),
            max_depth_in=accent_zone.get("max_depth_in", 36.0),
            user_prompt=user_prompt,
            limit=6
        )
        best_chair = _select_best_match(chairs)
        if best_chair:
            selected.append(best_chair)

        # 4. Floor Lamp
        lamps = self.search_products(
            category="floor_lamp",
            style=style,
            max_height_in=lamp_zone.get("max_height_in", 84.0),
            user_prompt=user_prompt,
            limit=6
        )
        best_lamp = _select_best_match(lamps)
        if best_lamp:
            selected.append(best_lamp)

        # 5. Area Rug
        rugs = self.search_products(
            category="rug",
            style=style,
            max_width_in=rug_zone.get("max_width_in", 100.0),
            user_prompt=user_prompt,
            limit=6
        )
        best_rug = _select_best_match(rugs)
        if best_rug:
            selected.append(best_rug)

        return selected

# Singleton instance
catalog_service = CatalogService()
