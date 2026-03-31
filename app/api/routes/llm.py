"""
app/api/routes/llm.py
----------------------
Rotas HTTP relacionadas à interação com o LLM e ao histórico de requisições.

Endpoints expostos:
  POST /api/v1/prompt   → envia um prompt ao LLM e retorna a resposta gerada.
  GET  /api/v1/history  → retorna as interações mais recentes registradas.
"""

from typing import List

from fastapi import APIRouter, Query

from app.models.interaction import InteractionRecord
from app.schemas.prompt import PromptRequest
from app.schemas.response import LLMResponse
from app.services.history_service import history_service
from app.services.llm_service import llm_service

router = APIRouter()


@router.post("/prompt", response_model=LLMResponse, tags=["LLM"])
async def send_prompt(request: PromptRequest):
    """
    Envia um prompt ao LLM configurado e retorna a resposta gerada.

    Após obter a resposta, registra automaticamente a interação no serviço
    de histórico para consulta futura via GET /history.

    @param request - Corpo da requisição com prompt, temperature e max_tokens.
    @returns LLMResponse com o texto gerado, metadados do modelo e uso de tokens.
    """
    response = await llm_service.process_prompt(request)

    # Persiste a interação no histórico em memória após geração bem-sucedida
    history_service.add_interaction(
        prompt=request.prompt,
        response_text=response.text,
        provider=response.provider,
        model=response.model_name,
    )

    return response


@router.get("/history", response_model=List[InteractionRecord], tags=["LLM"])
async def get_history(limit: int = Query(10, gt=0, le=50)):
    """
    Retorna o histórico recente de interações com o LLM.

    O histórico é mantido em memória e zerado a cada reinicialização da API.

    @param limit - Número de registros a retornar (mín: 1, máx: 50, padrão: 10).
    @returns Lista de InteractionRecord ordenada do mais antigo ao mais recente.
    """
    history_data = history_service.get_recent_history(limit)
    return [InteractionRecord(**item) for item in history_data]
