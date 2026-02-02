# System Resource Metrics Monitoring - PRD

## 1. Overview

### 1.1 Purpose
서버의 시스템 리소스를 실시간으로 수집하고 모니터링하여 서버 상태를 파악하고, 성능 이슈를 사전에 감지하는 시스템을 구축한다.

### 1.2 Goals
- 실시간 시스템 리소스 메트릭 수집
- 수집된 데이터의 저장 및 조회 기능
- 임계값 기반 알림 시스템
- 직관적인 메트릭 시각화

### 1.3 Target Users
- DevOps 엔지니어
- 시스템 관리자
- 백엔드 개발자

---

## 2. Core Metrics

### 2.1 CPU Metrics
| 메트릭 | 설명 | 수집 주기 | 단위 |
|--------|------|-----------|------|
| cpu_percent | 전체 CPU 사용률 | 1초 | % |
| cpu_percent_per_core | 코어별 CPU 사용률 | 1초 | % |
| cpu_count_logical | 논리 CPU 개수 | 최초 1회 | 개 |
| cpu_count_physical | 물리 CPU 개수 | 최초 1회 | 개 |
| cpu_freq_current | 현재 CPU 주파수 | 5초 | MHz |

### 2.2 Memory Metrics
| 메트릭 | 설명 | 수집 주기 | 단위 |
|--------|------|-----------|------|
| memory_total | 전체 메모리 용량 | 최초 1회 | Bytes |
| memory_available | 사용 가능한 메모리 | 1초 | Bytes |
| memory_used | 사용 중인 메모리 | 1초 | Bytes |
| memory_percent | 메모리 사용률 | 1초 | % |
| memory_buffers | 버퍼 메모리 | 5초 | Bytes |
| memory_cached | 캐시 메모리 | 5초 | Bytes |
| swap_total | 전체 스왑 용량 | 최초 1회 | Bytes |
| swap_used | 사용 중인 스왑 | 5초 | Bytes |
| swap_percent | 스왑 사용률 | 5초 | % |

### 2.3 Disk Metrics
| 메트릭 | 설명 | 수집 주기 | 단위 |
|--------|------|-----------|------|
| disk_usage_total | 디스크 전체 용량 | 30초 | Bytes |
| disk_usage_used | 디스크 사용량 | 30초 | Bytes |
| disk_usage_percent | 디스크 사용률 | 30초 | % |
| disk_read_count | 디스크 읽기 횟수 | 5초 | 회 |
| disk_write_count | 디스크 쓰기 횟수 | 5초 | 회 |
| disk_read_bytes | 디스크 읽기 바이트 | 5초 | Bytes/s |
| disk_write_bytes | 디스크 쓰기 바이트 | 5초 | Bytes/s |
| disk_read_time | 디스크 읽기 소요 시간 | 5초 | ms |
| disk_write_time | 디스크 쓰기 소요 시간 | 5초 | ms |

### 2.4 Network Metrics
| 메트릭 | 설명 | 수집 주기 | 단위 |
|--------|------|-----------|------|
| network_bytes_sent | 송신 바이트 | 1초 | Bytes/s |
| network_bytes_recv | 수신 바이트 | 1초 | Bytes/s |
| network_packets_sent | 송신 패킷 수 | 1초 | 개/s |
| network_packets_recv | 수신 패킷 수 | 1초 | 개/s |
| network_errin | 수신 에러 수 | 5초 | 개 |
| network_errout | 송신 에러 수 | 5초 | 개 |
| network_dropin | 수신 드롭 패킷 수 | 5초 | 개 |
| network_dropout | 송신 드롭 패킷 수 | 5초 | 개 |
| network_connections | 활성 네트워크 연결 수 | 5초 | 개 |

---

## 3. Technical Requirements

### 3.1 System Architecture
```
┌─────────────────┐
│  Metric Collector│
│   (Python/Go)   │
└────────┬────────┘
         │ collect
         ▼
┌─────────────────┐
│   Time-Series   │
│      DB         │
│  (InfluxDB)     │
└────────┬────────┘
         │ query
         ▼
┌─────────────────┐     ┌─────────────┐
│   API Server    │────▶│  Dashboard  │
│  (FastAPI/REST) │     │  (Grafana)  │
└────────┬────────┘     └─────────────┘
         │
         ▼
┌─────────────────┐
│  Alert System   │
│  (Prometheus)   │
└─────────────────┘
```

