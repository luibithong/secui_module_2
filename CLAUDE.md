# CLAUDE.md

이 파일은 이 저장소에서 작업할 때 Claude Code (claude.ai/code)에 제공되는 가이드입니다.

## 프로젝트 개요

System Resource Metrics Monitoring - 서버의 시스템 리소스를 실시간으로 수집하고 모니터링하는 시스템

## 아키텍처

```
Metric Collector (Python/psutil)
    ↓
Time-Series DB (InfluxDB)
    ↓
API Server (FastAPI)
    ↓
Dashboard (Grafana) + Alert System (Prometheus)
```

**핵심 구성 요소:**
- **Collector**: psutil을 사용한 메트릭 수집 (CPU, Memory, Disk, Network)
- **Storage**: InfluxDB 2.x로 시계열 데이터 저장 (retention policy: 24h raw → 1년 집계)
- **API**: FastAPI 기반 REST API (실시간/히스토리/통계 조회)
- **Alerting**: 임계값 기반 알림 시스템

## 프로젝트 구조

```
module_3/
├── src/
│   ├── collector/          # 메트릭 수집 로직
│   │   ├── cpu.py
│   │   ├── memory.py
│   │   ├── disk.py
│   │   └── network.py
│   ├── api/                # FastAPI 서버
│   │   ├── routes/
│   │   │   ├── metrics.py
│   │   │   └── health.py
│   │   └── main.py
│   ├── storage/            # InfluxDB 연동
│   │   └── influxdb_client.py
│   └── alert/              # 알림 시스템
│       └── alertmanager.py
├── tests/
│   ├── test_collector.py
│   ├── test_api.py
│   └── test_storage.py
├── config/
│   ├── influxdb.yaml
│   └── alerts.yaml
├── grafana/
│   └── dashboards/         # Grafana 대시보드 JSON
├── docs/
│   └── system-resource-metrics-prd.md
└── requirements.txt
```

## 개발 환경 설정

### 환경 설정
```bash
# Python 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 필수 의존성
```
psutil==5.9.8
influxdb-client==1.39.0
fastapi==0.109.0
uvicorn==0.27.0
prometheus-client==0.19.0
pytest==7.4.0
```

### 수집기 실행
```bash
# 메트릭 수집기 실행
python src/collector/main.py
```

### API 서버 실행
```bash
# API 서버 실행
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 테스트 실행
```bash
# 전체 테스트 실행
pytest

# 특정 테스트 파일 실행
pytest tests/test_collector.py

# 커버리지 포함 테스트
pytest --cov=src tests/
```

## 주요 구현 세부사항

### 메트릭 수집 주기
- **CPU, Memory, Network**: 1초마다 수집
- **Disk I/O**: 5초마다 수집
- **Disk Usage**: 30초마다 수집

### API 엔드포인트
- `GET /api/v1/metrics/current` - 실시간 메트릭 조회
- `GET /api/v1/metrics/history` - 히스토리 데이터 (query params: metric, start_time, end_time, interval)
- `GET /api/v1/metrics/summary` - 통계 요약 (avg, min, max, P95)
- `GET /health` - 헬스체크

### 알림 임계값
- CPU > 80% (5분 지속): Warning
- CPU > 95% (1분 지속): Critical
- Memory > 85%: Warning
- Memory > 95%: Critical
- Disk > 80%: Warning
- Disk > 90%: Critical

### 데이터 보관 정책
- Raw data (1초): 24시간
- 5분 집계: 7일
- 1시간 집계: 30일
- 1일 집계: 1년

## 성능 요구사항
- 메트릭 수집 지연: < 100ms
- API 응답 시간: < 200ms (P95)
- 저장소 쓰기 처리량: > 10,000 points/sec

## 구현 단계

**Phase 1 (MVP)**: CPU/Memory 수집, InfluxDB 연동, 기본 API, Grafana 대시보드
**Phase 2**: Disk/Network 추가, 히스토리 조회, 알림 시스템
**Phase 3**: 다중 서버 지원, 커스텀 알림 규칙, 메트릭 집계
**Phase 4**: 로드 테스트, 보안, 배포 자동화

## 인프라 요구사항
- Python 3.10+
- InfluxDB 2.7+
- Grafana 10.0+
