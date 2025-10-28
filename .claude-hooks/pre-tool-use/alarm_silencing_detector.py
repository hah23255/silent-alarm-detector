#!/usr/bin/env python3
"""
Silent Alarm Detector Hook (Pre-Tool-Use)
Detects when LLM is about to silence alarms or bypass "minor" issues.
Integrates with Claude Code hooks system.
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

# Add analyzers to path
hook_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(hook_dir))

try:
    from analyzers.pattern_detector import SilentAlarmDetector, Severity
    from analyzers.impact_assessor import ImpactAssessor
except ImportError as e:
    print(f"⚠️  Silent Alarm Detector: Module import failed: {e}", file=sys.stderr)
    sys.exit(0)  # Allow on import error


def extract_code_from_tool_input(tool_input: dict) -> str:
    """Extract code content from tool input."""
    code_content = ""

    # Check for code in various tool input fields
    if 'content' in tool_input:
        code_content = tool_input['content']
    elif 'new_string' in tool_input:  # Edit tool
        code_content = tool_input['new_string']
    elif 'command' in tool_input:  # Bash tool
        code_content = tool_input['command']

    return code_content


def should_analyze(tool_name: str, tool_input: dict) -> bool:
    """Determine if we should analyze this tool use."""
    # Analyze Write, Edit, and potentially Bash tools
    code_tools = ['Write', 'Edit', 'Bash']

    if tool_name not in code_tools:
        return False

    # For Bash, only analyze if it contains code patterns
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        # Only analyze if bash contains Python/code patterns
        if not any(keyword in command for keyword in ['python', 'def ', 'class ', 'import ']):
            return False

    return True


def log_detection(detections: list, impact_score: dict):
    """Log detection to history file."""
    log_file = hook_dir / 'data' / 'detection_history.jsonl'
    log_file.parent.mkdir(exist_ok=True)

    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'num_detections': len(detections),
        'impact_score': impact_score,
        'detections': [
            {
                'pattern': d.pattern_type.value,
                'severity': d.severity.value,
                'line': d.line_number,
                'description': d.description
            }
            for d in detections
        ]
    }

    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


def main():
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)
        tool_name = hook_input.get('tool_name', '')
        tool_input = hook_input.get('tool_input', {})

        # Check if we should analyze this tool use
        if not should_analyze(tool_name, tool_input):
            sys.exit(0)  # Pass through

        # Extract code
        code = extract_code_from_tool_input(tool_input)
        if not code or len(code) < 20:  # Skip trivial code
            sys.exit(0)

        # Analyze for alarm-silencing patterns
        detector = SilentAlarmDetector()
        detections = detector.analyze_code(code)

        if not detections:
            sys.exit(0)  # No issues found, pass through

        # Assess impact
        assessor = ImpactAssessor()
        impact = assessor.assess_impact(detections)

        # Log detection
        log_detection(detections, {
            'total_score': impact.total_score,
            'risk_level': impact.risk_level,
            'performance_cost': impact.performance_cost,
            'security_risk': impact.security_risk
        })

        # Determine if we should block or warn
        critical_count = sum(1 for d in detections if d.severity == Severity.CRITICAL)

        if critical_count > 0 or impact.risk_level == "CRITICAL":
            # BLOCK: Critical alarm-silencing detected
            print("🚨 CRITICAL ALARM-SILENCING DETECTED!", file=sys.stderr)
            print("", file=sys.stderr)
            print(f"Found {len(detections)} pattern(s) where LLM is silencing alarms:", file=sys.stderr)
            print("", file=sys.stderr)

            for d in detections:
                if d.severity == Severity.CRITICAL:
                    print(f"❌ Line {d.line_number}: {d.description}", file=sys.stderr)
                    print(f"   Impact: {d.impact}", file=sys.stderr)
                    print(f"   Fix: {d.recommendation}", file=sys.stderr)
                    print("", file=sys.stderr)

            print(f"🎯 Risk Level: {impact.risk_level}", file=sys.stderr)
            print(f"📊 Impact Score: {impact.total_score}/100", file=sys.stderr)
            print("", file=sys.stderr)
            print("⚠️  These 'minor' issues will have CRUSHING impact on production!", file=sys.stderr)
            print("   Please fix before proceeding.", file=sys.stderr)

            sys.exit(2)  # Block the tool use

        elif impact.risk_level in ["HIGH", "MEDIUM"]:
            # WARN: Non-critical but significant issues
            print(f"⚠️  Alarm-Silencing Warning ({len(detections)} patterns)", file=sys.stderr)
            print(f"   Risk: {impact.risk_level} | Impact: {impact.total_score}/100", file=sys.stderr)

            # Show top 2 issues
            sorted_detections = sorted(detections, key=lambda d: d.severity.value, reverse=True)
            for d in sorted_detections[:2]:
                print(f"   • Line {d.line_number}: {d.description}", file=sys.stderr)

            print(f"   ⏱️  Est. debug time if these cause issues: {impact.estimated_debug_hours}h", file=sys.stderr)

            sys.exit(0)  # Warn but allow

        else:
            # INFO: Minor issues
            print(f"💡 {len(detections)} minor alarm-silencing pattern(s) detected", file=sys.stderr)
            sys.exit(0)  # Allow

    except Exception as e:
        # Never block on hook errors
        print(f"⚠️  Silent Alarm Detector error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
