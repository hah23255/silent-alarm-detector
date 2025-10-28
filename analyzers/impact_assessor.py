#!/usr/bin/env python3
"""
Impact Assessor - Calculate performance and security cost of detected patterns.
"""

from typing import List, Dict
from dataclasses import dataclass

# Try relative import first, fall back to direct import for standalone testing
try:
    from .pattern_detector import Detection, PatternType, Severity
except ImportError:
    from pattern_detector import Detection, PatternType, Severity


@dataclass
class ImpactScore:
    """Quantified impact of detections."""
    total_score: int  # 0-100
    performance_cost: int  # 0-100
    security_risk: int  # 0-100
    maintainability_debt: int  # 0-100
    estimated_debug_hours: float  # Hours to fix if it causes production issue
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"


class ImpactAssessor:
    """Calculates quantified impact of alarm-silencing patterns."""

    # Impact weights for each pattern type
    PATTERN_WEIGHTS = {
        PatternType.SILENT_FALLBACK: {
            'performance': 10,
            'security': 30,
            'maintainability': 50,
            'debug_hours': 8.0
        },
        PatternType.WARNING_SUPPRESSION: {
            'performance': 5,
            'security': 20,
            'maintainability': 40,
            'debug_hours': 4.0
        },
        PatternType.ASSUMPTION_BYPASS: {
            'performance': 10,
            'security': 40,
            'maintainability': 30,
            'debug_hours': 6.0
        },
        PatternType.DUPLICATE_CODE: {
            'performance': 15,
            'security': 10,
            'maintainability': 60,
            'debug_hours': 12.0
        },
        PatternType.PERFORMANCE_DEGRADATION: {
            'performance': 70,
            'security': 5,
            'maintainability': 20,
            'debug_hours': 16.0
        },
        PatternType.SECURITY_SHORTCUT: {
            'performance': 5,
            'security': 95,
            'maintainability': 30,
            'debug_hours': 24.0
        },
        PatternType.ERROR_MASKING: {
            'performance': 10,
            'security': 15,
            'maintainability': 45,
            'debug_hours': 10.0
        },
        PatternType.TEST_AVOIDANCE: {
            'performance': 5,
            'security': 10,
            'maintainability': 50,
            'debug_hours': 20.0
        },
    }

    # Severity multipliers
    SEVERITY_MULTIPLIERS = {
        Severity.CRITICAL: 2.0,
        Severity.WARNING: 1.0,
        Severity.INFO: 0.5,
    }

    def assess_impact(self, detections: List[Detection]) -> ImpactScore:
        """
        Calculate quantified impact of all detections.

        Args:
            detections: List of Detection objects

        Returns:
            ImpactScore with quantified metrics
        """
        if not detections:
            return ImpactScore(
                total_score=0,
                performance_cost=0,
                security_risk=0,
                maintainability_debt=0,
                estimated_debug_hours=0.0,
                risk_level="LOW"
            )

        performance = 0
        security = 0
        maintainability = 0
        debug_hours = 0.0

        for detection in detections:
            weights = self.PATTERN_WEIGHTS.get(detection.pattern_type, {
                'performance': 10,
                'security': 10,
                'maintainability': 10,
                'debug_hours': 4.0
            })

            multiplier = self.SEVERITY_MULTIPLIERS[detection.severity]
            confidence = detection.confidence

            performance += weights['performance'] * multiplier * confidence
            security += weights['security'] * multiplier * confidence
            maintainability += weights['maintainability'] * multiplier * confidence
            debug_hours += weights['debug_hours'] * multiplier * confidence

        # Normalize to 0-100 scale
        num_detections = len(detections)
        performance_cost = min(100, int(performance / max(num_detections, 1)))
        security_risk = min(100, int(security / max(num_detections, 1)))
        maintainability_debt = min(100, int(maintainability / max(num_detections, 1)))

        # Calculate total score (weighted average)
        total_score = int(
            performance_cost * 0.3 +
            security_risk * 0.4 +
            maintainability_debt * 0.3
        )

        # Determine risk level
        if total_score >= 80 or security_risk >= 90:
            risk_level = "CRITICAL"
        elif total_score >= 60 or security_risk >= 70:
            risk_level = "HIGH"
        elif total_score >= 40:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return ImpactScore(
            total_score=total_score,
            performance_cost=performance_cost,
            security_risk=security_risk,
            maintainability_debt=maintainability_debt,
            estimated_debug_hours=round(debug_hours, 1),
            risk_level=risk_level
        )

    def generate_impact_report(self, detections: List[Detection]) -> str:
        """Generate human-readable impact report."""
        impact = self.assess_impact(detections)

        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                     IMPACT ASSESSMENT                          ║
╚════════════════════════════════════════════════════════════════╝

🎯 Risk Level: {impact.risk_level}
📊 Total Impact Score: {impact.total_score}/100

┌─ BREAKDOWN ────────────────────────────────────────────────────┐
│ 🐌 Performance Cost:      {impact.performance_cost:>3}/100  {'█' * (impact.performance_cost // 10)}
│ 🔓 Security Risk:         {impact.security_risk:>3}/100  {'█' * (impact.security_risk // 10)}
│ 🔧 Maintainability Debt:  {impact.maintainability_debt:>3}/100  {'█' * (impact.maintainability_debt // 10)}
│ ⏱️  Est. Debug Hours:      {impact.estimated_debug_hours:>5.1f}h (if issues hit production)
└────────────────────────────────────────────────────────────────┘

📋 Detected {len(detections)} alarm-silencing pattern(s):
"""

        # Group by severity
        critical = [d for d in detections if d.severity == Severity.CRITICAL]
        warnings = [d for d in detections if d.severity == Severity.WARNING]
        info = [d for d in detections if d.severity == Severity.INFO]

        if critical:
            report += f"\n🚨 CRITICAL ({len(critical)}):\n"
            for d in critical[:3]:  # Show top 3
                report += f"  • Line {d.line_number}: {d.description}\n"

        if warnings:
            report += f"\n⚠️  WARNING ({len(warnings)}):\n"
            for d in warnings[:3]:
                report += f"  • Line {d.line_number}: {d.description}\n"

        if info:
            report += f"\n💡 INFO ({len(info)}):\n"
            for d in info[:2]:
                report += f"  • Line {d.line_number}: {d.description}\n"

        # Recommendations
        report += f"\n{'═' * 64}\n"
        report += "🎯 TOP RECOMMENDATIONS:\n\n"

        # Prioritize by impact
        sorted_detections = sorted(
            detections,
            key=lambda d: (
                self.SEVERITY_MULTIPLIERS[d.severity] *
                sum(self.PATTERN_WEIGHTS.get(d.pattern_type, {
                    'performance': 10, 'security': 10, 'maintainability': 10
                }).values())
            ),
            reverse=True
        )

        for i, d in enumerate(sorted_detections[:5], 1):
            report += f"{i}. {d.recommendation}\n"

        return report


def main():
    """Test impact assessor."""
    try:
        from .pattern_detector import SilentAlarmDetector
    except ImportError:
        from pattern_detector import SilentAlarmDetector

    test_code = '''
def vulnerable_function(user_input):
    try:
        query = f"SELECT * FROM users WHERE name = '{user_input}'"
        result = execute_query(query)
    except:
        pass

    password = "hardcoded_secret_123"
    return result
'''

    detector = SilentAlarmDetector()
    detections = detector.analyze_code(test_code)

    assessor = ImpactAssessor()
    report = assessor.generate_impact_report(detections)

    print(report)


if __name__ == "__main__":
    main()
