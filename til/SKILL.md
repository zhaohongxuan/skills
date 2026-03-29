---
name: til
description: "Summarize links/URLs and create TIL (Today I Learned) note cards as separate Obsidian files with double links. Use when: user shares a link/URL and wants to save a summary to their knowledge base. This skill fetches the URL content, extracts key information, generates relevant tags, creates a dedicated .md file in Resources/TIL/, and adds a double link in the daily journal with #TIL hashtag."
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["curl", "python3"] } } }
---

## Summary
The `til` skill transforms links into knowledge cards stored as separate Obsidian notes with double links.

### Use Cases
- User shares a link → skill creates separate TIL note → adds double link to journal
- Build a knowledge base from articles, tutorials, docs
- Quick way to save interesting findings without cluttering journal

### Features
- Fetch URL content automatically
- Extract title and key information
- Generate relevant tags based on content
- Create formatted note card as **separate .md file**
- Add **double link** to daily journal (not inline content)
- Auto Git commit and push

### File Structure
```
/root/obsidian-vault-xuan/Resources/TIL/
  └── 2026-03-26_我对_Spec_Driven_Development_的看法.md

/root/obsidian-vault-xuan/Journal/2026/03/2026-03-26.md
  └── - 21:15 📚 TIL: [[Resources/TIL/2026-03-26_我对_Spec_Driven_Development_的看法.md|我对 Spec Driven Development...]]
```

### Recommended Script
1. `til.py` - Main script to fetch URL, create TIL file, and add journal link

### Usage

```bash
# Basic usage - summarize a URL and create TIL note
python3 skills/til/scripts/til.py https://example.com/article

# With custom note
python3 skills/til/scripts/til.py https://example.com/article "这篇讲的是 AI 进展"

# Dry run (don't save, just show output)
python3 skills/til/scripts/til.py https://example.com --dry-run
```

### Output Format

**TIL File** (`Resources/TIL/YYYY-MM-DD_title.md`):
```markdown
---
title: Article Title
source: https://example.com/article
date: 2026-03-26
tags: [#Python #AI #技术]
---

# Article Title

> **来源**: [https://example.com/article](https://example.com/article)
> **标签**: #Python #AI #技术

## 📝 摘要

文章的主要内容摘要...

## 💡 我的笔记

> 个人评注（可选）

---
#TIL #知识积累 #Python #AI #技术
```

**Journal Entry** (double link):
```
- HH:MM 📚 TIL: [[Resources/TIL/2026-03-26_article-title.md|Article Title...]]
```

### Integration
- TIL files saved to: `/root/obsidian-vault-xuan/Resources/TIL/`
- Journal updated: `/root/obsidian-vault-xuan/Journal/YYYY/MM/YYYY-MM-DD.md`
- Uses `journal-manager` pattern for git add/commit/push

### Benefits
1. **知识库分离**: TIL 内容不污染日记，保持日记简洁
2. **双链引用**: 日记中通过 `[[Resources/TIL/...]]` 引用
3. **可搜索**: TIL 文件可独立搜索和整理
4. **可扩展**: 未来可以添加 `Resources/TIL` 到 MOC (Map of Content)