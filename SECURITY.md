# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**IMPORTANT: Do NOT open public issues for security vulnerabilities.**

### How to Report

1. **Email**: security@ccvs.tech
2. **Subject**: "Silent Alarm Detector Security Issue"
3. **Include**:
   - Vulnerability description
   - Impact assessment
   - Reproduction steps
   - Potential bypass methods

### Response Timeline

- **Acknowledgment**: 24 hours
- **Assessment**: 72 hours
- **Fix Timeline**:
  - Critical (bypass of detection): 3-7 days
  - High (false negatives): 7-14 days
  - Medium (false positives): 14-30 days

## Security Considerations

### Hook Execution

- Hooks run with same permissions as git
- Can access staged file contents
- Cannot access network by default
- Logs stored locally

### Detection Bypass

If you discover a way to bypass detection:
1. Report immediately via security email
2. Do not share publicly until patched
3. We will credit you in the fix

### False Positives

While not security issues, false positives undermine trust:
- Report via GitHub issues
- Include code sample
- Explain why detection is incorrect

## Best Practices

### For Users

```bash
# Review hook code before installation
cat .claude-hooks/pre-tool-use/alarm_silencing_detector.py

# Restrict hook file permissions
chmod 700 .claude-hooks/
chmod 600 .claude-hooks/pre-tool-use/*.py

# Monitor detection logs
tail -f .claude-hooks/detection_history.jsonl
```

### For Contributors

- Never execute arbitrary code from patterns
- Validate all file paths (no path traversal)
- Sanitize all output
- No network calls without explicit consent

## Known Limitations

1. **Language Coverage**: Python only currently
2. **Regex Limitations**: Complex patterns may be missed
3. **Performance**: Large files (>10k lines) may be slow

## Contact

- **Security Email**: security@ccvs.tech
- **Response Time**: 24 hours
- **PGP Key**: [Available on request]

---

**Thank you for helping keep codebases safe!** 🚨
