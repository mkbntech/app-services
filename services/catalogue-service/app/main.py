"""
TrailHead Supply Co. — Product Catalogue Service
Stack: Python 3.12 + FastAPI

Owns product data. In a real deployment this would sit in front of
Postgres/Cosmos DB; here it serves an in-memory catalogue so the
service is dependency-free and starts instantly.
"""
import logging
import os
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.data import get_all_products, get_product, get_by_category

SERVICE_NAME = "catalogue-service"
VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(SERVICE_NAME)

app = FastAPI(title="TrailHead Catalogue Service", version=VERSION)

from prometheus_fastapi_instrumentator import Instrumentator

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

START_TIME = time.time()


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": SERVICE_NAME,
        "version": VERSION,
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }


@app.get("/api/products")
def list_products(category: str | None = None):
    if category:
        return {"items": get_by_category(category)}
    return {"items": get_all_products()}


@app.get("/api/products/{product_id}")
def product_detail(product_id: str):
    product = get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"product '{product_id}' not found")
    return product


@app.get("/api/categories")
def categories():
    cats = sorted({p["category"] for p in get_all_products()})
    return {"items": cats}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
