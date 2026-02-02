"""FastAPI 메인 애플리케이션"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from src.api.routes import metrics, health
from src.storage.influxdb_client import InfluxDBClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# InfluxDB 클라이언트 전역 인스턴스
influxdb_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    global influxdb_client
    # 시작 시
    logger.info("Starting FastAPI application")
    influxdb_client = InfluxDBClient()
    yield
    # 종료 시
    logger.info("Shutting down FastAPI application")
    if influxdb_client:
        await influxdb_client.close()


app = FastAPI(
    title="System Resource Metrics API",
    description="서버 시스템 리소스 메트릭 모니터링 API",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(health.router, tags=["Health"])
app.include_router(metrics.router, prefix="/api/v1/metrics", tags=["Metrics"])

# Prometheus 메트릭 엔드포인트
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "service": "System Resource Metrics API",
        "version": "1.0.0",
        "status": "running",
    }


def get_influxdb_client() -> InfluxDBClient:
    """InfluxDB 클라이언트 의존성"""
    return influxdb_client
