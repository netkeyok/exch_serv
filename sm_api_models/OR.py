from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class SMSPECOR(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    ARTICLE: str
    DISPLAYITEM: int
    ITEMPRICE: float
    ITEMPRICECUR: float
    QUANTITY: float
    SUGGESTQUANTITY: float = Field(default=0.0)
    TOTALPRICE: float
    TOTALPRICECUR: float


class SMDOCOR(BaseModel):
    ID: str
    DOCTYPE: str = Field(default="OR")
    CLIENTCOMMENTARY: Optional[str] = None
    COMMENTARY: Optional[str] = None
    CROSSLOCATION: Optional[int] = None
    ORDERDATE: datetime
    OURSELFCLIENT: int
    SUPPLYDATE: str | None = None
    SUPPLYTIME: int = Field(default=0)
    SUPPLYTIMETILL: int = Field(default=1439)
    USEFORAUTOGEN: str = Field(default="1")


class SMDOCUMENTS(BaseModel):
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
    TOTALSUM: float
    TOTALSUMCUR: float
    USEROP: Optional[int] = None


class OR(BaseModel):
    SMDOCUMENTS: List[SMDOCUMENTS]
    SMDOCOR: List[SMDOCOR]
    SMSPECOR: List[SMSPECOR]


class POSTOBJECT(BaseModel):
    description: str
    action: str
    Id: str
    OR: OR


class Package(BaseModel):
    name: str
    POSTOBJECT: List[POSTOBJECT]


class Data(BaseModel):
    PACKAGE: Package
