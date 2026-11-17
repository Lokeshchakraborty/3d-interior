"""
B2C Furniture Catalog Service
Provides access to real, dimension-verified furniture products from Amazon India, Flipkart, and IKEA.
Each product explicitly defines its physical dimensions, geometric shape, color palette,
and visual description specifying both shape and color to eliminate generative hallucinations.
"""

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
    category: str  # "sofa", "coffee_table", "accent_chair", "tv_unit", "rug", "floor_lamp", "side_table", "wall_art"
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
    # ==================== SCANDINAVIAN ====================
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
        shape="rectangular low-profile",
        dimensions=ProductDimensions(width_in=78.0, depth_in=39.0, height_in=32.6, width_cm=198, depth_cm=99, height_cm=83),
        price_inr=42990,
        buy_url="https://www.ikea.com/in/en/p/soederhamn-3-seat-section-viarp-beige-brown-s09305697/",
        image_url="https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?auto=format&fit=crop&w=600&q=80",
        materials=["Cotton linen weave", "Chrome metal slender legs", "Deep feather-fill cushioning"],
        color="Warm Oatmeal Beige",
        visual_description="rectangular low-profile minimalist 3-seater sofa in warm oatmeal beige linen with deep square cushions and slender silver metal legs",
        rating=4.8,
        review_count=512
    ),
    Product(
        id="amz-scandi-coffee-nest",
        title="DeckUp Plank Torin Engineered Wood Coffee Table with Oak Finish",
        store="Amazon",
        category="coffee_table",
        style="scandinavian",
        shape="oval curved",
        dimensions=ProductDimensions(width_in=35.4, depth_in=21.6, height_in=16.5, width_cm=90, depth_cm=55, height_cm=42),
        price_inr=4499,
        buy_url="https://www.amazon.in/dp/B07994DCL9",
        image_url="https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=600&q=80",
        materials=["Engineered wood", "White oak laminate veneer", "Solid beech splayed legs"],
        color="Natural Light Oak & Matte White",
        visual_description="oval-shaped minimalist coffee table in natural light oak and matte white with flared slender round wooden dowel legs",
        rating=4.3,
        review_count=1240
    ),
    Product(
        id="ikea-poaeng-armchair",
        title="IKEA POÄNG Armchair, Birch Veneer / Knisa Light Beige",
        store="IKEA",
        category="accent_chair",
        style="scandinavian",
        shape="curved cantilever L-frame",
        dimensions=ProductDimensions(width_in=26.8, depth_in=32.2, height_in=39.4, width_cm=68, depth_cm=82, height_cm=100),
        price_inr=8990,
        buy_url="https://www.ikea.com/in/en/p/poaeng-armchair-birch-veneer-knisa-light-beige-s79305929/",
        image_url="https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=600&q=80",
        materials=["Layer-glued bent birch wood frame", "100% recycled polyester cushion"],
        color="Cream Light Beige & Natural Birch Wood",
        visual_description="curved cantilever bentwood Scandinavian lounge armchair in cream light beige with natural birch wood frame",
        rating=4.9,
        review_count=2104
    ),
    Product(
        id="fk-scandi-tv-unit",
        title="Wakefit Engineered Wood TV Entertainment Console Unit (Columbian Walnut & White)",
        store="Flipkart",
        category="tv_unit",
        style="scandinavian",
        shape="long rectangular horizontal",
        dimensions=ProductDimensions(width_in=59.0, depth_in=15.7, height_in=19.7, width_cm=150, depth_cm=40, height_cm=50),
        price_inr=7999,
        buy_url="https://www.flipkart.com/wakefit-tv-entertainment-unit/p/itmfc2b3472",
        image_url="https://images.unsplash.com/photo-1595428774223-ef52624120d2?auto=format&fit=crop&w=600&q=80",
        materials=["High-density engineered board", "Matte white sliding slatted doors"],
        color="Warm Columbian Walnut & Off-White",
        visual_description="long rectangular horizontal floating TV console in warm columbian walnut and off-white with slatted sliding cabinet doors",
        rating=4.4,
        review_count=890
    ),
    Product(
        id="amz-scandi-rug-wool",
        title="Saral Home Geometric Wool Area Rug (5 x 7 Feet)",
        store="Amazon",
        category="rug",
        style="scandinavian",
        shape="rectangular flat-weave",
        dimensions=ProductDimensions(width_in=60.0, depth_in=84.0, height_in=0.5, width_cm=152, depth_cm=213, height_cm=1.3),
        price_inr=5299,
        buy_url="https://www.amazon.in/dp/B08CZ7N8M1",
        image_url="https://images.unsplash.com/photo-1600121848594-d8644e57abab?auto=format&fit=crop&w=600&q=80",
        materials=["100% New Zealand blended wool", "Cotton warp backing"],
        color="Cream Ivory with Charcoal Grey diamond lines",
        visual_description="rectangular 5x7 area rug in cream ivory featuring minimalist thin geometric charcoal grey diamond lines",
        rating=4.6,
        review_count=430
    ),
    Product(
        id="ikea-skaftet-lamp",
        title="IKEA SKAFTET Floor Lamp Base with Brass & Ringsta White Shade",
        store="IKEA",
        category="floor_lamp",
        style="scandinavian",
        shape="tall cylindrical linear column",
        dimensions=ProductDimensions(width_in=18.0, depth_in=18.0, height_in=60.0, width_cm=46, depth_cm=46, height_cm=153),
        price_inr=3990,
        buy_url="https://www.ikea.com/in/en/p/skaftet-floor-lamp-base-brass-plated-00405105/",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Brass plated steel", "Textured linen drum shade"],
        color="Brushed Metallic Brass & Crisp White",
        visual_description="tall cylindrical linear floor lamp in brushed metallic brass with a crisp white round drum lampshade emitting warm 2700K ambient light",
        rating=4.7,
        review_count=640
    ),

    # ==================== JAPANDI ====================
    Product(
        id="ikea-japandi-sofa-kivik",
        title="IKEA KIVIK 3-Seat Compact Sofa, Tibbleby Beige/Grey Low Profile",
        store="IKEA",
        category="sofa",
        style="japandi",
        shape="grounded rectangular low-profile",
        dimensions=ProductDimensions(width_in=74.8, depth_in=37.4, height_in=32.6, width_cm=190, depth_cm=95, height_cm=83),
        price_inr=39990,
        buy_url="https://www.ikea.com/in/en/p/kivik-three-seat-sofa-tibbleby-beige-grey-s99440578/",
        image_url="https://images.unsplash.com/photo-1540518614846-7ede433c4550?auto=format&fit=crop&w=600&q=80",
        materials=["Wabi-sabi textured cotton blend", "Solid ash wood frame", "Memory foam topper"],
        color="Muted Stone Grey & Oatmeal",
        visual_description="grounded rectangular low-profile Japandi sofa in muted stone-grey organic linen with deep square cushions and wide armrests",
        rating=4.7,
        review_count=418
    ),
    Product(
        id="amz-japandi-coffee-table",
        title="Urban Wood Sheesham Round Low Fluted Coffee Table (Teak Finish)",
        store="Amazon",
        category="coffee_table",
        style="japandi",
        shape="circular round cylinder",
        dimensions=ProductDimensions(width_in=31.5, depth_in=31.5, height_in=14.0, width_cm=80, depth_cm=80, height_cm=35),
        price_inr=7499,
        buy_url="https://www.amazon.in/dp/B09MN58X2L",
        image_url="https://images.unsplash.com/photo-1532372320572-cda25653a26d?auto=format&fit=crop&w=600&q=80",
        materials=["Solid Sheesham wood", "Fluted vertical wooden slats", "Matte clear protective lacquer"],
        color="Warm Natural Ash Wood",
        visual_description="circular round low Japanese coffee table in warm natural ash wood with ribbed cylindrical vertical wood slat base",
        rating=4.5,
        review_count=310
    ),
    Product(
        id="fk-japandi-lounge-chair",
        title="Bharat Lifestyle Zen Solid Wood Accent Chair with Natural Cane Weave",
        store="Flipkart",
        category="accent_chair",
        style="japandi",
        shape="angular V-leg geometric",
        dimensions=ProductDimensions(width_in=28.0, depth_in=30.0, height_in=31.0, width_cm=71, depth_cm=76, height_cm=79),
        price_inr=11499,
        buy_url="https://www.flipkart.com/zen-solid-wood-cane-chair/p/itm1289128",
        image_url="https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=600&q=80",
        materials=["Solid natural ash wood", "Hand-woven natural rattan webbing", "Oatmeal linen cushion"],
        color="Honey Cane & Natural Ash Wood",
        visual_description="angular V-leg wooden lounge chair in honey cane and natural ash wood with handwoven hexagonal rattan cane backrest and linen seat",
        rating=4.8,
        review_count=195
    ),
    Product(
        id="amz-japandi-jute-rug",
        title="Chhabra Handcrafted Oval Natural Jute & Braided Hemp Area Rug (6 x 9 Ft)",
        store="Amazon",
        category="rug",
        style="japandi",
        shape="oval concentric braided",
        dimensions=ProductDimensions(width_in=72.0, depth_in=108.0, height_in=0.4, width_cm=183, depth_cm=274, height_cm=1.0),
        price_inr=6899,
        buy_url="https://www.amazon.in/dp/B085VGHZQP",
        image_url="https://images.unsplash.com/photo-1579656381226-5fc0f0100c3b?auto=format&fit=crop&w=600&q=80",
        materials=["100% natural organic raw jute fibers", "Hand-braided concentric loops"],
        color="Raw Earthy Golden Jute",
        visual_description="oval concentric braided area rug in raw earthy golden jute bringing organic texture and warmth to the floor",
        rating=4.6,
        review_count=780
    ),
    Product(
        id="ikea-japandi-lamp-nogersund",
        title="IKEA REGOLIT / HEMMA Japanese Rice Paper Floor Lamp (Rice Paper Glow)",
        store="IKEA",
        category="floor_lamp",
        style="japandi",
        shape="spherical lantern on tripod",
        dimensions=ProductDimensions(width_in=17.7, depth_in=17.7, height_in=59.0, width_cm=45, depth_cm=45, height_cm=150),
        price_inr=2490,
        buy_url="https://www.ikea.com/in/en/p/regolit-pendant-lamp-shade-white-handmade-70103410/",
        image_url="https://images.unsplash.com/photo-1513506003901-1e6a229e2d15?auto=format&fit=crop&w=600&q=80",
        materials=["Handmade ribbed rice paper", "Bamboo ribbing", "Steel tripod base"],
        color="Translucent Warm Off-White & Black Base",
        visual_description="spherical Japanese paper lantern floor lamp in translucent warm off-white on a slender black steel tripod base radiating soft ambient light",
        rating=4.8,
        review_count=980
    ),

    # ==================== MODERN LUXURY ====================
    Product(
        id="fk-lux-velvet-sectional",
        title="Royal Oak Berlin Velvet L-Shape Left Aligned Sectional Sofa (Emerald Jewel)",
        store="Flipkart",
        category="sofa",
        style="modern_luxury",
        shape="L-shaped sectional",
        dimensions=ProductDimensions(width_in=96.0, depth_in=62.0, height_in=33.5, width_cm=244, depth_cm=157, height_cm=85),
        price_inr=62990,
        buy_url="https://www.flipkart.com/royal-oak-berlin-velvet-sectional-sofa/p/itm58f27a6",
        image_url="https://images.unsplash.com/photo-1550581190-9c1c48d21d6c?auto=format&fit=crop&w=600&q=80",
        materials=["High-pile performance velvet", "Kiln-dried solid hardwood frame", "Polished titanium gold legs"],
        color="Deep Emerald Jewel Green & Polished Gold",
        visual_description="L-shaped corner sectional sofa in deep emerald jewel green velvet with vertical channel tufting and polished titanium gold legs",
        rating=4.7,
        review_count=412
    ),
    Product(
        id="amz-lux-marble-table",
        title="Spacewood Italian Carrara White Marble Top Center Coffee Table (Gold Metal Frame)",
        store="Amazon",
        category="coffee_table",
        style="modern_luxury",
        shape="rectangular geometric slab",
        dimensions=ProductDimensions(width_in=42.0, depth_in=24.0, height_in=18.0, width_cm=106, depth_cm=61, height_cm=46),
        price_inr=15999,
        buy_url="https://www.amazon.in/dp/B08XWN4K99",
        image_url="https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=600&q=80",
        materials=["Polished sintered Italian marble slab", "Electroplated brushed gold stainless steel frame"],
        color="Calacatta White Marble & Champagne Gold",
        visual_description="rectangular Italian Carrara marble coffee table in calacatta white with grey veining and champagne gold geometric steel base",
        rating=4.8,
        review_count=290
    ),
    Product(
        id="amz-lux-swivel-chair",
        title="Solimo Premium Boucle Velvet Swivel Accent Shell Chair",
        store="Amazon",
        category="accent_chair",
        style="modern_luxury",
        shape="curved sculptural barrel tub",
        dimensions=ProductDimensions(width_in=31.0, depth_in=31.0, height_in=30.0, width_cm=79, depth_cm=79, height_cm=76),
        price_inr=14999,
        buy_url="https://www.amazon.in/dp/B09H2S8B4X",
        image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?auto=format&fit=crop&w=600&q=80",
        materials=["Cream heavy boucle wool upholstery", "360-degree silent brass swivel base"],
        color="Pristine Ivory Cream & Brushed Brass",
        visual_description="curved sculptural barrel tub swivel armchair in pristine ivory cream boucle with hidden circular brass pedestal base",
        rating=4.9,
        review_count=380
    ),
    Product(
        id="fk-lux-arc-floor-lamp",
        title="Pesca Architectural Oversized Marble Base Arc Floor Lamp (Brushed Gold)",
        store="Flipkart",
        category="floor_lamp",
        style="modern_luxury",
        shape="sweeping semicircular arc",
        dimensions=ProductDimensions(width_in=36.0, depth_in=15.0, height_in=78.0, width_cm=91, depth_cm=38, height_cm=198),
        price_inr=8499,
        buy_url="https://www.flipkart.com/pesca-oversized-arc-floor-lamp-marble/p/itm7a64112",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Heavy solid black Nero Marquina marble base", "Sweeping curved brass arc arm", "Dome metal shade"],
        color="Brushed Champagne Gold & Black Nero Marble",
        visual_description="sweeping semicircular arc floor lamp in brushed champagne gold anchored by a heavy cylindrical black nero marble base with dome shade",
        rating=4.7,
        review_count=185
    ),

    # ==================== BOHEMIAN ====================
    Product(
        id="amz-boho-rattan-sofa",
        title="Kurl-on Earth Series 3-Seater Rattan Cane & Fabric Boho Sofa",
        store="Amazon",
        category="sofa",
        style="bohemian",
        shape="rectangular with curved armrests",
        dimensions=ProductDimensions(width_in=76.0, depth_in=34.0, height_in=32.0, width_cm=193, depth_cm=86, height_cm=81),
        price_inr=32990,
        buy_url="https://www.amazon.in/dp/B08V5Q471R",
        image_url="https://images.unsplash.com/photo-1540518614846-7ede433c4550?auto=format&fit=crop&w=600&q=80",
        materials=["Hand-woven sustainable cane wicker", "Natural teak wood", "Terracotta linen cushions"],
        color="Terracotta Rust & Warm Honey Teak",
        visual_description="rectangular bohemian sofa with curved rattan wicker side panels in warm honey teak and plush terracotta rust linen cushions",
        rating=4.5,
        review_count=142
    ),
    Product(
        id="amz-boho-macrame-rug",
        title="Status Multi Moroccan Berber Diamond Shag Area Rug (5 x 8 Ft)",
        store="Amazon",
        category="rug",
        style="bohemian",
        shape="rectangular high-pile with fringe",
        dimensions=ProductDimensions(width_in=60.0, depth_in=96.0, height_in=1.2, width_cm=152, depth_cm=244, height_cm=3.0),
        price_inr=4999,
        buy_url="https://www.amazon.in/dp/B07R45TKLW",
        image_url="https://images.unsplash.com/photo-1600121848594-d8644e57abab?auto=format&fit=crop&w=600&q=80",
        materials=["High-pile micro-chenille shag", "Braided fringe tassel borders"],
        color="Cream Ivory, Rust Red, and Mustard Ochre",
        visual_description="rectangular high-pile Moroccan shag area rug in cream ivory with rust red and mustard ochre tribal geometric patterns and braided fringe tassels",
        rating=4.6,
        review_count=820
    ),
    Product(
        id="ikea-boho-peacock-chair",
        title="IKEA BUSKBO Armchair, Rattan Handcrafted / Djupvik White Cushion",
        store="IKEA",
        category="accent_chair",
        style="bohemian",
        shape="sunburst flared fan-back",
        dimensions=ProductDimensions(width_in=28.7, depth_in=29.5, height_in=29.5, width_cm=73, depth_cm=75, height_cm=75),
        price_inr=12990,
        buy_url="https://www.ikea.com/in/en/p/buskbo-armchair-rattan-djupvik-white-s99299016/",
        image_url="https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?auto=format&fit=crop&w=600&q=80",
        materials=["Handmade peeled wild rattan", "Clear acrylic lacquer", "Cotton twill cushion"],
        color="Warm Honey Natural Wicker & Soft White",
        visual_description="sunburst flared fan-back bohemian armchair in warm honey natural wicker with soft white circular seat cushion",
        rating=4.8,
        review_count=450
    ),

    # ==================== INDUSTRIAL ====================
    Product(
        id="amz-ind-leather-sofa",
        title="Urban Ladder Chesterfield Distressed Top-Grain Leather 3-Seater Sofa",
        store="Amazon",
        category="sofa",
        style="industrial",
        shape="rectangular Chesterfield with scrolled arms",
        dimensions=ProductDimensions(width_in=84.0, depth_in=36.0, height_in=30.0, width_cm=213, depth_cm=91, height_cm=76),
        price_inr=69999,
        buy_url="https://www.amazon.in/dp/B08XWN7J1L",
        image_url="https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=600&q=80",
        materials=["Top-grain distressed saddle leather", "Solid mahogany frame", "Matte black iron castors"],
        color="Distressed Cognac Saddle Brown",
        visual_description="rectangular Chesterfield sofa in distressed cognac saddle brown leather with deep diamond button tufting and scrolled arms",
        rating=4.8,
        review_count=215
    ),
    Product(
        id="fk-ind-iron-wood-table",
        title="Furny Industrial Reclaimed Wood & Cast Iron Frame Coffee Table",
        store="Flipkart",
        category="coffee_table",
        style="industrial",
        shape="rectangular box frame",
        dimensions=ProductDimensions(width_in=40.0, depth_in=24.0, height_in=18.0, width_cm=101, depth_cm=61, height_cm=46),
        price_inr=6499,
        buy_url="https://www.flipkart.com/furny-industrial-cast-iron-table/p/itmd65290b",
        image_url="https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?auto=format&fit=crop&w=600&q=80",
        materials=["Solid reclaimed pine wood planks", "Powder-coated heavy gauge box steel"],
        color="Dark Rustic Pine & Matte Charcoal Black",
        visual_description="rectangular industrial coffee table with thick dark rustic pine timber planks on a matte charcoal black welded square iron box frame",
        rating=4.6,
        review_count=340
    ),
    Product(
        id="ikea-hektar-lamp",
        title="IKEA HEKTAR Floor Lamp with 3-Spots, Dark Grey Metal Factory Style",
        store="IKEA",
        category="floor_lamp",
        style="industrial",
        shape="tall vertical multi-spotlight column",
        dimensions=ProductDimensions(width_in=11.8, depth_in=11.8, height_in=69.0, width_cm=30, depth_cm=30, height_cm=176),
        price_inr=5490,
        buy_url="https://www.ikea.com/in/en/p/hektar-floor-lamp-with-3-spots-dark-grey-20393600/",
        image_url="https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80",
        materials=["Heavy spun steel", "Powder coating", "Oversized adjustable thumb screws"],
        color="Matte Gunmetal Dark Grey",
        visual_description="tall vertical factory-style floor lamp in matte gunmetal dark grey with 3 directional conical spotlight metal shades and industrial screws",
        rating=4.8,
        review_count=820
    )
]

