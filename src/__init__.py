from fastapi import FastAPI
from src.api.book import router
from src.api.user import auth_router
from src.core.db import engine, init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Démarrage de l'application...")
    await init_db()
    yield
    print("Arrêt de l'application...")
    await engine.dispose()

app = FastAPI(
    title="Book API",
    description="A simple API to manage a collection of books", 
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")

