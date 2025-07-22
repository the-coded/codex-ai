# Token Management & Git Log Modes

> Technical documentation for Codex-AI's intelligent token allocation and 3-level git log strategy.

## Overview

Codex-AI implements a sophisticated token management system that automatically selects the optimal git log mode based on content size and model constraints. This ensures maximum quality while staying within Claude's context limits.

## Token Allocation Strategy

### Formula
```python
# Using constants from constants/ai.py
effective_limit = (
    AI_MODELS["CLAUDE_4_SONNET"]["max_tokens"] -           # 200,000 tokens
    AI_MODELS["CLAUDE_4_SONNET"]["max_output_tokens"] -    # 64,000 tokens
    TOKEN_STRATEGY["PROMPT_OVERHEAD"]                      # 15,000 tokens
) * TOKEN_STRATEGY["SAFETY_MARGIN"]                       # 0.95 (95%)

# Result: (200K - 64K - 15K) × 0.95 = 114,950 tokens available for git log
```

### Component Breakdown
| Component | Tokens | Percentage | Purpose |
|-----------|--------|------------|---------|
| **Git Log Content** | 114,950 | 57% | Actual commit data |
| **AI Response** | 64,000 | 32% | Generated changelog |
| **Prompt + Metadata** | 15,000 | 8% | Instructions + overhead |
| **Safety Buffer** | 6,050 | 3% | Error margin |
| **Total** | 200,000 | 100% | Claude context window |

## 3-Level Git Log Strategy

### Mode Selection Logic
```python
def select_git_log_mode(commit_count: int) -> str:
    """Select optimal git log mode based on commit count and token estimation."""
    
    # Estimate tokens for each mode
    detailed_estimate = commit_count * 15000  # ~15K tokens per commit (full patch)
    medium_estimate = commit_count * 3000     # ~3K tokens per commit (diff summary)
    simple_estimate = commit_count * 120      # ~120 tokens per commit (file list)
    
    token_limit = get_effective_token_limit("CLAUDE_4_SONNET")  # 114,950
    
    if detailed_estimate <= token_limit:
        return "detailed"
    elif medium_estimate <= token_limit:
        return "medium"
    else:
        return "simple"
```

### Mode Characteristics

#### 1. Detailed Mode (≤7 commits)
- **Content**: Full git patches with complete diff context
- **Token Usage**: ~15,000 tokens per commit
- **Quality**: Maximum - includes all code changes
- **Use Case**: Small feature branches, bug fixes, single commits

**Example Output:**
```
COMMIT: a1b2c3d4 | John Doe | 2024-06-24 10:30:00
  feat: Add user authentication

diff --git a/src/auth.js b/src/auth.js
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/src/auth.js
@@ -0,0 +1,25 @@
+export function authenticate(user, password) {
+  // Full implementation here...
+}
```

#### 2. Medium Mode (8-20 commits)
- **Content**: File statistics + limited diff summaries
- **Token Usage**: ~3,000 tokens per commit
- **Quality**: Balanced - shows key changes without full context
- **Use Case**: Feature development, moderate-sized PRs

**Configuration (from `constants/git.py`):**
```python
GIT_LOG_LIMITS = {
    "MEDIUM_MAX_LINES_PER_FILE": 50,    # Max diff lines per file
    "MEDIUM_MAX_LINE_LENGTH": 200,      # Max characters per line
    "MEDIUM_TRUNCATION_MARKER": "... [truncated]"
}
```

**Example Output:**
```
COMMIT: a1b2c3d4 | John Doe | 2024-06-24 10:30:00
  feat: Add user authentication
  Files:
    A	src/auth.js
    M	src/app.js

File Statistics:
 src/auth.js  | 25 +++++++++++++++++++++++++
 src/app.js   |  3 +++
 2 files changed, 28 insertions(+)

Diff Summary:
diff --git a/src/auth.js b/src/auth.js
new file mode 100644
+export function authenticate(user, password) {
+  return validateCredentials(user, password);
+}
... [diff truncated after 50 lines]
```

#### 3. Simple Mode (21+ commits)
- **Content**: File lists with change status only
- **Token Usage**: ~120 tokens per commit
- **Quality**: Basic - shows what changed, not how
- **Use Case**: Large releases, full project history

**Example Output:**
```
COMMIT: a1b2c3d4 | John Doe | 2024-06-24 10:30:00
  feat: Add user authentication
  Files:
    A	src/auth.js
    M	src/app.js
    M	package.json
```

## Automatic Fallback Chain

### Implementation
```python
def generate_changelog_with_fallback(commits, since_commit=None):
    """Generate changelog with automatic mode fallback."""
    
    # Try detailed first
    if try_detailed_log(commits):
        return generate_detailed_changelog()
    
    # Fall back to medium
    if try_medium_log(commits):
        return generate_medium_changelog()
    
    # Final fallback to simple (always works)
    return generate_simple_changelog()
```

