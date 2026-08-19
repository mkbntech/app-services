"""Seed product data for TrailHead Supply Co.

In a real enterprise this would live in Postgres / Cosmos DB. For this
reference platform we keep an in-memory catalogue so the service has
zero external dependencies and starts instantly in any environment.
"""

PRODUCTS = [
    {
        "id": "th-001",
        "name": "Contour 55 Backpack",
        "category": "packs",
        "price": 189.00,
        "currency": "USD",
        "description": "A 55L top-loader with a mapped-out compartment system, "
                        "built for multi-day ridge routes.",
        "image": "/img/pack.jpg",
        "tags": ["multi-day", "hiking", "ventilated"],
    },
    {
        "id": "th-002",
        "name": "Switchback Trail Boots",
        "category": "footwear",
        "price": 145.00,
        "currency": "USD",
        "description": "Waterproof leather boots with a lugged sole for loose "
                        "scree and switchback descents.",
        "image": "/img/boots.jpg",
        "tags": ["waterproof", "hiking", "boots"],
    },
    {
        "id": "th-003",
        "name": "Basecamp 2P Tent",
        "category": "shelter",
        "price": 279.00,
        "currency": "USD",
        "description": "A freestanding 2-person tent that pitches in under "
                        "three minutes, tested to 40mph ridgeline gusts.",
        "image": "/img/tent.jpg",
        "tags": ["camping", "freestanding", "3-season"],
    },
    {
        "id": "th-004",
        "name": "Ridge Line Softshell",
        "category": "apparel",
        "price": 129.00,
        "currency": "USD",
        "description": "A wind-resistant softshell with pit zips for the "
                        "climb and a packable hood for the summit.",
        "image": "/img/jacket.jpg",
        "tags": ["softshell", "layering"],
    },
    {
        "id": "th-005",
        "name": "Compass Rose Cookset",
        "category": "cookware",
        "price": 65.00,
        "currency": "USD",
        "description": "Anodized aluminum cookset that nests down to the size "
                        "of a 1L bottle, includes a folding handle.",
        "image": "/img/cookset.jpg",
        "tags": ["ultralight", "camping"],
    },
    {
        "id": "th-006",
        "name": "Summit Trekking Poles",
        "category": "gear",
        "price": 89.00,
        "currency": "USD",
        "description": "Carbon-fiber poles with cork grips and quick-flip "
                        "locks for fast elevation changes.",
        "image": "/img/poles.jpg",
        "tags": ["carbon", "trekking"],
    },
    {
        "id": "th-007",
        "name": "Alpine Down Quilt",
        "category": "shelter",
        "price": 219.00,
        "currency": "USD",
        "description": "800-fill down quilt rated to 20F, cinches into a "
                        "stuff sack the size of a loaf of bread.",
        "image": "/img/quilt.jpg",
        "tags": ["down", "3-season", "ultralight"],
    },
    {
        "id": "th-008",
        "name": "Traverse Hiking Shorts",
        "category": "apparel",
        "price": 59.00,
        "currency": "USD",
        "description": "Quick-dry ripstop shorts with a gusseted crotch for "
                        "the full stride of a scramble.",
        "image": "/img/shorts.jpg",
        "tags": ["quick-dry", "layering"],
    },
    {
        "id": "th-009",
        "name": "Solstice Solar Charger",
        "category": "gear",
        "price": 49.00,
        "currency": "USD",
        "description": "A rugged, water-resistant folding solar panel with dual smart USB outputs for charging at camp.",
        "image": "/img/charger.jpg",
        "tags": ["solar", "charging", "waterproof"],
    },
    {
        "id": "th-010",
        "name": "Glacier Fleece Pullover",
        "category": "apparel",
        "price": 79.00,
        "currency": "USD",
        "description": "An ultra-soft high-loft grid fleece pullover that locks in heat as a mid-layer or stand-alone piece.",
        "image": "/img/fleece.jpg",
        "tags": ["fleece", "warm", "layering"],
    },
    {
        "id": "th-011",
        "name": "Trailhead Titanium Mug",
        "category": "cookware",
        "price": 29.00,
        "currency": "USD",
        "description": "An ultralight, single-walled titanium mug with folding butterfly handles to save pack space.",
        "image": "/img/mug.jpg",
        "tags": ["titanium", "ultralight", "cookware"],
    },
]


def get_all_products():
    return PRODUCTS


def get_product(product_id: str):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def get_by_category(category: str):
    return [p for p in PRODUCTS if p["category"] == category]
