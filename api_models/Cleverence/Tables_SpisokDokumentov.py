from typing import Optional
from pydantic import BaseModel, Field


class SpisokDokumentov(BaseModel):
    uid: Optional[str] = Field(None, description="Unique row identifier")
    docdate: Optional[str] = Field(None)
    docType: Optional[str] = Field(None)
    docBarcode: Optional[str] = Field(None)
    idKontragenta: Optional[str] = Field(None)
    summaDokumenta: Optional[float] = Field(None, description="Summa dokumenta")
    warehouseId: Optional[str] = Field(None)
