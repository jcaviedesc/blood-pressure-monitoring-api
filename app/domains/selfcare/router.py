from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.core.enums import PageLimitEnum, usersTypesEnum
from .utils import get_title_from_html
from ...dependencies.database import get_repository
from .schema import SelfcareTipSchema
from .model import SelfcareModel
from .repository import SelfcareRepository

router = APIRouter(prefix="/selfcare", tags=["Selfcare"])


@router.post("", status_code=HTTP_201_CREATED)
async def create_selfcare_tip(
    tip: SelfcareTipSchema = Body(...),
    selfcare_repo: SelfcareRepository = Depends(get_repository(SelfcareRepository))) -> JSONResponse:
    title = get_title_from_html(tip.editor.patient)
    data = SelfcareModel(**tip.dict(), title=title)
    # data.add_user(user={"name": "juan", "avatar": "https", "id": "fd2"})
    selfcare_created = await selfcare_repo.insert_selfcare_tip(tip=data)
    return JSONResponse(status_code=HTTP_201_CREATED, content=jsonable_encoder(selfcare_created, exclude_defaults=True, by_alias=False))


@router.get("/{tip_id}", status_code=HTTP_200_OK)
async def get_selfcare_tip_by_id(tip_id: str, selfcare_repo: SelfcareRepository = Depends(get_repository(SelfcareRepository))):
    selfcarte_tip = await selfcare_repo.find_selfcare_tip_by_id(tip_id=tip_id)
    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(selfcarte_tip, exclude_defaults=True, by_alias=False))

@router.get("/{user_type}/search", status_code=HTTP_200_OK)
async def search_selfcare_tips(
    q: str,
    page: int,
    limit: PageLimitEnum,
    user_type: usersTypesEnum, 
    selfcare_repo: SelfcareRepository = Depends(get_repository(SelfcareRepository))
):
    selfcare_search_result = await selfcare_repo.search_selfcare(query=q, limit=limit, to=user_type)
    return JSONResponse(status_code=HTTP_200_OK, content=jsonable_encoder(selfcare_search_result, exclude_defaults=True, by_alias=False))
