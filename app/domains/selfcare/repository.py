from fastapi.encoders import jsonable_encoder
from ...db.repositoryBase import BaseRepository, Entities
from ...db.projections import make_excluded_fields
from .model import SelfcareModel, SelfcareReturnInsertModel


class SelfcareRepository(BaseRepository):
    """"
    All database actions associated with the Selfcare resource
    """
    async def insert_selfcare_tip(self, *, tip: SelfcareModel):
        selfcare_body = jsonable_encoder(tip, by_alias=True)
        try:
            inserted_tip = await self.get_entity(Entities.SELFCARE_TIPS).insert_one(selfcare_body)
        except:
            # TODO agregar errorhandler
            return None
        projection = make_excluded_fields()
        user_result = await self.get_entity(Entities.SELFCARE_TIPS).find_one({"_id": inserted_tip.inserted_id}, projection)
        return SelfcareReturnInsertModel(**user_result)
