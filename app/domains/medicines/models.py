from typing import Optional
from ...core.baseModel import DatetimeModelMixin, IDModelMixin
from .schemas import MedicinesSchema

class MedicineModelCreate(IDModelMixin, DatetimeModelMixin, MedicinesSchema):
    user_id: Optional[str]
    
    def set_user_id(self, id: str):
        self.user_id = id