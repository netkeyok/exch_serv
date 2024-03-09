from typing import List, Optional
from pydantic import BaseModel


class Warehouse(BaseModel):

    storageId: Optional[str]
    id: Optional[str]
    name: Optional[str]
