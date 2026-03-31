from fastapi import HTTPException, status

class LLMServiceException(HTTPException):
    """Exceção base para erros relacionados ao serviço de LLM."""
    def __init__(self, detail: str = "Ocorreu um erro no processamento do LLM"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class ProviderNotConfiguredException(LLMServiceException):
    """Exceção para quando o provedor de LLM não está devidamente configurado."""
    def __init__(self, provider: str):
        super().__init__(detail=f"O provedor '{provider}' não está configurado corretamente. Verifique as chaves de API e configurações.")

class ExternalAPIException(LLMServiceException):
    """Exceção para falhas na comunicação com APIs externas."""
    def __init__(self, message: str):
        super().__init__(detail=f"Erro na API externa: {message}")
