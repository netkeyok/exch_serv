from pydantic import BaseModel, Field
from typing import List, Optional

class SMCARD(BaseModel):
    ARTICLE: str
    ACCEPTED: int
    ALTNAME1: Optional[str]
    ALTNAME2: Optional[str]
    BORNIN: str
    CALORIES: Optional[str]
    CARBS: Optional[str]
    CARDCOMMENT: Optional[str]
    CASHLOAD: str
    COUNTRY: str
    CUTPRICEDAYS: int
    DATASUBTYPE: int
    DATATYPE: int
    DEADLINE: int
    FATS: Optional[str]
    FLAGS: int
    GLOBALARTICLE: str
    HEIGHT: Optional[str]
    ICING: Optional[str]
    IDCLASS: int
    IDCODETNVED: Optional[str]
    IDLOSSESGROUP: Optional[str]
    IDMARKETINGGROUP: Optional[str]
    IDMEASDIM: Optional[str]
    IDMEASUREMENT: int
    IDMEASWEIGHT: Optional[str]
    IDOKPD2: Optional[str]
    IDONETORG: Optional[str]
    IDPERSONALPROTECTION: Optional[str]
    IDSCALE: Optional[str]
    IDSPIRITCODE: Optional[str]
    IDTHREETORG: Optional[str]
    LENGTH: Optional[str]
    LOSSES: float
    MESABBREV: str
    MESNAME: str
    MINPROFIT: float
    NAME: str
    NOMINALVALUE: Optional[str]
    PROTEINS: Optional[str]
    QUANTITYDEVIATION: float
    RECEIPTOK: str
    SCALELOAD: str
    SCRAP: float
    SHORTNAME: str
    STATEREGULATION: Optional[str]
    STORAGE: int
    SUBARTICLE: Optional[str]
    SUPPLYPRICEPERCENTM: Optional[str]
    SUPPLYPRICEPERCENTP: Optional[str]
    USETIME: int
    USETIMEDIM: int
    WASTE: float
    WEIGHT: Optional[str]
    WIDTH: Optional[str]

class SMCARDPROPERTIES(BaseModel):
    ARTICLE:str 
    PROPID:str 
    PROPVAL:str

class SMCARDTAX(BaseModel):
    ARTICLE:str 
    RGNID:int 
    DATEFROM:str 
    DATETO:str 
    TAXGROUPID:int

class CD(BaseModel):
    SMCARD : List[SMCARD] = Field(...)
    SMCARDPROPERTIES : List[SMCARDPROPERTIES] = Field(...)
    SMCARDTAX : List[SMCARDTAX] = Field(...)

class POSTOBJECT(BaseModel):
    description:str 
    action:str 
    Id:str 
    CD : CD = Field(...)

class PACKAGE(BaseModel):
    name:str 
    POSTOBJECT : List[POSTOBJECT] = Field(...)
    