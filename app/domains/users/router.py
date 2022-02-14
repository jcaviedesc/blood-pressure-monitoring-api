from fastapi import APIRouter

router = APIRouter(prefix="/users",tags=["Users"])

@router.post("/")
async def create_user():
    return "user created"