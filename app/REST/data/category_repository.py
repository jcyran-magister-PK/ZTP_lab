from sqlalchemy.orm import Session
from sqlalchemy import select

from app.REST.model.product_orm import CategoriesORM
from app.db.database import Base, engine


def create_tables():
    Base.metadata.create_all(engine)


def get_all_categories(db: Session):
    query = select(CategoriesORM)
    result = db.execute(query)
    return result.scalars().all()


def get_category_by_id(db: Session, id: int):
    query = select(CategoriesORM).where(CategoriesORM.id == id)
    result = db.execute(query).scalars().all()

    try:
        return result[0]
    except:
        return None
