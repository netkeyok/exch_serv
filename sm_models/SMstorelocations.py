from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SMStoreLocations(Base):
    __tablename__ = 'SMSTORELOCATIONS'

    ID = Column(Integer, primary_key=True, nullable=False)
    NAME = Column(String(255), nullable=False)
    IDCLASS = Column(Integer, nullable=False)
    ACCEPTED = Column(String(1), nullable=False)
    PRTY = Column(Integer, nullable=False)
    FLAGS = Column(Integer, nullable=False)
    LOCTYPE = Column(Integer, nullable=False)
    PARENTLOC = Column(Integer)
    RGNID = Column(Integer, default=-1, nullable=False)
    ADDRESS = Column(String(255))
    TEL = Column(String(40))
    FAX = Column(String(40))
    COMMENTARY = Column(String(255))
    ORDERALG = Column(String(255), default='*', nullable=False)
    CARDTYPE = Column(Integer)
    FORMATID = Column(Integer)
    PRICINGMETHOD = Column(Integer, default=0, nullable=False)
    SUGGESTORDERALG = Column(String(50), default='EFFECTIVE', nullable=False)
    FLOORSPACE = Column(Float)
    GLN = Column(String(13))
    SHORTNAME = Column(String(255))
    SPOILAGELOC = Column(Integer)
    CLOSEDEDITDATE = Column(DateTime)
    KPP = Column(String(9))
    CLOSEDEDITDOCID = Column(String(50))
    CLOSEDEDITDATEOLD = Column(DateTime)
    CLOSEDEDITDOCIDOLD = Column(String(50))
