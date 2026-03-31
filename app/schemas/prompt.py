"""
app/schemas/prompt.py
----------------------
Schemas Pydantic para validação dos dados de entrada relacionados a prompts.

`PromptRequest` é o schema utilizado pelo endpoint POST /api/v1/prompt e
herda os campos base de `PromptBase`, adicionando suporte a opções extras
específicas por provedor.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class PromptBase(BaseModel):
    """
    Campos base compartilhados por todos os schemas de prompt.

    @field prompt      - Texto obrigatório a ser processado pelo LLM (mín. 1 char).
    @field temperature - Controla a criatividade da resposta; varia de 0.0 a 2.0.
    @field max_tokens  - Limite de tokens na resposta gerada (deve ser > 0).
    """

    prompt: str = Field(
        ...,
        min_length=1,
        description="Texto do prompt a ser processado pelo LLM.",
    )
    temperature: Optional[float] = Field(
        0.7,
        ge=0.0,
        le=2.0,
        description="Controla a criatividade do modelo (0.0 a 2.0).",
    )
    max_tokens: Optional[int] = Field(
        500,
        gt=0,
        description="Número máximo de tokens na resposta.",
    )


class PromptRequest(PromptBase):
    """
    Schema completo de requisição para o endpoint POST /api/v1/prompt.

    Estende `PromptBase` com um campo opcional para parâmetros adicionais
    específicos do provedor de LLM (ex.: system prompt, stop sequences).

    @field provider_options - Dict livre com opções extras do provedor (opcional).
    """

    provider_options: Optional[Dict[str, Any]] = Field(
        None,
        description="Opções extras específicas do provedor (opcional).",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt": "Explique o que é FastAPI em poucas palavras.",
                "temperature": 0.5,
                "max_tokens": 150,
            }
        }
    }
