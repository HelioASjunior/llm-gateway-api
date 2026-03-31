from typing import Dict, Any
from app.clients.llm_client import LLMClient, get_llm_client
from app.schemas.prompt import PromptRequest
from app.schemas.response import LLMResponse
from loguru import logger

class LLMService:
    """Serviço de negócio para interações com LLM."""
    
    def __init__(self, client: LLMClient = None):
        self.client = client or get_llm_client()

    async def process_prompt(self, request: PromptRequest) -> LLMResponse:
        """Processa um prompt e retorna uma resposta formatada."""
        logger.info(f"Processando prompt: '{request.prompt[:50]}...' via provedor: {self.client.__class__.__name__}")
        
        # Chama o cliente para obter a resposta do modelo
        response_data = await self.client.generate_response(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Cria e retorna o objeto de resposta baseado no schema Pydantic
        return LLMResponse(**response_data)

# Singleton do serviço
llm_service = LLMService()
