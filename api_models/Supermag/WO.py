from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SMDOCUMENTS(BaseModel):
    ID: str
    DOCTYPE: str
    BORNIN: str
    CLIENTINDEX: int
    COMMENTARY: Optional[str] = None
    CREATEDAT: datetime
    CURRENCYMULTORDER: int
    CURRENCYRATE: float
    CURRENCYTYPE: int
    DOCSTATE: int
    ISROUBLES: str
    LOCATION: Optional[str] = None
    LOCATIONFROM: int
    LOCATIONTO: Optional[str] = None
    OPCODE: int
    PRICEROUNDMODE: int
    TOTALSUM: float
    TOTALSUMCUR: float
    USEROP: Optional[str] = None


class SMSPEC(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    ARTICLE: str
    CAUSEID: Optional[str] = None
    CAUSESPECITEM: Optional[str] = None
    CAUSETYPE: Optional[str] = None
    DISPLAYITEM: int
    ITEMPRICE: float
    ITEMPRICECUR: float
    ITEMPRICENOTAX: float
    QUANTITY: float
    TOTALPRICE: float
    TOTALPRICECUR: float
    TOTALPRICENOTAX: float


class SMWAYBILLSOUT(BaseModel):
    ID: str
    DOCTYPE: str
    CONSIGNEE: Optional[str] = None
    INVOICE: str
    INVOICEDATE: Optional[str] = None
    OURSELFCLIENT: Optional[str] = None
    OURUTDID: Optional[str] = None
    PAYCASH: str
    SHIPPER: Optional[str] = None
    SUPPLIERUTDID: Optional[str] = None


class SMDOCTRANSPORT(BaseModel):
    DOCID: str
    DOCTYPE: str
    ADDRESSLOADING: Optional[str] = None
    ADDRESSUNLOADING: Optional[str] = None
    CARRIER: Optional[str] = None
    CUSTOMER: Optional[str] = None
    DELIVERYDATE: Optional[str] = None
    DRIVER: Optional[str] = None
    DRIVERLICENCE: Optional[str] = None
    EXPEDITOR: Optional[str] = None
    GLNUNLOADING: Optional[str] = None
    TRAILER: Optional[str] = None
    TRAINTYPE: Optional[str] = None
    TRUCKNUMBER: Optional[str] = None
    TRUCKTYPE: Optional[str] = None


class SMSPECNACL(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    CORRECTINVOICE: Optional[str] = None
    CORRECTINVOICEDATE: Optional[str] = None
    COUNTRY: str
    DISPLAYITEMEXT: Optional[str] = None


class SMSPECTAX(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    TAXID: int
    TAXRATE: float
    TAXSUM: float


class WO(BaseModel):
    SMDOCUMENTS: List[SMDOCUMENTS]
    SMSPEC: List[SMSPEC]
    SMWAYBILLSOUT: List[SMWAYBILLSOUT]
    SMDOCTRANSPORT: List[SMDOCTRANSPORT]
    SMSPECNACL: List[SMSPECNACL]
    SMSPECTAX: List[SMSPECTAX]


class POSTOBJECT(BaseModel):
    description: str
    action: str
    Id: str
    WO: WO


class PACKAGE(BaseModel):
    name: str
    POSTOBJECT: List[POSTOBJECT]


class RootModel(BaseModel):
    PACKAGE: PACKAGE
