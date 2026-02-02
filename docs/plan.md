# 개발 계획 (Development Plan)

## 현재 완료 상태 ✓

### 프로젝트 초기 설정
- [x] 프로젝트 구조 생성
- [x] CLAUDE.md 작성 (Python 스택)
- [x] CLAUDE.md 스킬 섹션 추가 (code-review, git-commit)
- [x] CLAUDE.md C/C++ 코드 리뷰 스킬 추가
- [x] C/C++ 보안 중심 코드 리뷰 가이드라인 작성
- [x] requirements.txt 의존성 정의
- [x] .env.example 환경 변수 템플릿 작성
- [x] 설정 파일 작성 (influxdb.yaml, alerts.yaml)
- [x] Git 저장소 초기화 및 커밋

### 기본 코드 구조
- [x] 메트릭 수집기 기본 구조 (cpu.py, memory.py, disk.py, network.py, main.py)
- [x] FastAPI 서버 기본 구조 (main.py, routes/)
- [x] InfluxDB 클라이언트 기본 구조 (influxdb_client.py)
- [x] 알림 시스템 기본 구조 (alertmanager.py)
- [x] 테스트 코드 기본 구조 (test_*.py)
- [x] Grafana 대시보드 템플릿 작성

---

## Phase 1: MVP (Minimum Viable Product) - 다음 단계

### 1. 개발 환경 설정 (우선순위: 최상)
```bash
# 예상 소요 시간: 30분
```
- [x] Python 가상환경 생성 및 활성화 (스크립트 작성 완료)
- [x] requirements.txt 의존성 설치 (Docker Compose로 자동화)
- [x] .env 파일 생성 및 설정
- [x] InfluxDB 설치 (Docker Compose로 자동화)
- [x] InfluxDB 초기 설정 (Docker Compose로 자동 설정)

**완료 기준**:
- ✅ Docker Compose 파일 작성 완료
- ✅ 환경 변수 설정 완료
- ⚠️ Docker 설치 필요 (사용자 환경)

### 2. 메트릭 수집기 구현 및 테스트
```bash
# 예상 소요 시간: 1시간
```
- [x] 메트릭 수집 함수 단위 테스트 스크립트 작성 (`test_collector_simple.py`)
- [x] DRY-RUN 모드 구현 (InfluxDB 없이 동작)
- [x] 메트릭 수집기 실행 스크립트 작성 (`run_collector_dryrun.py`)
- [x] 수집 주기 조정 (CPU/Memory: 1초, Disk I/O: 5초, Disk Usage: 30초)
- [x] 로깅 설정 및 에러 핸들링 개선
- [x] 수집 시간 측정 및 성능 모니터링 추가
- [x] 테스트 출력 형식 개선 (이모지 → 텍스트 기반 표시)

**완료 기준**:
- ✅ `python test_collector_simple.py` 정상 실행
- ✅ `python run_collector_dryrun.py` DRY-RUN 모드 동작
- ⏳ InfluxDB 연동 테스트 (Docker 설치 후)

### 3. REST API 서버 구현 및 테스트
```bash
# 예상 소요 시간: 1.5시간
```
- [ ] FastAPI 서버 실행 테스트 (`uvicorn src.api.main:app --reload`)
- [ ] 헬스체크 엔드포인트 테스트 (`GET /health`)
- [ ] 실시간 메트릭 조회 API 테스트 (`GET /api/v1/metrics/current`)
- [ ] API 응답 시간 측정 (목표: < 200ms P95)
- [ ] CORS 설정 확인
- [ ] Prometheus 메트릭 엔드포인트 확인 (`GET /metrics`)

**완료 기준**:
- API 서버 정상 실행
- 모든 엔드포인트에서 정상 응답
- API 테스트 통과 (`pytest tests/test_api.py`)

### 4. Grafana 대시보드 설정
```bash
# 예상 소요 시간: 1시간
```
- [ ] Grafana 설치 (Docker 또는 로컬)
- [ ] InfluxDB 데이터소스 연동
- [ ] CPU 사용률 패널 생성 (실시간 그래프)
- [ ] Memory 사용률 패널 생성
- [ ] 대시보드 레이아웃 구성
- [ ] 자동 새로고침 설정 (5초 간격)

**완료 기준**:
- Grafana에서 실시간 메트릭 시각화 확인
- 대시보드 JSON 파일 저장

### 5. 통합 테스트 및 문서화
```bash
# 예상 소요 시간: 1시간
```
- [ ] 전체 시스템 통합 테스트 (수집기 → InfluxDB → API → Grafana)
- [ ] 성능 테스트 (메트릭 수집 지연 < 100ms 확인)
- [ ] README.md 업데이트 (설치 및 실행 가이드)
- [ ] 문제 발생 시 트러블슈팅 가이드 작성
- [ ] MVP 완료 커밋 및 푸쉬

**완료 기준**:
- 전체 워크플로우 정상 동작
- 문서화 완료

---

## Phase 2: 확장 기능

### 히스토리 데이터 조회 API
- [ ] 히스토리 조회 엔드포인트 구현 (`GET /api/v1/metrics/history`)
- [ ] 시간 범위 필터링 (start_time, end_time 파라미터)
- [ ] 메트릭 타입별 필터링
- [ ] Flux 쿼리 최적화
- [ ] 페이지네이션 구현 (선택사항)

### 통계 API 고도화
- [ ] 통계 요약 API 정확도 개선
- [ ] 시간대별 집계 기능 (1분, 5분, 1시간)
- [ ] P95, P99 백분위수 계산
- [ ] 메트릭 비교 기능 (전일 대비, 전주 대비)

