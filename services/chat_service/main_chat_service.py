from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
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

comments = {}

@app.get("/")
def root():
    return {"status": "chat ok"}

@app.post("/comment")
def add_comment(c: dict):
    product_id = c.get("product_id")

    if product_id is None:
        return {"error": "product_id required"}

    comments.setdefault(product_id, []).append({
        "product_id": product_id,
        "user": c.get("user", "anon"),
        "text": c.get("text", "")
    })

    return {"status": "added", "comments": comments[product_id]}


@app.get("/comment/{product_id}")
def get_comments(product_id: int):
    return comments.get(product_id, [])