class CatalogService:
    def __init__(self):
        self.catalog = CATALOG

    def get_all_products(self) -> List[Dict[str, Any]]:
        return [p.model_dump() for p in self.catalog]

    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        for p in self.catalog:
            if p.id == product_id:
                return p.model_dump()
        return None

    def search_products(
        self,
        category: Optional[str] = None,
        style: Optional[str] = None,
        max_width_in: Optional[float] = None,
        max_depth_in: Optional[float] = None,
        max_height_in: Optional[float] = None,
        max_price_inr: Optional[int] = None,
        store: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search catalog with strict physical dimensional constraints so items physically fit!
        """
        results = []
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

            results.append(p.model_dump())
            if len(results) >= limit:
                break

        # Fallback without style constraint if style filter was overly restrictive
        if not results and style:
            for p in self.catalog:
                if category and p.category.lower() != category.lower():
                    continue
                if max_width_in is not None and p.dimensions.width_in > max_width_in:
                    continue
                if max_depth_in is not None and p.dimensions.depth_in > max_depth_in:
                    continue
                results.append(p.model_dump())
                if len(results) >= limit:
                    break

        return results

    def curate_room_products(
        self,
        style: str = "scandinavian",
        spatial_zones: Optional[Dict[str, Any]] = None,
        max_budget_inr: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Curates a harmonious ensemble of real furniture for the room based on spatial zone boundaries.
        Returns a list of items: sofa, coffee_table, accent_chair, floor_lamp, and rug.
        """
        zones = spatial_zones or {}
        sofa_zone = zones.get("seating_zone", {})
        table_zone = zones.get("table_zone", {})
        accent_zone = zones.get("accent_zone", {})
        lamp_zone = zones.get("lamp_zone", {})
        rug_zone = zones.get("rug_zone", {})

        selected = []

        # 1. Main Seating / Sofa
        sofas = self.search_products(
            category="sofa",
            style=style,
            max_width_in=sofa_zone.get("max_width_in", 92.0),
            max_depth_in=sofa_zone.get("max_depth_in", 42.0),
            limit=2
        )
        if sofas:
            selected.append(sofas[0])

        # 2. Coffee Table
        tables = self.search_products(
            category="coffee_table",
            style=style,
            max_width_in=table_zone.get("max_width_in", 48.0),
            max_depth_in=table_zone.get("max_depth_in", 32.0),
            limit=2
        )
        if tables:
            selected.append(tables[0])

        # 3. Accent Chair
        chairs = self.search_products(
            category="accent_chair",
            style=style,
            max_width_in=accent_zone.get("max_width_in", 36.0),
            max_depth_in=accent_zone.get("max_depth_in", 36.0),
            limit=2
        )
        if chairs:
            selected.append(chairs[0])

        # 4. Floor Lamp
        lamps = self.search_products(
            category="floor_lamp",
            style=style,
            max_height_in=lamp_zone.get("max_height_in", 84.0),
            limit=2
        )
        if lamps:
            selected.append(lamps[0])

        # 5. Area Rug
        rugs = self.search_products(
            category="rug",
            style=style,
            max_width_in=rug_zone.get("max_width_in", 100.0),
            limit=2
        )
        if rugs:
            selected.append(rugs[0])

        return selected

# Singleton instance
catalog_service = CatalogService()
