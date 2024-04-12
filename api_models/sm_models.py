from pydantic import BaseModel


class SMCARD(BaseModel):
    article: str
    shortname: str


class SMSTOREUNITS(BaseModel):
    barcode: str
    article: str  # предполагается, что это внешний ключ, связанный с полем article в модели SMCARD
