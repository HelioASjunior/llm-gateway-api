"""
app/clients/llm_client.py
--------------------------
Camada de integração com provedores de LLM.

Define a interface abstrata `LLMClient` e suas implementações concretas:
  - OpenAIClient  → API da OpenAI (cloud)
  - OllamaClient  → Ollama rodando localmente via HTTP
  - MockLLMClient → resposta simulada para testes/demo sem custo

A função de fábrica `get_llm_client()` seleciona a implementação correta com
base na variável de ambiente `LLM_PROVIDER`.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any

import httpx
from openai import OpenAI

from app.core.config import settings
from app.core.exceptions import ProviderNotConfiguredException, ExternalAPIException


class LLMClient(ABC):
    """
    Interface abstrata para clientes de provedores de LLM.

    Todas as implementações concretas devem implementar `generate_response`,
    garantindo que o serviço de negócio (LLMService) seja independente do
    provedor escolhido (princípio de inversão de dependência).
    """

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> Dict[str, Any]:
        """
        Gera uma resposta textual a partir de um prompt.

        @param prompt      - Texto de entrada enviado ao modelo.
        @param temperature - Criatividade da geração (0.0 = determinístico, 2.0 = máximo).
        @param max_tokens  - Limite de tokens na resposta gerada.
        @returns Dict com as chaves: text, model_name, provider, usage.
        """


class OpenAIClient(LLMClient):
    """
    Implementação do cliente para a API da OpenAI.

    Requer que `OPENAI_API_KEY` esteja definida nas configurações; caso
    contrário, lança `ProviderNotConfiguredException` no construtor.
    """

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ProviderNotConfiguredException("openai")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> Dict[str, Any]:
        """
        Envia o prompt à API da OpenAI usando o endpoint de chat completions.

        @param prompt      - Texto do usuário enviado como mensagem de role "user".
        @param temperature - Controla a aleatoriedade da resposta.
        @param max_tokens  - Número máximo de tokens a serem gerados.
        @returns Dict padronizado com text, model_name, provider e usage.
        @raises ExternalAPIException se a chamada à API falhar.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            return {
                "text": response.choices[0].message.content,
                "model_name": self.model,
                "provider": "openai",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }
        except Exception as e:
            raise ExternalAPIException(str(e))


class OllamaClient(LLMClient):
    """
    Implementação do cliente para o Ollama (servidor local de LLMs open-source).

    Comunica-se com o servidor Ollama via HTTP REST. A URL base e o modelo são
    lidos de `settings.OLLAMA_BASE_URL` e `settings.OLLAMA_MODEL`.
    """

    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> Dict[str, Any]:
        """
        Envia o prompt ao endpoint `/api/generate` do Ollama e aguarda a resposta
        completa (stream=False).

        @param prompt      - Texto do usuário.
        @param temperature - Controla a aleatoriedade da geração.
        @param max_tokens  - Mapeado para `num_predict` nas opções do Ollama.
        @returns Dict padronizado com text, model_name, provider e usage.
        @raises ExternalAPIException se a requisição HTTP falhar.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens,
                        },
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "text": data.get("response", ""),
                    "model_name": self.model,
                    "provider": "ollama",
                    "usage": {
                        "prompt_tokens": data.get("prompt_eval_count", 0),
                        "completion_tokens": data.get("eval_count", 0),
                        "total_tokens": (
                            data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                        ),
                    },
                }
            except Exception as e:
                raise ExternalAPIException(str(e))


class MockLLMClient(LLMClient):
    """
    Implementação simulada do cliente de LLM.

    Retorna uma resposta estática sem realizar chamadas externas. Útil para
    testes locais, demonstrações e ambientes sem chaves de API configuradas.
    """

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> Dict[str, Any]:
        """
        Retorna uma resposta fictícia baseada nos primeiros 30 caracteres do prompt.

        @param prompt      - Texto de entrada (apenas os primeiros 30 chars são usados).
        @param temperature - Ignorado nesta implementação.
        @param max_tokens  - Ignorado nesta implementação.
        @returns Dict com valores fixos e usage simulado.
        """
        return {
            "text": f"Esta é uma resposta simulada para o prompt: '{prompt[:30]}...'",
            "model_name": "mock-gpt-3.5",
            "provider": "mock",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
        }


def get_llm_client() -> LLMClient:
    """
    Fábrica que instancia o cliente de LLM correspondente ao provedor configurado.

    Lê `settings.LLM_PROVIDER` e retorna a implementação adequada:
      - "openai"  → OpenAIClient
      - "ollama"  → OllamaClient
      - qualquer outro valor → MockLLMClient (fallback seguro)

    @returns Instância concreta de LLMClient pronta para uso.
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "openai":
        return OpenAIClient()
    elif provider == "ollama":
        return OllamaClient()

    # Fallback para mock quando o provedor não é reconhecido
    return MockLLMClient()
