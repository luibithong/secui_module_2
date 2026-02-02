"""디스크 메트릭 수집 모듈"""
import psutil
from typing import Dict, List


def get_disk_usage() -> List[Dict[str, float]]:
    """
    디스크 사용량 메트릭 수집

    Returns:
        List[Dict[str, float]]: 각 파티션별 디스크 사용량
    """
    partitions = psutil.disk_partitions()
    disk_usage_list = []

    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage_list.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })
        except PermissionError:
            continue

    return disk_usage_list


def get_disk_io() -> Dict[str, int]:
    """
    디스크 I/O 메트릭 수집

    Returns:
        Dict[str, int]: 디스크 읽기/쓰기 카운트 및 바이트
    """
    disk_io = psutil.disk_io_counters()
    if disk_io is None:
        return {}

    return {
        "disk_read_count": disk_io.read_count,
        "disk_write_count": disk_io.write_count,
        "disk_read_bytes": disk_io.read_bytes,
        "disk_write_bytes": disk_io.write_bytes,
        "disk_read_time": disk_io.read_time,
        "disk_write_time": disk_io.write_time,
    }
