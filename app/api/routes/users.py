from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "This is a placeholder route."}
