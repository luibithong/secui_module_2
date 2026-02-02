#!/usr/bin/env python3
"""
메트릭 수집기 DRY-RUN 모드 실행 스크립트

InfluxDB 없이 메트릭 수집기를 실행하여 동작을 확인합니다.
Ctrl+C로 중지할 수 있습니다.
"""
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 환경 변수 설정
os.environ["DRY_RUN"] = "true"
os.environ["LOG_LEVEL"] = "INFO"
os.environ["COLLECTOR_INTERVAL"] = "2"  # 2초 간격으로 수집

print("="*60)
print("System Metrics Collector - DRY-RUN Mode")
print("="*60)
print("This will collect system metrics every 2 seconds")
print("Press Ctrl+C to stop")
print("="*60)
print()

# 수집기 실행
from src.collector.main import main
import asyncio

asyncio.run(main())
