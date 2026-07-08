from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
for path in (_REPO_ROOT, _REPO_ROOT / "scripts"):
    entry = str(path)
    if entry not in sys.path:
        sys.path.insert(0, entry)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.routers import (
    brief,
    character,
    health,
    journal,
    message,
    npc,
    proposals,
    routing,
    save,
    search,
    session_commands,
)
from motor.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Cyberpunk Solo Narration API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type"],
    )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_request: Request, exc: StarletteHTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        if exc.status_code == 404 and isinstance(exc.detail, str):
            return JSONResponse(status_code=404, content={"error": exc.detail})
        if isinstance(exc.detail, str):
            return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
        return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})

    app.include_router(health.router)
    app.include_router(journal.router)
    app.include_router(brief.router)
    app.include_router(session_commands.router)
    app.include_router(character.router)
    app.include_router(npc.router)
    app.include_router(message.router)
    app.include_router(search.router)
    app.include_router(routing.router)
    app.include_router(proposals.router)
    app.include_router(save.router)

    if settings.frontend_dir.exists():
        app.mount("/", StaticFiles(directory=str(settings.frontend_dir), html=True), name="frontend")

    return app


app = create_app()


def main() -> int:
    import uvicorn

    from motor.settings import choose_provider, provider_display_name

    settings = get_settings()
    choose_provider(settings.provider)

    if not settings.frontend_dir.exists():
        print(f"Frontend nao encontrado em: {settings.frontend_dir}")
        return 2

    print(f"Servidor iniciado em http://{settings.host}:{settings.port}")
    print(f"Provider: {settings.provider} - {provider_display_name()}")
    uvicorn.run(
        "api.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level="info",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())