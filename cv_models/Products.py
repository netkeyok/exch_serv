from pydantic import BaseModel
from typing import List, Optional


# определяем класс для упаковки
class Packing(BaseModel):
    name: Optional[str] = None
    self_weight: Optional[float] = None
    self_volume: Optional[float] = None
    unitsQuantity: Optional[float] = None
    barcode: Optional[str] = None
    barcodes: Optional[List[str]] = None
    id: Optional[str] = None
    marking: Optional[str] = None


# определяем класс для политики количества
class QuantityPolicy(BaseModel):
    multiline: Optional[bool] = None
    id: Optional[str] = None
    packing_ids: Optional[List[str]] = None


# определяем класс для продукта
class Product(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    packings: Optional[List[Packing]] = None
    barcode: Optional[str] = None
    basePackingId: Optional[str] = None
    marking: Optional[str] = None
    quantity_policy: Optional[QuantityPolicy] = None
