#!/usr/bin/env python3
"""
메트릭 수집기 간단 테스트 스크립트

InfluxDB 없이 메트릭 수집 기능을 테스트합니다.
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.collector.cpu import get_cpu_metrics, get_cpu_times
from src.collector.memory import get_memory_metrics
from src.collector.disk import get_disk_usage, get_disk_io
from src.collector.network import get_network_io


def test_cpu_metrics():
    """CPU 메트릭 수집 테스트"""
    print("\n=== CPU Metrics ===")
    try:
        metrics = get_cpu_metrics()
        print(f"✓ CPU Usage: {metrics['cpu_percent']:.1f}%")
        print(f"✓ CPU Count (Logical): {metrics['cpu_count_logical']}")
        print(f"✓ CPU Count (Physical): {metrics['cpu_count_physical']}")

        times = get_cpu_times()
        print(f"✓ CPU User Time: {times['cpu_time_user']:.2f}s")
        print(f"✓ CPU System Time: {times['cpu_time_system']:.2f}s")
        return True
    except Exception as e:
        print(f"✗ CPU metrics failed: {e}")
        return False


def test_memory_metrics():
    """메모리 메트릭 수집 테스트"""
    print("\n=== Memory Metrics ===")
    try:
        metrics = get_memory_metrics()
        total_gb = metrics['memory_total'] / (1024**3)
        used_gb = metrics['memory_used'] / (1024**3)
        print(f"✓ Memory Total: {total_gb:.2f} GB")
        print(f"✓ Memory Used: {used_gb:.2f} GB")
        print(f"✓ Memory Usage: {metrics['memory_percent']:.1f}%")
        print(f"✓ Swap Usage: {metrics['swap_percent']:.1f}%")
        return True
    except Exception as e:
        print(f"✗ Memory metrics failed: {e}")
        return False


def test_disk_metrics():
    """디스크 메트릭 수집 테스트"""
    print("\n=== Disk Metrics ===")
    try:
        # Disk Usage
        usage_list = get_disk_usage()
        print(f"✓ Found {len(usage_list)} disk partition(s)")
        for disk in usage_list[:3]:  # 최대 3개만 출력
            total_gb = disk['total'] / (1024**3)
            used_gb = disk['used'] / (1024**3)
            print(f"  - {disk['mountpoint']}: {used_gb:.1f}/{total_gb:.1f} GB ({disk['percent']:.1f}%)")

        # Disk I/O
        io_metrics = get_disk_io()
        if io_metrics:
            print(f"✓ Disk Read: {io_metrics['disk_read_bytes'] / (1024**2):.2f} MB")
            print(f"✓ Disk Write: {io_metrics['disk_write_bytes'] / (1024**2):.2f} MB")
        else:
            print("⚠ Disk I/O metrics not available")
        return True
    except Exception as e:
        print(f"✗ Disk metrics failed: {e}")
        return False


def test_network_metrics():
    """네트워크 메트릭 수집 테스트"""
    print("\n=== Network Metrics ===")
    try:
        metrics = get_network_io()
        sent_mb = metrics['network_bytes_sent'] / (1024**2)
        recv_mb = metrics['network_bytes_recv'] / (1024**2)
        print(f"✓ Network Sent: {sent_mb:.2f} MB")
        print(f"✓ Network Received: {recv_mb:.2f} MB")
        print(f"✓ Packets Sent: {metrics['network_packets_sent']}")
        print(f"✓ Packets Received: {metrics['network_packets_recv']}")
        return True
    except Exception as e:
        print(f"✗ Network metrics failed: {e}")
        return False


def main():
    """메인 테스트 실행"""
    print("="*50)
    print("System Metrics Collector - Simple Test")
    print("="*50)

    results = []
    results.append(("CPU", test_cpu_metrics()))
    results.append(("Memory", test_memory_metrics()))
    results.append(("Disk", test_disk_metrics()))
    results.append(("Network", test_network_metrics()))

    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:15} {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All tests passed! Metrics collection is working.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
