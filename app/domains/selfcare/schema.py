from pydantic import BaseModel, Field, PositiveFloat, HttpUrl


class SelfcareTipSchemaBase(BaseModel):
    title: str = Field(..., alias="tle")
    description: str = Field(..., alias="desc")

    class Config:
        allow_population_by_field_name = True


class SelfcareTipSchema(BaseModel):
    professional: SelfcareTipSchemaBase = Field(...)
    patient: SelfcareTipSchemaBase = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "professional": {
                    "title": "super alimentos",
                    "description": "<div></div>",
                },
                "patient": {
                    "title": "Alimentos para mantener la presion arterial",
                    "description": "<div>hola</div>",
                }
            }
        }
