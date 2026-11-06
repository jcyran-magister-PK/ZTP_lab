from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Numeric, ForeignKey

from data.database import Base


class ForbiddenNamesORM(Base):
    __tablename__ = "forbidden_names"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)


class CategoriesORM(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    min_price: Mapped[float] = mapped_column(Numeric(10, 2))
    max_price: Mapped[float] = mapped_column(Numeric(10, 2))
    products: Mapped[list["ProductORM"]] = relationship(back_populates="category")


class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[CategoriesORM] = relationship(
        back_populates="products", 
        foreign_keys=[category_id],
    )
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    stock: Mapped[int] = mapped_column(Integer)
