"""CPU 메트릭 수집 모듈"""
import psutil
from typing import Dict


def get_cpu_metrics() -> Dict[str, float]:
    """
    CPU 메트릭 수집

    Returns:
        Dict[str, float]: CPU 사용률 및 관련 메트릭
    """
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "cpu_percent_per_core": psutil.cpu_percent(interval=1, percpu=True),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_freq_current": psutil.cpu_freq().current if psutil.cpu_freq() else 0,
        "cpu_freq_min": psutil.cpu_freq().min if psutil.cpu_freq() else 0,
        "cpu_freq_max": psutil.cpu_freq().max if psutil.cpu_freq() else 0,
    }


def get_cpu_times() -> Dict[str, float]:
    """
    CPU 시간 통계 수집

    Returns:
        Dict[str, float]: CPU 시간 메트릭 (user, system, idle 등)
    """
    cpu_times = psutil.cpu_times()
    return {
        "cpu_time_user": cpu_times.user,
        "cpu_time_system": cpu_times.system,
        "cpu_time_idle": cpu_times.idle,
    }
