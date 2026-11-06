from sqlalchemy.orm import Session
from sqlalchemy import select

from app.REST.model.product_orm import ForbiddenNamesORM
from app.db.database import Base, engine


def create_tables():
    Base.metadata.create_all(engine)


def get_all_forbidden_names(db: Session):
    query = select(ForbiddenNamesORM)
    result = db.execute(query)
    return result.scalars().all()


def get_forbidden_name_by_id(db: Session, id: int):
    query = select(ForbiddenNamesORM).where(ForbiddenNamesORM.id == id)
    result = db.execute(query).scalars().all()

    try:
        return result[0]
    except:
        return None

def get_forbidden_name_by_name(db: Session, name: str):
    query = select(ForbiddenNamesORM).where(ForbiddenNamesORM.name == name)
    result = db.execute(query).scalars().all()

    try:
        return result[0]
    except:
        return None
