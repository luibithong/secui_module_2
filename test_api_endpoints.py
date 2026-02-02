#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API 엔드포인트 테스트 스크립트

FastAPI 서버의 주요 엔드포인트를 테스트합니다.
"""

import time
import requests
from typing import Dict, Any


API_BASE_URL = "http://localhost:8000"


def test_endpoint(name: str, url: str, expected_status: int = 200) -> bool:
    """
    API 엔드포인트 테스트

    Args:
        name: 테스트 이름
        url: 테스트할 URL
        expected_status: 예상 상태 코드

    Returns:
        테스트 성공 여부
    """
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        elapsed_ms = (time.time() - start_time) * 1000

        if response.status_code == expected_status:
            print(f"[PASS] {name}")
            print(f"  Status: {response.status_code}")
            print(f"  Response Time: {elapsed_ms:.2f}ms")

            # JSON 응답 출력 (간략하게)
            try:
                data = response.json()
                if isinstance(data, dict):
                    # 중요한 필드만 출력
                    important_keys = ['status', 'timestamp', 'service', 'version']
                    for key in important_keys:
                        if key in data:
                            print(f"  {key}: {data[key]}")
            except:
                pass

            print()
            return True
        else:
            print(f"[FAIL] {name}")
            print(f"  Expected: {expected_status}, Got: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            print()
            return False

    except requests.exceptions.ConnectionError:
        print(f"[FAIL] {name} - Connection refused (서버가 실행 중이 아닙니다)")
        print()
        return False
    except requests.exceptions.Timeout:
        print(f"[FAIL] {name} - Request timeout")
        print()
        return False
    except Exception as e:
        print(f"[FAIL] {name} - {str(e)}")
        print()
        return False


def test_metrics_endpoint(name: str, url: str) -> bool:
    """
    메트릭 엔드포인트 특별 테스트

    Args:
        name: 테스트 이름
        url: 테스트할 URL

    Returns:
        테스트 성공 여부
    """
    try:
        start_time = time.time()
        response = requests.get(url, timeout=5)
        elapsed_ms = (time.time() - start_time) * 1000

        if response.status_code == 200:
            print(f"[PASS] {name}")
            print(f"  Status: {response.status_code}")
            print(f"  Response Time: {elapsed_ms:.2f}ms")

            # 메트릭 데이터 확인
            try:
                data = response.json()
                if isinstance(data, dict):
                    # CPU 메트릭 확인
                    if 'cpu' in data:
                        cpu = data['cpu']
                        if 'cpu_percent' in cpu:
                            print(f"  CPU Usage: {cpu['cpu_percent']:.1f}%")

                    # Memory 메트릭 확인
                    if 'memory' in data:
                        memory = data['memory']
                        if 'memory_percent' in memory:
                            print(f"  Memory Usage: {memory['memory_percent']:.1f}%")
            except:
                pass

            print()
            return True
        else:
            print(f"[FAIL] {name}")
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
            print()
            return False

    except requests.exceptions.ConnectionError:
        print(f"[FAIL] {name} - Connection refused")
        print()
        return False
    except Exception as e:
        print(f"[FAIL] {name} - {str(e)}")
        print()
        return False


def main():
    """메인 테스트 실행"""
    print("=" * 60)
    print("FastAPI 엔드포인트 테스트")
    print("=" * 60)
    print()

    # 서버 연결 대기
    print("서버 연결 확인 중...")
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=2)
            if response.status_code == 200:
                print(f"[OK] 서버 연결 성공\n")
                break
        except:
            if i < max_retries - 1:
                print(f"재시도 중... ({i + 1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"[ERROR] 서버에 연결할 수 없습니다.")
                print(f"서버를 시작하세요: uvicorn src.api.main:app --reload\n")
                return 1

    # 테스트 목록
    tests = [
        ("Root Endpoint", f"{API_BASE_URL}/"),
        ("Health Check", f"{API_BASE_URL}/health"),
        ("Readiness Check", f"{API_BASE_URL}/readiness"),
        ("Liveness Check", f"{API_BASE_URL}/liveness"),
    ]

    # 기본 엔드포인트 테스트
    results = []
    for name, url in tests:
        result = test_endpoint(name, url)
        results.append((name, result))

    # 메트릭 엔드포인트 테스트
    print("--- 메트릭 엔드포인트 ---\n")

    result = test_metrics_endpoint(
        "Current Metrics",
        f"{API_BASE_URL}/api/v1/metrics/current"
    )
    results.append(("Current Metrics", result))

    # Prometheus 메트릭 엔드포인트
    result = test_endpoint(
        "Prometheus Metrics",
        f"{API_BASE_URL}/metrics",
        expected_status=200
    )
    results.append(("Prometheus Metrics", result))

    # 결과 요약
    print("=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {name}")

    print()
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n[SUCCESS] 모든 API 엔드포인트 테스트 통과!")
        return 0
    else:
        print(f"\n[WARNING] {total - passed}개 테스트 실패")
        return 1


if __name__ == "__main__":
    exit(main())
