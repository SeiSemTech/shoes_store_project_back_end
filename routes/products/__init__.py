from fastapi import APIRouter
from routes.products.category import app_category
from routes.products.configuration import app_configuration
from routes.products.product import app_product
from routes.products.product_configuration import app_product_configuration

app_products = APIRouter()

app_products.include_router(app_category)
app_products.include_router(app_configuration)
app_products.include_router(app_product)
app_products.include_router(app_product_configuration)
