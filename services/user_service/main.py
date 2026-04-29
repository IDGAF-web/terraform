from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import jwt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET = "secret"

# 🧠 fake DB
users_db = {}

class ProfileUpdate(BaseModel):
    email: str | None = None
    password: str | None = None


def get_user(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data["sub"]
    except:
        raise HTTPException(401, "invalid token")


# GET PROFILE
@app.get("/me")
def me(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401)

    user = get_user(authorization.replace("Bearer ", ""))

    return users_db.get(user, {"email": user})


# UPDATE PROFILE
@app.put("/me")
def update_profile(
    body: ProfileUpdate,
    authorization: str = Header(None)
):
    user = get_user(authorization.replace("Bearer ", ""))

    profile = users_db.get(user, {"email": user})

    if body.email:
        profile["email"] = body.email
    if body.password:
        profile["password"] = body.password

    users_db[user] = profile

    return {"status": "updated", "profile": profile}


# DELETE PROFILE
@app.delete("/me")
def delete_profile(authorization: str = Header(None)):
    user = get_user(authorization.replace("Bearer ", ""))

    if user in users_db:
        del users_db[user]

    return {"status": "deleted"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)