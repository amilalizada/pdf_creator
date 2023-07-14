from fastapi.applications import FastAPI
from core.config import settings
from app import views as api_views
from core.database import db, db_connection
from core.middlewares import CatchExceptionsMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware


def register_extensions(app: object):
    """Register third part extensions."""
    db.initialize(db_connection)

    return None


def register_routers(app):
    """Register app routers."""
    # app.include_router(api_views.router, prefix=settings.api_prefix)
    app.include_router(api_views.router, prefix="/api/pdf")

    return None

def register_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(CatchExceptionsMiddleware)

def create_app() -> FastAPI:
    """App factory."""
    if settings.app_env == "production":
        docs_url = None
        redoc_url = None
        openapi_url = None
    else:
        docs_url = "/api/pdf/docs"
        openapi_url = "/api/pdf/openapi.json"
        redoc_url = None
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.api_version,
        docs_url=docs_url,
        openapi_url=openapi_url,
        redoc_url=redoc_url,
        # on_startup=[on_startup],
        # on_shutdown=[on_shutdown],
    )
    app.mount("/static", StaticFiles(directory="static"), name="static")

    register_extensions(app)
    register_routers(app)
    register_middleware(app)
    # register_exceptions(app)
    # custom_openapi(app)
    # do_migrations(app)

    return app
