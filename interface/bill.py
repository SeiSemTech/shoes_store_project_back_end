from typing import Optional
from pydantic import BaseModel


class Bill(BaseModel):
    id: Optional[int] = None
    id_user: int
    date: str
    total_quantity: float
    total_price: float

class BillDescription(BaseModel):
    id_bill: int
    id_product_config: int
    product_name: str
    description: str
    quantity: int
    price: float
    total: float

class BillFront(BaseModel):
    product_id: int
    stock: int
    price: float