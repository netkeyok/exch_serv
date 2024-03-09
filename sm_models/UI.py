from pydantic import BaseModel


class SmDocuments(BaseModel):
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
    LOCATION: int
    LOCATIONFROM: str | None = None
    LOCATIONTO: str | None = None
    OPCODE: int
    PRICEROUNDMODE: int
    TOTALSUM: float
    TOTALSUMCUR: float
    USEROP: str | None = None


class SmCommonBases(BaseModel):
    ID: str
    DOCTYPE: str
    BASEDOCTYPE: str
    BASEID: str


class SmWaybillsExt(BaseModel):
    ID: str
    DOCTYPE: str
    CONSIGNEE: str | None = None
    DELIVERYTOTALSUM: str | None = None
    DEVIATIONREASON: int
    EDOID: str
    EXCHANGEERRORTEXT: str | None = None
    EXCHANGESTATE: int
    GOODSOWNER: int
    INNSIGNATORY: str | None = None
    NAMESIGNATORY: str | None = None
    OURSELFCLIENT: int
    OURUTDID: str
    PAYCASH: str
    SHIPPER: str | None = None
    SUPPLIERCORRECTCREATE: str | None = None
    SUPPLIERCORRECTINVOICE: str | None = None
    SUPPLIERDOC: str
    SUPPLIERINVOICE: str
    SUPPLIERUTDID: str | None = None
    SUPPLINVOICECREATE: str
    UTDDATE: str | None = None
    UTDFUNCTION: str
    UTDSUPPDOC: str | None = None


class Smspecwe(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    ARTICLE: str
    COUNTRY: str | None = None
    DELIVERYSUM: str | None = None
    DISPLAYITEM: int
    DISPLAYITEMUI: int | None = None
    EXTRACHARGE: str | None = None
    ITEMPRICE: float
    ITEMPRICECUR: float
    ITEMPRICENOTAX: float
    MANUFACTURERSPRICE: str | None = None
    QUANTITY: float
    QUANTITYUI: float | None = None
    RETAILPRICE: float | None = None
    SPECITEMUI: int | None = None
    STATEREGULATION: int
    TOTALPRICE: float
    TOTALPRICECUR: float
    TOTALPRICENOTAX: float
    VATRATE: float
    VATSUM: float


class Smspecosucodewe(BaseModel):
    DOCID: str
    DOCTYPE: str
    SPECITEM: int
    OSUCODE: str


class UI(BaseModel):
    SMDOCUMENTS: list[SmDocuments]
    SMCOMMONBASES: list[SmCommonBases]
    SMWAYBILLSEXT: list[SmWaybillsExt]
    SMSPECWE: list[Smspecwe]
    SMSPECOSUCODEWE: list[Smspecosucodewe]


class PostObject(BaseModel):
    description: str
    action: str
    Id: str
    UI: UI


class Package(BaseModel):
    name: str
    POSTOBJECT: list[PostObject]


class UtmsPackageResponse(BaseModel):
    PACKAGE: Package
