from app.REST.web.routes import router as products_router
from fastapi import FastAPI

products_docs_app = FastAPI(
    title="Products API",
    docs_url="/",
    redoc_url=None,
    openapi_url="/openapi.json"
)

products_docs_app.include_router(products_router)
