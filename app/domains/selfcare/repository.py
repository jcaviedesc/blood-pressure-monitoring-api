from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from ...db.repositoryBase import BaseRepository
from ...db.projections import make_excluded_fields
from .model import SelfcareModel, SelfcareReturnInsertModel, SelfcarePublicModel


class SelfcareRepository(BaseRepository):
    """"
    All database actions associated with the Selfcare resource
    """
    async def insert_selfcare_tip(self, *, tip: SelfcareModel):
        selfcare_body = jsonable_encoder(tip, by_alias=True)
        try:
            inserted_tip = await self.get_entity('SelfcareTips').insert_one(selfcare_body)
        except:
            # TODO agregar errorhandler
            return None
        projection = make_excluded_fields()
        user_result = await self.get_entity('SelfcareTips').find_one({"_id": inserted_tip.inserted_id}, projection)
        return SelfcareReturnInsertModel(**user_result)

    async def find_selfcare_tip_by_id(self, *, tip_id: str):
        selfcare_tip = await self.get_entity('SelfcareTips').find_one({"_id": tip_id})
        return SelfcarePublicModel(**selfcare_tip) if selfcare_tip is not None else None

    async def search_selfcare(self, *, query: str, to: str, limit: int):
        path_user = 'editor.patient' if to == 'patient' else 'editor.professional'
        pipeline = [
            {
                '$search': {
                    'index': 'default',
                    'text': {
                        'query': query,
                        'path': ['title', path_user]
                    }
                }
            }, {
                '$limit': limit
            }, {
                '$project': {
                    '_id': 0,
                    'title': 1,
                    'editor': 1,
                    'owner': 1,
                    'keywords': 1,
                }
            }
        ]
        result = []
        selfcare_results = await self.get_entity('SelfcareTips').aggregate(pipeline).to_list(length=limit)
        for selfcare_tip in selfcare_results:
            parse_to_selfcare_model = SelfcarePublicModel(**selfcare_tip)
            result.append(parse_to_selfcare_model)
        return result
