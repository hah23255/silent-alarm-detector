#!/usr/bin/env python3
"""
Silent Alarm Pattern Detector
Detects 8 critical patterns where LLMs silence alarms or bypass issues.
"""

import re
import ast
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class PatternType(Enum):
    """Types of alarm-silencing patterns."""
    SILENT_FALLBACK = "silent_fallback"
    WARNING_SUPPRESSION = "warning_suppression"
    ASSUMPTION_BYPASS = "assumption_bypass"
    DUPLICATE_CODE = "duplicate_code"
    PERFORMANCE_DEGRADATION = "performance_degradation"
    SECURITY_SHORTCUT = "security_shortcut"
    ERROR_MASKING = "error_masking"
    TEST_AVOIDANCE = "test_avoidance"


class Severity(Enum):
    """Detection severity levels."""
    CRITICAL = "CRITICAL"    # Will cause production issues
    WARNING = "WARNING"      # Will accumulate as tech debt
    INFO = "INFO"            # Best practice violation


@dataclass
class Detection:
    """Single pattern detection result."""
    pattern_type: PatternType
    severity: Severity
    line_number: int
    code_snippet: str
    description: str
    impact: str
    recommendation: str
    confidence: float  # 0.0-1.0


class SilentAlarmDetector:
    """
    Detects patterns where LLMs silence alarms or bypass issues
    that seem "minor" but have crushing impact on performance.
    """

    def __init__(self):
        self.detections: List[Detection] = []

    def analyze_code(self, code: str) -> List[Detection]:
        """
        Analyze code for all alarm-silencing patterns.

        Args:
            code: Source code to analyze

        Returns:
            List of Detection objects
        """
        self.detections = []
        lines = code.split('\n')

        # Run all pattern detectors
        self._detect_silent_fallback(code, lines)
        self._detect_warning_suppression(code, lines)
        self._detect_assumption_bypass(code, lines)
        self._detect_duplicate_code(code, lines)
        self._detect_performance_degradation(code, lines)
        self._detect_security_shortcuts(code, lines)
        self._detect_error_masking(code, lines)
        self._detect_test_avoidance(code, lines)

        return self.detections

    def _detect_silent_fallback(self, code: str, lines: List[str]):
        """Detect silent exception handling without logging."""

        # Pattern 1: except: pass
        pattern1 = r'except\s*:\s*pass'
        for match in re.finditer(pattern1, code, re.MULTILINE):
            line_num = code[:match.start()].count('\n') + 1
            self.detections.append(Detection(
                pattern_type=PatternType.SILENT_FALLBACK,
                severity=Severity.CRITICAL,
                line_number=line_num,
                code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                description="Bare except: pass silences ALL exceptions including critical ones",
                impact="⚠️ Crashes and errors will be invisible. Debugging impossible. Production failures go unnoticed.",
                recommendation="Add logging: logger.exception('Error in X') OR catch specific exceptions",
                confidence=1.0
            ))

        # Pattern 2: except Exception: pass (slightly better but still bad)
        pattern2 = r'except\s+Exception\s*:\s*pass'
        for match in re.finditer(pattern2, code, re.MULTILINE):
            line_num = code[:match.start()].count('\n') + 1
            self.detections.append(Detection(
                pattern_type=PatternType.SILENT_FALLBACK,
                severity=Severity.WARNING,
                line_number=line_num,
                code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                description="Exception silenced without logging",
                impact="🔇 Errors hidden. No visibility into failures. Silent degradation.",
                recommendation="Log the exception: logger.warning(f'Error: {e}', exc_info=True)",
                confidence=0.95
            ))

        # Pattern 3: Empty except blocks
        pattern3 = r'except\s+\w+\s*:\s*\n\s*$'
        for match in re.finditer(pattern3, code, re.MULTILINE):
            line_num = code[:match.start()].count('\n') + 1
            self.detections.append(Detection(
                pattern_type=PatternType.SILENT_FALLBACK,
                severity=Severity.WARNING,
                line_number=line_num,
                code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                description="Empty except block - error swallowed",
                impact="🕳️ Error disappears without trace. Impossible to debug.",
                recommendation="Add at minimum: logger.exception('Context message')",
                confidence=0.9
            ))

        # Pattern 4: return None without logging in except
        pattern4 = r'except.*?:\s*return\s+None\s*$'
        for match in re.finditer(pattern4, code, re.MULTILINE):
            line_num = code[:match.start()].count('\n') + 1
            if 'log' not in match.group().lower():
                self.detections.append(Detection(
                    pattern_type=PatternType.SILENT_FALLBACK,
                    severity=Severity.WARNING,
                    line_number=line_num,
                    code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                    description="Silent None return on exception",
                    impact="🎭 Failure masked as 'no result'. Caller can't distinguish error from empty.",
                    recommendation="Log before returning OR raise a custom exception",
                    confidence=0.85
                ))

    def _detect_warning_suppression(self, code: str, lines: List[str]):
        """Detect deliberate warning suppression."""

        patterns = [
            (r'warnings\.filterwarnings\(["\']ignore["\']\)',
             "warnings.filterwarnings('ignore') suppresses ALL warnings"),
            (r'-W\s+ignore',
             "Command line -W ignore flag suppresses warnings"),
            (r'@pytest\.mark\.filterwarnings\(["\']ignore',
             "pytest filterwarnings(ignore) hides test warnings"),
            (r'import\s+warnings.*?warnings\.simplefilter\(["\']ignore["\']\)',
             "warnings.simplefilter('ignore') globally suppresses warnings"),
        ]

        for pattern, desc in patterns:
            for match in re.finditer(pattern, code):
                line_num = code[:match.start()].count('\n') + 1
                self.detections.append(Detection(
                    pattern_type=PatternType.WARNING_SUPPRESSION,
                    severity=Severity.WARNING,
                    line_number=line_num,
                    code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                    description=desc,
                    impact="🙈 Deprecations, resource leaks, and API changes invisible. Technical debt accumulates.",
                    recommendation="Suppress specific warnings only: warnings.filterwarnings('ignore', category=SpecificWarning)",
                    confidence=0.95
                ))

    def _detect_assumption_bypass(self, code: str, lines: List[str]):
        """Detect skipped edge case validation."""

        # Pattern: Using variables without None checks
        # Look for function parameters used without validation
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if function uses parameters without validation
                    param_names = [arg.arg for arg in node.args.args]
                    has_validation = False

                    # Check for if param is None or isinstance checks
                    for child in ast.walk(node):
                        if isinstance(child, ast.If):
                            has_validation = True
                            break

                    if param_names and not has_validation and len(param_names) > 0:
                        line_num = node.lineno
                        self.detections.append(Detection(
                            pattern_type=PatternType.ASSUMPTION_BYPASS,
                            severity=Severity.WARNING,
                            line_number=line_num,
                            code_snippet=f"def {node.name}({', '.join(param_names)})",
                            description=f"Function uses parameters without validation",
                            impact="💥 Will crash on edge cases: None, empty strings, negative numbers, etc.",
                            recommendation=f"Add validation: if {param_names[0]} is None: raise ValueError(...)",
                            confidence=0.7
                        ))
        except SyntaxError:
            pass  # Can't parse, skip AST analysis

    def _detect_duplicate_code(self, code: str, lines: List[str]):
        """Detect code duplication (copy-paste)."""

        # Simple duplicate detection: find identical lines >10 lines long
        seen_blocks = {}
        block_size = 10

        for i in range(len(lines) - block_size):
            block = '\n'.join(lines[i:i+block_size])
            normalized = re.sub(r'\s+', ' ', block).strip()

            if len(normalized) > 50:  # Skip trivial blocks
                if normalized in seen_blocks:
                    self.detections.append(Detection(
                        pattern_type=PatternType.DUPLICATE_CODE,
                        severity=Severity.WARNING,
                        line_number=i+1,
                        code_snippet=f"Duplicate block at line {i+1} (also at {seen_blocks[normalized]})",
                        description=f"{block_size}-line duplicate code block",
                        impact="📋 Violates DRY. Bug fixes need multiple changes. Maintenance nightmare.",
                        recommendation="Extract to function or refactor common logic",
                        confidence=0.9
                    ))
                else:
                    seen_blocks[normalized] = i+1

    def _detect_performance_degradation(self, code: str, lines: List[str]):
        """Detect inefficient patterns."""

        # Pattern 1: Nested loops (potential O(n²))
        nested_loop_pattern = r'for\s+\w+\s+in.*?:\s*\n.*?for\s+\w+\s+in'
        for match in re.finditer(nested_loop_pattern, code, re.DOTALL):
            line_num = code[:match.start()].count('\n') + 1
            self.detections.append(Detection(
                pattern_type=PatternType.PERFORMANCE_DEGRADATION,
                severity=Severity.INFO,
                line_number=line_num,
                code_snippet="Nested for loops detected",
                description="Potential O(n²) complexity",
                impact="🐌 Performance degrades quadratically. 100 items = 10K operations. 1000 items = 1M operations.",
                recommendation="Consider using dict lookup (O(1)) or set operations instead",
                confidence=0.6
            ))

        # Pattern 2: Repeated API calls in loops
        api_in_loop = r'for\s+.*?:\s*\n.*?(requests\.|http\.|fetch\(|get\()'
        for match in re.finditer(api_in_loop, code, re.DOTALL):
            line_num = code[:match.start()].count('\n') + 1
            self.detections.append(Detection(
                pattern_type=PatternType.PERFORMANCE_DEGRADATION,
                severity=Severity.WARNING,
                line_number=line_num,
                code_snippet="API call inside loop",
                description="Repeated API calls without batching",
                impact="⏱️ N+1 query problem. 100 items = 100 API calls. Slow + rate limit issues.",
                recommendation="Batch API calls or use bulk endpoints",
                confidence=0.8
            ))

    def _detect_security_shortcuts(self, code: str, lines: List[str]):
        """Detect security vulnerabilities."""

        security_patterns = [
            (r'\.format\(.*SELECT.*FROM',
             "SQL injection via string formatting",
             "🔓 SQL INJECTION! Attacker can execute arbitrary SQL, dump database, delete data.",
             "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"),

            (r'eval\(',
             "eval() allows arbitrary code execution",
             "☠️ REMOTE CODE EXECUTION! Attacker can run ANY Python code on your server.",
             "Never use eval(). Parse JSON with json.loads() or use ast.literal_eval() for literals"),

            (r'exec\(',
             "exec() allows arbitrary code execution",
             "☠️ REMOTE CODE EXECUTION! Attacker can run ANY Python code.",
             "Refactor to avoid exec(). Use functions, classes, or importlib instead"),

            (r'(password|secret|api_key)\s*=\s*["\'][^"\']+["\']',
             "Hardcoded credentials",
             "🔑 CREDENTIAL LEAK! Credentials in code will be in git, logs, error messages.",
             "Use environment variables: os.environ['API_KEY'] or secrets manager"),
        ]

        for pattern, desc, impact, recommendation in security_patterns:
            for match in re.finditer(pattern, code, re.IGNORECASE):
                line_num = code[:match.start()].count('\n') + 1
                self.detections.append(Detection(
                    pattern_type=PatternType.SECURITY_SHORTCUT,
                    severity=Severity.CRITICAL,
                    line_number=line_num,
                    code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                    description=desc,
                    impact=impact,
                    recommendation=recommendation,
                    confidence=0.95
                ))

    def _detect_error_masking(self, code: str, lines: List[str]):
        """Detect generic error messages that hide root cause."""

        # Pattern: Generic exception raising
        generic_errors = [
            r'raise\s+Exception\(["\']Error["\']',
            r'raise\s+Exception\(["\']Something went wrong["\']',
            r'raise\s+Exception\(["\']Failed["\']',
        ]

        for pattern in generic_errors:
            for match in re.finditer(pattern, code):
                line_num = code[:match.start()].count('\n') + 1
                self.detections.append(Detection(
                    pattern_type=PatternType.ERROR_MASKING,
                    severity=Severity.INFO,
                    line_number=line_num,
                    code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                    description="Generic error message without context",
                    impact="🤷 Users/developers can't understand what failed or why. Support burden increases.",
                    recommendation="Use specific exceptions: raise ValueError(f'Invalid input {x}: must be > 0')",
                    confidence=0.8
                ))

    def _detect_test_avoidance(self, code: str, lines: List[str]):
        """Detect lack of tests or test-skipping patterns."""

        # Pattern: @pytest.mark.skip or unittest.skip
        skip_patterns = [
            r'@pytest\.mark\.skip',
            r'@unittest\.skip',
            r'skipTest\(',
        ]

        for pattern in skip_patterns:
            for match in re.finditer(pattern, code):
                line_num = code[:match.start()].count('\n') + 1
                self.detections.append(Detection(
                    pattern_type=PatternType.TEST_AVOIDANCE,
                    severity=Severity.WARNING,
                    line_number=line_num,
                    code_snippet=lines[line_num-1].strip() if line_num <= len(lines) else "",
                    description="Test marked as skip",
                    impact="🧪 Skipped tests = untested code. Regressions will go unnoticed.",
                    recommendation="Fix the test instead of skipping. If temporary, add issue reference and deadline.",
                    confidence=0.9
                ))


def main():
    """Test the detector."""
    test_code = '''
def process_data(data):
    try:
        result = expensive_operation(data)
        return result
    except:
        pass

    warnings.filterwarnings("ignore")
    password = "hardcoded123"

    for item in items:
        for subitem in subitems:
            process(item, subitem)
'''

    detector = SilentAlarmDetector()
    detections = detector.analyze_code(test_code)

    print(f"Found {len(detections)} alarm-silencing patterns:\n")
    for d in detections:
        print(f"[{d.severity.value}] Line {d.line_number}: {d.description}")
        print(f"  Impact: {d.impact}")
        print(f"  Fix: {d.recommendation}\n")


if __name__ == "__main__":
    main()
