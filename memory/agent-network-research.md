# Agent Network Research - Custom Build

## Date: 2026-05-15

---

## 1. FEATURE COMPARISON - BEST OF EACH SYSTEM

### Felix (sausheong/felix)
**Best Features:**
- ✅ Single binary, zero config - works out of the box
- ✅ Bundled Ollama - runs fully offline with no API keys
- ✅ Per-agent tool allow/deny lists - granular security
- ✅ Stream-failure resilience - auto-retries via non-streaming endpoint
- ✅ Cache-stability invariant - byte-stable request prefixes across turns
- ✅ Smart compaction - token/message threshold triggers with circuit breaker
- ✅ Localhost-only by default + optional bearer token auth
- ✅ File access contained to agent workspace with symlink resolution

### HeyRon
**Best Features:**
- ✅ Agent library with community skills/templates
- ✅ Multiple communication channels (Discord, Telegram, web)
- ✅ Strong memory/persistence system
- ✅ SOUL.md personality customization
- ✅ Cron/scheduled tasks
- ✅ Clear expectations documentation - "can and can't do"

### InstantlyClaw
**Best Features:**
- ✅ Pre-built 9-agent hierarchy (CEO → Managers → Specialists)
- ✅ 15 pre-installed skills/configured integrations
- ✅ 1-click deploy - 60 second setup
- ✅ No Docker/terminal required
- ✅ Managed SSL, firewall, security hardening
- ✅ Team delegation - autonomous task completion

### MaxClaw (MiniMax)
**Best Features:**
- ✅ 10-second one-click deployment
- ✅ 200K+ token persistent memory
- ✅ M2.5 model - 229B params, 1/7-1/20 cost vs Claude
- ✅ 100 tokens/sec inference speed
- ✅ Native Telegram/Discord/Slack integration
- ✅ Always-on, fully managed - zero maintenance
- ✅ Custom persona support
- ✅ Hybrid Lightning Attention architecture

---

## 2. COMMON PROBLEMS & ISSUES

### From OpenClaw GitHub Issues (current):
1. **Approval replay failures** - APPROVAL_CLIENT_MISMATCH for webchat
2. **Tool/status timeout** - Embedded tool runs timeout while text-only succeeds
3. **CLI cold-start regression** - ~14s startup after 2026.5.12 update
4. **Cron cost amplification** - Full transcript sent per tick on long-lived sessions
5. **Truncation sentinels leaking** - `...(truncated)...` appears in final replies
6. **WeChat hot-reload issues** - Monitor stops after new account login
7. **Slack mention formatting** - Plain text instead of mention format

### General Agent Network Issues:
1. **Context window limits** - Forgets after long conversations
2. **Token usage anxiety** - Heavy usage burns credits fast
3. **Browser automation limits** - Can't click through JavaScript-heavy flows
4. **Social media API blocks** - Direct posting often blocked
5. **Memory persistence** - Each channel has separate conversation history
6. **Voice/TTS setup issues** - Requires correct voice ID + API key
7. **Timezone confusion** - Agent reports wrong time of day
8. **Background work stops** - Closing chat tab stops in-thread work
9. **Stale file references** - Agent uses old version of files
10. **API key management** - Rotation, security, environment variables

---

## 3. TROUBLESHOOTING GUIDE

### Issue: Agent Not Responding
- [ ] Check if gateway/service is running
- [ ] Verify API keys are set (ANTHROPIC_API_KEY, etc.)
- [ ] Check network connectivity
- [ ] Review session logs for errors

### Issue: Memory Not Persisting
- [ ] Verify memory files exist in workspace
- [ ] Check memory compaction hasn't run
- [ ] Ensure channel has single conversation (separate = no memory share)
- [ ] Check token limits - may auto-compact

### Issue: Tool Execution Fails
- [ ] Check tool allow/deny lists in config
- [ ] Verify MCP server is running
- [ ] Review per-agent tool permissions
- [ ] Check timeout settings

### Issue: Browser Actions Not Working
- [ ] JavaScript-heavy sites may not work
- [ ] Verify browser capability is enabled
- [ ] Check for CAPTCHAs or bot detection
- [ ] Use web_fetch for simple pages instead

### Issue: High Token Usage
- [ ] Enable token-aware mode (concise responses)
- [ ] Check for cron job amplification
- [ ] Review session compaction settings
- [ ] Set explicit message limits

