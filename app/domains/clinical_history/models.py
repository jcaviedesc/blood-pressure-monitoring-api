from typing import Literal
from pydantic import Field
from app.core.baseModel import IDModelMixin, DatatimeModelMixin

REQUEST_CLINICAL_HISTORY_STATUS = Literal['on hold',
                                       'approved', 'rejected', 'expired']


class ClinalHistoryRequestsCreateModel(IDModelMixin, DatatimeModelMixin):
    request_by: str = Field(...) # professional_id
    patiend_id: str = Field(...)
    status: REQUEST_CLINICAL_HISTORY_STATUS = Field('on hold')