### 3.2 Technology Stack
- **Collector**: Python 3.10+ with psutil library
- **Database**: InfluxDB 2.x (Time-series database)
- **API**: FastAPI or Flask
- **Visualization**: Grafana
- **Alert**: Prometheus Alertmanager or custom webhook

### 3.3 Data Storage
- **Retention Policy**:
  - Raw data (1초 간격): 24시간 보관
  - 5분 집계 데이터: 7일 보관
  - 1시간 집계 데이터: 30일 보관
  - 1일 집계 데이터: 1년 보관

### 3.4 Performance Requirements
- 메트릭 수집 지연: < 100ms
- API 응답 시간: < 200ms (P95)
- 저장소 쓰기 처리량: > 10,000 points/sec
- 동시 접속 지원: 100+ concurrent users

---

## 4. Functional Requirements

### 4.1 Metric Collection
```python
# 예시 구현
import psutil
import time
from datetime import datetime

class MetricCollector:
    def collect_cpu_metrics(self):
        return {
            'timestamp': datetime.utcnow(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'cpu_percent_per_core': psutil.cpu_percent(percpu=True),
            'cpu_count_logical': psutil.cpu_count(logical=True),
            'cpu_count_physical': psutil.cpu_count(logical=False)
        }

    def collect_memory_metrics(self):
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            'timestamp': datetime.utcnow(),
            'memory_total': mem.total,
            'memory_available': mem.available,
            'memory_used': mem.used,
            'memory_percent': mem.percent,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent
        }

    def collect_disk_metrics(self, path='/'):
        usage = psutil.disk_usage(path)
        io = psutil.disk_io_counters()
        return {
            'timestamp': datetime.utcnow(),
            'disk_usage_total': usage.total,
            'disk_usage_used': usage.used,
            'disk_usage_percent': usage.percent,
            'disk_read_count': io.read_count,
            'disk_write_count': io.write_count,
            'disk_read_bytes': io.read_bytes,
            'disk_write_bytes': io.write_bytes
        }

    def collect_network_metrics(self):
        net_io = psutil.net_io_counters()
        connections = len(psutil.net_connections())
        return {
            'timestamp': datetime.utcnow(),
            'network_bytes_sent': net_io.bytes_sent,
            'network_bytes_recv': net_io.bytes_recv,
            'network_packets_sent': net_io.packets_sent,
            'network_packets_recv': net_io.packets_recv,
            'network_errin': net_io.errin,
            'network_errout': net_io.errout,
            'network_connections': connections
        }
```

### 4.2 API Endpoints

#### GET /api/v1/metrics/current
실시간 메트릭 조회
```json
{
  "timestamp": "2026-02-02T14:30:00Z",
  "cpu": {
    "percent": 45.2,
    "per_core": [42.1, 48.3, 44.5, 46.0]
  },
  "memory": {
    "total": 16777216000,
    "used": 8388608000,
    "percent": 50.0
  },
  "disk": {
    "usage_percent": 65.3,
    "read_bytes_per_sec": 1048576,
    "write_bytes_per_sec": 524288
  },
  "network": {
    "bytes_sent_per_sec": 102400,
    "bytes_recv_per_sec": 204800,
    "connections": 42
  }
}
```

#### GET /api/v1/metrics/history
히스토리 메트릭 조회
```
Query Parameters:
- metric: cpu|memory|disk|network
- start_time: ISO 8601 timestamp
- end_time: ISO 8601 timestamp
- interval: 1m|5m|1h|1d
```

#### GET /api/v1/metrics/summary
통계 요약 조회 (평균, 최소, 최대, P95)
```json
{
  "period": {
    "start": "2026-02-02T00:00:00Z",
    "end": "2026-02-02T23:59:59Z"
  },
  "cpu": {
    "avg": 35.5,
    "min": 10.2,
    "max": 85.3,
    "p95": 72.1
  }
}
```

