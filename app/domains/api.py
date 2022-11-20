from fastapi import APIRouter

from .users import router as user_router
from .blood_pressure import router as bp_router
from .selfcare import router as selfcare_router
from .medicines import router as medicines_router
from .clinical_monitoring import router as clinical_router

router = APIRouter()
router.include_router(user_router.router)
router.include_router(bp_router.router)
router.include_router(selfcare_router.router)
router.include_router(medicines_router.router)
router.include_router(clinical_router.router)
