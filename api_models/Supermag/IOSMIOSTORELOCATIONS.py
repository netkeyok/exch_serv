from pydantic import BaseModel, Field
from typing import List, Optional


class SMIOSTORELOCATION(BaseModel):
    iLocID: int
    iClassID: int
    iLocType: int
    iParentLoc: Optional[int] = None
    iRgnID: int
    nFloorSpace: Optional[float] = None
    sAddress: Optional[str] = None
    sClassName: str
    sClassTree: str
    sGLN: Optional[str] = None
    sKPP: Optional[str] = None
    sLocName: str
    sLocShortName: Optional[str] = None
    sTel: Optional[str] = None

    # class Config:
    #     populate_by_name = True


class IOSMIOSTORELOCATIONS(BaseModel):
    SMIOSTORELOCATIONS: List[SMIOSTORELOCATION]


class POSTOBJECT(BaseModel):
    description: str
    action: str
    Id: str  # = Field(alias='IOSMIOSTORELOCATIONS')
    IOSMIOSTORELOCATIONS: IOSMIOSTORELOCATIONS

    # class Config:
    #     populate_by_name = True


class PACKAGE(BaseModel):
    name: str
    POSTOBJECT: List[POSTOBJECT]

    # class Config:
    #     populate_by_name = True


class DataModel(BaseModel):
    PACKAGE: PACKAGE

    # class Config:
    #     populate_by_name = True
