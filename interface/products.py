from pydantic import BaseModel

class Category(BaseModel):
    id: int
    name: str
    status: int
    display_order: int


class Product(BaseModel):
    id: int
    name: str
    status: int
    image: str
    price: int
    description: str
    category_id: int
    display_order: int

class ProductId(BaseModel): # Interface creada para consulta
    id: int

class Configuration(BaseModel):
    id: int
    name: str
    sub_configuratuion: str
    extra_price: int


class ProductConfiguration(BaseModel):
    id: int
    product_id: int
    configuration_id: int
    config_display_order: int
    sub_config_display_order: int
    stock: int
