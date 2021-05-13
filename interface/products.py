from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: Optional[int] = None
    name: str
    status: int
    display_order: int


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    status: int
    image: str
    price: int
    description: str
    category_id: int
    display_order: int


class Configuration(BaseModel):
    id: Optional[int] = None
    name: str
    sub_configuration: str
    extra_price: int


class ProductConfiguration(BaseModel):
    id: Optional[int] = None
    product_id: int
    configuration_id: int
    config_display_order: int
    sub_config_display_order: int
    stock: int
