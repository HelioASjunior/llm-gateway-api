"""
app/models/interaction.py
--------------------------
Modelo de domínio que representa uma interação armazenada no histórico.

`InteractionRecord` é o schema de saída do endpoint GET /api/v1/history e
espelha a estrutura dos dicts gerados por `HistoryService.add_interaction`.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class InteractionRecord(BaseModel):
    """
    Representa um registro completo de uma interação com o LLM.

    @field id        - Identificador sequencial único da interação.
    @field prompt    - Texto original enviado pelo usuário.
    @field response  - Resposta gerada pelo LLM.
    @field provider  - Provedor utilizado na geração (ex.: "openai").
    @field model     - Modelo específico utilizado (ex.: "gpt-3.5-turbo").
    @field timestamp - Data e hora UTC do registro da interação.
    """

    id: int = Field(..., description="ID sequencial da interação.")
    prompt: str = Field(..., description="Prompt original enviado pelo usuário.")
    response: str = Field(..., description="Resposta gerada pelo LLM.")
    provider: str = Field(..., description="Provedor utilizado (ex: OpenAI).")
    model: str = Field(..., description="Nome do modelo utilizado.")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Horário do registro.",
    )
