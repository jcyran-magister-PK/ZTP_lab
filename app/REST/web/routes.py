from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from model.history_schema import ProductHistoryEntry
from service.product_validation import ConflictError, ResourceNotFoundError, ValidationError
from service.product_history_service import list_history
from service.product_service import create_product, list_products, remove_product, replace_product
from data.database import get_db
from model.product_schema import Product, ProductCreate


router = APIRouter()


@router.get("/api/v1/products", response_model=list[Product])
def get_products_endpoint(db: Session = Depends(get_db)):
    return list_products(db)


@router.get("/api/v1/products/{id}")
def get_product_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    try:
        return list_products(db, id)
    except ResourceNotFoundError as err:
        raise HTTPException(status_code=404, detail=repr(err))


@router.post("/api/v1/products", response_model=Product, status_code=201)
def post_product_endpoint(payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_product(db, payload)
    except ResourceNotFoundError as err:
        raise HTTPException(status_code=404, detail=repr(err))
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=repr(err))
    except ConflictError as err:
        raise HTTPException(status_code=409, detail=repr(err))


@router.put("/api/v1/products/{id}", response_model=Product, status_code=201)
def put_product_endpoint(id: int, payload: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = replace_product(db, id, payload)
    except ResourceNotFoundError as err:
        raise HTTPException(status_code=404, detail=repr(err))
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=repr(err))

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.delete("/api/v1/products/{id}", status_code=204)
def delete_product_endpoint(id: int, db: Session = Depends(get_db)):
    try:
        if not remove_product(db, id):
            raise HTTPException(status_code=404, detail="Product not found")
    except ResourceNotFoundError as err:
        raise HTTPException(status_code=404, detail=repr(err))
    
    return Response(status_code=204)



@router.get("/api/v1/products/{id}/history", response_model=list[ProductHistoryEntry])
def get_product_history_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    history = list_history(db, id)

    if not history:
        raise HTTPException(status_code=404, detail="History for this product not found")

    return history
