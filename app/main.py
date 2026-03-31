"""
app/main.py
-----------
Ponto de entrada da aplicação FastAPI.

`create_app()` configura a instância do FastAPI com:
  - Metadados (título, descrição, versão, URLs de documentação)
  - Middleware de logging com tempo de processamento por requisição
  - Handler global para exceções não capturadas
  - Registro das rotas de health check e LLM

O objeto `app` (instância criada no módulo) é referenciado pelo Uvicorn:
    uvicorn app.main:app --reload
"""

import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from app.api.routes import health, llm
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Configura e retorna a instância principal do FastAPI.

    Registra middlewares, handlers de erro e routers antes de retornar
    o objeto `app` pronto para ser servido pelo Uvicorn.

    @returns Instância configurada de FastAPI.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        API profissional para portfólio, integrando serviços de LLM (OpenAI/Ollama).
        Desenvolvida com foco em arquitetura limpa, escalabilidade e boas práticas de POO.
        """,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """
        Middleware que mede o tempo de processamento de cada requisição HTTP.

        Adiciona o cabeçalho `X-Process-Time` na resposta e registra um log
        INFO com o método, caminho e duração em segundos.
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(
            f"Requisição: {request.method} {request.url.path} "
            f"- Tempo: {process_time:.4f}s"
        )
        return response

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Handler global para exceções não tratadas pelos handlers específicos.

        Loga o erro em nível ERROR e retorna HTTP 500 com mensagem genérica,
        evitando vazar detalhes internos ao cliente.
        """
        logger.error(f"Erro não tratado: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Erro interno no servidor. Verifique os logs."},
        )

    app.include_router(health.router, prefix=settings.API_V1_STR)
    app.include_router(llm.router, prefix=settings.API_V1_STR)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
