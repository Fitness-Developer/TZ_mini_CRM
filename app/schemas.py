from pydantic import BaseModel
from typing import Optional
class OperatorCreate(BaseModel):
    name: str
    active: bool = True
    load_limit: int = 5


class SourceCreate(BaseModel):
    name: str


class WeightCreate(BaseModel):
    operator_id: int
    weight: int


class ContactCreate(BaseModel):
    external_id: str
    source_id: int
    text: Optional[str] = None