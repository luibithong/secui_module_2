# System Resource Metrics Monitoring

서버의 시스템 리소스를 실시간으로 수집하고 모니터링하는 시스템

## 기술 스택

- **Backend**: Python 3.10+ + FastAPI
- **메트릭 수집**: psutil
- **Time-Series DB**: InfluxDB 2.7+
- **Dashboard**: Grafana 10.0+
- **Alerting**: Prometheus (선택사항)
- **Container**: Docker + Docker Compose

## 아키텍처

```
Metric Collector (Python/psutil)
    ↓
Time-Series DB (InfluxDB)
    ↓
API Server (FastAPI)
    ↓
Dashboard (Grafana)
```

## 빠른 시작 (Docker Compose)

### 사전 요구사항

- Docker Desktop 설치 (Windows/Mac)
- Docker Compose v2.0+

### 1. 전체 시스템 실행

```bash
# 모든 서비스 시작 (InfluxDB, Grafana, Collector, API)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그만 확인
docker-compose logs -f collector
docker-compose logs -f api
```

### 2. 서비스 접속

| 서비스 | URL | 계정 |
|--------|-----|------|
| **API Server** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **InfluxDB** | http://localhost:8086 | admin / admin12345 |
| **Grafana** | http://localhost:3000 | admin / admin |

### 3. 서비스 상태 확인

```bash
# 모든 컨테이너 상태 확인
docker-compose ps

# 헬스체크
curl http://localhost:8000/health

# 실시간 메트릭 조회
curl http://localhost:8000/api/v1/metrics/current
```

### 4. 서비스 중지 및 제거

```bash
# 서비스 중지
docker-compose stop

# 서비스 중지 및 컨테이너 제거
docker-compose down

# 데이터까지 모두 삭제
docker-compose down -v
```

## 로컬 개발 환경 설정

Docker 없이 로컬에서 개발하는 경우:

### 1. Python 가상환경 설정

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. InfluxDB 설치 및 설정

```bash
# Docker로 InfluxDB만 실행
docker run -d -p 8086:8086 \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=admin12345 \
  -e DOCKER_INFLUXDB_INIT_ORG=my-org \
  -e DOCKER_INFLUXDB_INIT_BUCKET=system-metrics \
  -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token \
  --name influxdb \
  influxdb:2.7
```

### 3. 환경 변수 설정

```bash
# .env 파일 수정 (로컬 환경용)
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=my-super-secret-auth-token
INFLUXDB_ORG=my-org
INFLUXDB_BUCKET=system-metrics
```

### 4. 애플리케이션 실행

```bash
# 메트릭 수집기 실행
python src/collector/main.py

# API 서버 실행 (다른 터미널)
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## API 엔드포인트

### 헬스체크
```bash
GET /health
GET /readiness
GET /liveness
```

### 메트릭 조회
```bash
# 실시간 메트릭
GET /api/v1/metrics/current

# 히스토리 데이터
GET /api/v1/metrics/history?metric=cpu&start_time=-1h&end_time=now()

# 통계 요약
GET /api/v1/metrics/summary?metric=cpu&period=-1h
```

### Prometheus 메트릭
```bash
GET /metrics
```

## Grafana 대시보드 설정

1. Grafana 접속: http://localhost:3000
2. 로그인: admin / admin
3. **Configuration** → **Data Sources** → **Add data source**
4. **InfluxDB** 선택
5. 설정:
   - Query Language: **Flux**
   - URL: `http://influxdb:8086`
   - Organization: `my-org`
   - Token: `my-super-secret-auth-token`
   - Default Bucket: `system-metrics`
6. **Save & Test**
7. **Dashboards** → **Import** → `grafana/dashboards/system-metrics-dashboard.json` 업로드

## 테스트 실행

### 빠른 테스트 (Python만 있으면 실행 가능)

```bash
# 메트릭 수집 기능 간단 테스트 (InfluxDB 불필요)
python test_collector_simple.py

# 메트릭 수집기 DRY-RUN 모드 실행 (InfluxDB 불필요)
python run_collector_dryrun.py
```

### pytest를 사용한 전체 테스트

```bash
# 전체 테스트
pytest

# 특정 테스트 파일
pytest tests/test_collector.py

# 커버리지 포함
pytest --cov=src tests/

# 상세 출력
pytest -v
```

## 프로젝트 구조

```
module_3/
├── src/
│   ├── collector/          # 메트릭 수집 로직
│   │   ├── cpu.py
│   │   ├── memory.py
│   │   ├── disk.py
│   │   ├── network.py
│   │   └── main.py
│   ├── api/                # FastAPI 서버
│   │   ├── routes/
│   │   │   ├── metrics.py
│   │   │   └── health.py
│   │   └── main.py
│   ├── storage/            # InfluxDB 연동
│   │   └── influxdb_client.py
│   └── alert/              # 알림 시스템
│       └── alertmanager.py
├── tests/                  # 테스트 코드
├── config/                 # 설정 파일
├── grafana/dashboards/     # Grafana 대시보드
├── docker-compose.yml      # Docker Compose 설정
├── Dockerfile.collector    # 수집기 Dockerfile
├── Dockerfile.api          # API 서버 Dockerfile
└── requirements.txt        # Python 의존성
```

## 메트릭 수집 항목

### CPU
- 전체 사용률 (%)
- 코어별 사용률
- CPU 주파수
- CPU 시간 통계

### Memory
- 전체/사용/가용 메모리
- 메모리 사용률 (%)
- Swap 메모리 정보

### Disk
- 파티션별 사용량
- 디스크 I/O (읽기/쓰기)
- 디스크 사용률 (%)

### Network
- 송수신 바이트/패킷
- 네트워크 에러/드롭
- 연결 상태 통계

## 성능 요구사항

- 메트릭 수집 지연: < 100ms
- API 응답 시간: < 200ms (P95)
- 저장소 쓰기 처리량: > 10,000 points/sec

## 데이터 보관 정책

- Raw data (1초): 24시간
- 5분 집계: 7일
- 1시간 집계: 30일
- 1일 집계: 1년

## 트러블슈팅

### InfluxDB 연결 실패
```bash
# InfluxDB 컨테이너 로그 확인
docker logs influxdb

# 연결 테스트
curl http://localhost:8086/health
```

### 메트릭이 수집되지 않음
```bash
# 수집기 로그 확인
docker-compose logs collector

# InfluxDB에 데이터 확인
docker exec -it influxdb influx query 'from(bucket:"system-metrics") |> range(start: -5m)'
```

### API 서버 응답 없음
```bash
# API 컨테이너 로그 확인
docker-compose logs api

# 헬스체크
curl http://localhost:8000/health
```

## 라이선스

MIT License

## 문의

프로젝트 이슈: https://github.com/your-repo/issues
