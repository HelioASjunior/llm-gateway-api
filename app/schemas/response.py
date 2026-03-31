"""
app/schemas/response.py
------------------------
Schemas Pydantic para as respostas da API.

`LLMResponse`   → resposta do endpoint POST /api/v1/prompt.
`HealthResponse` → resposta do endpoint GET /api/v1/health.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """
    Resposta padronizada gerada pelo serviço de LLM.

    @field text       - Conteúdo textual gerado pelo modelo.
    @field model_name - Identificador do modelo usado (ex.: "gpt-3.5-turbo").
    @field provider   - Nome do provedor (ex.: "openai", "ollama", "mock").
    @field usage      - Estatísticas de consumo de tokens (prompt, completion, total).
    @field timestamp  - Momento UTC em que a resposta foi gerada.
    """

    text: str = Field(..., description="O conteúdo gerado pelo modelo.")
    model_name: str = Field(..., description="Nome do modelo utilizado.")
    provider: str = Field(..., description="Nome do provedor utilizado.")
    usage: Optional[Dict[str, int]] = Field(
        None, description="Estatísticas de uso de tokens."
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Horário em que a resposta foi gerada.",
    )


class HealthResponse(BaseModel):
    """
    Resposta do endpoint de health check.

    @field status  - Estado da API ("ok", "degraded", etc.).
    @field version - Versão atual da API em formato semântico.
    @field details - Informações adicionais sobre subsistemas (uptime, database, etc.).
    """

    status: str = Field(..., description="Status atual da API (ex: 'ok', 'degraded').")
    version: str = Field(..., description="Versão atual da API.")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Detalhes adicionais de status."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
                "version": "1.0.0",
                "details": {"uptime": "10h", "database": "connected"},
            }
        }
    }
