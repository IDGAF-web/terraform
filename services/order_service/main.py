from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orders = []

@app.get("/")
def root():
    return {"status": "order running"}

@app.post("/orders")
def create_order(order: dict):
    orders.append(order)
    return {"status": "created", "orders": orders}

@app.get("/orders")
def get_orders():
    return orders


# ✅ FIX: METRICS
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)