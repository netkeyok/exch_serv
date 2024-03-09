from pydantic import BaseModel
from typing import List, Optional


# определяем класс Contragent, наследуемый от BaseModel
class Contragent(BaseModel):
    # определяем атрибуты класса с аннотациями типов
    uid: Optional[str] = None
    kod: Optional[str] = None
    naimenovanie: Optional[str] = None
    shK: Optional[str] = None
    etoPapka: Optional[bool] = None
    idRoditelya: Optional[str] = None
    iNN: Optional[str] = None
    naimenovanieDlyaPoiska: Optional[str] = None
    id: Optional[str] = None
