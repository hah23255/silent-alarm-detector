# Contributing to Silent Alarm Detector

Thank you for your interest in contributing to Silent Alarm Detector! This document provides guidelines and instructions for contributing.

## 🎯 How Can I Contribute?

### 1. 🐛 Reporting Bugs

**Before submitting a bug report:**
- Check the [existing issues](https://github.com/yourusername/silent-alarm-detector/issues) to avoid duplicates
- Test with the latest version
- Gather relevant information (logs, config, Python version)

**When submitting a bug report, include:**
- **Description:** Clear and concise description of the bug
- **Steps to reproduce:** Numbered steps to reproduce the behavior
- **Expected behavior:** What you expected to happen
- **Actual behavior:** What actually happened
- **Environment:**
  - Python version (`python3 --version`)
  - Claude Code version
  - OS and version
- **Logs:** Relevant output from detection_history.jsonl or error messages
- **Code sample:** Minimal code that triggers the issue

**Bug report template:**
```markdown
## Bug Description
[Clear description]

## Steps to Reproduce
1. Install hook
2. Run Claude Code with code containing...
3. See error

## Expected Behavior
Hook should detect...

## Actual Behavior
Hook crashes with...

## Environment
- Python: 3.12
- OS: Ubuntu 22.04
- Claude Code: v1.2.3

## Logs
```
[Paste relevant logs]
```

## Code Sample
```python
[Minimal code that reproduces the issue]
```
```

---

### 2. 💡 Suggesting Enhancements

**Enhancement suggestions can include:**
- New pattern detectors
- Improved detection accuracy
- Performance optimizations
- Better error messages
- Documentation improvements
- New configuration options

**When suggesting an enhancement:**
- Use a clear and descriptive title
- Provide detailed explanation of the feature
- Explain **why** this enhancement would be useful
- Provide examples or mockups if applicable
- Discuss potential implementation approaches

---

### 3. 🔧 Contributing Code

#### **Fork and Clone**

1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/YOUR_USERNAME/silent-alarm-detector.git
cd silent-alarm-detector
```

3. Add upstream remote:
```bash
git remote add upstream https://github.com/yourusername/silent-alarm-detector.git
```

#### **Create a Branch**

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming conventions:**
- `feature/add-pattern-detector` - New features
- `fix/sql-injection-detection` - Bug fixes
- `docs/improve-readme` - Documentation updates
- `refactor/impact-scoring` - Code refactoring
- `test/add-unit-tests` - Test additions

#### **Make Changes**

1. **Code Style:**
   - Follow PEP 8 style guide
   - Use type hints where appropriate
   - Add docstrings to all functions and classes
   - Keep functions focused and under 50 lines when possible

2. **Commit Messages:**
   - Use present tense ("Add feature" not "Added feature")
   - Start with a capital letter
   - Limit first line to 72 characters
   - Add detailed description after blank line if needed

**Good commit messages:**
```
Add detector for missing context managers

Detects when files are opened without using context managers
(with statement), which can lead to resource leaks.

Addresses issue #42
```

3. **Testing:**
   - Test your changes thoroughly
   - Run existing test suite:
   ```bash
   python3 analyzers/pattern_detector.py
   python3 analyzers/impact_assessor.py
   ```
   - Add new tests for new features
   - Ensure all tests pass before submitting

4. **Documentation:**
   - Update README.md if adding user-facing features
   - Update DECISIONS.md if making architecture changes
   - Add inline comments for complex logic
   - Update config/detection_rules.yaml if adding new patterns

#### **Submit Pull Request**

1. Push to your fork:
```bash
git push origin feature/your-feature-name
```

2. Create Pull Request on GitHub

3. **PR Description should include:**
   - **What** changes were made
   - **Why** the changes were necessary
   - **How** the changes work
   - **Testing** done
   - **Related issues** (if any)

**PR template:**
```markdown
## Description
[Clear description of changes]

## Motivation
[Why are these changes needed?]

## Changes Made
- Added X detector
- Improved Y algorithm
- Fixed Z bug

## Testing
- [x] Tested manually with sample code
- [x] All existing tests pass
- [x] Added new test cases

## Related Issues
Closes #123
```

4. **Review Process:**
   - Maintainers will review your PR
   - Address any requested changes
   - Keep commits clean (squash if needed)
   - Be patient and respectful

---

## 🧪 Development Setup

### Prerequisites

- Python 3.7 or higher
- Claude Code installed
- Git

### Local Development

1. Clone the repository
2. Create test environment:
```bash
cd silent-alarm-detector
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
# No external dependencies required!
# All standard library
```

4. Run tests:
```bash
python3 analyzers/pattern_detector.py
python3 analyzers/impact_assessor.py
```

5. Test hook integration:
```bash
echo '{"tool_name":"Write","tool_input":{"content":"try:\n    x=1/0\nexcept:\n    pass"}}' | \
    python3 .claude-hooks/pre-tool-use/alarm_silencing_detector.py
```

---

## 📝 Code Style Guide

### Python Style

**Follow PEP 8 with these specifics:**

```python
#!/usr/bin/env python3
"""
Module docstring explaining purpose.
"""

import standard_library
from typing import List, Dict, Optional

# Constants in CAPS
MAX_DETECTION_LIMIT = 100

class DetectorClass:
    """Class docstring."""

    def __init__(self, param: str):
        """Constructor docstring."""
        self.param = param

    def detect_pattern(self, code: str) -> List[Detection]:
        """
        Function docstring with Args, Returns, Raises.

        Args:
            code: Source code to analyze

        Returns:
            List of Detection objects

        Raises:
            ValueError: If code is empty
        """
        if not code:
            raise ValueError("Code cannot be empty")

        # Implementation
        return []
```

**Key points:**
- ✅ Type hints on all function signatures
- ✅ Docstrings on all public functions
- ✅ 4 spaces for indentation (no tabs)
- ✅ Max line length: 100 characters
- ✅ Blank lines to separate logical sections

### Documentation Style

**Use clear, concise language:**
- Write in present tense
- Use active voice
- Provide examples
- Explain **why** not just **what**

**Good documentation:**
```python
def calculate_impact(detections: List[Detection]) -> int:
    """
    Calculate total impact score from detections.

    Uses weighted scoring where CRITICAL issues count 2x and
    WARNING issues count 1x. This prioritizes security over
    maintainability because prod incidents are more expensive.

    Example:
        >>> detections = [Detection(severity=Severity.CRITICAL, ...)]
        >>> score = calculate_impact(detections)
        >>> print(score)  # 85
    """
```

---

## 🔍 Adding New Pattern Detectors

**Process for adding a new pattern:**

1. **Research the pattern:**
   - Find examples in real LLM-generated code
   - Understand why it's problematic
   - Determine severity (CRITICAL/WARNING/INFO)

2. **Add to `analyzers/pattern_detector.py`:**

```python
def _detect_your_pattern(self, code: str, lines: List[str]):
    """Detect your pattern description."""

    pattern = r'your_regex_pattern'

    for match in re.finditer(pattern, code):
        line_num = code[:match.start()].count('\n') + 1

        self.detections.append(Detection(
            pattern_type=PatternType.YOUR_PATTERN,
            severity=Severity.WARNING,  # or CRITICAL/INFO
            line_number=line_num,
            code_snippet=lines[line_num-1].strip(),
            description="Clear description of the issue",
            impact="🎯 Explain the real-world impact",
            recommendation="Specific fix: do X instead of Y",
            confidence=0.9  # 0.0-1.0
        ))
```

3. **Add pattern type to enum:**

```python
class PatternType(Enum):
    # Existing patterns...
    YOUR_PATTERN = "your_pattern"
```

4. **Add to impact weights:**

```python
PATTERN_WEIGHTS = {
    # Existing patterns...
    PatternType.YOUR_PATTERN: {
        'performance': 20,
        'security': 10,
        'maintainability': 30,
        'debug_hours': 5.0
    },
}
```

5. **Update configuration:**

Add to `config/detection_rules.yaml`:
```yaml
patterns:
  your_pattern:
    enabled: true
    severity_override: null
```

6. **Document the pattern:**

Add to README.md with examples of bad and good code.

7. **Test thoroughly:**

```python
def test_your_pattern():
    detector = SilentAlarmDetector()

    bad_code = '''
    # Code that should be detected
    '''

    detections = detector.analyze_code(bad_code)
    assert len(detections) > 0
    assert detections[0].pattern_type == PatternType.YOUR_PATTERN
```

---

## 📚 Documentation Contributions

**Ways to improve documentation:**
- Fix typos and grammar
- Add more examples
- Clarify confusing sections
- Translate to other languages
- Create video tutorials
- Write blog posts

**Documentation locations:**
- `README.md` - Main user-facing docs
- `INSTALLATION.md` - Setup guide
- `DECISIONS.md` - Architecture rationale
- `CONTRIBUTING.md` - This file
- Inline code comments - Technical details

---

## 🧪 Testing Guidelines

### Test Coverage

**We aim for:**
- Pattern detection: 100% coverage
- Impact scoring: 100% coverage
- Main hook: 90% coverage
- Edge cases: Well covered

### Writing Tests

**Test structure:**
```python
def test_feature_name():
    """Test description."""
    # Arrange
    detector = SilentAlarmDetector()
    test_code = "..."

    # Act
    result = detector.analyze_code(test_code)

    # Assert
    assert len(result) == expected_count
    assert result[0].severity == Severity.CRITICAL
```

**Test edge cases:**
- Empty input
- Very large input
- Invalid syntax
- Unicode characters
- Mixed patterns

---

## 🔄 Review Process

**What reviewers look for:**
1. **Correctness:** Does the code work as intended?
2. **Tests:** Are there adequate tests?
3. **Documentation:** Is it well documented?
4. **Style:** Does it follow code style guide?
5. **Performance:** Any performance concerns?
6. **Breaking changes:** Will it break existing functionality?

**Response time:**
- Initial review: Within 3-5 days
- Follow-up reviews: Within 2-3 days
- **Be patient!** Maintainers are volunteers

---

## 🎖️ Recognition

**Contributors will be:**
- Listed in CONTRIBUTORS.md
- Mentioned in CHANGELOG.md
- Credited in release notes
- Given attribution in documentation

**Top contributors may:**
- Become project maintainers
- Get early access to new features
- Help shape project direction

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- ✅ Using welcoming and inclusive language
- ✅ Being respectful of differing viewpoints
- ✅ Gracefully accepting constructive criticism
- ✅ Focusing on what is best for the community
- ✅ Showing empathy towards others

**Unacceptable behavior:**
- ❌ Trolling, insulting/derogatory comments, personal attacks
- ❌ Public or private harassment
- ❌ Publishing others' private information
- ❌ Other conduct which could reasonably be considered inappropriate

### Enforcement

Violations may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to: [maintainer-email@example.com]

---

## 📞 Getting Help

**Need help contributing?**

- **Documentation:** Read existing docs first
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/silent-alarm-detector/discussions)
- **Issues:** Open an issue with "question" label
- **Chat:** [Discord/Slack link if available]

---

## 🚀 Release Process

**Maintainers only:**

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.2.0`
4. Push tag: `git push origin v1.2.0`
5. Create GitHub release
6. Announce on discussions/blog

---

## 📊 Project Status

**Current priorities:**
1. ✅ Core pattern detectors (v1.0 complete)
2. 🔄 Community building
3. 📋 Next: ML-based detection (v2.0)

**Looking for contributors for:**
- More pattern detectors
- Multi-language support
- Dashboard development
- Documentation improvements

---

## 🙏 Thank You!

Every contribution helps make Silent Alarm Detector better. Whether you're fixing a typo, reporting a bug, or adding a major feature — thank you! 🎉

**Together we're preventing "minor" issues from becoming major disasters!**

---

**Questions?** Open a [discussion](https://github.com/yourusername/silent-alarm-detector/discussions) or [issue](https://github.com/yourusername/silent-alarm-detector/issues).

*Happy contributing!* 🚀
