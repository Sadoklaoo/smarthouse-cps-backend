from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdateRole, UserResponse
from app.services.user_service import create_user, update_user_role, get_users
from app.core.database import get_db
from typing import List

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)


@router.put("/{user_id}/role", response_model=UserResponse)
def change_user_role(user_id: str, role_data: UserUpdateRole, db: Session = Depends(get_db)):
    return update_user_role(db, user_id, role_data)


@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)