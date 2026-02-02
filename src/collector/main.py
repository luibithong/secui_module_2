"""메트릭 수집기 메인 모듈"""
import asyncio
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional

from src.collector.cpu import get_cpu_metrics, get_cpu_times
from src.collector.memory import get_memory_metrics
from src.collector.disk import get_disk_usage, get_disk_io
from src.collector.network import get_network_io, get_network_connections
from src.storage.influxdb_client import InfluxDBClient

# 환경 변수에서 로그 레벨 가져오기
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetricsCollector:
    """시스템 메트릭 수집 및 저장 클래스"""

    def __init__(self, influxdb_client: Optional[InfluxDBClient] = None, dry_run: bool = False):
        """
        Args:
            influxdb_client: InfluxDB 클라이언트 (None이면 dry-run 모드)
            dry_run: True면 데이터를 저장하지 않고 로그만 출력
        """
        self.influxdb_client = influxdb_client
        self.dry_run = dry_run or influxdb_client is None
        self.running = False
        self.metrics_collected = 0
        self.last_disk_check = 0
        self.last_disk_usage_check = 0

        if self.dry_run:
            logger.warning("Running in DRY-RUN mode - metrics will not be saved to InfluxDB")

    async def collect_all_metrics(self) -> Dict[str, Any]:
        """
        모든 메트릭 수집

        수집 주기:
        - CPU, Memory, Network: 매번 수집 (1초)
        - Disk I/O: 5초마다
        - Disk Usage: 30초마다
        """
        start_time = time.time()
        current_time = time.time()

        metrics = {
            "timestamp": datetime.utcnow(),
            "cpu": get_cpu_metrics(),
            "cpu_times": get_cpu_times(),
            "memory": get_memory_metrics(),
            "network_io": get_network_io(),
        }

        # Disk I/O: 5초마다 수집
        if current_time - self.last_disk_check >= 5:
            metrics["disk_io"] = get_disk_io()
            self.last_disk_check = current_time
            logger.debug("Collected disk I/O metrics")

        # Disk Usage: 30초마다 수집
        if current_time - self.last_disk_usage_check >= 30:
            metrics["disk_usage"] = get_disk_usage()
            self.last_disk_usage_check = current_time
            logger.debug("Collected disk usage metrics")

        # Network connections (에러 발생 가능)
        try:
            network_connections = get_network_connections()
            metrics["network_connections"] = network_connections
        except Exception as e:
            logger.warning(f"Failed to get network connections: {e}")
            metrics["network_connections"] = {}

        # 수집 시간 측정
        collection_time = (time.time() - start_time) * 1000
        logger.debug(f"Metrics collection took {collection_time:.2f}ms")

        if collection_time > 100:
            logger.warning(f"Metrics collection took longer than expected: {collection_time:.2f}ms")

        return metrics

    async def collect_loop(self, interval: int = 1):
        """메트릭 수집 루프"""
        self.running = True
        logger.info(f"Starting metrics collection loop (interval: {interval}s, dry_run: {self.dry_run})")

        while self.running:
            try:
                metrics = await self.collect_all_metrics()

                if self.dry_run:
                    # Dry-run 모드: 수집된 메트릭 로그 출력
                    logger.info(f"[DRY-RUN] Collected metrics: CPU={metrics['cpu'].get('cpu_percent', 0):.1f}%, "
                                f"Memory={metrics['memory'].get('memory_percent', 0):.1f}%")
                else:
                    # 실제로 InfluxDB에 저장
                    await self.influxdb_client.write_metrics(metrics)
                    logger.debug("Metrics collected and written successfully")

                self.metrics_collected += 1

                # 10회마다 통계 출력
                if self.metrics_collected % 10 == 0:
                    logger.info(f"Total metrics collected: {self.metrics_collected}")

            except Exception as e:
                logger.error(f"Error collecting metrics: {e}", exc_info=True)

            await asyncio.sleep(interval)

    def stop(self):
        """수집 중지"""
        logger.info("Stopping metrics collection")
        self.running = False


async def main():
    """메인 실행 함수"""
    # 환경 변수에서 설정 읽기
    interval = int(os.getenv("COLLECTOR_INTERVAL", "1"))
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

    influxdb_client = None

    # InfluxDB 클라이언트 초기화 시도
    if not dry_run:
        try:
            influxdb_client = InfluxDBClient()
            logger.info("InfluxDB client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize InfluxDB client: {e}")
            logger.warning("Switching to DRY-RUN mode")
            dry_run = True

    # 메트릭 수집기 생성 및 실행
    collector = MetricsCollector(influxdb_client, dry_run=dry_run)

    try:
        await collector.collect_loop(interval=interval)
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        collector.stop()
    finally:
        if influxdb_client:
            await influxdb_client.close()


if __name__ == "__main__":
    asyncio.run(main())
