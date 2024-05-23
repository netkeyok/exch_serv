from pydantic import BaseModel, UUID4
from typing import List, Optional


class USIOBARINFO(BaseModel):
    BARCODE: str
    QUANTITY: float
    UNITNAME: str


class IOUSIOBARINFO(BaseModel):
    USIOBARINFO: List[USIOBARINFO]


class PostObject(BaseModel):
    description: str
    action: str
    Id: str
    IOUSIOBARINFO: Optional[IOUSIOBARINFO]


class Package(BaseModel):
    name: UUID4
    POSTOBJECT: List[PostObject]


class DataModel(BaseModel):
    PACKAGE: Package
