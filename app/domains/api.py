from fastapi import APIRouter

from app.domains.users import router as user_router


router = APIRouter()
router.include_router(user_router.router)