### Issue: Discord Actions Missing
- [ ] Some UI actions (pin messages) may not be available
- [ ] Verify bot permissions
- [ ] Check if feature requires specific intent

### Issue: Voice/TTS Not Working
- [ ] Verify ElevenLabs API key is correct
- [ ] Check voice ID exists in your account
- [ ] Ensure voice is shared/accessible

---

## 4. FREQUENTLY ASKED QUESTIONS

### Q: How do I deploy an agent?
**A:** Most systems offer 1-click deploy. MaxClaw: 10 seconds. InstantlyClaw: 60 seconds. Self-hosted (OpenClaw): Docker + config.

### Q: Can agents work offline?
**A:** Felix (bundled Ollama) - yes. Others - require API keys for cloud models.

### Q: How does memory work?
**A:** Each platform handles differently. MaxClaw: 200K+ tokens persistent. OpenClaw: local files + vector search. HeyRon: Markdown memory files.

### Q: Which platforms can agents integrate with?
**A:** Most support: Telegram, Discord, Slack, web chat. OpenClaw has broad plugin ecosystem.

### Q: How much do they cost?
**A:** MaxClaw: 1/7-1/20 Claude pricing. InstantlyClaw: $4,497 one-time + $250/yr hosting. Self-hosted: API costs + server.

### Q: Can agents post directly to social media?
**A:** Generally no - API constraints. Can draft content for manual post.

### Q: Why does my agent say "good night" at 3pm?
**A:** Timezone mismatch. Tell agent to check local time and save your timezone in memory.

### Q: Can agents remember across different chat channels?
**A:** Usually no - each channel (Discord DM vs channel) has separate conversation history.

### Q: What's the difference between cloud-hosted vs self-hosted?
**A:** Cloud: zero maintenance, always-on, pay-for-service. Self-hosted: full control, privacy, but requires server management.

### Q: Can agents execute shell commands?
**A:** Yes, but security varies. Felix uses allowlist mode for bash tool. OpenClaw has exec tool with approval system.

---

## 5. SECURITY FEATURES COMPARISON

### Felix Security
- ✅ Localhost-only binding by default
- ✅ Bash tool in allowlist mode (not full shell)
- ✅ Blocks web requests to internal IPs + cloud metadata
- ✅ File access contained to workspace + symlink resolution
- ✅ Owner-only permissions on config/session files
- ✅ Per-agent tool allow/deny lists
- ✅ Optional bearer token auth
- ✅ Config hot-reload (edits apply immediately)

### OpenClaw Security
- ✅ Approval system for elevated commands
- ✅ Configurable security policies
- ✅ Gateway authentication options
- ✅ Tool execution sandboxing

### InstantlyClaw Security
- ✅ SSL encryption
- ✅ Firewall configuration
- ✅ Security hardening (managed)
- ✅ Dedicated instance (data isolation)

### MaxClaw Security
- ✅ Managed infrastructure
- ✅ MiniMax cloud security
- ✅ Data stays on dedicated instance

---

## 6. CUSTOM AGENCY NETWORK DESIGN

### Architecture: "FreedomAgent Network"

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (You)                       │
│                      User Interface                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    🔥 JAMES (Director)                      │
│            Main Agent - Coordination &决策                   │
│         Memory: 200K+ tokens | Model: M2.5/Sonnet            │
└─────────────────────────────────────────────────────────────┘
           │            │            │            │
           ▼            ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   RESEARCH  │ │   CONTENT   │ │   OPERATIONS │ │    HELPER    │
│    AGENT    │ │    AGENT    │ │    AGENT     │ │    AGENT     │
│              │ │              │ │              │ │              │
│ - Web search │ │ - Drafting  │ │ - Execution  │ │ - FAQ answ.  │
│ - Data fetch │ │ - Editing   │ │ - Automation │ │ - Troubleshooting│
│ - Analysis   │ │ - Publishing│ │ - Tasks      │ │ - Self-heal  │
│ - Reports    │ │ - SEO       │ │ - Scheduling │ │ - Monitoring │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
                                                              │
                                                              ▼
                                                   ┌──────────────────┐
                                                   │   AUTO-RESOLVE   │
                                                   │    MECHANISM     │
                                                   │                  │
                                                   │ - Issue detection│
                                                   │ - Self-diagnosis │
                                                   │ - Auto-remediation│
                                                   │ - Escalation     │
                                                   └──────────────────┘
