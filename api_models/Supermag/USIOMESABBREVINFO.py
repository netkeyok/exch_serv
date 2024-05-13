from typing import List, Optional
from pydantic import BaseModel, UUID4


class USIOMESABBREVINFO(BaseModel):
    ARTICLE: str
    MESABBREV: str


class IOUSIOMESABBREVINFO(BaseModel):
    USIOMESABBREVINFO: List[USIOMESABBREVINFO]


class POSTOBJECT(BaseModel):
    description: str
    action: str
    Id: str
    IOUSIOMESABBREVINFO: Optional[IOUSIOMESABBREVINFO]


class PACKAGE(BaseModel):
    name: UUID4
    POSTOBJECT: List[POSTOBJECT]


class DataModel(BaseModel):
    PACKAGE: PACKAGE
