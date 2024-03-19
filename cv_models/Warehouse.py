from typing import Optional
from pydantic import BaseModel


class Warehouse(BaseModel):

    storageId: Optional[str]
    id: Optional[str]
    name: Optional[str]
