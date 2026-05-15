from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api.v1.router import router as v1_router
from src.infrastructure.config.settings import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Car Insurance Premium Simulator",
        description="Calculates car insurance premiums based on car age, value, deductible and broker fee",
        version="0.1.0",
        lifespan=lifespan
    )

    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/health", tags=["health"], summary="Health check")
    async def health() -> JSONResponse:
        return JSONResponse({
            "status": "It's ok and aqui é galo!"
        })

    return app


app = create_app()
