from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from auth.dependencies import get_current_user
from auth.jwt_utils import create_access_token
from auth.password_utils import hash_password, verify_password
from database import crud
from database.db import get_db

router = APIRouter()

async def _read_credentials(request: Request) -> tuple[str, str]:
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" not in content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content-Type must be application/json.",
        )

    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON body.",
        ) from exc

    username = str(payload.get("username", "")).strip() if isinstance(payload, dict) else ""
    password = str(payload.get("password", "")) if isinstance(payload, dict) else ""

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required.",
        )

    return username, password


@router.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    username, password = await _read_credentials(request)

    if len(username) < 3 or len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be at least 3 characters and password at least 8 characters.",
        )

    existing_user = crud.get_user(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    created_user = crud.create_user(
        db,
        username=username,
        password=hash_password(password),
    )
    token = create_access_token({"sub": created_user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": created_user.id,
            "username": created_user.username,
        },
    }


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    username, password = await _read_credentials(request)
    db_user = crud.get_user(db, username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": db_user.username})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
        },
    }


@router.get("/me")
def me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
    }
