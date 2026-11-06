from typing import Optional

from app.REST.service.product_history_service import append_history
from app.REST.model.product_orm import ProductORM
from app.REST.service.product_validation import ConflictError, ResourceNotFoundError, validate_category_exists_id, validate_product_exists_id, validate_product_exists_name, validate_product_values
from sqlalchemy.orm import Session
from app.REST.data.product_repository import add_product, delete_product, get_all_products, save_product
from app.REST.model.product_schema import ProductCreate


def list_products(db: Session, id: Optional[int]=None):
    return validate_product_exists_id(db, id) if id else get_all_products(db)


def create_product(db: Session, payload: ProductCreate):
    try:
        validate_product_exists_name(db, payload.name)

        raise ConflictError("Produkt z taką nazwą już istnieje.")
    except ResourceNotFoundError:
        pass
    
    validate_product_values(db, payload)

    validate_category_exists_id(db, payload.category_id)

    product = ProductORM(
        name=payload.name,
        category_id=payload.category_id,
        price=payload.price,
        stock=payload.stock,
    )

    db_product = None

    with append_history(db, product, "create"):
        db_product = add_product(db, product)

    return db_product


def replace_product(db: Session, product_id: int, payload: ProductCreate):
    product = validate_product_exists_id(db, product_id)
    validate_product_values(db, payload)

    product.name = payload.name
    product.category_id = payload.category_id
    product.price = payload.price
    product.stock = payload.stock

    db_product = None

    with append_history(db, product, "update"):
        db_product = save_product(db, product)

    return db_product


def remove_product(db: Session, product_id: int):
    product = validate_product_exists_id(db, product_id)

    if product is None:
        return False

    with append_history(db, product, "delete"):
        delete_product(db, product)
        product = None

    return True

