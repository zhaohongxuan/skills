---
name: recap
description: "Generate a daily or weekly summary/recap from journal entries. Use when: user wants to review their day/week, generate a recap summary, add a recap to weekly note, or analyze productivity and activities. This skill reads journal files, analyzes content, and produces a formatted summary with categories like tech, exercise, work, and mood."
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"] } } }
---

## Summary
The `recap` skill generates summaries from journal entries, helping you review your day or week at a glance.

### Use Cases
- Generate a daily recap from today's journal entries
- Create a weekly summary for your week note
- Analyze productivity and categorize activities
- Add formatted recap to weekly notes automatically

### Features
- Read and analyze journal entries
- Categorize content (tech, exercise, work, mood)
- Generate formatted summary with emoji indicators
- Auto-add to weekly note (via journal-manager integration)

### Recommended Script
1. `recap.py` - Main script to generate recap from journal

### Usage

```bash
# Generate today's recap
python3 skills/recap/scripts/recap.py

# Generate recap for a specific date
python3 skills/recap/scripts/recap.py --date 2026-03-26

# Generate weekly recap
python3 skills/recap/scripts/recap.py --week
```

### Output Format
The recap includes:
- **Date/Period**: YYYY-MM-DD or Week X
- **Entry Count**: Number of journal entries
- **Categories**: Tech 💻, Exercise 💪, Work 📋, Mood 🎭
- **Highlights**: Key events and achievements
- **Summary**: AI-generated brief overview

### Integration
Works with `journal-manager` skill to:
- Read from `/root/obsidian-vault-xuan/Journal/YYYY/MM/YYYY-MM-DD.md`
- Write to `/root/obsidian-vault-xuan/Journal/YYYY/MM/YYYY-WXX.md` (weekly note)
