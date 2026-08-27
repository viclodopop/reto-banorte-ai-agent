from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz", tags=["Health"])
def health_check():
    """Endpoint ligero para liveness y readiness probes."""
    return {"status": "ok", "message": "Microservicio RAG operando correctamente."}