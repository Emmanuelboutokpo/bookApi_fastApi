from fastapi import FastAPI
from src.api.routes import router
app = FastAPI(
    title="Book API",
    description="A simple API to manage a collection of books", 
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

