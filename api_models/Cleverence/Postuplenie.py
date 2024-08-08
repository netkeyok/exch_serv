from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional


class DocumentItem(BaseModel):
    # определяем атрибуты класса с аннотациями типов
    nomerStrokiDokumenta: Optional[int] = None
    uid: Optional[str] = None
    createdBy: Optional[str] = (
        None  # = Field(None, choices=[0, 1, 2, 3], read_only=True)
    )
    # createdBy: Optional[str] = '2'
    productId: Optional[str]
    declaredQuantity: Optional[float]
    currentQuantity: Optional[float] = None
    packingId: Optional[str] = None
    registrationDate: Optional[str] = None
    productName: Optional[str] = Field(None, write_only=True)
    productMarking: Optional[str] = Field(None, write_only=True)
    productBarcode: Optional[str] = Field(None, write_only=True)
    packingName: Optional[str] = Field(None, write_only=True)
    cena: Optional[float] = (
        None  # Необходимо вручную добавить дополнительное поле строки в документ в CV
    )
    CenaPriemki: Optional[float] = None
    priceTotal: Optional[float] = (
        None  # Необходимо вручную добавить дополнительное поле строки в документ в CV
    )
    bindedLineUid: Optional[str] = None
    idEdinicyIzmereniya: Optional[str] = None
    IdDokumenta: Optional[str] = None
    KodStroki: Optional[int] = None


class Postuplenie(BaseModel):
    id: str
    name: Optional[str] = None
    appointment: Optional[str] = None
    userId: Optional[str] = None
    userName: Optional[str] = None
    lastChangeDate: Optional[datetime] = None
    createDate: Optional[datetime] = None
    createdOnPDA: Optional[bool] = None
    documentTypeName: str = "Поступление"
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
    idKontragenta: Optional[str] = None
    declaredItems: Optional[list[DocumentItem]] = Field(None, read_only=True)
    summaDokumenta: Optional[float] = (
        None  # Необходимо вручную добавить дополнительное поле шапки в вид документа в CV
    )
    selfclient: Optional[int] = (
        None  # Необходимо вручную добавить дополнительное поле шапки в вид документа в CV
    )
