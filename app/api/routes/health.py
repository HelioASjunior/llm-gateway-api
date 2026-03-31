"""
app/api/routes/health.py
-------------------------
Rota de health check da aplicação.

Usada por orquestradores (Kubernetes, Docker Compose) e ferramentas de
monitoramento para verificar se a API está online e respondendo.
"""

from fastapi import APIRouter

from app.schemas.response import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Monitoramento"])
async def check_health():
    """
    Verifica o status operacional da aplicação.

    Retorna informações estáticas de versão e estado dos subsistemas.
    Útil para probes de liveness/readiness em ambientes containerizados.

    @returns HealthResponse com status "ok", versão da API e detalhes do ambiente.
    """
    return {
        "status": "ok",
        "version": "1.0.0",
        "details": {
            "uptime": "online",
            "database": "in-memory (portfólio)",
        },
    }
