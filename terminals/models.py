from pydantic import BaseModel


class SourceModel(BaseModel):
    id: int
    name: str
    server: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class InstrumentModel(BaseModel):
    id: int
    source_id: int
    name: str
    path: str
    currency_base: str
    currency_margin: str
    currency_profit: str
    description: str
    digits: int
    volume_min: float
    volume_max: float
    volume_step: float
    spread_floating: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
