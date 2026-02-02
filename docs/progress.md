# 개발 진행 상황 (Development Progress)

> 최종 업데이트: 2026-02-02

---

## 전체 진행률

- **Phase 1 (MVP)**: 0% (0/29 작업 완료)
- **Phase 2 (확장)**: 0% (0/22 작업 완료)
- **Phase 3 (알림)**: 0% (0/16 작업 완료)
- **Phase 4 (프로덕션)**: 0% (0/28 작업 완료)

**전체 진행률**: 0% (0/95 작업 완료)

---

## Phase 1: MVP (Minimum Viable Product)

### 메트릭 수집기 (Metric Collector) - 0/5
- [ ] systeminformation 라이브러리 설치 및 설정
- [ ] CPU 메트릭 수집 모듈 구현 (`src/collector/cpu.js`)
- [ ] Memory 메트릭 수집 모듈 구현 (`src/collector/memory.js`)
- [ ] 메트릭 수집 스케줄러 구현 (1초 간격)
- [ ] 수집기 메인 엔트리포인트 구현 (`src/collector/index.js`)

### 데이터 저장소 (Storage) - 0/5
- [ ] QuestDB 설치 및 초기 설정
- [ ] QuestDB 클라이언트 연동 구현 (`src/storage/questdb-client.js`)
- [ ] 메트릭 데이터 스키마 설계 (테이블 구조)
- [ ] 데이터 삽입 로직 구현
- [ ] 연결 풀 및 에러 핸들링 구현

### REST API 서버 (Fastify) - 0/7
- [ ] Fastify 프로젝트 초기 설정
- [ ] 서버 메인 엔트리포인트 구현 (`src/api/server.js`)
- [ ] 헬스체크 엔드포인트 구현 (`GET /health`)
- [ ] 현재 메트릭 조회 API 구현 (`GET /api/v1/metrics/current`)
- [ ] CORS 및 보안 미들웨어 설정
- [ ] 에러 핸들링 미들웨어 구현
- [ ] 로깅 설정 (Pino)

### 대시보드 (Apache ECharts) - 0/6
- [ ] 기본 HTML 페이지 구조 작성 (`public/index.html`)
- [ ] Apache ECharts 라이브러리 통합
- [ ] CPU 사용률 실시간 차트 구현
- [ ] Memory 사용률 실시간 차트 구현
- [ ] API 연동 및 데이터 갱신 로직 구현
- [ ] 반응형 레이아웃 구현

### 테스트 및 문서화 - 0/4
- [ ] 수집기 단위 테스트 작성 (`tests/collector.test.js`)
- [ ] API 엔드포인트 테스트 작성 (`tests/api.test.js`)
- [ ] README.md 작성 (설치 및 실행 가이드)
- [ ] 환경 변수 설정 문서화 (`.env.example`)

---

## Phase 2: 확장 기능

### 추가 메트릭 수집 - 0/4
- [ ] Disk I/O 메트릭 수집 모듈 구현 (`src/collector/disk.js`)
- [ ] Network 메트릭 수집 모듈 구현 (`src/collector/network.js`)
- [ ] Disk 사용률 수집 로직 구현
- [ ] 수집 주기 최적화 (Disk: 5초, Disk Usage: 30초)

### WebSocket 실시간 스트리밍 - 0/5
- [ ] Fastify WebSocket 플러그인 설치 및 설정
- [ ] WebSocket 엔드포인트 구현 (`WS /ws/metrics`)
- [ ] 실시간 메트릭 브로드캐스트 로직 구현
- [ ] 클라이언트 연결 관리 (연결/해제 처리)
- [ ] WebSocket 에러 핸들링 및 재연결 로직

### 히스토리 데이터 조회 - 0/5
- [ ] 히스토리 조회 API 구현 (`GET /api/v1/metrics/history`)
- [ ] 시간 범위 필터링 (start_time, end_time)
- [ ] 메트릭 타입별 필터링 (CPU, Memory, Disk, Network)
- [ ] 데이터 집계 간격 설정 (1초, 1분, 5분, 1시간)
- [ ] 페이지네이션 구현

### 통계 API - 0/5
- [ ] 통계 요약 API 구현 (`GET /api/v1/metrics/summary`)
- [ ] 평균(avg) 계산 로직
- [ ] 최소/최대(min/max) 값 조회
- [ ] P95 백분위수 계산
- [ ] 시간대별 통계 조회

