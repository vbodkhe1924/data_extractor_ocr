# app/models/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class InvoiceOutput(BaseModel):
    document_id: str
    vendor_name: str
    invoice_number: str
    date: str
    total: float
    line_items: List[LineItem]
    raw_text: Optional[str]