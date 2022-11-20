
from pydantic import Field
from app.core.baseModel import IDModelMixin, DatetimeModelMixin
from .types import REQUEST_CLINICAL_HISTORY_STATUS


class ClinicalMonitoringRequestsCreateModel(IDModelMixin, DatetimeModelMixin):
    request_by: str = Field(...) # professional_id
    patient_id: str = Field(...)
    status: REQUEST_CLINICAL_HISTORY_STATUS = Field('pending')

