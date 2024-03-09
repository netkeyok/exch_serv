from sqlalchemy import Column, Integer, String, DateTime, Float, CHAR, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()


class SMDocuments(Base):
    __tablename__ = 'SMDOCUMENTS'
    DOCTYPE = Column(CHAR(2), primary_key=True, nullable=False)
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
    CURRENCYRATE = Column(Numeric(precision=8, scale=4), nullable=False)
    CURRENCYMULTORDER = Column(Integer, nullable=False, default=0)
    TOTALSUM = Column(Numeric(precision=19, scale=4), nullable=False)
    TOTALSUMCUR = Column(Numeric(precision=19, scale=4), nullable=False)
    PRICEROUNDMODE = Column(Integer, nullable=False)
    ISROUBLES = Column(CHAR(1), nullable=False, default='1')
    COMMENTARY = Column(Text)
