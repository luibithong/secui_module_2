"""InfluxDB 클라이언트 모듈"""
import os
import logging
from typing import Dict, Any, List
from datetime import datetime

from influxdb_client import InfluxDBClient as InfluxClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

logger = logging.getLogger(__name__)


class InfluxDBClient:
    """InfluxDB 연동 클라이언트"""

    def __init__(
        self,
        url: str = None,
        token: str = None,
        org: str = None,
        bucket: str = None,
    ):
        self.url = url or os.getenv("INFLUXDB_URL", "http://localhost:8086")
        self.token = token or os.getenv("INFLUXDB_TOKEN", "")
        self.org = org or os.getenv("INFLUXDB_ORG", "my-org")
        self.bucket = bucket or os.getenv("INFLUXDB_BUCKET", "system-metrics")

        self.client = InfluxClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

        logger.info(f"InfluxDB client initialized: {self.url}, bucket: {self.bucket}")

    async def write_metrics(self, metrics: Dict[str, Any]):
        """
        메트릭을 InfluxDB에 저장

        Args:
            metrics: 수집된 메트릭 데이터
        """
        points = self._convert_to_points(metrics)
        try:
            self.write_api.write(bucket=self.bucket, record=points)
        except Exception as e:
            logger.error(f"Failed to write metrics to InfluxDB: {e}")
            raise

    def _convert_to_points(self, metrics: Dict[str, Any]) -> List[Point]:
        """메트릭 데이터를 InfluxDB Point로 변환"""
        points = []
        timestamp = metrics.get("timestamp", datetime.utcnow())

        # CPU 메트릭
        if "cpu" in metrics:
            point = Point("cpu").time(timestamp)
            for key, value in metrics["cpu"].items():
                if isinstance(value, (int, float)):
                    point = point.field(key, value)
                elif isinstance(value, list):
                    for i, v in enumerate(value):
                        point = point.field(f"{key}_core{i}", v)
            points.append(point)

        # 메모리 메트릭
        if "memory" in metrics:
            point = Point("memory").time(timestamp)
            for key, value in metrics["memory"].items():
                point = point.field(key, value)
            points.append(point)

        # 디스크 I/O 메트릭
        if "disk_io" in metrics and metrics["disk_io"]:
            point = Point("disk_io").time(timestamp)
            for key, value in metrics["disk_io"].items():
                point = point.field(key, value)
            points.append(point)

        # 디스크 사용량 메트릭
        if "disk_usage" in metrics:
            for disk in metrics["disk_usage"]:
                point = (
                    Point("disk_usage")
                    .time(timestamp)
                    .tag("device", disk.get("device", "unknown"))
                    .tag("mountpoint", disk.get("mountpoint", "unknown"))
                    .field("total", disk.get("total", 0))
                    .field("used", disk.get("used", 0))
                    .field("free", disk.get("free", 0))
                    .field("percent", disk.get("percent", 0))
                )
                points.append(point)

        # 네트워크 I/O 메트릭
        if "network_io" in metrics:
            point = Point("network_io").time(timestamp)
            for key, value in metrics["network_io"].items():
                point = point.field(key, value)
            points.append(point)

        # 네트워크 연결 메트릭
        if "network_connections" in metrics and metrics["network_connections"]:
            point = Point("network_connections").time(timestamp)
            for key, value in metrics["network_connections"].items():
                point = point.field(key, value)
            points.append(point)

        return points

    async def query_metrics(
        self,
        measurement: str,
        start: str = "-1h",
        stop: str = "now()",
        filters: Dict[str, str] = None,
    ) -> List[Dict]:
        """
        InfluxDB에서 메트릭 조회

        Args:
            measurement: 측정 이름 (cpu, memory 등)
            start: 시작 시간
            stop: 종료 시간
            filters: 추가 필터

        Returns:
            조회된 메트릭 데이터 리스트
        """
        query = f'''
        from(bucket: "{self.bucket}")
          |> range(start: {start}, stop: {stop})
          |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        '''

        if filters:
            for key, value in filters.items():
                query += f'\n  |> filter(fn: (r) => r["{key}"] == "{value}")'

        try:
            result = self.query_api.query(query=query)
            records = []
            for table in result:
                for record in table.records:
                    records.append({
                        "time": record.get_time(),
                        "measurement": record.get_measurement(),
                        "field": record.get_field(),
                        "value": record.get_value(),
                    })
            return records
        except Exception as e:
            logger.error(f"Failed to query metrics from InfluxDB: {e}")
            raise

    async def close(self):
        """클라이언트 연결 종료"""
        self.client.close()
        logger.info("InfluxDB client closed")
