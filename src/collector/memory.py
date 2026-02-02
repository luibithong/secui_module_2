"""메모리 메트릭 수집 모듈"""
import psutil
from typing import Dict


def get_memory_metrics() -> Dict[str, float]:
    """
    메모리 메트릭 수집

    Returns:
        Dict[str, float]: 메모리 사용률 및 관련 메트릭
    """
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return {
        "memory_total": mem.total,
        "memory_available": mem.available,
        "memory_used": mem.used,
        "memory_free": mem.free,
        "memory_percent": mem.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_free": swap.free,
        "swap_percent": swap.percent,
    }
