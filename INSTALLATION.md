# Silent Alarm Detector - Installation Guide

Complete step-by-step guide to install and activate the Silent Alarm Detector hook.

## 📋 Prerequisites

- Claude Code installed
- Python 3.7 or higher
- Bash shell access

## 🚀 Quick Install (5 minutes)

### Step 1: Verify Hook Files

The hook should already be in your system. Verify:

```bash
ls -la ~/.claude/hooks/silent-alarm-detector/
```

You should see:
```
.claude-hooks/
analyzers/
config/
data/ (may not exist yet, will be created)
README.md
INSTALLATION.md (this file)
```

### Step 2: Test Hook Components

```bash
# Test pattern detector
cd ~/.claude/hooks/silent-alarm-detector/analyzers
python3 pattern_detector.py
```

Expected output:
```
Found X alarm-silencing patterns:

[CRITICAL] Line X: Bare except: pass silences ALL exceptions
  Impact: ⚠️ Crashes and errors will be invisible...
  Fix: Add logging: logger.exception('Error in X')...
```

If you see this, the detector is working!

### Step 3: Add to Claude Code Settings

Edit your Claude Code settings:

```bash
nano ~/.claude/settings.json
```

Add the Silent Alarm Detector hook to the `PreToolUse` section:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /data/data/com.termux/files/home/.claude/hooks/security_guard.py"
          }
        ]
      },
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 /data/data/com.termux/files/home/.claude/hooks/silent-alarm-detector/.claude-hooks/pre-tool-use/alarm_silencing_detector.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /data/data/com.termux/files/home/.claude/hooks/auto_format.sh"
          }
        ]
      }
    ]
  }
}
```

**Important**: The Silent Alarm Detector runs **after** security_guard.py for coordinated protection.

### Step 4: Verify Installation

Create a test file with problematic code:

```bash
cat > /tmp/test_alarm_silencing.py << 'EOF'
def risky_function():
    try:
        result = 1 / 0
    except:
        pass
    return None
EOF
```

Now test the hook manually:

```bash
cd ~/.claude/hooks/silent-alarm-detector

echo '{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/tmp/test.py",
    "content": "try:\n    x = 1/0\nexcept:\n    pass"
  }
}' | python3 .claude-hooks/pre-tool-use/alarm_silencing_detector.py
```

Expected output (should BLOCK):
```
🚨 CRITICAL ALARM-SILENCING DETECTED!

Found 1 pattern(s) where LLM is silencing alarms:

❌ Line 3: Bare except: pass silences ALL exceptions
   Impact: ⚠️ Crashes and errors will be invisible...
   Fix: Add logging: logger.exception('Error in X')...

🎯 Risk Level: CRITICAL
📊 Impact Score: 85/100

⚠️  These 'minor' issues will have CRUSHING impact on production!
   Please fix before proceeding.
```

If you see this, installation is complete! ✅

## ⚙️ Configuration (Optional)

### Customize Detection Thresholds

Edit the configuration file:

```bash
nano ~/.claude/hooks/silent-alarm-detector/config/detection_rules.yaml
```

Key settings:

```yaml
# Sensitivity mode
sensitivity:
  mode: balanced  # Options: strict, balanced, permissive

# When to block vs warn
thresholds:
  block_on_critical_count: 1   # Block if >= N critical issues
  block_on_impact_score: 80    # Block if total impact >= this
  warn_on_impact_score: 40     # Warn if impact >= this

# Enable/disable specific patterns
patterns:
  silent_fallback:
    enabled: true  # Set to false to disable
```

### Sensitivity Modes

**strict** (Recommended for production code):
- Blocks on any critical issue
- Warns on all warnings
- Maximum protection

**balanced** (Default):
- Blocks on critical issues
- Warns on high/medium impact
- Good balance of protection and flexibility

**permissive** (For experimentation):
- Only blocks on severe security issues
- Minimal warnings
- Use for prototyping only

## 📊 Monitoring

### View Detection Log

```bash
# Real-time monitoring
tail -f ~/.claude/hooks/silent-alarm-detector/data/detection_history.jsonl

# View recent detections (pretty)
tail -10 ~/.claude/hooks/silent-alarm-detector/data/detection_history.jsonl | jq
```

### Analyze Trends

```bash
cd ~/.claude/hooks/silent-alarm-detector/data

# Count by pattern type
cat detection_history.jsonl | jq -r '.detections[].pattern' | sort | uniq -c

# Average impact over time
cat detection_history.jsonl | jq '.impact_score.total_score' | \
    awk '{sum+=$1; n++} END {if(n>0) print "Average Impact:", sum/n}'

