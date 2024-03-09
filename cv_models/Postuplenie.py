from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional


class DocumentItem(BaseModel):
    # определяем атрибуты класса с аннотациями типов
    uid: Optional[str] = None
    createdBy: Optional[str] = None  # = Field(None, choices=[0, 1, 2, 3], read_only=True)
    productId: Optional[str]
    declaredQuantity: Optional[float]
    currentQuantity: Optional[float] = None
    packingId: Optional[str] = None
    registrationDate: Optional[str] = None
    productName: Optional[str] = Field(None, write_only=True)
    productMarking: Optional[str] = Field(None, write_only=True)
    productBarcode: Optional[str] = Field(None, write_only=True)
    packingName: Optional[str] = Field(None, write_only=True)
    price: Optional[float] = None  # Необходимо вручную добавить дополнительное поле строки в документ в CV
    cenaPostavki: Optional[float] = None  # Необходимо вручную добавить дополнительное поле строки в документ в CV


class Postuplenie(BaseModel):
    id: str
    name: str
    appointment: Optional[str] = None
    userId: Optional[str] = None
    userName: Optional[str] = None
    lastChangeDate: datetime
    createDate: datetime
    createdOnPDA: Optional[bool] = None
    documentTypeName: str
    modified: Optional[bool] = None
    inProcess: Optional[bool] = None
    finished: Optional[bool] = None
    warehouseId: Optional[str] = None
    barcode: Optional[str] = None
    priority: Optional[int] = None
    description: Optional[str] = None
    distributeByBarcode: Optional[bool] = None
    autoAppointed: Optional[bool] = None
    serverHosted: Optional[bool] = None
    deviceId: Optional[str] = None
    deviceName: Optional[str] = None
    deviceIP: Optional[str] = None
    # licenseStatus: Optional[str] = None
    idKontragenta: Optional[str] = None
    declaredItems: Optional[list[DocumentItem]] = Field(None, read_only=True)
    summadokumenta: Optional[float] = None  # Необходимо вручную добавить дополнительное поле шапки в вид документа в CV
