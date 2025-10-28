# Pull Request

## 📋 Description

<!-- Provide a clear and concise description of what this PR does -->

## 🎯 Motivation

<!-- Why are these changes needed? What problem does this solve? -->

Closes #(issue number)

## 🔄 Type of Change

<!-- Mark the relevant option with an 'x' -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code style/refactoring (no functional changes)
- [ ] 🧪 Test additions/updates
- [ ] ⚙️ Configuration changes

## 📊 Changes Made

<!-- List the specific changes in this PR -->

- Added ...
- Modified ...
- Removed ...
- Fixed ...

## 🧪 Testing

<!-- Describe the tests you ran and how to reproduce them -->

**Test Configuration:**
- Python version:
- OS:
- Claude Code version:

**Tests Performed:**
- [ ] Ran existing test suite (`python3 analyzers/pattern_detector.py`)
- [ ] Ran impact assessor tests (`python3 analyzers/impact_assessor.py`)
- [ ] Tested main hook integration
- [ ] Tested with Claude Code in real workflow
- [ ] Added new test cases for new features
- [ ] All tests pass

**Manual Testing:**
```bash
# Commands used to test
```

## 📸 Screenshots / Examples

<!-- If applicable, add screenshots or example outputs -->

**Before:**
```
[paste before behavior/output]
```

**After:**
```
[paste after behavior/output]
```

## ✅ Checklist

<!-- Mark completed items with an 'x' -->

### Code Quality
- [ ] My code follows the project's code style (PEP 8)
- [ ] I have added type hints to new functions
- [ ] I have added docstrings to new functions/classes
- [ ] I have commented complex logic
- [ ] My changes generate no new warnings

### Testing
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing unit tests pass locally
- [ ] I have tested edge cases
- [ ] I have tested error handling

### Documentation
- [ ] I have updated relevant documentation (README, INSTALLATION, etc.)
- [ ] I have updated CHANGELOG.md with my changes
- [ ] I have added inline code comments for clarity
- [ ] My commit messages are clear and descriptive

### Configuration
- [ ] I updated `config/detection_rules.yaml` if needed
- [ ] I updated `.gitignore` if adding new generated files
- [ ] I updated `DECISIONS.md` if making architecture changes

## 🔗 Related Issues/PRs

<!-- Link related issues or PRs -->

- Relates to #
- Depends on #
- Blocks #

## 📝 Additional Notes

<!-- Any additional information, concerns, or context -->

## 🎓 Learning

<!-- (Optional) What did you learn while working on this? -->

## 🙋 Questions for Reviewers

<!-- Any specific areas you'd like reviewers to focus on? -->

---

## For Maintainers

**Review Checklist:**
- [ ] Code quality is acceptable
- [ ] Tests are comprehensive
- [ ] Documentation is updated
- [ ] No breaking changes (or properly documented)
- [ ] Performance impact is acceptable
- [ ] Security implications considered
- [ ] CHANGELOG.md updated