### Fallback Triggers
1. **Detailed → Medium**: When detailed log exceeds 114,950 tokens
2. **Medium → Simple**: When medium log exceeds 114,950 tokens
3. **Simple**: Always succeeds (guaranteed under token limit)

## Performance Benchmarks

### Real-World Test Results

| Commits | Detailed Tokens | Medium Tokens | Simple Tokens | Mode Used | Quality Score |
|---------|----------------|---------------|---------------|-----------|---------------|
| 7       | 101,238        | -             | -             | Detailed  | 10/10         |
| 17      | 192,161        | 62,634        | -             | Medium    | 8/10          |
| 68      | 330,363        | 162,713       | 8,323         | Simple    | 6/10          |

### Token Efficiency
- **Detailed**: 14,462 tokens/commit average
- **Medium**: 3,684 tokens/commit average  
- **Simple**: 122 tokens/commit average

## Configuration Constants

### AI Models (`constants/ai.py`)
```python
AI_MODELS = {
    "CLAUDE_4_SONNET": {
        "max_tokens": 200000,        # Context window
        "max_output_tokens": 64000,  # Reserved for response
        "priority": 1
    }
}

TOKEN_STRATEGY = {
    "SAFETY_MARGIN": 0.95,          # 95% utilization limit
    "PROMPT_OVERHEAD": 15000,       # Prompt + metadata tokens
    "AUTO_MODEL_SELECTION": True,
    "SIMPLE_LOG_FALLBACK": True
}
```

### Git Log Limits (`constants/git.py`)
```python
GIT_LOG_LIMITS = {
    "MEDIUM_MAX_LINES_PER_FILE": 50,    # Diff lines per file
    "MEDIUM_MAX_LINE_LENGTH": 200,      # Characters per line
    "MEDIUM_TRUNCATION_MARKER": "... [truncated]"
}
```

## Optimization Techniques

### 1. Intelligent Truncation
- **Line Limits**: Prevent extremely long diffs
- **Character Limits**: Avoid token-heavy lines
- **Smart Markers**: Clear truncation indicators

### 2. Content Filtering
- **Exclude Patterns**: Skip generated/binary files
- **Relevant Changes**: Focus on meaningful modifications
- **Merge Handling**: Special processing for merge commits

### 3. Token Estimation
- **Pre-calculation**: Estimate before generation
- **Dynamic Adjustment**: Real-time token counting
- **Fallback Triggers**: Automatic mode switching

## Troubleshooting

### Common Issues

#### "Detailed log too large"
```bash
📊 Detailed log tokens: 192,161
⚠️ Detailed log too large (192,161 tokens), trying medium...
```
**Solution**: Automatic fallback to medium mode. No action needed.

#### "Even simple log too large"
```bash
📊 Simple log tokens: 250,000
❌ Even simple log too large (250,000 tokens)
```
**Solution**: Reduce commit range with `--since` parameter.

#### Token count discrepancies
**Cause**: Different tokenization between estimation and actual usage.
**Solution**: Constants are calibrated based on real-world testing.

### Debug Commands
```bash
# Verbose mode shows token decisions
codex-ai changelog --verbose

# Test with specific ranges
codex-ai changelog --since "HEAD~10" --verbose
codex-ai changelog --since "v1.0.0" --verbose
```

## Best Practices

### For Users
1. **Small Changes**: Use detailed mode for maximum quality
2. **Medium Changes**: Trust medium mode for good balance
3. **Large Changes**: Accept simple mode for overview
4. **Custom Ranges**: Use `--since` to control scope

### For Developers
1. **Constant Updates**: Modify `GIT_LOG_LIMITS` for different quality/size trade-offs
2. **Token Monitoring**: Watch real-world usage patterns
3. **Fallback Testing**: Ensure all modes work correctly
4. **Performance Tuning**: Optimize token estimation accuracy

## Future Improvements

### Planned Enhancements
1. **Dynamic Limits**: Adjust based on content type
2. **Smart Sampling**: Include most important changes in medium mode
3. **Compression**: Better diff summarization algorithms
4. **Model-Specific**: Different strategies per AI model

### Configuration Options
```yaml
# Future codex.config.yaml options
token_management:
  detailed_threshold: 0.6    # Use detailed if under 60% of limit
  medium_threshold: 0.9      # Use medium if under 90% of limit
  custom_limits:
    max_lines_per_file: 75   # Override default 50
    max_line_length: 300     # Override default 200
```

---

**This token management system ensures Codex-AI always generates the highest quality changelog possible within Claude's constraints, automatically adapting to any project size.**
