"""
app/services/llm_service.py
----------------------------
Camada de serviço (regras de negócio) para o processamento de prompts.

`LLMService` orquestra a chamada ao cliente de LLM e converte o resultado
bruto (dict) no schema Pydantic `LLMResponse`, mantendo o controller
(route handler) livre de lógica de negócio.
"""

from app.clients.llm_client import LLMClient, get_llm_client
from app.schemas.prompt import PromptRequest
from app.schemas.response import LLMResponse
from loguru import logger


class LLMService:
    """
    Serviço de negócio responsável por processar requisições de prompt.

    Recebe um `PromptRequest`, delega a geração ao `LLMClient` configurado
    e retorna um `LLMResponse` validado pelo Pydantic.
    """

    def __init__(self, client: LLMClient = None):
        """
        Inicializa o serviço com o cliente de LLM fornecido ou com o
        cliente padrão obtido pela fábrica `get_llm_client()`.

        @param client - Instância opcional de LLMClient (útil em testes).
        """
        self.client = client or get_llm_client()

    async def process_prompt(self, request: PromptRequest) -> LLMResponse:
        """
        Processa um prompt recebido via requisição HTTP e retorna a resposta
        formatada segundo o schema `LLMResponse`.

        Fluxo:
          1. Loga o início do processamento com os primeiros 50 chars do prompt.
          2. Chama `client.generate_response` com os parâmetros da requisição.
          3. Desempacota o dict de resposta no schema Pydantic.

        @param request - Objeto `PromptRequest` com prompt, temperature e max_tokens.
        @returns LLMResponse com text, model_name, provider, usage e timestamp.
        """
        logger.info(
            f"Processando prompt: '{request.prompt[:50]}...' "
            f"via provedor: {self.client.__class__.__name__}"
        )

        response_data = await self.client.generate_response(
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        return LLMResponse(**response_data)


# Instância singleton — reutilizada em todas as requisições para evitar
# recriação desnecessária do cliente de LLM a cada chamada
llm_service = LLMService()
