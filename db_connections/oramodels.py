import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship

# определить базовый класс для моделей SQLAlchemy
Base = declarative_base()


# определить класс для таблицы данных
# определяем класс для таблицы SMCARD
class SMCard(Base):
    # указываем имя таблицы
    __tablename__ = "SMCARD"

    # определяем столбцы таблицы с соответствующими типами данных и ограничениями
    article = Column(String, primary_key=True)  # используем article как первичный ключ
    globalarticle = Column(String)
    arrivedfrom = Column(Integer)
    bornin = Column(String)
    name = Column(String)
    shortname = Column(String)
    idmeasurement = Column(Integer)
    idclass = Column(Integer)
    idscale = Column(Integer)
    subarticle = Column(String)
    accepted = Column(Integer)
    datatype = Column(Integer)
    datasubtype = Column(Integer)
    scaleload = Column(Integer)
    cashload = Column(Integer)
    receiptok = Column(Integer)
    storage = Column(Integer)
    deadline = Column(Integer)
    losses = Column(Integer)
    scrap = Column(Integer)
    waste = Column(Integer)
    mesname = Column(String)
    mesabbrev = Column(String)
    country = Column(String)
    cardcomment = Column(String)
    flags = Column(Integer)
    cutpricedays = Column(Integer)
    supplypricepercentp = Column(Integer)
    supplypricepercentm = Column(Integer)
    minprofit = Column(Integer)
    idthreetorg = Column(Integer)
    idonetorg = Column(Integer)
    idspiritcode = Column(Integer)
    idmarketinggroup = Column(Integer)
    idlossesgroup = Column(Integer)
    quantitydeviation = Column(Integer)
    usetime = Column(Integer)
    usetimedim = Column(Integer)
    weight = Column(Integer)
    idmeasweight = Column(Integer)
    width = Column(Integer)
    length = Column(Integer)
    height = Column(Integer)
    idmeasdim = Column(Integer)
    stateregulation = Column(Integer)
    icing = Column(Integer)
    altname1 = Column(String)
    altname2 = Column(String)
    nominalvalue = Column(String)
    idcodetnved = Column(String)
    proteins = Column(String)
    fats = Column(String)
    carbs = Column(String)
    calories = Column(String)
    idpersonalprotection = Column(String)
    idokpd2 = Column(String)

    # определяем отношение один-ко-многим с таблицей SMSTOREUNITS
    store_units = relationship("SMStoreUnits", back_populates="card")

    # определяем класс для таблицы SMSTOREUNITS


class SMStoreUnits(Base):
    # указываем имя таблицы
    __tablename__ = "SMSTOREUNITS"

    # определяем столбцы таблицы с соответствующими типами данных и ограничениями
    barcode = Column(String, primary_key=True)  # используем barcode как первичный ключ
    barcodetype = Column(Integer)
    unitname = Column(String)
    # указываем, что article ссылается на article в таблице SMCARD
    article = Column(String, ForeignKey("SMCARD.article"))
    quantity = Column(Integer)
    facequantity = Column(Integer)
    flags = Column(Integer)
    subarticle = Column(String)
    boxid = Column(String)
    nestedbar = Column(String)
    weight = Column(String)
    tareweight = Column(String)
    tarewidth = Column(String)
    tarelength = Column(String)
    tareheight = Column(String)
    maxy = Column(String)
    packid = Column(String)

    # определяем отношение многие-к-одному с таблицей SMCARD
    card = relationship("SMCard", back_populates="store_units")


class SMClientInfo(Base):
    __tablename__ = 'SMCLIENTINFO'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    accepted = Column(Integer, default=0, nullable=False)
    inn = Column(String(20))
    kpp = Column(String(9))
    gln = Column(String(13))
    commentary = Column(String(255))


class SMDocuments(Base):
    __tablename__ = 'SMDOCUMENTS'
    DOCTYPE = Column(String(2), primary_key=True, nullable=False)
    ID = Column(String(50), nullable=False)
    BORNIN = Column(String(16), nullable=False)
    CREATEDAT = Column(DateTime, nullable=False, default=datetime.datetime.now)
    DOCSTATE = Column(Integer, nullable=False)
    OPCODE = Column(Integer, nullable=False)
    USEROP = Column(Integer)
    CLIENTINDEX = Column(Integer)
    LOCATIONFROM = Column(Integer)
    LOCATIONTO = Column(Integer)
    LOCATION = Column(Integer)
    CURRENCYTYPE = Column(Integer, nullable=False)
    CURRENCYRATE = Column(Float)
    CURRENCYMULTORDER = Column(Integer, nullable=False, default=0)
    TOTALSUM = Column(Float)
    TOTALSUMCUR = Column(Float)
    PRICEROUNDMODE = Column(Integer, nullable=False)
    ISROUBLES = Column(String(1), nullable=False, default='1')
    COMMENTARY = Column(String)
