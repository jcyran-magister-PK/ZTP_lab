from contextlib import asynccontextmanager
from fastapi import FastAPI
from threading import Thread

from app.notifications.docs_app import notifications_docs_app
from app.REST.docs_app import products_docs_app

from app.notifications.web.routes import router as notifications_router
from app.notifications.service.notification_worker import run_worker
from app.REST.web.routes import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = Thread(target=run_worker, daemon=True)
    thread.start()
    yield


app = FastAPI(
    title="Laboratorium 2 - Powiadomienia",
    lifespan=lifespan,
)

app.include_router(products_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")

app.mount("/products-docs", products_docs_app)
app.mount("/notifications-docs", notifications_docs_app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
