"""API 엔드포인트 테스트"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestHealthEndpoints:
    """헬스체크 엔드포인트 테스트"""

    def test_health_check(self):
        """헬스체크 테스트"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data

    def test_readiness_check(self):
        """준비 상태 확인 테스트"""
        response = client.get("/readiness")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"

    def test_liveness_check(self):
        """생존 상태 확인 테스트"""
        response = client.get("/liveness")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "alive"


class TestMetricsEndpoints:
    """메트릭 엔드포인트 테스트"""

    def test_get_current_metrics(self):
        """실시간 메트릭 조회 테스트"""
        response = client.get("/api/v1/metrics/current")
        assert response.status_code == 200
        data = response.json()
        assert "cpu" in data
        assert "memory" in data
        assert "disk_usage" in data
        assert "timestamp" in data

    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "System Resource Metrics API"
        assert data["status"] == "running"


class TestMetricsHistory:
    """메트릭 히스토리 엔드포인트 테스트"""

    def test_get_metrics_history_requires_metric(self):
        """히스토리 조회 시 metric 파라미터 필수 테스트"""
        response = client.get("/api/v1/metrics/history")
        assert response.status_code == 422  # Validation error

    def test_get_metrics_summary_requires_metric(self):
        """통계 요약 조회 시 metric 파라미터 필수 테스트"""
        response = client.get("/api/v1/metrics/summary")
        assert response.status_code == 422  # Validation error
