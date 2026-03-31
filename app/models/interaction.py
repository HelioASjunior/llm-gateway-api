from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class InteractionRecord(BaseModel):
    """Modelo de dado para representar uma interação registrada."""
    id: int = Field(..., description="ID sequencial da interação.")
    prompt: str = Field(..., description="Prompt original enviado pelo usuário.")
    response: str = Field(..., description="Resposta gerada pelo LLM.")
    provider: str = Field(..., description="Provedor utilizado (ex: OpenAI).")
    model: str = Field(..., description="Nome do modelo utilizado.")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Horário do registro.")
