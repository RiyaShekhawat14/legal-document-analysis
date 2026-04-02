from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth.passward_utils import hash_password, verify_password
from auth.jwt_utils import create_access_token

router = APIRouter()

users_db = {}

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)
    users_db[user.username] = hashed

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin):
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="User not found")

    hashed_password = users_db[user.username]

    if not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }