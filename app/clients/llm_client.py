from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
from openai import OpenAI
from app.core.config import settings
from app.core.exceptions import ProviderNotConfiguredException, ExternalAPIException

class LLMClient(ABC):
    """Interface abstrata para clientes de provedores de LLM."""
    
    @abstractmethod
    async def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> Dict[str, Any]:
        """Gera uma resposta baseada em um prompt."""
        pass

class OpenAIClient(LLMClient):
    """Cliente para integração com a OpenAI API."""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ProviderNotConfiguredException("openai")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> Dict[str, Any]:
        try:
            # Nota: Usando execução síncrona dentro de thread se necessário, 
            # mas para portfólio, simplificamos com a lib oficial
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return {
                "text": response.choices[0].message.content,
                "model_name": self.model,
                "provider": "openai",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            raise ExternalAPIException(str(e))

class OllamaClient(LLMClient):
    """Cliente para integração com Ollama (local)."""
    
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL
        self.model = settings.OLLAMA_MODEL

    async def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> Dict[str, Any]:
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
                            "num_predict": max_tokens
                        }
                    },
                    timeout=60.0
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
                        "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                    }
                }
            except Exception as e:
                raise ExternalAPIException(str(e))

class MockLLMClient(LLMClient):
    """Cliente Mock para testes e demonstração sem custos de API."""
    
    async def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 500) -> Dict[str, Any]:
        return {
            "text": f"Esta é uma resposta simulada para o prompt: '{prompt[:30]}...'",
            "model_name": "mock-gpt-3.5",
            "provider": "mock",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
        }

def get_llm_client() -> LLMClient:
    """Factory para obter o cliente de LLM configurado."""
    provider = settings.LLM_PROVIDER.lower()
    if provider == "openai":
        return OpenAIClient()
    elif provider == "ollama":
        return OllamaClient()
    return MockLLMClient()
