from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from DB import *
from tarjimani.lang2lang import create_models, translate



create_database()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
translation_models = {}


class CustomerCreate(BaseModel):
    name: str
    phone: str
    email: Optional[str] = "none@none.none"


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class ProductCreate(BaseModel):
    name: str
    price: float
    stock_quantity: int = 1
    latitude: float
    longitude: float
    category: str
    item: str
    description: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    category: Optional[str] = None
    item: Optional[str] = None
    description: Optional[str] = None


class TranslateRequest(BaseModel):
    text: str
    lang_from: str
    lang_to: str


@app.get("/")
def root():
    return {"message": "Store API with Translation"}


@app.post("/customers")
def create_customer(customer: CustomerCreate):
    try:
        customers_insert_one(customer.name, customer.phone, customer.email)
        return {"message": "Customer created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/customers")
def get_customers():
    customers = customers_get_many()
    return {"customers": customers}


@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = customers_get_one(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"customer": customer}


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: CustomerUpdate):
    try:
        customers_update_one(customer_id, name=customer.name, phone=customer.phone, email=customer.email)
        return {"message": "Customer updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    try:
        customers_delete_one(customer_id)
        return {"message": "Customer deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/products")
def create_product(product: ProductCreate):
    try:
        products_insert_one(
            product.name,
            product.price,
            product.stock_quantity,
            product.latitude,
            product.longitude,
            product.category,
            product.item,
            product.description
        )
        return {"message": "Product created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/products")
def get_products(category: Optional[str] = None):
    if category:
        products = products_get_many("category = ?", (category,))
    else:
        products = products_get_many()
    return {"products": products}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = products_get_one(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"product": product}


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    try:
        products_update_one(
            product_id,
            name=product.name,
            price=product.price,
            stock_quantity=product.stock_quantity,
            latitude=product.latitude,
            longitude=product.longitude,
            category=product.category,
            item=product.item,
            description=product.description
        )
        return {"message": "Product updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    try:
        products_delete_one(product_id)
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/translate")
def translate_text(request: TranslateRequest):
    cache_key = f"{request.lang_from}_{request.lang_to}"

    if cache_key not in translation_models:
        result = create_models(request.lang_from, request.lang_to)
        if result == "<unsupported_language_pair>":
            raise HTTPException(status_code=400, detail="Unsupported language pair")
        translation_models[cache_key] = result

    (tokenizer_send, model_send), _ = translation_models[cache_key]
    translated = translate(request.text, tokenizer_send, model_send)

    return {"translated_text": translated}


@app.get("/supported-languages")
def supported_languages():
    return {
        "pairs": [
            {"from": "en", "to": "ka"},
            {"from": "ka", "to": "en"},
            {"from": "en", "to": "ru"},
            {"from": "ru", "to": "en"}
        ]
    }