from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import health, llm
from app.core.config import settings
from loguru import logger
import time

def create_app() -> FastAPI:
    """Configura e inicializa a aplicação FastAPI."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
        API profissional para portfólio, integrando serviços de LLM (OpenAI/Ollama).
        Desenvolvida com foco em arquitetura limpa, escalabilidade e boas práticas de POO.
        """,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Middleware simples para logging de tempo de resposta
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Requisição: {request.method} {request.url.path} - Tempo: {process_time:.4f}s")
        return response

    # Tratamento global de erros genéricos
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error(f"Erro não tratado: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Erro interno no servidor. Verifique os logs."},
        )

    # Inclusão de rotas
    app.include_router(health.router, prefix=settings.API_V1_STR)
    app.include_router(llm.router, prefix=settings.API_V1_STR)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
