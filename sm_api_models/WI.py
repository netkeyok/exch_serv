from pydantic import BaseModel


class SMSpec(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    ARTICLE: str
    DISPLAYITEM: int
    ITEMPRICE: float
    QUANTITY: float
    TOTALPRICE: float
    TOTALPRICECUR: float


class SMWaybillIn(BaseModel):
    ID: str
    DOCTYPE: str
    CONSIGNEE: str | None = None
    DELIVERYTOTALSUM: float | None = None
    EXTRAEXPENSESCURRMULTORDER: int | None = None
    EXTRAEXPENSESCURRRATE: float | None = None
    GOODSOWNER: int
    OURSELFCLIENT: int | None = None
    OURUTDID: str | None = None
    PAYCASH: str
    SHIPPER: str | None = None
    SUPPLDOCSUM: float
    SUPPLIERDOC: str
    SUPPLIERDOCCREATE: str
    SUPPLIERINVOICE: str | None = None
    SUPPLIERUTDID: str | None = None
    SUPPLINVOICECREATE: str | None = None


class SMDocTransport(BaseModel):
    DOCID: str
    DOCTYPE: str
    ADDRESSLOADING: str | None = None
    ADDRESSUNLOADING: str | None = None
    CARRIER: str | None = None
    CUSTOMER: str | None = None
    DELIVERYDATE: str | None = None
    DRIVER: str | None = None
    DRIVERLICENCE: str | None = None
    EXPEDITOR: str | None = None
    GLNUNLOADING: str | None = None
    TRAILER: str | None = None
    TRAINTYPE: str | None = None
    TRUCKNUMBER: str | None = None
    TRUCKTYPE: str | None = None


class SMSpecNacl(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    CORRECTINVOICE: str | None = None
    CORRECTINVOICEDATE: str | None = None
    COUNTRY: str
    DISPLAYITEMEXT: int | None = None


class SMSpecTax(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    TAXID: int
    TAXRATE: float
    TAXSUM: float


class SMSpecStat(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    CASHPRICE: float
    CASHPRICEFROM: float | None = None
    EVENTTIME: str
    EVENTTIMEFROM: str | None = None


class SMDocuments(BaseModel):
    ID: str
    DOCTYPE: str
    BORNIN: str
    CLIENTINDEX: int
    COMMENTARY: str | None = None
    CREATEDAT: str
    CURRENCYMULTORDER: int
    CURRENCYRATE: float
    CURRENCYTYPE: int
    DOCSTATE: int
    ISROUBLES: str
    LOCATION: str | None = None
    LOCATIONFROM: str | None = None
    LOCATIONTO: int
    OPCODE: int
    PRICEROUNDMODE: int
    TOTALSUM: float | None = None
    TOTALSUMCUR: float | None = None
    USEROP: str | None = None


class SMCommonbases(BaseModel):
    ID: str
    DOCTYPE: str
    BASEDOCTYPE: str
    BASEID: str


class SMDocProps(BaseModel):
    DOCID: str
    DOCTYPE: str
    PARAMNAME: str
    PARAMVALUE: str


class SLSpecqmismatch(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    # ARTICLE: str | None = None
    QUANTBYDOC: int
    REASON: str | None = None
    REASON2: str | None = None


class WI(BaseModel):
    SMDOCUMENTS: list[SMDocuments]
    SMCOMMONBASES: list[SMCommonbases]
    # SMDOCPROPS: list[SMDocProps] | None = None
    SMSPEC: list[SMSpec]
    SMWAYBILLSIN: list[SMWaybillIn] | None = None
    SLSPECQMISMATCH: list[SLSpecqmismatch] | None = None
    # SMDOCTRANSPORT: list[SMDocTransport] | None = None
    # SMSPECNACL: list[SMSpecNacl] | None = None
    # SMSPECTAX: list[SMSpecTax] | None = None
    # SMSPECSTAT: list[SMSpecStat] | None = None


class Item(BaseModel):
    description: str
    action: str
    Id: str
    WI: WI


class Package(BaseModel):
    name: str
    POSTOBJECT: list[Item]


class Data(BaseModel):
    PACKAGE: Package
