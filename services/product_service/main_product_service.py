from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest
from fastapi.responses import Response
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}


Instrumentator().instrument(app).expose(app)

products = {}
product_id = 1

class Product(BaseModel):
    name: str
    description: str | None = None
    price: float | None = None   

@app.get("/products")
def get_products():
    return list(products.values())

@app.post("/products")
def add_product(product: Product):
    global product_id

    prod = {
        "id": product_id,
        "name": product.name,
        "description": product.description,
        "price": product.price   
    }

    products[product_id] = prod
    product_id += 1

    return prod

@app.get("/products/{pid}")
def get_product(pid: int):
    return products.get(pid, {"error": "not found"})
