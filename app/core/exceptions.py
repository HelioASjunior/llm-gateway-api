"""
app/core/exceptions.py
----------------------
Define a hierarquia de exceções personalizadas do serviço de LLM.

Todas as exceções estendem HTTPException do FastAPI, garantindo que o
framework serialize automaticamente a resposta de erro com o status HTTP
correto e o campo `detail` padronizado.

Hierarquia:
    LLMServiceException          ← erro genérico 500
    ├── ProviderNotConfiguredException  ← provedor sem credenciais
    └── ExternalAPIException            ← falha na chamada à API remota
"""

from fastapi import HTTPException, status


class LLMServiceException(HTTPException):
    """
    Exceção base para todos os erros relacionados ao serviço de LLM.

    Retorna HTTP 500 com a mensagem fornecida no campo `detail`.

    @param detail - Mensagem de erro legível pelo cliente.
    """

    def __init__(self, detail: str = "Ocorreu um erro no processamento do LLM"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class ProviderNotConfiguredException(LLMServiceException):
    """
    Lançada quando o provedor de LLM selecionado não possui as credenciais
    ou configurações mínimas necessárias (ex.: OPENAI_API_KEY ausente).

    @param provider - Nome do provedor mal configurado (ex.: "openai").
    """

    def __init__(self, provider: str):
        super().__init__(
            detail=(
                f"O provedor '{provider}' não está configurado corretamente. "
                "Verifique as chaves de API e configurações."
            )
        )


class ExternalAPIException(LLMServiceException):
    """
    Lançada quando a chamada HTTP a uma API externa (OpenAI, Ollama, etc.)
    falha por qualquer motivo (timeout, erro de rede, resposta inválida).

    @param message - Mensagem de erro originada pela exceção capturada.
    """

    def __init__(self, message: str):
        super().__init__(detail=f"Erro na API externa: {message}")
