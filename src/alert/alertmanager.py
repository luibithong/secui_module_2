"""알림 관리 모듈"""
import logging
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class AlertLevel(str, Enum):
    """알림 레벨"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertRule:
    """알림 규칙 클래스"""

    def __init__(
        self,
        name: str,
        metric: str,
        condition: str,
        threshold: float,
        level: AlertLevel,
        duration: int = 0,
    ):
        self.name = name
        self.metric = metric
        self.condition = condition  # ">", "<", ">=", "<=", "=="
        self.threshold = threshold
        self.level = level
        self.duration = duration  # 지속 시간 (초)
        self.triggered_at: Optional[datetime] = None

    def check(self, value: float) -> bool:
        """
        규칙 조건 확인

        Args:
            value: 메트릭 값

        Returns:
            조건 충족 여부
        """
        if self.condition == ">":
            return value > self.threshold
        elif self.condition == ">=":
            return value >= self.threshold
        elif self.condition == "<":
            return value < self.threshold
        elif self.condition == "<=":
            return value <= self.threshold
        elif self.condition == "==":
            return value == self.threshold
        return False


class AlertManager:
    """알림 관리자 클래스"""

    def __init__(self):
        self.rules: List[AlertRule] = []
        self.active_alerts: Dict[str, Dict] = {}
        self._initialize_default_rules()

    def _initialize_default_rules(self):
        """기본 알림 규칙 초기화"""
        default_rules = [
            AlertRule("CPU High Warning", "cpu_percent", ">=", 80.0, AlertLevel.WARNING, duration=300),
            AlertRule("CPU Critical", "cpu_percent", ">=", 95.0, AlertLevel.CRITICAL, duration=60),
            AlertRule("Memory High Warning", "memory_percent", ">=", 85.0, AlertLevel.WARNING),
            AlertRule("Memory Critical", "memory_percent", ">=", 95.0, AlertLevel.CRITICAL),
            AlertRule("Disk High Warning", "disk_percent", ">=", 80.0, AlertLevel.WARNING),
            AlertRule("Disk Critical", "disk_percent", ">=", 90.0, AlertLevel.CRITICAL),
        ]
        self.rules.extend(default_rules)
        logger.info(f"Initialized {len(default_rules)} default alert rules")

    def add_rule(self, rule: AlertRule):
        """
        알림 규칙 추가

        Args:
            rule: 추가할 알림 규칙
        """
        self.rules.append(rule)
        logger.info(f"Added alert rule: {rule.name}")

    def check_metrics(self, metrics: Dict[str, float]) -> List[Dict]:
        """
        메트릭을 규칙과 비교하여 알림 발생 확인

        Args:
            metrics: 확인할 메트릭 딕셔너리

        Returns:
            발생한 알림 리스트
        """
        triggered_alerts = []

        for rule in self.rules:
            if rule.metric not in metrics:
                continue

            value = metrics[rule.metric]
            if rule.check(value):
                alert = {
                    "rule_name": rule.name,
                    "metric": rule.metric,
                    "value": value,
                    "threshold": rule.threshold,
                    "level": rule.level,
                    "timestamp": datetime.utcnow(),
                }

                # 지속 시간 확인 로직 (간단 구현)
                if rule.duration > 0:
                    if rule.name not in self.active_alerts:
                        rule.triggered_at = datetime.utcnow()
                        self.active_alerts[rule.name] = alert
                        logger.debug(f"Alert triggered: {rule.name}, waiting for duration")
                    else:
                        # 지속 시간 경과 확인
                        elapsed = (datetime.utcnow() - rule.triggered_at).total_seconds()
                        if elapsed >= rule.duration:
                            triggered_alerts.append(alert)
                            logger.warning(f"Alert fired: {rule.name}, value: {value}")
                else:
                    triggered_alerts.append(alert)
                    logger.warning(f"Alert fired: {rule.name}, value: {value}")
            else:
                # 알림 해제
                if rule.name in self.active_alerts:
                    del self.active_alerts[rule.name]
                    rule.triggered_at = None
                    logger.info(f"Alert resolved: {rule.name}")

        return triggered_alerts

    async def send_alert(self, alert: Dict):
        """
        알림 전송 (이메일, Slack, Webhook 등)

        Args:
            alert: 전송할 알림 정보
        """
        # TODO: 실제 알림 전송 구현 (이메일, Slack 등)
        logger.info(f"Sending alert: {alert['rule_name']}")
        print(f"[ALERT] {alert['level'].upper()}: {alert['rule_name']}")
        print(f"  Metric: {alert['metric']} = {alert['value']} (threshold: {alert['threshold']})")

    def get_active_alerts(self) -> List[Dict]:
        """
        활성 알림 조회

        Returns:
            활성 알림 리스트
        """
        return list(self.active_alerts.values())
