"""메트릭 수집기 테스트"""
import pytest
from src.collector.cpu import get_cpu_metrics, get_cpu_times
from src.collector.memory import get_memory_metrics
from src.collector.disk import get_disk_usage, get_disk_io
from src.collector.network import get_network_io


class TestCPUCollector:
    """CPU 메트릭 수집 테스트"""

    def test_get_cpu_metrics(self):
        """CPU 메트릭 수집 테스트"""
        metrics = get_cpu_metrics()
        assert "cpu_percent" in metrics
        assert isinstance(metrics["cpu_percent"], (int, float))
        assert 0 <= metrics["cpu_percent"] <= 100

    def test_get_cpu_times(self):
        """CPU 시간 통계 수집 테스트"""
        times = get_cpu_times()
        assert "cpu_time_user" in times
        assert "cpu_time_system" in times
        assert isinstance(times["cpu_time_user"], float)


class TestMemoryCollector:
    """메모리 메트릭 수집 테스트"""

    def test_get_memory_metrics(self):
        """메모리 메트릭 수집 테스트"""
        metrics = get_memory_metrics()
        assert "memory_total" in metrics
        assert "memory_used" in metrics
        assert "memory_percent" in metrics
        assert 0 <= metrics["memory_percent"] <= 100


class TestDiskCollector:
    """디스크 메트릭 수집 테스트"""

    def test_get_disk_usage(self):
        """디스크 사용량 수집 테스트"""
        usage_list = get_disk_usage()
        assert isinstance(usage_list, list)
        if usage_list:
            disk = usage_list[0]
            assert "total" in disk
            assert "used" in disk
            assert "free" in disk
            assert "percent" in disk

    def test_get_disk_io(self):
        """디스크 I/O 수집 테스트"""
        io_metrics = get_disk_io()
        if io_metrics:  # 일부 환경에서는 None 반환 가능
            assert "disk_read_count" in io_metrics
            assert "disk_write_count" in io_metrics


class TestNetworkCollector:
    """네트워크 메트릭 수집 테스트"""

    def test_get_network_io(self):
        """네트워크 I/O 수집 테스트"""
        metrics = get_network_io()
        assert "network_bytes_sent" in metrics
        assert "network_bytes_recv" in metrics
        assert isinstance(metrics["network_bytes_sent"], int)
