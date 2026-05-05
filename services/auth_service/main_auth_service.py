from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import generate_latest
from fastapi.responses import Response
import jwt
import datetime
from fastapi.middleware.cors import CORSMiddleware
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

SECRET = "secret"

fake_users = {}




class User(BaseModel):
    email: str
    password: str

@app.post("/register")
def register(user: User):
    if user.email in fake_users:
        return {"error": "user exists"}

    fake_users[user.email] = user.password
    return {"status": "registered"}

@app.post("/login")
def login(user: User):
    if fake_users.get(user.email) != user.password:
        return {"error": "invalid credentials"}

    token = jwt.encode({
        "sub": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET, algorithm="HS256")

    return {"access_token": token}

