from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from starlette.middleware.cors import CORSMiddleware
from src.core.db import engine
from src.core.logging import setup_logging
from src.utils.class_object import singleton
from src.core.config import BACKEND_CORS_ORIGINS
from src.api.core_import.router import router as import_router
from src.api.datasources.router import router as datasources_router
from src.api.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


@singleton
class AppCreator:
    def __init__(self):
        setup_logging()

        self.app = FastAPI(
            title="Data Management Service",
            lifespan=lifespan,
        )
        # store engine on app state if needed elsewhere
        self.app.state.engine = engine

        if BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                # allow_origins=BACKEND_CORS_ORIGINS,  # type: ignore
                allow_origins=["http://localhost:3000"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        @self.app.get("/")
        def root():
            return {"message": "Service is working"}

        @self.app.get("/health")
        async def health_check():
            try:
                async with engine.connect() as connection:
                    await connection.execute(text("SELECT 1"))
                return {"status": "PostgreSQL is connected"}
            except Exception as e:
                return {"status": "PostgreSQL connection failed", "error": str(e)}

        self.app.include_router(auth_router)
        self.app.include_router(import_router)
        self.app.include_router(datasources_router)


app_creator = AppCreator()
app = app_creator.app
