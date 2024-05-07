from typing import List, Optional
from pydantic import BaseModel, Field


class USIOSMCONTRAGENT(BaseModel):
    ID: int
    INN: str
    NAME: Optional[str] = None


class IOUSIOSMCONTRAGENT(BaseModel):
    USIOSMCONTRAGENT: List[USIOSMCONTRAGENT]


class POSTOBJECT(BaseModel):
    description: str
    action: str
    Id: str = Field(..., alias='Id')
    IOUSIOSMCONTRAGENT: IOUSIOSMCONTRAGENT


class PACKAGE(BaseModel):
    name: str
    POSTOBJECT: List[POSTOBJECT]


class DataModel(BaseModel):
    PACKAGE: PACKAGE
