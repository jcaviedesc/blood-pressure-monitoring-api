from typing import Optional
from ...core.baseModel import DatatimeModelMixin, IDModelMixin
from .schemas import MedicinesSchema

class MedicineModelCreate(IDModelMixin, DatatimeModelMixin, MedicinesSchema):
    user_id: Optional[str]
    
    def set_user_id(self, id: str):
        self.user_id = id