### 대시보드 확장 - 0/5
- [ ] Disk I/O 차트 추가
- [ ] Network 트래픽 차트 추가
- [ ] WebSocket 기반 실시간 업데이트 구현
- [ ] 히스토리 데이터 시각화 (시간 범위 선택)
- [ ] 차트 줌/패닝 기능 구현

---

## Phase 3: 알림 시스템

### 알림 규칙 엔진 - 0/5
- [ ] 알림 매니저 구현 (`src/alert/alert-manager.js`)
- [ ] 임계값 기반 알림 규칙 정의
- [ ] 알림 상태 관리 (Warning/Critical)
- [ ] 알림 지속 시간 체크 로직
- [ ] 중복 알림 방지 (디바운싱)

### 알림 채널 구현 - 0/5
- [ ] 이메일 알림 구현 (nodemailer)
- [ ] SMTP 설정 및 템플릿 작성
- [ ] Slack Webhook 연동
- [ ] Discord Webhook 연동
- [ ] 알림 채널 설정 파일 작성 (`config/alerts.json`)

### 커스텀 알림 규칙 - 0/5
- [ ] 사용자 정의 임계값 설정 API
- [ ] 알림 규칙 CRUD API 구현
- [ ] 알림 규칙 저장소 (QuestDB 또는 JSON 파일)
- [ ] 알림 히스토리 조회 API
- [ ] 알림 음소거(Mute) 기능

### 대시보드 알림 UI - 0/4
- [ ] 알림 설정 화면 구현
- [ ] 현재 알림 상태 표시
- [ ] 알림 히스토리 목록
- [ ] 알림 테스트 기능

---

## Phase 4: 프로덕션 준비

### 다중 서버 지원 - 0/5
- [ ] 서버 식별자(hostname/IP) 수집
- [ ] 멀티 서버 메트릭 저장 스키마 설계
- [ ] 서버별 메트릭 조회 API
- [ ] 서버 선택 UI 구현
- [ ] 서버 그룹 관리 기능

### 데이터 집계 및 보관 정책 - 0/5
- [ ] Raw 데이터 보관 정책 (24시간)
- [ ] 5분 집계 테이블 생성 및 자동화 (7일 보관)
- [ ] 1시간 집계 테이블 생성 및 자동화 (30일 보관)
- [ ] 1일 집계 테이블 생성 및 자동화 (1년 보관)
- [ ] QuestDB 파티션 삭제 자동화

### 성능 최적화 - 0/5
- [ ] 메트릭 수집 배치 처리
- [ ] API 응답 캐싱 (Redis 선택사항)
- [ ] QuestDB 인덱싱 최적화
- [ ] API 레이트 리미팅 구현
- [ ] 로드 테스트 수행 (10,000 points/sec)

### 보안 - 0/5
- [ ] API 인증 구현 (JWT 또는 API Key)
- [ ] HTTPS 설정 (프로덕션)
- [ ] 환경 변수 암호화
- [ ] 입력 유효성 검사 강화
- [ ] SQL 인젝션 방어

### 배포 자동화 - 0/5
- [ ] Docker 이미지 작성 (Dockerfile)
- [ ] Docker Compose 설정 (QuestDB 포함)
- [ ] CI/CD 파이프라인 구성 (GitHub Actions)
- [ ] 프로덕션 배포 스크립트 작성
- [ ] 모니터링 및 로깅 인프라 구축

### 문서화 - 0/5
- [ ] API 문서 자동 생성 (Swagger/OpenAPI)
- [ ] 아키텍처 다이어그램 작성
- [ ] 운영 가이드 작성
- [ ] 트러블슈팅 가이드 작성
- [ ] 성능 벤치마크 문서화

---

## 최근 완료된 작업

### 2026-02-02 (저녁 - Phase 1 완료)
- **문서화 완료 (5번 과정)**
  - README.md 업데이트 완료
    - API 테스트 방법 추가
    - InfluxDB 선택적 연결 안내 추가
    - 트러블슈팅 가이드 확장
    - Windows 환경 설정 가이드 추가
  - test_api_endpoints.py 스크립트 문서화
  - 빠른 시작 가이드 개선

**Phase 1 MVP 완료 상태:**
- ✅ 1. 개발 환경 설정
- ✅ 2. 메트릭 수집기 구현 및 테스트
- ✅ 3. REST API 서버 구현 및 테스트
- ✅ 4. Grafana 대시보드 설정 (설정 파일 완료, Docker 실행 대기)
- ✅ 5. 통합 테스트 및 문서화

