from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdateRole
from fastapi import HTTPException


def create_user(db: Session, user_data: UserCreate):
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,  # Hash the password in production!
        role=user_data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_role(db: Session, user_id: str, role_data: UserUpdateRole):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role_data.role
    db.commit()
    db.refresh(user)
    return user


def get_users(db: Session):
    return db.query(User).all()