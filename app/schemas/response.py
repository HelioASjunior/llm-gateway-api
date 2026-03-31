from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class LLMResponse(BaseModel):
    """Modelo de resposta gerado pelo serviço de LLM."""
    text: str = Field(..., description="O conteúdo gerado pelo modelo.")
    model_name: str = Field(..., description="Nome do modelo utilizado.")
    provider: str = Field(..., description="Nome do provedor utilizado.")
    usage: Optional[Dict[str, int]] = Field(None, description="Estatísticas de uso de tokens.")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Horário em que a resposta foi gerada.")

class HealthResponse(BaseModel):
    """Modelo de resposta para o endpoint de health check."""
    status: str = Field(..., description="Status atual da API (ex: 'ok', 'degraded').")
    version: str = Field(..., description="Versão atual da API.")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes adicionais de status.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "version": "1.0.0",
                "details": {"uptime": "10h", "database": "connected"}
            }
        }
    }
