from pydantic import BaseModel


# определяем модель для SMSpecNacl
class SMSpecNacl(BaseModel):
    DOCID: str 
    DOCTYPE: str 
    SPECITEM: int 
    CORRECTINVOICE: str | None = None 
    CORRECTINVOICEDATE: str | None = None 
    COUNTRY: str 
    DISPLAYITEMEXT: int | None = None

# определяем модель для SMSpecTax
class SMSpecTax(BaseModel):
    DOCID: str 
    DOCTYPE: str 
    SPECITEM: int 
    TAXID: int 
    TAXRATE: float 
    TAXSUM: float

# определяем модель для SMSpecStat
class SMSpecStat(BaseModel):
    DOCID: str 
    DOCTYPE: str 
    SPECITEM: int 
    CASHPRICE: float
    CASHPRICEFROM: float | None = None
    EVENTTIME: str
    EVENTTIMEFROM: str | None = None

# определяем модель для SMDocuments
class SMDocuments(BaseModel):
    ID: str
    DOCTYPE: str
    BORNIN: str
    CLIENTINDEX: int | None = None
    COMMENTARY: str | None = None
    CREATEDAT: str
    CURRENCYMULTORDER: int
    CURRENCYRATE: float
    CURRENCYTYPE: int
    DOCSTATE: int
    ISROUBLES: str
    LOCATION: int | None = None
    LOCATIONFROM: int | None = None
    LOCATIONTO: int | None = None
    OPCODE: int
    PRICEROUNDMODE: int
    TOTALSUM: float
    TOTALSUMCUR: float
    USEROP: str | None = None

# определяем модель для SMDocProps
class SMDocProps(BaseModel):
    DOCID: str
    DOCTYPE: str
    PARAMNAME: str
    PARAMVALUE: str

# определяем модель для SMSpec
class SMSpec(BaseModel):
    DOCID:str 
    DOCTYPE:str 
    SPECITEM:int 
    ARTICLE:str 
    CAUSEID:str | None = None 
    CAUSESPECITEM:int | None = None 
    CAUSETYPE:str | None = None 
    DISPLAYITEM:int 
    ITEMPRICE:float | None = None 
    ITEMPRICECUR:float | None = None 
    ITEMPRICENOTAX:float | None = None 
    QUANTITY:float 
    TOTALPRICE:float 
    TOTALPRICECUR:float 
    TOTALPRICENOTAX:float | None = None

# определяем модель для SMWaybillIn
class SMWaybillIn(BaseModel):
    ID:str 
    DOCTYPE:str 
    CONSIGNEE:str | None = None 
    DELIVERYTOTALSUM:float | None = None 
    EXTRAEXPENSESCURRMULTORDER:int | None = None 
    EXTRAEXPENSESCURRRATE:float | None = None 
    GOODSOWNER:int 
    OURSELFCLIENT:str | None = None 
    OURUTDID:str | None = None 
    PAYCASH:str 
    SHIPPER:str | None = None 
    SUPPLDOCSUM:float 
    SUPPLIERDOC:str  
    SUPPLIERDOCCREATE:str  
    SUPPLIERINVOICE:str  
    SUPPLIERUTDID:str|None=None  
    SUPPLINVOICECREATE:str 

# определяем модель для SMDocTransport
class SMDocTransport(BaseModel):
    DOCID:str  
    DOCTYPE:str  
    ADDRESSLOADING:str|None=None  
    ADDRESSUNLOADING:str|None=None  
    CARRIER:str|None=None  
    CUSTOMER:str|None=None  
    DELIVERYDATE:str|None=None  
    DRIVER:str|None=None  
    DRIVERLICENCE:str|None=None  
    EXPEDITOR:str|None=None  
    GLNUNLOADING:str|None=None  
    TRAILER:str|None=None  
    TRAINTYPE:str|None=None  
    TRUCKNUMBER:str|None=None  
    TRUCKTYPE:str|None=None 

# определяем модель для SMRolls
class SMRolls(BaseModel):
    ID: str 
    DOCTYPE: str 
    FILLSPECTYPE: int 
    FINALDATE: str 
    ISACTIVEONLY: str 
    ISFILLCOMPLETE: str 
    ORDERNO: str | None = None 
    OURSELFCLIENT: int | None = None 
    PREAMBLEDATE: str 
    PRICEMODE: int 
    PRICETYPE: int | None = None 
    ROLLMODE: int 
    SPECTYPENAME: str | None = None 
    STORELOC: int 
    WITHDUE: str 
    ZONEID: int | None = None

# определяем модель для SMSpecRL
class SMSpecRL(BaseModel):
    DOCID:str  
    DOCTYPE:str  
    SPECITEM:int  
    ACTUALQUANTITY:float  
    AWAITQUANTITY:float  
    AWAITTOTALPRICE:float  
    AWAITTOTALPRICECUR:float 

# определяем модель для SMSpecRLBases
class SMSpecRLBases(BaseModel):
    DOCID:str  
    DOCTYPE:str  
    SPECITEM:int  
    ORDNUM:int  
    BASEDOCID:str  
    BASEDOCTYPE:str  
    BASESPECITEM:int  
    FORCEDMAPPING:str  
    QUANTITY:float 

# определяем модель для WI
class WI(BaseModel):
    SMDOCUMENTS:list[SMDocuments] 
    SMDOCPROPS:list[SMDocProps] | None = None
    SMSPEC:list[SMSpec] 
    SMWAYBILLSIN:list[SMWaybillIn] | None = None
    SMDOCTRANSPORT:list[SMDocTransport] | None = None
    SMSPECNACL:list[SMSpecNacl] | None = None
    SMSPECTAX:list[SMSpecTax] | None = None
    SMSPECSTAT:list[SMSpecStat] | None = None
    SMROLLS:list[SMRolls] | None = None
    SMSPECRL:list[SMSpecRL] | None = None
    SMSPECRLBASES:list[SMSpecRLBases] | None = None

# определяем модель для Item
class Item(BaseModel):
    description:str  
    action:str  
    Id:str  
    RL:WI

# определяем модель для Package
class Package(BaseModel):
    name:str 
    POSTOBJECT:list[Item]

# определяем модель для Data
class Data(BaseModel):
    PACKAGE:Package
