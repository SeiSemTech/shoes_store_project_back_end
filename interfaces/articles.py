from pydantic import BaseModel

class Category(BaseModel):
    name: str
    status: int
    displayOrder: int
    image: str

class Product(BaseModel):
    name: str
    image: str
    price: int
    status: int
    description: str
    stockQuantity: int
    categoryId: int

class Configuration(BaseModel):
    name: str
    subConfiguratuion: str
    extraPrice: int
    minConfiguration: int
    maxConfiguration: int

class ProductConfiguration(BaseModel):
    productId: int
    configurationId: int
    configDisplayOrder: int
    subConfigDisplayOrder: int
