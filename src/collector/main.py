"""메트릭 수집기 메인 모듈"""
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any

from src.collector.cpu import get_cpu_metrics, get_cpu_times
from src.collector.memory import get_memory_metrics
from src.collector.disk import get_disk_usage, get_disk_io
from src.collector.network import get_network_io, get_network_connections
from src.storage.influxdb_client import InfluxDBClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetricsCollector:
    """시스템 메트릭 수집 및 저장 클래스"""

    def __init__(self, influxdb_client: InfluxDBClient):
        self.influxdb_client = influxdb_client
        self.running = False

    async def collect_all_metrics(self) -> Dict[str, Any]:
        """모든 메트릭 수집"""
        metrics = {
            "timestamp": datetime.utcnow(),
            "cpu": get_cpu_metrics(),
            "cpu_times": get_cpu_times(),
            "memory": get_memory_metrics(),
            "disk_usage": get_disk_usage(),
            "disk_io": get_disk_io(),
            "network_io": get_network_io(),
        }

        try:
            network_connections = get_network_connections()
            metrics["network_connections"] = network_connections
        except Exception as e:
            logger.warning(f"Failed to get network connections: {e}")
            metrics["network_connections"] = {}

        return metrics

    async def collect_loop(self, interval: int = 1):
        """메트릭 수집 루프"""
        self.running = True
        logger.info(f"Starting metrics collection loop (interval: {interval}s)")

        while self.running:
            try:
                metrics = await self.collect_all_metrics()
                await self.influxdb_client.write_metrics(metrics)
                logger.debug("Metrics collected and written successfully")
            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")

            await asyncio.sleep(interval)

    def stop(self):
        """수집 중지"""
        logger.info("Stopping metrics collection")
        self.running = False


async def main():
    """메인 실행 함수"""
    # InfluxDB 클라이언트 초기화 (환경변수에서 설정 로드)
    influxdb_client = InfluxDBClient()

    # 메트릭 수집기 생성 및 실행
    collector = MetricsCollector(influxdb_client)

    try:
        await collector.collect_loop(interval=1)
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        collector.stop()
    finally:
        await influxdb_client.close()


if __name__ == "__main__":
    asyncio.run(main())