# High-risk detections only
cat detection_history.jsonl | jq 'select(.impact_score.risk_level == "HIGH" or .impact_score.risk_level == "CRITICAL")'
```

## 🧪 Testing the Hook in Claude Code

Once installed, the hook will automatically activate when Claude Code tries to write code with alarm-silencing patterns.

Test by asking Claude Code to:

```
"Write a Python function that catches all exceptions and returns None"
```

The hook should BLOCK with a warning about silent exception handling.

## 🔧 Troubleshooting

### Problem: Hook Not Running

**Diagnosis:**
```bash
# Check settings.json is valid
cat ~/.claude/settings.json | jq '.hooks'

# If error, fix JSON syntax
nano ~/.claude/settings.json
```

**Solution:**
- Ensure JSON is valid (no trailing commas, quotes balanced)
- Verify Python path is correct
- Check file permissions: `chmod +x .claude-hooks/pre-tool-use/alarm_silencing_detector.py`

### Problem: Import Errors

**Diagnosis:**
```bash
cd ~/.claude/hooks/silent-alarm-detector
python3 -c "from analyzers.pattern_detector import SilentAlarmDetector; print('OK')"
```

**Solution:**
- Ensure all files are in correct locations
- Check Python version: `python3 --version` (need >= 3.7)
- Reinstall if files are missing

### Problem: Too Many False Positives

**Solution:**
Edit `config/detection_rules.yaml`:

```yaml
# Reduce sensitivity
sensitivity:
  mode: permissive

# Increase thresholds
thresholds:
  block_on_critical_count: 2  # Only block on >= 2 critical
  block_on_impact_score: 90   # Higher threshold

# Disable specific patterns
patterns:
  assumption_bypass:
    enabled: false  # Disable this check
```

### Problem: Hook Blocking Valid Code

Some patterns (like `except: pass` in testing/mocking) may be intentional.

**Options:**

1. **Add logging to make it non-silent:**
```python
# Instead of:
try:
    risky_op()
except:
    pass

# Use:
try:
    risky_op()
except Exception as e:
    logger.debug(f"Expected error in test: {e}")
```

2. **Disable for specific tools:**
Edit `config/detection_rules.yaml`:
```yaml
monitored_tools:
  - Write
  # - Edit  # Disable monitoring of Edit tool
```

3. **Temporarily disable hook:**
Comment out in `~/.claude/settings.json`

## 📈 Performance Impact

The hook is designed for minimal performance impact:

- **Activation time:** ~50-100ms per tool use
- **Memory:** ~10MB
- **CPU:** Negligible (pattern matching is fast)

For very large files (>50K lines), detection is automatically skipped.

## 🔄 Updating

To update the hook with new patterns:

1. Edit `analyzers/pattern_detector.py`
2. Add new detection methods
3. Update `config/detection_rules.yaml` with new pattern settings
4. Test: `python3 analyzers/pattern_detector.py`

## 🤝 Integration with Other Hooks

The Silent Alarm Detector coordinates with other hooks:

### Execution Order

1. **security_guard.py** (Pre-Tool-Use) - Blocks malicious code
2. **alarm_silencing_detector.py** (Pre-Tool-Use) - Blocks quality issues
3. **Tool Executes** (Write/Edit/Bash)
4. **auto_format.sh** (Post-Tool-Use) - Formats code

### Complementary Protection

- **security_guard.py**: Command injection, malicious patterns
- **alarm_silencing_detector.py**: Code quality, technical debt prevention
- **auto_format.sh**: Code style consistency

Together they provide comprehensive code quality enforcement!

## 📞 Support

### Check Hook Status

```bash
# Verify all components
cd ~/.claude/hooks/silent-alarm-detector

echo "Testing pattern_detector.py..."
python3 analyzers/pattern_detector.py

echo "Testing impact_assessor.py..."
python3 analyzers/impact_assessor.py

echo "Testing main hook..."
echo '{"tool_name":"Write","tool_input":{"content":"x=1"}}' | \
    python3 .claude-hooks/pre-tool-use/alarm_silencing_detector.py

echo "All tests passed!"
```

### View Logs

```bash
# Hook execution errors (if any)
tail -20 ~/.claude/debug/*.txt | grep -i "alarm"

# Detection history
cat ~/.claude/hooks/silent-alarm-detector/data/detection_history.jsonl
```

## ✅ Verification Checklist

After installation, verify:

- [ ] Hook files present in `~/.claude/hooks/silent-alarm-detector/`
- [ ] Test scripts run without errors
- [ ] `settings.json` updated with hook configuration
- [ ] Manual test blocks problematic code
- [ ] Detection log file created (after first detection)
- [ ] No errors in Claude Code when writing code

## 🎓 Next Steps

1. **Use Claude Code normally** - Hook runs automatically
2. **Monitor detection log** - See what issues are being caught
3. **Adjust sensitivity** - Configure based on your needs
4. **Review blocked code** - Learn from the patterns detected
5. **Share with team** - Install on all development machines

---

**Installation Complete!** 🎉

The Silent Alarm Detector will now protect your codebase from "minor" issues that have crushing impact.

For detailed usage and examples, see [README.md](README.md).
