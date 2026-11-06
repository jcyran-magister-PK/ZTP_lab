from contextlib import contextmanager

from sqlalchemy.orm import Session
from app.REST.data.product_history_repository import add_product_history, get_product_history_by_product_id
from app.REST.model.history_orm import ProductHistoryORM
from app.REST.model.product_orm import ProductORM


from contextlib import contextmanager
from sqlalchemy.orm import Session

def _build_product_snapshot(product: ProductORM) -> dict:
    category = product.category
    
    category_data = {}
    if category:
        category_data = {
            "id": category.id,
            "name": category.name,
            "min_price": float(category.min_price) if category.min_price is not None else None,
            "max_price": float(category.max_price) if category.max_price is not None else None,
        }

    return {
        "id": product.id,
        "name": product.name,
        "category": category_data,
        "price": float(product.price) if product.price is not None else None,
        "stock": product.stock,
    }


def _save_product_history(
    db: Session,
    product_id: int | None,
    previous_state: dict,
    current_state: dict,
    action: str,
):
    history_entry = ProductHistoryORM(
        product_id=product_id,
        action=action,
        previous_state=previous_state,
        current_state=current_state,
    )

    return add_product_history(db, history_entry)


@contextmanager
def append_history(db: Session, product: ProductORM, action: str):
    if product.id is None:
        previous_state = {}
    else:
        previous_state = _build_product_snapshot(product)

    saved_product_id = product.id

    try:
        yield product
    finally:
        if action == "delete":
            current_state = {}
        else:
            current_state = _build_product_snapshot(product)
            saved_product_id = product.id

        _save_product_history(
            db,
            saved_product_id,
            previous_state,
            current_state,
            action,
        )

def list_history(db: Session, id: int):
    return get_product_history_by_product_id(db, id)
