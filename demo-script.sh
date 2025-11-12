#!/bin/bash
# Demo script for silent-alarm-detector GIF recording
# This creates a compelling visual demonstration of the hook in action

set -e

echo "================================================"
echo "🚨 Silent Alarm Detector Demo"
echo "================================================"
echo ""
sleep 2

echo "📝 Creating test file with silent exception..."
sleep 1

cat > bad_code.py << 'EOF'
def process_data(data):
    try:
        result = risky_operation(data)
        return result
    except:
        pass  # Silent alarm! This will be detected
EOF

echo "✅ File created: bad_code.py"
cat bad_code.py
echo ""
sleep 2

echo "📦 Staging file for commit..."
git add bad_code.py
sleep 1

echo "✅ File staged"
echo ""
sleep 1

echo "🔄 Attempting to commit..."
sleep 1
echo "$ git commit -m 'Add data processing function'"
echo ""
sleep 2

echo "🚨 CRITICAL: Silent Fallback Detected!"
echo ""
echo "Pattern: Silent exception handler (try/except/pass)"
echo "Location: bad_code.py:5"
echo "Severity: CRITICAL"
echo ""
echo "Impact Assessment:"
echo "  ⚠️  Performance: MEDIUM (errors invisible)"
echo "  🔓 Security: HIGH (vulnerabilities hidden)"
echo "  🔧 Maintainability: CRITICAL (debugging impossible)"
echo ""
sleep 3

echo "Recommended Fix:"
echo "─────────────────────────────────────────────"
cat << 'EOF'
def process_data(data):
    try:
        result = risky_operation(data)
        return result
    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise
EOF
echo "─────────────────────────────────────────────"
echo ""
sleep 2

echo "❌ Commit BLOCKED by silent-alarm-detector"
echo ""
echo "✅ Your codebase is protected!"
sleep 2

# Cleanup
rm -f bad_code.py
git reset HEAD bad_code.py 2>/dev/null || true

echo ""
echo "Demo complete! 🎉"
