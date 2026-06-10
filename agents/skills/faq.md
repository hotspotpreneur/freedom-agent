# FAQ Lookup Skill

## Overview

This skill enables the Helper Agent to answer frequently asked questions by searching the knowledge base and providing relevant answers.

## Activation

This skill activates when:
1. User asks "how do I..." or "how to..."
2. User asks "what is..." or "explain..."
3. User asks "can agents..."
4. User asks FAQ-type questions
5. Manual trigger: `/faq [search term]`

## Knowledge Base Search

### Primary Sources
1. `agents/helper-agent.md` - Main FAQ knowledge base
2. `agents/SPEC.md` - Architecture specification
3. `MEMORY.md` - Long-term memory (if relevant)
4. `openclaw.json` - Configuration details

### Search Priority
1. Exact match in helper-agent.md
2. Partial match in helper-agent.md
3. Related content in SPEC.md
4. Context from MEMORY.md

## Response Templates

### For "How do I..." questions:
```
**Answer:**

[Step-by-step if applicable]

**Source:** [file]
```

### For "What is..." questions:
```
**Explanation:**

[Clear definition]

**More info:** [optional related context]
```

### For Troubleshooting:
```
**Issue:** [User's problem]

**Try this:**
1. [First step]
2. [Second step]
3. [If still not working]

**Need more help?** Let me know what happens.
```

---

## Known FAQ Categories

### Category: Getting Started
- How do I deploy an agent?
- Can agents work offline?
- How does memory work?
- Which platforms can agents integrate with?

### Category: Usage & Limits
- Why does my agent say "good night" at 3pm?
- Can agents remember across different channels?
- How much do they cost?
- Can agents post directly to social media?
- Why is my agent responding slowly?

### Category: Troubleshooting
- Agent not responding
- Memory not persisting
- Tool execution fails
- Browser actions not working
- High token usage
- Voice/TTS not working

### Category: Security
- Is my data secure?
- Can agents read my files?
- Can agents execute commands on my system?

---

## Quick Answers

### Q: How do I start?
A: Just talk to James (me)! I'll coordinate everything. Say what you need and I'll handle it.

### Q: Can you do X?
A: I can do most things - research, writing, automation. Some things need manual handoff (like posting to social media directly). What would you like to do?

### Q: Why aren't you responding?
A: Let me check... [runs diagnostics] Here's what I found: [issue/solution]

### Q: How do I change your settings?
A: I can update my configuration. What would you like to change?

### Q: Can you remember X?
A: Yes! I have persistent memory. Say "remember [thing]" and I'll save it. Want me to remember something?

---

## Escalation to Full Help

If FAQ doesn't fully answer the question:
1. Say "Let me dig deeper..."
2. Run research or diagnostics
3. Provide personalized answer
4. Update FAQ if it was a new question

---

## Usage

Paul can ask:
- "How do I..." → FAQ lookup
- "Why did X fail?" → Auto-resolve trigger
- "What's the status?" → Diagnostics
- "Help me with..." → Full support mode

---

*FAQ Lookup Skill v1.0 - Created 2026-05-15*