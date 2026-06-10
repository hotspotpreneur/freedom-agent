# FreedomAgent Network - Security Guide

## Security Philosophy

The FreedomAgent network is designed to be **secure by default** while remaining **fast and capable**. We balance safety with functionality - security shouldn't get in the way of getting things done.

---

## Security Layers

### Layer 1: Network Security

| Setting | Protection | Default |
|---------|------------|---------|
| Bind Address | Restricts who can access | LAN + localhost |
| Bearer Token | API authentication | Enabled |
| SSL/TLS | Encryption in transit | Required |
| Trusted Proxies | Internal network trust | Configured |

**Current Config:** Gateway binds to LAN with bearer token auth.

---

### Layer 2: Agent Permissions

Each agent has **tool allowlists** - they can only use approved tools.

#### James (Director)
```
✅ ALL TOOLS - Full access
✅ exec, read, write, edit
✅ web_search, web_fetch, browser
✅ message, spawn subagents
```

#### Research Agent
```
✅ web_search, web_fetch, browser
✅ read (workspace only)
✅ pdf
❌ exec - NOT ALLOWED
❌ write - NOT ALLOWED
❌ message - NOT ALLOWED
```

#### Content Agent
```
✅ read, write, edit
✅ pdf
❌ exec - NOT ALLOWED
❌ web_search - NOT ALLOWED (use Research Agent)
❌ browser - NOT ALLOWED
❌ message - NOT ALLOWED
```

#### Operations Agent
```
✅ exec (with approval for sensitive)
✅ read, write, edit
❌ web_search - NOT ALLOWED
❌ message - NOT ALLOWED
⚠️ Sensitive exec requires your approval
```

#### Helper Agent
```
✅ read (knowledge bases)
✅ search (FAQ lookup)
✅ Limited exec (self-healing only)
⚠️ Can restart tools, clear cache, re-auth
⚠️ Cannot modify user files
```

---

### Layer 3: Execution Controls

| Control | Purpose | Setting |
|---------|---------|---------|
| Timeout | Prevent hung operations | All tools have timeouts |
| Queue Cap | Resource limits | Configured per-tool |
| Approval | Sensitive command confirmation | On for exec |
| Cleanup | Resource cleanup after use | Automatic |

**Current Config:**
- `exec` security: "full" with ask="off" (but approval system active)
- All external calls have timeouts
- Sensitive operations require approval

---

### Layer 4: Data Protection

| Protection | Implementation |
|------------|----------------|
| File Isolation | Each agent has workspace boundary |
| Symlink Blocking | No escape via symlinks |
| Owner-Only | Sensitive files chmod 600 |
| No Internal Access | Blocks internal IP ranges |

**Workspaces:**
- James: Full workspace access
- Research: `workspace/research/`
- Content: `workspace/content/`
- Operations: `workspace/operations/`
- Helper: `workspace/helper/` + knowledge bases

---

### Layer 5: Monitoring & Audit

| Monitoring | Implementation |
|------------|----------------|
| Session Logging | All sessions logged to DAG structure |
| Tool Call Logging | Every tool call recorded |
| Issue Tracking | Issues logged to `memory/issues/` |
| Escalation | Automatic human notification |

---

## Threat Model & Mitigations

### Threat: Prompt Injection
**Risk:** External input could manipulate agent  
**Mitigation:** 
- Input sanitization
- No execution of injected commands
- Agent has boundaries

### Threat: Data Exfiltration  
**Risk:** Agent could leak sensitive data  
**Mitigation:**
- No external message sending without approval
- File access restricted to workspaces
- Network egress monitoring

### Threat: Unauthorized Access
**Risk:** Someone else accesses the agent  
**Mitigation:**
- Bearer token authentication
- Bind to LAN (not public)
- Token rotation possible

### Threat: Resource Exhaustion
**Risk:** Agent consumes excessive resources  
**Mitigation:**
- Timeout on all operations
- Queue caps
- Session compaction limits

---

## Configuration Reference

### Gateway Security
```json
{
  "gateway": {
    "bind": "lan",
    "auth": {
      "token": "token-..."
    }
  }
}
```

### Tool Security
```json
{
  "tools": {
    "exec": {
      "host": "gateway", 
      "security": "full",
      "ask": "off"
    }
  }
}
```

### Per-Agent Permissions
Each agent has `tools.allow` and `tools.deny` lists in config.

---

## Best Practices

### For Paul (You)
1. **Don't share your token** - Keep it secret
2. **Review approvals** - Check exec requests you get
3. **Use workspaces** - Keep agent workspaces separate
4. **Update keys** - Rotate API keys periodically

### For Agent Behavior
1. **Confirm destructive ops** - Ask before delete
2. **Log actions** - Show what you're doing
3. **Stay in bounds** - Don't access unauthorized paths
4. **Escalate if unsure** - Better to ask than to guess

---

## Emergency Procedures

### If You Suspect Compromise
1. Revoke the bearer token (regenerate in config)
2. Check session logs for anomalies
3. Rotate API keys
4. Review recent tool calls
5. Restore from known-good config backup

### If Agent Is Misbehaving
1. Kill the session: `/reset`
2. Check logs: `logs/`
3. Review recent commands
4. Restart gateway if needed

---

## Security Checklist

- [x] Bearer token configured
- [x] Gateway binds to LAN (not public)
- [x] Agent tool restrictions in place
- [x] Exec requires approval for sensitive
- [x] File access contained to workspaces
- [x] Session logging enabled
- [x] Issue tracking active

---

*Security Guide v1.0 - Created 2026-05-15*