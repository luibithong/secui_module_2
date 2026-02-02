"""네트워크 메트릭 수집 모듈"""
import psutil
from typing import Dict


def get_network_io() -> Dict[str, int]:
    """
    네트워크 I/O 메트릭 수집

    Returns:
        Dict[str, int]: 네트워크 송수신 바이트 및 패킷
    """
    net_io = psutil.net_io_counters()

    return {
        "network_bytes_sent": net_io.bytes_sent,
        "network_bytes_recv": net_io.bytes_recv,
        "network_packets_sent": net_io.packets_sent,
        "network_packets_recv": net_io.packets_recv,
        "network_errin": net_io.errin,
        "network_errout": net_io.errout,
        "network_dropin": net_io.dropin,
        "network_dropout": net_io.dropout,
    }


def get_network_connections() -> Dict[str, int]:
    """
    네트워크 연결 수 통계

    Returns:
        Dict[str, int]: 연결 상태별 개수
    """
    connections = psutil.net_connections(kind='inet')
    stats = {
        "ESTABLISHED": 0,
        "LISTEN": 0,
        "TIME_WAIT": 0,
        "CLOSE_WAIT": 0,
    }

    for conn in connections:
        if conn.status in stats:
            stats[conn.status] += 1

    return {
        "network_conn_established": stats["ESTABLISHED"],
        "network_conn_listen": stats["LISTEN"],
        "network_conn_time_wait": stats["TIME_WAIT"],
        "network_conn_close_wait": stats["CLOSE_WAIT"],
    }
