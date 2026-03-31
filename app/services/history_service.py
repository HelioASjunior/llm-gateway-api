"""
app/services/history_service.py
--------------------------------
Serviço de histórico de interações com o LLM.

Mantém um registro em memória de todos os prompts processados durante
o ciclo de vida da aplicação. Em uma versão de produção, esta lista
seria substituída por persistência em banco de dados (PostgreSQL, Redis, etc.).
"""

from typing import List, Dict, Any
from datetime import datetime

from loguru import logger


class HistoryService:
    """
    Gerencia o histórico de interações entre o usuário e o LLM.

    O armazenamento é feito em uma lista Python em memória (`_history`),
    o que significa que o histórico é perdido ao reiniciar a aplicação.
    """

    def __init__(self):
        """Inicializa o serviço com uma lista de histórico vazia."""
        self._history: List[Dict[str, Any]] = []

    def add_interaction(
        self,
        prompt: str,
        response_text: str,
        provider: str,
        model: str,
    ) -> None:
        """
        Registra uma nova interação no histórico.

        Atribui automaticamente um ID sequencial e o timestamp atual (UTC)
        antes de adicionar o registro à lista interna.

        @param prompt        - Texto do prompt enviado pelo usuário.
        @param response_text - Resposta gerada pelo LLM.
        @param provider      - Nome do provedor usado (ex.: "openai").
        @param model         - Nome do modelo usado (ex.: "gpt-3.5-turbo").
        """
        interaction = {
            "id": len(self._history) + 1,
            "prompt": prompt,
            "response": response_text,
            "provider": provider,
            "model": model,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._history.append(interaction)
        logger.debug(f"Interação #{interaction['id']} registrada no histórico.")

    def get_recent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retorna as interações mais recentes do histórico.

        Utiliza slicing negativo para obter os últimos `limit` registros,
        preservando a ordem cronológica original.

        @param limit - Número máximo de registros a retornar (padrão: 10).
        @returns Lista de dicts com os campos id, prompt, response, provider, model e timestamp.
        """
        return self._history[-limit:]


# Instância singleton — compartilhada entre todas as requisições para que
# o histórico persista durante toda a execução da aplicação
history_service = HistoryService()
