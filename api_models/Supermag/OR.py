from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SmDocProps(BaseModel):
    DOCID: str
    DOCTYPE: str
    PARAMNAME: str
    PARAMVALUE: str


class SmSpecOr(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    ARTICLE: str
    DISPLAYITEM: int
    ITEMPRICE: float
    ITEMPRICECUR: float
    QUANTITY: float
    SUGGESTQUANTITY: float = Field(default=0.0)
    TOTALPRICE: float | None = None
    TOTALPRICECUR: float | None = None


class SmDocOr(BaseModel):
    ID: str
    DOCTYPE: str = Field(default="OR")
    CLIENTCOMMENTARY: Optional[str] = None
    COMMENTARY: Optional[str] = None
    CROSSLOCATION: Optional[int] = None
    ORDERDATE: Optional[datetime]
    OURSELFCLIENT: Optional[int] = None
    SUPPLYDATE: str | None = None
    SUPPLYTIME: int = Field(default=0)
    SUPPLYTIMETILL: int = Field(default=1439)
    USEFORAUTOGEN: str = Field(default="1")


class SmDocuments(BaseModel):
    ID: str
    DOCTYPE: str
    BORNIN: str
    CLIENTINDEX: int
    COMMENTARY: Optional[str] = None
    CREATEDAT: datetime
    CURRENCYMULTORDER: int = Field(default=0)
    CURRENCYRATE: float
    CURRENCYTYPE: int
    DOCSTATE: int
    ISROUBLES: str = Field(default="1")
    LOCATION: int
    LOCATIONFROM: Optional[int] = None
    LOCATIONTO: Optional[int] = None
    OPCODE: int
    PRICEROUNDMODE: int
    TOTALSUM: Optional[float] = None
    TOTALSUMCUR: Optional[float] = None
    USEROP: Optional[int] = None


class Or(BaseModel):
    SMDOCUMENTS: List[SmDocuments]
    SMDOCOR: List[SmDocOr]
    SMSPECOR: List[SmSpecOr]
    SMDOCPROPS: Optional[List[SmDocProps]] = None


class PostObject(BaseModel):
    description: str
    action: str
    Id: str
    OR: Or


class Package(BaseModel):
    name: str
    POSTOBJECT: List[PostObject]


class Data(BaseModel):
    PACKAGE: Package
