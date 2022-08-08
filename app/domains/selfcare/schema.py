from pydantic import BaseModel, Field


class SelfcareTipEditorSchema(BaseModel):
    professional: str = Field(...)
    patient: str = Field(...)

    class Config:
        allow_population_by_field_name = True


class SelfcareTipSchema(BaseModel):
    editor: SelfcareTipEditorSchema = Field(...)
    keywords:list[str] = Field(..., min_items=1)

    class Config:
        schema_extra = {
            "example": {
                "editor": {
                    "professional": "<div></div>",
                    "patient": "<div>hola</div>"
                },
                "keywords": ["presion arterial", "alimentos"]
            }
        }
