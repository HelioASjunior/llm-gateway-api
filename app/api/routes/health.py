from fastapi import APIRouter
from app.schemas.response import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
async def check_health():
    """
    Verifica o status da aplicação.
    Útil para monitoramento e orquestração (Kubernetes/Docker).
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "details": {
            "uptime": "online",
            "database": "in-memory (portfólio)"
        }
    }
