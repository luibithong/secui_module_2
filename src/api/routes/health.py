"""헬스체크 라우터"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    헬스체크 엔드포인트

    Returns:
        헬스 상태 정보
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "system-metrics-api",
    }


@router.get("/readiness")
async def readiness_check():
    """
    준비 상태 확인 엔드포인트 (Kubernetes readiness probe)

    Returns:
        준비 상태 정보
    """
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/liveness")
async def liveness_check():
    """
    생존 상태 확인 엔드포인트 (Kubernetes liveness probe)

    Returns:
        생존 상태 정보
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }
