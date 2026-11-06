from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ProductHistoryEntry(BaseModel):
    id: int
    product_id: int
    action: str
    previous_state: dict[str, Any]
    current_state: dict[str, Any]
    changed_at: datetime

    model_config = ConfigDict(from_attributes=True)
