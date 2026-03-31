from typing import List, Dict, Any
from datetime import datetime
from loguru import logger

class HistoryService:
    """Serviço de histórico de interações (simulado em memória)."""
    
    def __init__(self):
        # Para portfólio, mantemos em memória para facilitar execução local
        # Em produção, isso seria substituído por uma persistência em banco de dados (ex: PostgreSQL/Redis)
        self._history: List[Dict[str, Any]] = []

    def add_interaction(self, prompt: str, response_text: str, provider: str, model: str):
        """Adiciona uma nova interação ao histórico."""
        interaction = {
            "id": len(self._history) + 1,
            "prompt": prompt,
            "response": response_text,
            "provider": provider,
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._history.append(interaction)
        logger.debug(f"Interação #{interaction['id']} registrada no histórico.")

    def get_recent_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retorna as interações mais recentes."""
        return self._history[-limit:]

# Singleton do serviço de histórico
history_service = HistoryService()
