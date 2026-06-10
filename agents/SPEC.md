# FreedomAgent Network - Architecture Specification

## Network Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (You - Paul)                     │
│                   Direct Communication Channel                   │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Direct commands
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🔥 JAMES (Director Agent)                    │
│                                                                  │
│  - Primary interface for you                                     │
│  - Receives all direct commands                                 │
│  - Delegates to specialist agents                               │
│  - Maintains network state & coordination                      │
│  - Long-term memory: persistent                                 │
│  - Model: MiniMax M2.5 (primary) / GPT-OSS (fallback)           │
└─────────────────────────────────────────────────────────────────┘
           │            │            │            │
    ┌──────┘            │            │            └──────┐
    │                   │            │                   │
    ▼                   ▼            ▼                   ▼
┌──────────┐      ┌──────────┐  ┌──────────┐      ┌──────────┐
│RESEARCH  │      │CONTENT   │  │OPERATIONS│      │ HELPER   │
│ AGENT    │      │ AGENT    │  │  AGENT   │      │ AGENT    │
│          │      │          │  │          │      │          │
│Web search│      │Drafting  │  │ Execution│      │FAQ answers│
│Data fetch│      │Editing   │  │Automation│      │Troubleshoot│
│Analysis │      │Publishing│  │ Tasks    │      │Self-heal │
│Reports   │      │SEO       │  │Scheduling│      │Monitoring│
└──────────┘      └──────────┘  └──────────┘      └──────────┘
                                                      │
                                                      ▼
                                           ┌──────────────────┐
                                           │  AUTO-RESOLVE    │
                                           │   MECHANISM      │
                                           │                  │
                                           │ - Issue detection│
                                           │ - Diagnostics    │
                                           │ - Self-remediation│
                                           │ - Escalation     │
                                           └──────────────────┘
```

## Agent Specifications

### JAMES (Director)

**Identity:**
- Name: James (named after Jimbob)
- Role: Director / Orchestrator
- Personality: Warm, capable, in-it-together

**Capabilities:**
- All tools available
- Can spawn subagents
- Can delegate to any specialist agent
- Persistent memory across sessions

**Memory:**
- Long-term: 200K+ tokens
- Stores: conversation history, preferences, network state

**Security:**
- Full tool access
- No restrictions

---

### RESEARCH AGENT

**Identity:**
- Name: Researcher
- Role: Data gathering and analysis

**Capabilities:**
- web_search, web_fetch, browser
- read (file access)
- Analysis and reporting

**Memory:**
- Session-scoped (per task)
- No persistent memory by default

**Security:**
- No exec tools
- No write access to sensitive paths
- Read-only to workspace

---

### CONTENT AGENT

**Identity:**
- Name: Creator
- Role: Content creation and editing

**Capabilities:**
- write, edit, read (file access)
- Email composition
- Publishing workflows

**Memory:**
- Persistent (learns your preferences)
- Stores style guides, brand voice

**Security:**
- No exec tools
- No shell commands
- File write to content directories only

---

### OPERATIONS AGENT

**Identity:**
- Name: Operator
- Role: Task execution and automation

**Capabilities:**
- exec (with approval for sensitive)
- cron scheduling
- webhooks
- Task automation

**Memory:**
- Session + scheduled task memory
- Stores automation configs

**Security:**
- Elevated exec (approval for sensitive)
- Timeout on all operations
- No file delete without confirmation

---

### HELPER AGENT (FAQ + Troubleshooting + Auto-Resolve)

**Identity:**
- Name: Helper
- Role: Support, FAQ, troubleshooting, self-healing

**Capabilities:**
- read (knowledge bases)
- search (FAQ database)
- diagnostics
- Limited exec for self-healing

**Memory:**
- Knowledge base + issue history
- Persistent across sessions

**Auto-Resolve Capabilities:**
1. Detect common issues
2. Run diagnostic checks
3. Apply known fixes
4. Verify resolution
5. Escalate if unresolved

**Security:**
- Read-only to most systems
- Limited self-heal exec (restart, clear cache, re-auth)

---

## Communication Protocol

### Delegation Flow

```
YOU → JAMES (Director)
         │
         ├─→ "Research X" → RESEARCH AGENT → Results → JAMES → YOU
         ├─→ "Write Y" → CONTENT AGENT → Draft → JAMES → YOU  
         ├─→ "Do Z" → OPERATIONS AGENT → Execute → JAMES → YOU
         └─→ "Help with issue" → HELPER AGENT → Resolution → JAMES → YOU
```

### Helper Agent Auto-Trigger

The Helper Agent activates automatically when:
1. Error/exception detected in execution
2. Tool returns failure
3. You ask "why did X fail?"
4. You ask "how do I..." (FAQ lookup)
5. System health check runs

---

## Security Layers

### Layer 1: Agent Permissions
- Each agent has tool allowlist
- No agent has full access by default
- Restricted paths for file operations

### Layer 2: Execution Controls
- Sensitive exec requires approval
- All external calls have timeouts
- Queue caps on resources

### Layer 3: Data Protection
- Sensitive files owner-only
- Symlink resolution blocked for escape
- No access to internal networks

### Layer 4: Monitoring
- All tool calls logged
- Issue tracking
- Escalation paths

---

## Model Selection Strategy

| Task Type | Primary Model | Fallback |
|-----------|---------------|----------|
| Direct conversation | MiniMax M2.5 | GPT-OSS |
| Research | MiniMax M2.5 | Gemini Flash |
| Content creation | MiniMax M2.5 | GPT-OSS |
| Operations | GPT-OSS | MiniMax M2.5 |
| Diagnostics | GPT-OSS | MiniMax M2.5 |

---

*Spec Version: 1.0*
*Created: 2026-05-15*