### 4.3 Alert Rules
| 조건 | 임계값 | 우선순위 | 조치 |
|------|--------|----------|------|
| CPU 사용률 | > 80% (5분 지속) | Warning | 알림 발송 |
| CPU 사용률 | > 95% (1분 지속) | Critical | 알림 발송 + 에스컬레이션 |
| 메모리 사용률 | > 85% | Warning | 알림 발송 |
| 메모리 사용률 | > 95% | Critical | 알림 발송 + 에스컬레이션 |
| 디스크 사용률 | > 80% | Warning | 알림 발송 |
| 디스크 사용률 | > 90% | Critical | 알림 발송 + 에스컬레이션 |
| 네트워크 에러율 | > 1% | Warning | 알림 발송 |

---

## 5. Non-Functional Requirements

### 5.1 Reliability
- 99.9% uptime (collector service)
- Graceful degradation (DB 장애 시 로컬 버퍼링)
- Auto-recovery on failure

### 5.2 Scalability
- Horizontal scaling support (multiple collectors)
- Sharding support for time-series data
- 서버 100대 이상 모니터링 가능

### 5.3 Security
- API 인증/인가 (JWT or API Key)
- TLS 암호화 통신
- 메트릭 데이터 접근 권한 관리

### 5.4 Observability
- Collector 자체 헬스체크 엔드포인트
- 수집 실패 메트릭 추적
- 로깅 (수집 오류, API 요청 로그)

---

## 6. Implementation Phases

### Phase 1: MVP (2 weeks)
- [ ] 기본 메트릭 수집 (CPU, Memory)
- [ ] InfluxDB 연동 및 데이터 저장
- [ ] 간단한 REST API 구현
- [ ] 기본 Grafana 대시보드

### Phase 2: Core Features (3 weeks)
- [ ] 디스크, 네트워크 메트릭 추가
- [ ] 히스토리 데이터 조회 API
- [ ] 알림 시스템 구축 (Webhook)
- [ ] 상세 대시보드 구성

### Phase 3: Advanced Features (2 weeks)
- [ ] 다중 서버 모니터링 지원
- [ ] 커스텀 알림 규칙 설정 UI
- [ ] 메트릭 집계 및 통계 기능
- [ ] 성능 최적화

### Phase 4: Production Ready (1 week)
- [ ] 로드 테스트 및 성능 튜닝
- [ ] 보안 강화 (인증/인가)
- [ ] 문서화 및 배포 자동화
- [ ] 모니터링 알림 테스트

---

## 7. Success Metrics

### 7.1 Technical Metrics
- 메트릭 수집 성공률: > 99.5%
- 데이터 손실률: < 0.1%
- 평균 수집 지연: < 50ms

### 7.2 Business Metrics
- 장애 사전 감지율: > 70%
- 장애 대응 시간 단축: > 50%
- 서버 리소스 최적화를 통한 비용 절감: > 20%

---

## 8. Risks and Mitigation

| 리스크 | 영향도 | 완화 방안 |
|--------|--------|-----------|
| 메트릭 수집이 서버 성능에 영향 | Medium | 수집 주기 조정, 리소스 제한 설정 |
| Time-series DB 용량 급증 | High | Retention policy 적용, 데이터 다운샘플링 |
| 수집 서비스 장애 | High | Health check, auto-restart, 다중화 |
| 네트워크 지연으로 데이터 유실 | Medium | 로컬 버퍼링, 재전송 로직 |

---

## 9. Dependencies

### 9.1 External Libraries
```
psutil==5.9.8
influxdb-client==1.39.0
fastapi==0.109.0
uvicorn==0.27.0
prometheus-client==0.19.0
```

### 9.2 Infrastructure
- InfluxDB 2.7+
- Grafana 10.0+
- Python 3.10+

---

## 10. References

- [psutil documentation](https://psutil.readthedocs.io/)
- [InfluxDB documentation](https://docs.influxdata.com/)
- [Grafana documentation](https://grafana.com/docs/)
- [Prometheus best practices](https://prometheus.io/docs/practices/)
