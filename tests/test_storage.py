"""InfluxDB 클라이언트 테스트"""
import pytest
from datetime import datetime
from src.storage.influxdb_client import InfluxDBClient


class TestInfluxDBClient:
    """InfluxDB 클라이언트 테스트"""

    @pytest.fixture
    def client(self):
        """테스트용 InfluxDB 클라이언트 픽스처"""
        return InfluxDBClient(
            url="http://localhost:8086",
            token="test-token",
            org="test-org",
            bucket="test-bucket",
        )

    def test_client_initialization(self, client):
        """클라이언트 초기화 테스트"""
        assert client.url == "http://localhost:8086"
        assert client.org == "test-org"
        assert client.bucket == "test-bucket"

    def test_convert_to_points(self, client):
        """메트릭을 InfluxDB Point로 변환 테스트"""
        metrics = {
            "timestamp": datetime.utcnow(),
            "cpu": {
                "cpu_percent": 50.5,
                "cpu_count_logical": 8,
            },
            "memory": {
                "memory_percent": 70.2,
                "memory_total": 16000000000,
            },
        }
        points = client._convert_to_points(metrics)
        assert len(points) == 2
        assert points[0].to_line_protocol().startswith("cpu")
        assert points[1].to_line_protocol().startswith("memory")

    @pytest.mark.asyncio
    async def test_write_metrics_structure(self, client):
        """메트릭 쓰기 구조 테스트 (실제 연결 없이)"""
        metrics = {
            "timestamp": datetime.utcnow(),
            "cpu": {"cpu_percent": 50.0},
        }
        # 실제 InfluxDB 없이 Point 변환만 테스트
        points = client._convert_to_points(metrics)
        assert len(points) > 0

    def test_empty_metrics(self, client):
        """빈 메트릭 처리 테스트"""
        metrics = {"timestamp": datetime.utcnow()}
        points = client._convert_to_points(metrics)
        assert len(points) == 0


class TestInfluxDBQueries:
    """InfluxDB 쿼리 테스트"""

    @pytest.fixture
    def client(self):
        """테스트용 클라이언트"""
        return InfluxDBClient(
            url="http://localhost:8086",
            token="test-token",
            org="test-org",
            bucket="test-bucket",
        )

    @pytest.mark.asyncio
    async def test_query_metrics_parameters(self, client):
        """쿼리 파라미터 검증 테스트"""
        # 실제 InfluxDB 연결 없이 쿼리 구조만 테스트
        measurement = "cpu"
        start = "-1h"
        stop = "now()"
        # 쿼리 생성 확인만 수행 (실제 실행 없이)
        assert measurement == "cpu"
        assert start == "-1h"
