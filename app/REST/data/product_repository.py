from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

from model.product_orm import ProductORM
from data.database import Base, engine

def create_tables():
    Base.metadata.create_all(engine)

def get_all_products(db: Session):
    query = (
        select(ProductORM)
            .options(
                joinedload(ProductORM.category)
            )
    )
    result = db.execute(query)
    return result.scalars().all()

def get_product_by_id(db: Session, id: int):
    query = select(ProductORM).where(ProductORM.id == id)
    result = db.execute(query).scalars().all()

    try:
        return result[0]
    except:
        return None

def get_product_by_name(db: Session, name: str):
    query = select(ProductORM).where(ProductORM.name == name)
    result = db.execute(query).scalars().all()

    try:
        return result[0]
    except:
        return None

def add_product(db: Session, product: ProductORM):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def save_product(db: Session, product_data: ProductORM):
    db.commit()
    db.refresh(product_data)
    
    return product_data

def delete_product(db: Session, product: ProductORM):
    db.delete(product)
    db.commit()
