"""메트릭 조회 라우터"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from src.storage.influxdb_client import InfluxDBClient
from src.api.main import get_influxdb_client
from src.collector.cpu import get_cpu_metrics, get_cpu_times
from src.collector.memory import get_memory_metrics
from src.collector.disk import get_disk_usage, get_disk_io
from src.collector.network import get_network_io

router = APIRouter()


class MetricsResponse(BaseModel):
    """메트릭 응답 모델"""
    timestamp: datetime
    cpu: Dict[str, Any]
    memory: Dict[str, Any]
    disk_usage: list
    disk_io: Dict[str, Any]
    network_io: Dict[str, Any]


@router.get("/current", response_model=MetricsResponse)
async def get_current_metrics():
    """
    실시간 메트릭 조회

    Returns:
        현재 시스템 메트릭
    """
    try:
        metrics = {
            "timestamp": datetime.utcnow(),
            "cpu": get_cpu_metrics(),
            "memory": get_memory_metrics(),
            "disk_usage": get_disk_usage(),
            "disk_io": get_disk_io(),
            "network_io": get_network_io(),
        }
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to collect metrics: {str(e)}")


@router.get("/history")
async def get_metrics_history(
    metric: str = Query(..., description="메트릭 이름 (cpu, memory, disk_io, network_io)"),
    start_time: Optional[str] = Query("-1h", description="시작 시간 (예: -1h, -30m)"),
    end_time: Optional[str] = Query("now()", description="종료 시간"),
    interval: Optional[str] = Query(None, description="집계 간격 (예: 1m, 5m)"),
    db_client: InfluxDBClient = Depends(get_influxdb_client),
):
    """
    히스토리 메트릭 조회

    Args:
        metric: 조회할 메트릭 이름
        start_time: 시작 시간
        end_time: 종료 시간
        interval: 집계 간격

    Returns:
        히스토리 메트릭 데이터
    """
    try:
        records = await db_client.query_metrics(
            measurement=metric,
            start=start_time,
            stop=end_time,
        )
        return {
            "metric": metric,
            "start_time": start_time,
            "end_time": end_time,
            "data": records,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query metrics: {str(e)}")


@router.get("/summary")
async def get_metrics_summary(
    metric: str = Query(..., description="메트릭 이름"),
    period: str = Query("-1h", description="조회 기간"),
    db_client: InfluxDBClient = Depends(get_influxdb_client),
):
    """
    메트릭 통계 요약 조회 (평균, 최소, 최대, P95)

    Args:
        metric: 메트릭 이름
        period: 조회 기간

    Returns:
        메트릭 통계 요약
    """
    try:
        records = await db_client.query_metrics(
            measurement=metric,
            start=period,
            stop="now()",
        )

        if not records:
            return {
                "metric": metric,
                "period": period,
                "summary": "No data available",
            }

        # 간단한 통계 계산
        values = [r["value"] for r in records if isinstance(r["value"], (int, float))]
        if not values:
            return {
                "metric": metric,
                "period": period,
                "summary": "No numeric data available",
            }

        sorted_values = sorted(values)
        p95_index = int(len(sorted_values) * 0.95)

        return {
            "metric": metric,
            "period": period,
            "summary": {
                "count": len(values),
                "avg": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "p95": sorted_values[p95_index] if p95_index < len(sorted_values) else sorted_values[-1],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate summary: {str(e)}")
