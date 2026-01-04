from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth_router, users_router, works_router, reports_router, exports_router, org_router
from app import init_data

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # Ensure tables exist (simple migration-free mode)
    Base.metadata.create_all(bind=engine)

    @app.on_event("startup")
    def _startup():
        init_data.auto_init_system()

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(works_router)
    app.include_router(reports_router)
    app.include_router(exports_router)
    app.include_router(org_router)

    return app

app = create_app()
