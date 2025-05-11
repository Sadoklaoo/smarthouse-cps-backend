# Example of role-based access control

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import require_roles, get_current_active_user
from app.models.user import User, UserRole

router = APIRouter()

@router.get("/admin-only")
async def admin_only_route(current_user: User = Depends(require_roles(["admin"]))):
    """
    This route can only be accessed by users with the admin role.
    """
    return {"message": f"Welcome admin user: {current_user.email}"}

@router.get("/users-and-admins")
async def users_and_admins_route(current_user: User = Depends(require_roles(["admin", "user"]))):
    """
    This route can be accessed by users with either admin or user roles.
    """
    return {"message": f"Welcome user: {current_user.email}"}

@router.get("/all-authenticated")
async def all_authenticated_route(current_user: User = Depends(get_current_active_user)):
    """
    This route can be accessed by any authenticated user.
    """
    return {"message": f"Welcome: {current_user.email}"}

@router.get("/role-info")
async def get_role_info(current_user: User = Depends(get_current_active_user)):
    """
    Returns user's role information.
    """
    return {
        "user": current_user.email,
        "roles": [role.value for role in current_user.roles],
        "is_admin": UserRole.ADMIN in current_user.roles,
        "is_user": UserRole.USER in current_user.roles,
        "is_guest": UserRole.GUEST in current_user.roles
    }
