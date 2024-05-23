from pydantic import BaseModel
from typing import List


class USIOCARDINFO(BaseModel):
    ARTICLE: str
    MESABBREV: str
    SHORTNAME: str


class IOUSIOCARDINFO(BaseModel):
    USIOCARDINFO: List[USIOCARDINFO]


class POSTOBJECT(BaseModel):
    description: str
    action: str
    Id: str
    IOUSIOCARDINFO: IOUSIOCARDINFO


class PACKAGE(BaseModel):
    name: str
    POSTOBJECT: List[POSTOBJECT]


class DataModel(BaseModel):
    PACKAGE: PACKAGE
