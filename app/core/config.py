"""
app/core/config.py
------------------
Carrega e expõe as configurações globais da aplicação a partir de variáveis de
ambiente (arquivo .env). Utiliza pydantic-settings para validação automática.

Uso:
    from app.core.config import settings
    print(settings.OPENAI_API_KEY)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """
    Configurações globais da aplicação.

    Todos os campos são lidos automaticamente a partir de variáveis de ambiente
    ou do arquivo .env na raiz do projeto. Os valores abaixo são os defaults
    usados quando a variável não está definida.
    """

    # Metadados da API
    PROJECT_NAME: str = "LLM Portfolio API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Provedor de LLM ativo ("openai" | "ollama" | "mock")
    LLM_PROVIDER: str = "openai"

    # Configurações da OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"

    # Configurações do Ollama (execução local)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"

    # Nível de log (DEBUG | INFO | WARNING | ERROR)
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


# Instância singleton — importar este objeto em todo o projeto
settings = Settings()