### Prometheus 연동
- [ ] Prometheus 설치 및 설정
- [ ] Prometheus scraping 설정 (API `/metrics` 엔드포인트)
- [ ] ServiceMonitor 설정 (Kubernetes 환경)
- [ ] Prometheus 쿼리 테스트 (PromQL)

### Grafana 대시보드 확장
- [ ] Disk I/O 패널 추가
- [ ] Network 트래픽 패널 추가
- [ ] 알림 임계값 표시선 추가
- [ ] 서버 정보 패널 추가 (hostname, uptime)
- [ ] 여러 시간 범위 뷰 (1시간, 6시간, 24시간, 7일)

---

## Phase 3: 알림 시스템

### 알림 규칙 엔진 구현
- [ ] AlertManager 클래스 완성 (src/alert/alertmanager.py)
- [ ] 설정 파일 기반 알림 규칙 로드 (config/alerts.yaml)
- [ ] 알림 상태 추적 (Pending → Firing → Resolved)
- [ ] 중복 알림 방지 로직 (repeat_interval)
- [ ] 알림 히스토리 저장

### 알림 채널 구현
- [ ] 이메일 알림 구현 (SMTP, nodemailer 대신 smtplib 사용)
- [ ] Slack Webhook 연동
- [ ] Discord Webhook 연동
- [ ] Webhook 일반화 (커스텀 엔드포인트 지원)
- [ ] 알림 템플릿 시스템 구현

### Prometheus Alertmanager 통합
- [ ] Alertmanager 설치 및 설정
- [ ] 알림 규칙 파일 작성 (Prometheus rules)
- [ ] Alertmanager 라우팅 설정
- [ ] 알림 그룹화 및 억제 규칙 설정
- [ ] Grafana 알림 연동

### 알림 관리 API
- [ ] 알림 규칙 조회 API (`GET /api/v1/alerts/rules`)
- [ ] 활성 알림 조회 API (`GET /api/v1/alerts/active`)
- [ ] 알림 히스토리 조회 API (`GET /api/v1/alerts/history`)
- [ ] 알림 음소거 API (`POST /api/v1/alerts/silence`)

---

## Phase 4: 프로덕션 준비

### 다중 서버 지원
- [ ] 서버 식별자 수집 (hostname, IP)
- [ ] InfluxDB 스키마에 host 태그 추가
- [ ] 서버별 메트릭 필터링 API
- [ ] Grafana 대시보드 변수 추가 (서버 선택)
- [ ] 서버 목록 조회 API

### 데이터 보관 정책 자동화
- [ ] InfluxDB Retention Policy 설정 (24시간 raw data)
- [ ] 다운샘플링 태스크 생성 (5분 집계)
- [ ] 집계 버킷 생성 (5분, 1시간, 1일)
- [ ] 자동 파티션 삭제 설정
- [ ] 데이터 보관 정책 모니터링

### 성능 최적화
- [ ] 메트릭 수집 배치 처리 (bulk write)
- [ ] InfluxDB 쓰기 성능 튜닝
- [ ] API 응답 캐싱 (functools.lru_cache)
- [ ] 쿼리 최적화 (Flux 쿼리 개선)
- [ ] 로드 테스트 (목표: 10,000 points/sec)

### 보안 강화
- [ ] API 인증 구현 (JWT 또는 API Key)
- [ ] FastAPI 보안 헤더 설정
- [ ] 환경 변수 암호화 (python-dotenv-vault)
- [ ] 입력 유효성 검사 (Pydantic 모델 강화)
- [ ] Rate limiting 구현 (slowapi)

### Docker 컨테이너화
- [ ] Dockerfile 작성 (멀티 스테이지 빌드)
- [ ] docker-compose.yml 작성 (수집기, API, InfluxDB, Grafana)
- [ ] 볼륨 마운트 설정 (데이터 영속성)
- [ ] 헬스체크 설정
- [ ] 이미지 최적화 (크기 축소)

### CI/CD 파이프라인
- [ ] GitHub Actions 워크플로우 작성
- [ ] 자동 테스트 실행 (pytest)
- [ ] 코드 품질 검사 (black, isort, flake8, mypy)
- [ ] Docker 이미지 빌드 및 푸시
- [ ] 자동 배포 스크립트 작성

### 문서화
- [ ] API 문서 자동 생성 (FastAPI Swagger UI)
- [ ] 아키텍처 다이어그램 업데이트
- [ ] 운영 가이드 작성 (배포, 백업, 복구)
- [ ] 트러블슈팅 가이드 작성
- [ ] 성능 벤치마크 문서화

---

## 추가 개선 사항 (선택사항)

### 고급 모니터링
- [ ] 예측 알림 (이상 감지 알고리즘)
- [ ] 커스텀 메트릭 수집 지원
- [ ] 메트릭 상관관계 분석
- [ ] 트렌드 분석 및 리포팅

### 관리 기능
- [ ] 웹 기반 관리 UI
- [ ] 사용자 인증 및 권한 관리
- [ ] 대시보드 공유 기능
- [ ] 메트릭 내보내기 (CSV, JSON)

---

## 마일스톤

| Phase | 목표 완료일 | 상태 |
|-------|------------|------|
| Phase 0: 초기 설정 | ✓ 완료 | ✅ |
| Phase 1: MVP | TBD | 🔄 진행 예정 |
| Phase 2: 확장 기능 | TBD | ⏳ 대기 중 |
| Phase 3: 알림 시스템 | TBD | ⏳ 대기 중 |
| Phase 4: 프로덕션 준비 | TBD | ⏳ 대기 중 |
