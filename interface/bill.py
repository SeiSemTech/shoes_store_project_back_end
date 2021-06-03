from typing import Optional, List
from pydantic import BaseModel

from interface.products import CustomerProducts


class Bill(BaseModel):
    id: Optional[int] = None
    id_user: int
    date: str
    total_quantity: float
    total_price: float


class BillDescription(BaseModel):
    id_bill: int
    id_product_config: int
    quantity: int
    price: float


class BillFront(BaseModel):
    id_product_config: int
    quantity: int
    price: float


class BillCustomerOrder(BaseModel):
    order: List[CustomerProducts]



