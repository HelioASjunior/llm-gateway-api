from fastapi import APIRouter, Depends, Query
from typing import List
from app.schemas.prompt import PromptRequest
from app.schemas.response import LLMResponse
from app.services.llm_service import llm_service
from app.services.history_service import history_service
from app.models.interaction import InteractionRecord

router = APIRouter()

@router.post("/prompt", response_model=LLMResponse, tags=["LLM"])
async def send_prompt(request: PromptRequest):
    """
    Envia um prompt ao LLM e retorna a resposta gerada.
    
    A resposta é gerada através do provedor configurado no ambiente (.env).
    """
    response = await llm_service.process_prompt(request)
    
    # Registra a interação no histórico (persistência simulada)
    history_service.add_interaction(
        prompt=request.prompt,
        response_text=response.text,
        provider=response.provider,
        model=response.model_name
    )
    
    return response

@router.get("/history", response_model=List[InteractionRecord], tags=["LLM"])
async def get_history(limit: int = Query(10, gt=0, le=50)):
    """
    Retorna o histórico recente de interações com o LLM.
    
    O histórico é mantido em memória para fins de demonstração.
    """
    history_data = history_service.get_recent_history(limit)
    return [InteractionRecord(**item) for item in history_data]