### 2026-02-02 (저녁 - Grafana 대시보드 완성)
- **Grafana 대시보드 설정 완료 (4번 과정)**
  - ✅ Grafana provisioning 디렉토리 구조 생성
    - `grafana/provisioning/datasources/influxdb.yml` (InfluxDB 자동 연동)
    - `grafana/provisioning/dashboards/dashboard.yml` (대시보드 자동 로드)
  - ✅ System Metrics 대시보드 JSON 완성
    - Grafana 10.0+ 호환 전체 스키마 구현
    - 5개 패널 구성:
      - Panel 1: CPU Usage (%) - 타임시리즈 차트
      - Panel 2: Current CPU - 게이지
      - Panel 3: Current Memory - 게이지
      - Panel 4: Memory Usage (%) - 타임시리즈 차트
      - Panel 5: Network I/O (Bytes/sec) - 타임시리즈 차트
    - Flux 쿼리 최적화 (aggregateWindow, derivative 적용)
    - 임계값 시각화 (CPU 70%/90%, Memory 80%/95%)
    - 5초 자동 새로고침, 15분 기본 시간 범위
    - 범례 테이블 표시 (last, mean, max 값)
  - ✅ docker-compose.yml 볼륨 마운트 추가
  - ✅ create_dashboard.py 헬퍼 스크립트 작성

**Docker 설치 후 실행 가능:**
- `docker-compose up -d` 명령으로 전체 시스템 실행
- Grafana 자동 설정 및 대시보드 로드 (http://localhost:3000)
- InfluxDB 데이터소스 자동 연동 완료

### 2026-02-02 (저녁 - API 테스트)
- **REST API 서버 구현 및 테스트 완료**
  - FastAPI 서버 성공적으로 시작
  - 필수 패키지 설치 (uvicorn, fastapi, requests, influxdb-client, prometheus-client 등)
  - 순환 import 문제 해결 (metrics.py ↔ main.py)
  - InfluxDB 선택적 연결 지원 구현
  - API 엔드포인트 테스트 스크립트 작성 (`test_api_endpoints.py`)
  - 전체 API 테스트 통과 (6/6)
    - Root Endpoint: ✓
    - Health Check: ✓
    - Readiness Check: ✓
    - Liveness Check: ✓
    - Current Metrics: ✓ (CPU 8.1%, Memory 35.5%)
    - Prometheus Metrics: ✓

### 2026-02-02 (오후)
- **C/C++ 코드 리뷰 가이드라인 작성**
  - `.claude/skills/c-code-review/SKILL.md` 파일 생성
  - 위험한 문자열 함수 대체 가이드 (strcpy → strncpy, sprintf → snprintf 등)
  - 포맷 스트링 취약점 방지
  - 메모리 안전성 (버퍼 오버플로우, 메모리 누수, Use-after-free 방지)
  - 정수 오버플로우 방지
  - 정적/동적 분석 도구 활용 (Valgrind, AddressSanitizer 등)

- **CLAUDE.md 스킬 섹션 확장**
  - C/C++ 코드 리뷰 스킬 추가
  - 보안 중심 코드 리뷰 가이드 링크 추가

### 2026-02-02 (오전)
- **CLAUDE.md 개선**
  - 스킬 섹션 추가 (Python 코드 리뷰, Git commit 자동화)
  - 프로젝트 가이드 체계화

- **테스트 스크립트 개선**
  - `test_collector_simple.py` 출력 형식 개선
  - 이모지 기반 표시 → 텍스트 기반 표시로 변경 ([OK], [FAIL], [WARN], [PASS], [SUCCESS])
  - UTF-8 인코딩 선언 추가
  - 크로스 플랫폼 호환성 개선

---

## 다음 작업 (Next Steps)

1. **프로젝트 초기 설정**
   - Node.js 패키지 초기화 (`package.json` 작성)
   - 필수 의존성 설치 (fastify, systeminformation, @questdb/nodejs-client 등)
   - 프로젝트 디렉토리 구조 생성

2. **개발 환경 구성**
   - QuestDB 로컬 설치 및 실행
   - 환경 변수 설정 파일 생성 (`.env`)
   - 개발 도구 설정 (ESLint, Prettier, Nodemon)

3. **Phase 1 착수**
   - CPU 메트릭 수집 모듈부터 구현 시작
   - QuestDB 연동 테스트
   - 기본 Fastify 서버 구축

---

## 이슈 및 블로커

*현재 이슈 없음*

---

## 참고 사항

- 개발은 Phase 순서대로 진행
- 각 Phase 완료 후 테스트 및 코드 리뷰 필수
- 성능 요구사항 충족 여부를 각 Phase에서 검증
- 문서화는 개발과 병행하여 진행
