from sqlalchemy.orm import Session
from sqlalchemy import desc, select

from model.history_orm import ProductHistoryORM
from data.database import Base, engine


def create_tables():
    Base.metadata.create_all(engine)


def get_product_history_by_product_id(db: Session, product_id: int):
    query = (
        select(ProductHistoryORM)
        .where(ProductHistoryORM.product_id == product_id)
        .order_by(
            desc(ProductHistoryORM.changed_at), 
            desc(ProductHistoryORM.id)
        ) 
    )

    result = db.execute(query)
    return result.scalars().all()


def add_product_history(db: Session, history_entry: ProductHistoryORM):
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry
