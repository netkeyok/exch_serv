from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentItem(BaseModel):
    uid: Optional[str] = None
    createdBy: Optional[int] = Field(
        None,
        description="Where the document line was created (accounting system, mobile device, server or unknown)",
    )
    productId: Optional[str] = None
    declaredQuantity: Optional[float] = None
    currentQuantity: Optional[float] = None
    firstStorageId: Optional[str] = None
    secondStorageId: Optional[str] = None
    packingId: Optional[str] = None
    sscc: Optional[str] = None
    registrationDate: Optional[str] = None
    expiredDate: Optional[str] = None
    bindedLineUid: Optional[str] = None
    productName: Optional[str] = Field(None, write_only=True)
    productMarking: Optional[str] = Field(None, write_only=True)
    productBarcode: Optional[str] = Field(None, write_only=True)
    packingName: Optional[str] = Field(None, write_only=True)
    packingUnitsQuantity: Optional[float] = Field(None, write_only=True)


class DocumentExtendedFields(BaseModel):
    underloaded: Optional[bool] = None
    overloaded: Optional[bool] = None
    underloadedOrOverloaded: Optional[bool] = None


class DocumentTable(BaseModel):
    version: Optional[str] = None
    lastChangeDate: Optional[str] = None
    name: Optional[str] = None
    searchOrder: Optional[List[int]] = Field(None, read_only=True)
    fields: Optional[List[str]] = Field(
        None, read_only=True
    )  # Assuming FieldInfo is a simple string
    rows: Optional[List[str]] = Field(
        None, read_only=True
    )  # Assuming Row is a simple string


class DocumentState(BaseModel):
    modified: Optional[bool] = None
    modifiedDate: Optional[str] = None
    inProcess: Optional[bool] = None
    inProcessDate: Optional[str] = None
    finished: Optional[bool] = None
    finishedDate: Optional[str] = None
    processingTime: Optional[str] = None
    userId: Optional[str] = None


class PodborDokumentov(BaseModel):
    id: str
    name: Optional[str] = None
    appointment: Optional[str] = None
    userId: Optional[str] = None
    userName: Optional[str] = None
    lastChangeDate: Optional[datetime] = None
    createDate: Optional[datetime] = None
    createdOnPDA: Optional[bool] = None
    documentTypeName: str
    declaredItems: Optional[List[DocumentItem]] = Field(None, read_only=True)
    extendedFields: Optional[DocumentExtendedFields] = Field(None, read_only=True)
    combinedItems: Optional[List[DocumentItem]] = Field(None, read_only=True)
    modified: Optional[bool] = None
    inProcess: Optional[bool] = None
    finished: Optional[bool] = None
    currentItems: Optional[List[DocumentItem]] = Field(None, read_only=True)
    warehouseId: Optional[str] = None
    barcode: Optional[str] = None
    priority: Optional[int] = None
    description: Optional[str] = None
    autoAppointed: Optional[bool] = None
    serverHosted: Optional[bool] = None
    deviceId: Optional[str] = None
    deviceName: Optional[str] = None
    deviceIP: Optional[str] = None
    licenseStatus: Optional[int] = Field(None, read_only=True)
    tables: Optional[List[DocumentTable]] = Field(None, read_only=True)
    states: Optional[List[DocumentState]] = Field(None, read_only=True)
    vybrannyjBPnaTSD: Optional[str] = None
    imyaBiznesProcessa: Optional[str] = None
    imyaBP: Optional[str] = None
    nastrojkaBiznesProcessa: Optional[str] = None
    pokazyvatBP: Optional[str] = None
    expiredDate: Optional[str] = None
    lastDatedProduct: Optional[str] = None
    registrationDate: Optional[str] = None
    idIshodnyhDokumentov: Optional[str] = None
    idUzla: Optional[str] = None
    predstavlenieImeniDokumenta: Optional[str] = None
    status: Optional[str] = None
    idSklada1S: Optional[str] = None
    imyaSklada: Optional[str] = None
    skladVvedenNaTSD: Optional[bool] = None


class ODataResponse(BaseModel):
    odata_context: Optional[str] = Field(None, alias="@odata.context")
    value: Optional[List[PodborDokumentov]] = None