```

### Agent Specifications

#### 🔥 JAMES (Director)
- **Role:** Main orchestrator, delegates to specialist agents
- **Memory:** Persistent, long-term (200K tokens)
- **Model:** MiniMax M2.5 or Claude Sonnet
- **Tools:** All available
- **Security:** Full access, authenticated

#### RESEARCH AGENT
- **Role:** Web research, data gathering, analysis
- **Memory:** Session-scoped
- **Tools:** web_search, web_fetch, browser, read
- **Security:** Limited exec, no file write to sensitive areas

#### CONTENT AGENT
- **Role:** Writing, editing, content creation, publishing
- **Memory:** Persistent (learns preferences)
- **Tools:** write, edit, file management, email
- **Security:** No exec, no system commands

#### OPERATIONS AGENT
- **Role:** Task execution, automation, scheduling
- **Memory:** Session + scheduled task memory
- **Tools:** exec, cron, webhooks, integrations
- **Security:** Elevated with approval for sensitive ops

#### HELPER AGENT (FAQ + Troubleshooting)
- **Role:** Answer questions, troubleshoot issues, self-heal
- **Memory:** Knowledge base + Issue history
- **Tools:** read, search, diagnostic tools
- **Special:** Autonomous issue resolution

### AUTO-RESOLVE MECHANISM

```
Issue Detected → Diagnostic Run → Root Cause ID'd
       │                                   │
       ▼                                   ▼
  [Known Issue?]                    [Remediation Plan]
       │                                   │
       ▼                                   ▼
   Execute Fix                  Apply Fix + Verify
       │                                   │
       ▼                                   ▼
   [Success?]                    [Report to User]
       │                                   │
       No                                 Yes
       ▼                                   ▼
  Escalate to              Mark Resolved + Log
  Human/User
```

**Auto-Resolve Capabilities:**
1. ✅ Restart failed tool/execution
2. ✅ Clear/rebuild session cache
3. ✅ Re-authenticate expired tokens
4. ✅ Rotate API keys on failure
5. ✅ Compaction when near limits
6. ✅ Fallback to alternative model
7. ✅ Escalate when unresolved

### SECURITY IMPLEMENTATION

#### Layer 1: Network Security
- Localhost-only binding (where possible)
- Bearer token authentication
- SSL/TLS encryption

#### Layer 2: Access Control
- Per-agent tool allow/deny lists
- Role-based permissions (Director > Specialists)
- No full shell - allowlist mode for exec

#### Layer 3: Execution Security
- Approval required for elevated commands
- Timeout on all external calls
- Queue caps + resource cleanup
- Block internal IP access

#### Layer 4: Data Security
- File access contained to workspaces
- Symlink resolution prevention
- Owner-only file permissions
- Sensitive data in encrypted storage

#### Layer 5: Monitoring
- Session logging with DAG view
- Automatic issue detection
- Escalation on failure
- Audit trails

### PERFORMANCE OPTIMIZATIONS

1. **Cache-Stable Requests** - Byte-stable prefixes across turns (Felix-inspired)
2. **Smart Compaction** - Token threshold triggers + circuit breaker
3. **Stream Failure Recovery** - Auto-retry via non-streaming endpoint
4. **Parallel Execution** - Independent tasks run concurrently
5. **Model Selection** - Cheap model for simple tasks, premium for complex
6. **Context Optimization** - Strip unused schema fields

### DEPLOYMENT

**Recommended Stack:**
- **Gateway:** OpenClaw (self-hosted for full control) or Felix
- **Model:** MiniMax M2.5 (cost) + Claude Sonnet (quality fallback)
- **Memory:** Local files + vector search
- **Deployment:** Docker on VPS or local machine
- **Channels:** Discord + Telegram

---

## Action Items

- [ ] Implement agent hierarchy in code
- [ ] Build Helper Agent with FAQ knowledge base
- [ ] Create Auto-Resolve mechanism
- [ ] Configure security policies
- [ ] Test each agent's tool permissions
- [ ] Set up monitoring + logging
- [ ] Document initial FAQ answers

---

*Research completed: 2026-05-15*
*Sources: Felix GitHub, HeyRon docs, InstantlyClaw, MaxClaw, OpenClaw issues*