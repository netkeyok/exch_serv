from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SMSpecor(Base):
    __tablename__ = 'SMSPECOR'

    DOCTYPE = Column(String(2), primary_key=True, nullable=False)
    DOCID = Column(String(50), primary_key=True, nullable=False)
    SPECITEM = Column(Integer, primary_key=True, nullable=False)
    DISPLAYITEM = Column(Integer, primary_key=True, nullable=False)
    ARTICLE = Column(String(50), nullable=False)
    QUANTITY = Column(Float)
    SUGGESTQUANTITY = Column(Float)
    ITEMPRICE = Column(Float)
    TOTALPRICE = Column(Float)
    ITEMPRICECUR = Column(Float)
    TOTALPRICECUR = Column(Float)
