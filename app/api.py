from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from threading import Thread
import logging
from src.DataBase.config import get_settings
from src.DataBase.init_db import init_db
from src.MQ.consumer import start_result_consumer
from routes.balance import balance_rout
from routes.users import user_route
from routes.thread import thread_rout
from routes.transactions import transaction_rout
from routes.audio_save import worker_rout

logger = logging.getLogger(__name__)
settings = get_settings()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Audio Script Service",
        description="REST API",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключаем роуты
    app.include_router(user_route, prefix="/api/users", tags=["Users"])
    app.include_router(balance_rout, prefix="/api/balance", tags=["Balance"])
    app.include_router(thread_rout, prefix="/api/thread", tags=["Prediction"])
    app.include_router(transaction_rout, prefix="/api/transactions", tags=["History"])
    app.include_router(worker_rout, prefix="/api/transcribation", tags=["Audio"])
    return app


app = create_app()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup():
    try:
        logger.info("Initializing database...")
        init_db()
        Thread(target=start_result_consumer, daemon=True).start()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
