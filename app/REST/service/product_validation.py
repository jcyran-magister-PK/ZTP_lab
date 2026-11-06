from app.REST.data.forbidden_name_repository import get_forbidden_name_by_name
from app.REST.data.category_repository import get_category_by_id
from app.REST.data.product_repository import get_product_by_id, get_product_by_name
from app.REST.model.product_schema import ProductCreate
from sqlalchemy.orm import Session

class ValidationError(Exception):
    pass

class ConflictError(Exception):
    pass

class ResourceNotFoundError(Exception):
    pass


def validate_product_exists_id(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)

    if not product:
        raise ResourceNotFoundError("Nie ma produktu o takim ID.")

    return product


def validate_product_exists_name(db: Session, product_name: str):
    product = get_product_by_name(db, product_name)

    if not product:
        raise ResourceNotFoundError("Nie ma produktu o takiej nazwie.")

    return product


def validate_category_exists_id(db: Session, category_id: int):
    category = get_category_by_id(db, category_id)

    if not category:
        raise ResourceNotFoundError("Nie ma kategorii o takim ID.")

    return category


def validate_product_name_length(product_name: str):
    if not (3 <= len(product_name) <= 20):
        raise ValidationError("Nazwa produktu musi mieć długość od 3 do 20 znaków.")


def validate_product_name_alphanumeric(product_name: str):
    if not product_name.replace(" ", "").isalnum():
        raise ValidationError("Nazwa produktu może zawierać wyłącznie litery i cyfry.")


def validate_product_price(db: Session, category_id: int, product_price: float):
    category = validate_category_exists_id(db, category_id)

    if not (category.min_price <= product_price <= category.max_price):
        raise ValidationError(f"Cena produktu w kategorii {category.name} musi się mieścić " +
                              f"w przedziale {category.min_price} do {category.max_price}.")


def validate_product_stock(product_stock: int):
    if product_stock < 0:
        raise ValidationError("Ilość dostępnych sztuk produktu musi być większa od zera.")


def validate_product_name_forbidden(db: Session, product_name: str):
    if get_forbidden_name_by_name(db, product_name):
        raise ValidationError("Nazwa znajduje się w rejestrze zakazanych nazw.")


def validate_product_values(db: Session, product: ProductCreate):
    if product.category_id is not None:
        validate_category_exists_id(db, product.category_id)

        if product.price is not None:
            validate_product_price(db, product.category_id, product.price)

    if product.name is not None:
        validate_product_name_length(product.name)
        validate_product_name_alphanumeric(product.name)
        validate_product_name_forbidden(db, product.name)

    if product.stock is not None:
        validate_product_stock(product.stock)

