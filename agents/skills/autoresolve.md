# Auto-Resolve Skill

## Overview

This skill enables autonomous issue detection, diagnosis, and resolution for the FreedomAgent network. When issues occur, this skill orchestrates the fix attempt sequence.

## Triggers

This skill activates when:
1. A tool returns an error
2. A tool times out
3. A user asks "why did X fail?"
4. A health check runs
5. Manual trigger: `/autoresolve`

## Issue Categories & Resolution Playbooks

### CATEGORY: TOOL_TIMEOUT

**Symptoms:**
- Tool call exceeds timeout
- "Request timed out" error

**Resolution Playbook:**
```
1. Log: "Timeout on [tool_name], attempt [N]"
2. Retry with exponential backoff (2s, 4s, 8s)
3. If tool supports, try with reduced complexity
4. If still failing after 3 attempts:
   a. Check if alternative tool exists
   b. Try fallback approach
   c. If all fail, escalate with context
```

### CATEGORY: AUTH_FAILURE

**Symptoms:**
- HTTP 401/403 from provider
- "Invalid API key" or "Unauthorized"

**Resolution Playbook:**
```
1. Log: "Auth failure for [provider]"
2. Check config for key validity
3. If key appears invalid:
   a. Note in issue log
   b. Attempt to re-validate
   c. If cannot resolve, flag for human
4. If key valid but rate limited:
   a. Wait and retry with backoff
   b. Use fallback model if available
```

### CATEGORY: CONTEXT_OVERFLOW

**Symptoms:**
- "Context length exceeded" error
- Provider returns max tokens error

**Resolution Playbook:**
```
1. Log: "Context overflow, triggering compaction"
2. Run session compaction
3. Retry the operation
4. If still overflow:
   a. Reset session (warn user first)
   b. Resume with compact context
5. Log what was compacted
```

### CATEGORY: MODEL_UNAVAILABLE

**Symptoms:**
- "Model not found" error
- Provider returns 404
- Rate limiting from specific model

**Resolution Playbook:**
```
1. Log: "Model [model_name] unavailable"
2. Check available models in config
3. Switch to fallback model
4. Resume operation with fallback
5. Notify user of model switch
```

### CATEGORY: NETWORK_ERROR

**Symptoms:**
- Connection refused
- DNS failure
- Timeout on network request

**Resolution Playbook:**
```
1. Log: "Network error: [specific_error]"
2. Retry after 2 seconds
3. Retry with different endpoint if applicable
4. If persistent:
   a. Queue operation for retry later
   b. Notify user of issue
   c. Log for investigation
```

### CATEGORY: FILE_ERROR

**Symptoms:**
- File not found (404)
- Permission denied
- Path traversal blocked

**Resolution Playbook:**
```
1. Log: "File error: [path] - [error]"
2. Verify parent directory exists
3. For read: suggest alternative paths
4. For write: create directory if needed
5. If permission error, escalate
```

### CATEGORY: BROWSER_ERROR

**Symptoms:**
- Cannot connect to browser CDP
- Browser returns error
- Page load failure

**Resolution Playbook:**
```
1. Log: "Browser error: [details]"
2. Check browser service status
3. Attempt CDP reconnection
4. Fall back to web_fetch if browser fails
5. If all fail, note in issue log
```

### CATEGORY: MEMORY_ERROR

**Symptoms:**
- Cannot read memory files
- Memory file corrupted
- Memory write fails

**Resolution Playbook:**
```
1. Log: "Memory error: [file]"
2. Backup corrupted file if exists
3. Recreate memory structure
4. Start fresh memory context
5. Log incident for review
```

---

## Resolution Statuses

| Status | Meaning | Next Action |
|--------|---------|-------------|
| DETECTED | Issue identified | Run playbook |
| RESOLVED | Fix successful | Log and report |
| FAILED | Fix attempted but didn't work | Try next playbook or escalate |
| ESCALATED | Cannot resolve automatically | Notify human |

---

## Escalation Criteria

Escalate to Paul when:
- [ ] 3+ failed resolution attempts
- [ ] Unknown issue (no matching category)
- [ ] Data loss risk
- [ ] Security concern
- [ ] Recurring same issue 3+ times
- [ ] Paul explicitly requested notification

**Escalation Message Format:**
```
⚠️ ESCALATION: [Issue Title]

**What happened:** [Brief description]
**Error:** [Specific error message]
**Tried:** [List of attempted fixes]
**Suggestion:** [What might help]
```

---

## Diagnostic Commands

The Helper Agent can run these when troubleshooting:

### /diagnose session
Checks:
- Token usage / context size
- Session file integrity
- Last activity time
- Compaction status

### /diagnose memory
Checks:
- Memory files exist and readable
- Recent writes
- Corruption detection
- Size estimates

### /diagnose tools
Checks:
- Available tools
- Tool permissions
- MCP server status
- Recent tool errors

### /diagnose network
Checks:
- Provider connectivity
- API key status
- Rate limit status
- Latency estimates

### /diagnose models
Checks:
- Configured models
- Model availability
- Fallback chain status

### /diagnose config
Checks:
- Current configuration
- Security settings
- Channel status

### /diagnose recent
Checks:
- Last 10 errors
- Error patterns
- Issue history

---

## Logging

All auto-resolve actions are logged to:
`memory/issues/[YYYY-MM-DD].md`

Format:
```
## [Timestamp] - [Issue Category]
**Status:** [RESOLVED|FAILED|ESCALATED]
**Issue:** [Description]
**Attempts:** [N]
**Resolution:** [What worked/didn't work]
```

---

## Manual Override

Paul can always:
1. Run `/autoresolve` to force a check
2. Ask "what issues have you fixed?"
3. Request manual escalation
4. Disable auto-resolve with "/autoresolve off"

---

*Auto-Resolve Skill v1.0 - Created 2026-05-15*