from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdateRole, UserResponse, UserRole  # Import UserRole
from app.services.user_service import create_user, update_user_role, get_users
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password
from app.models.user import User
from sqlalchemy.future import select

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user_data)  # Await the create_user function


@router.put("/{user_id}/role", response_model=UserResponse)
def change_user_role(user_id: str, role_data: UserUpdateRole, db: Session = Depends(get_db)):
    return update_user_role(db, user_id, role_data)


@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_role(UserRole.ADMIN))])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()  # Get the first result or None

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}