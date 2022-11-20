from pydantic import BaseModel, Field
from .types import REQUEST_CLINICAL_HISTORY_STATUS

class ClinicalMonitoringRequestsUpdateSchema(BaseModel):
    patient_id: str = Field(...)
    status: REQUEST_CLINICAL_HISTORY_STATUS = Field(...)