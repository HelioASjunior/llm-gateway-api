from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class PromptBase(BaseModel):
    """Modelo base para envio de prompts ao LLM."""
    prompt: str = Field(..., min_length=1, description="Texto do prompt a ser processado pelo LLM.")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Controla a criatividade do modelo (0.0 a 2.0).")
    max_tokens: Optional[int] = Field(500, gt=0, description="Número máximo de tokens na resposta.")

class PromptRequest(PromptBase):
    """Esquema de requisição para envio de prompts."""
    provider_options: Optional[Dict[str, Any]] = Field(None, description="Opções extras específicas do provedor (opcional).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt": "Explique o que é FastAPI em poucas palavras.",
                "temperature": 0.5,
                "max_tokens": 150
            }
        }
    }
