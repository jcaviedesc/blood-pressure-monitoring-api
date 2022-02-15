from fastapi import APIRouter

from app.domains.users import router as user_router
from app.domains.bloodPressure import router as bp_router


router = APIRouter()
router.include_router(user_router.router)
router.include_router(bp_router.router)
