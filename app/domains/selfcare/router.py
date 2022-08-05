from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.core.enums import PageLimitEnum

router = APIRouter(prefix="/selfcare", tags=["Selfcare"])


@router.post("", status_code=HTTP_201_CREATED)
async def create_selfcare_tip(tip=Body(...)) -> JSONResponse:
    return JSONResponse(status_code=HTTP_201_CREATED, content="")


@router.get("/{tip_id}", status_code=HTTP_200_OK)
async def get_selfcare_tip_by_id(tip_id: str):
    pass

@router.get("/search", status_code=HTTP_200_OK)
async def search_selfcare_tips(q: str, page: int, limit: PageLimitEnum):
    pass
