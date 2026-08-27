from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as chat_router
from app.api.health import router as health_router
from app.config.settings import settings
import logging


def configure_logging() -> None:
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="API del Agente CV de Víctor Molina, compatible con Open Responses.",
        docs_url="/docs",
        redoc_url=None
    )

    # Permitimos peticiones cruzadas (CORS) para evitar bloqueos del frontend de Banorte
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En un entorno real estricto, esto se limita al dominio del banco
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inyección de rutas
    app.include_router(health_router)
    app.include_router(chat_router, prefix="/v1")

    return app

app = create_app()