from fastapi import APIRouter

from .users import router as user_router
from .blood_pressure import router as bp_router
from .selfcare import router as selfcare_router


router = APIRouter()
router.include_router(user_router.router)
router.include_router(bp_router.router)
router.include_router(selfcare_router.router)
