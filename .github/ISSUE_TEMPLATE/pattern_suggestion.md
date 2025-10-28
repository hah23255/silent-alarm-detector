---
name: New Pattern Suggestion
about: Suggest a new alarm-silencing pattern to detect
title: '[PATTERN] '
labels: pattern, enhancement
assignees: ''
---

## 🔍 Pattern Description

A clear description of the alarm-silencing pattern you want to detect.

**Pattern Name:** (e.g., "Resource Leak", "Implicit Type Coercion")

## ❌ Bad Code Example

```python
# Example of code that exhibits this problematic pattern
# This should be detected and blocked/warned
```

## ✅ Good Code Example

```python
# Example of the correct way to write this code
# What the recommendation should suggest
```

## 💥 Real-World Impact

Why is this pattern problematic? What are the consequences?

**Impact Categories:**
- [ ] 🐌 Performance degradation
- [ ] 🔓 Security vulnerability
- [ ] 🔧 Maintainability issues
- [ ] 🧪 Testing problems
- [ ] 📊 Other: ___________

**Estimated Impact:**
- Performance cost: ___ (0-100)
- Security risk: ___ (0-100)
- Maintainability debt: ___ (0-100)
- Est. debug hours: ___ (if it causes issues)

## 📚 Research / Evidence

Provide evidence that this is a real problem:

- [ ] I've seen LLMs generate this pattern
- [ ] This caused a production issue for me/my team
- [ ] Research papers/articles document this issue
- [ ] Similar tools detect this pattern

**Links/References:**
- Article: [link]
- StackOverflow: [link]
- GitHub issue: [link]

## 🎯 Severity Suggestion

What severity should this detection have?

- [ ] 🚨 CRITICAL - Block execution
- [ ] ⚠️ WARNING - Warn but allow
- [ ] 💡 INFO - Inform only

**Rationale:** ...

## 🔎 Detection Method

(Optional) How might this pattern be detected?

- [ ] Regex pattern matching
- [ ] AST (Abstract Syntax Tree) analysis
- [ ] Both regex + AST
- [ ] Other approach: ___________

**Suggested regex/AST logic:**
```python
# If you have ideas on implementation
```

## 📈 Frequency

How often do you see LLMs generate this pattern?

- [ ] Very frequently (daily)
- [ ] Often (weekly)
- [ ] Sometimes (monthly)
- [ ] Rarely (have seen it)
- [ ] Never seen, but theoretically possible

## 🔄 Similar Patterns

Are there existing patterns in the detector that are similar?

## 📊 False Positive Risk

How likely is this detection to produce false positives?

- [ ] Low - Very specific pattern
- [ ] Medium - Some edge cases
- [ ] High - Many legitimate uses

**Known edge cases where this pattern is acceptable:**
1. ...
2. ...

## 🎓 Educational Value

Would detecting this pattern teach developers good practices?

**What lesson does this teach?**
- ...

---

**Example Pattern Submission:**

```markdown
## Pattern: Implicit None Comparison

❌ Bad:
if variable:  # Implicit None check
    process(variable)

✅ Good:
if variable is not None:  # Explicit None check
    process(variable)

Impact: Breaks when variable is 0, False, [], "" - all falsy but not None
Severity: WARNING
Detection: Regex for `if \w+:` without explicit comparison
```

---

**Checklist:**
- [ ] I provided both bad and good code examples
- [ ] I explained the real-world impact
- [ ] I suggested a severity level
- [ ] I estimated false positive risk
- [ ] I checked if similar patterns already exist
