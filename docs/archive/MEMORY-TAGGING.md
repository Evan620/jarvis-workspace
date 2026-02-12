# Memory Tagging System - Guidelines & Reference

## Overview
This system ensures every piece of information can be:
- **Classified** automatically by type
- **Retrieved** quickly by tag/context
- **Actioned** with clear next steps

---

## Tag Taxonomy

### Primary Tags (Content Type)

#### #task
- Actionable items with clear outcomes
- Examples: "Fix bug in X", "Call John", "Write documentation"
- Always has: [[next-action]] and @context

#### #idea
- Concepts, brainstorming, possibilities
- Examples: "App idea for Y", "Z improvement concept"
- May have: @project or @research

#### #reference
- Information to look up later
- Examples: "API endpoint docs", "Article link", "Tutorial URL"
- Always has: @source or @category

#### #project
- Ongoing work with multiple related tasks
- Examples: "JARVIS Second Brain", "Client ABC automation"
- Always has: [[next-action]] and status (active|on-hold|completed)

#### #meeting
- Notes from calls, conversations, events
- Examples: "Standup with team", "Client discovery call"
- Always has: @participants and date

#### #learning
- New knowledge, tutorials, courses
- Examples: "Learned about X pattern", "Completed Y tutorial"
- Always has: @category and progress level

---

## Context Tags (@)

### @work
Professional tasks, client work, business operations

### @personal
Personal life, health, hobbies, family

### @learning
Education, courses, skill development

### @project-[name]
Specific project contexts (@project-jarvis, @project-client-x)

### @urgent
Time-sensitive, do today

### @waiting
Blocked on someone/something else

### @someday
Nice to have, no deadline

### @source-[where]
Origin of information (@source-video, @source-article, @source-conversation)

---

## Next Actions Syntax

### Format
```
[[next-action: ACTION TEXT | priority: high|medium|low | due: DATE/TIME]]
```

### Examples
```
[[next-action: Draft proposal email to client | priority: high | due: 2026-02-07 10:00]]
[[next-action: Test Zapier automation before deploying | priority: medium | due: This week]]
[[next-action: Read Python async programming tutorial | priority: low | due: Someday]]
```

---

## Complete Entry Examples

### Task Entry
```markdown
## 2026-02-06 14:30: Fix Zapier webhook timeout issue

#task #bug @work @urgent @project-client-abc

Context: Client's Zapier integration is timing out after 30s when processing large payloads.

[[next-action: Increase timeout to 120s in Zapier step, test with 5MB payload | priority: high | due: 2026-02-06 18:00]]

Error details:
- Zapier step: "Webhooks - Catch Hook"
- Current timeout: 30s
- Payload size: ~8MB
- Error message: "Execution timed out after 30s"
```

### Idea Entry
```markdown
## 2026-02-06 11:15: AI-powered meeting notes auto-classifier

#idea @work @project-jarvis

Concept: Use Claude/ChatGPT API to automatically classify meeting notes into action items, decisions, and context notes.

Possible implementation:
1. Zapier receives meeting notes (Slack/Notion)
2. Send to AI API for classification
3. Route to NEXT-ACTIONS.md (if task) or MEMORY.md (if reference)
4. Add appropriate tags automatically

Benefits:
- No manual tagging required
- Faster action item extraction
- Better retrieval later
```

### Reference Entry
```markdown
## 2026-02-06 09:00: Nate Jones Second Brain Article

#reference #learning @source-article @second-brain

URL: https://natesnewsletter.substack.com/p/50-people-ignored-my-tool-recommendations

Key takeaways:
- Architecture is portable, tools are not
- Community + AI = pattern library + implementation
- If agent builds it, agent can maintain it
- System should be infrastructure, not tool

Related: Nate Jones YouTube video analysis (see session-logs/2026-02-06.md)
```

### Project Entry
```markdown
## 2026-02-06 08:00: JARVIS Second Brain Upgrade

#project @project-jarvis @work

Status: active
Started: 2026-02-06
Goal: Implement Nate Jones' 8 second brain improvements

[[next-action: Complete Week 1 implementation (session logging + next action tracking) | priority: high | due: 2026-02-06]]

Milestones:
- ✅ Week 1: Session logging + Next actions (2026-02-06)
- ⏳ Week 2: Auto-classification + Tagging system (2026-02-13)
- ⏳ Week 3: Fix button + Principles-based skills (2026-02-20)
- ⏳ Week 4: Self-maintenance + Daily outputs (2026-02-27)

Dependencies:
- Nate Jones video analysis ✅
- SKILL file availability ✅
```

---

## Auto-Classification Rules (For JARVIS)

When processing incoming information, apply these rules:

### 1. Actionable with deadline? → #task @urgent
   - Add: [[next-action: ... | priority: high | due: DATE]]

### 2. Actionable without deadline? → #task @work/@personal
   - Add: [[next-action: ... | priority: medium | due: This week]]

### 3. Concept/possibility? → #idea
   - Add: @project if related, @research if exploratory

### 4. Resource/tutorial/article? → #reference
   - Add: @source-video, @source-article, @source-conversation

### 5. Multi-step ongoing work? → #project
   - Add: milestones and dependencies

### 6. Notes from conversation? → #meeting
   - Add: @participants, date, any action items as nested #task

### 7. New skill learned? → #learning
   - Add: @category, progress level (beginner|intermediate|advanced)

---

## Retrieval Examples

### Find all urgent tasks
```
Search: #task @urgent
```

### Find project-related references
```
Search: #reference @project-jarvis
```

### Find meeting notes with specific person
```
Search: #meeting @participants-john
```

### Find learning resources on a topic
```
Search: #learning @category-python
```

### Find all action items for a project
```
Search: @project-client-abc
```

---

## Integration Points

### In Daily Notes (memory/YYYY-MM-DD.md)
- Tag every entry with appropriate #tag and @context
- Add [[next-action]] for all actionable items
- Link to project with @project-[name] if applicable

### In MEMORY.md
- Use #reference and #learning tags for long-term knowledge
- Use @source-[where] for provenance
- Link to specific daily notes with "See: memory/YYYY-MM-DD.md"

### In NEXT-ACTIONS.md
- All #task entries should have corresponding entry
- Update status as tasks complete
- Remove from queue when done

---

## Best Practices

1. **One tag per entry** (primary purpose)
2. **Multiple @context tags** (cross-reference)
3. **Always add [[next-action]] for #task**
4. **Date everything** (YYYY-MM-DD format)
5. **Be specific with @project** (use -name suffix)
6. **Link related items** (See: memory/YYYY-MM-DD.md)
7. **Review weekly** during maintenance cycle
8. **Archive completed tasks** (move to completed section)

---

**Last Updated:** 2026-02-06
**Version:** 1.0
**Maintained By:** JARVIS
