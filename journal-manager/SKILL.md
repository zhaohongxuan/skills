---
name: journal-manager
description: "Manage Markdown-based Obsidian journal entries: create and safely append timestamped notes, convert between time zones, generate per-entry IDs, and avoid accidental overwrites or race conditions. Use when adding daily notes, programmatically appending journal lines, converting existing timestamps between time zones, or when safe atomic appends under concurrent access are required."
metadata: { "openclaw": { "emoji": "📓", "requires": { "bins": ["python3"] } } }
---

## Summary

### Quick Command: /daily
- Use `/daily` to quickly add an entry to the day's journal.

### Features
- Append timestamped lines to daily notes programmatically, with customizable formats (e.g., `HH:MM` for local time).
- Convert journal timestamps across time zones accurately.
- Safely manage concurrent appends to shared journal files.
- Automate backups to prevent data loss during operations.

### Use Cases
- Add a quick note or reflection to today's journal.
- Convert timestamps when traveling or moving between time zones.
- Programmatic journal entry from scripts or automation (e.g., cron jobs).
- Safe concurrent writes from multiple devices (via file locking).

### Recommended Scripts
1. `daily.py` - Quickly add an entry to today's journal with automatic date/time resolution.
2. `append_entry.py` - Handles appending entries with safeguards like locking, duplication checks, and atomic writes.
3. `convert_tz.py` - Converts timestamps in journal files across time zones.
4. `preview_entry.py` - Displays recent journal entries without modifications.
5. `upload_pic.py` - Upload images to GitHub Picgo repository and return markdown/raw links.

### Safeguards
- Atomic writes via temporary files and `os.replace()`.
- Advisory locking to avoid race conditions (optional, requires `filelock` package).
- Backups of older versions before modifications.
- Validation of file formats and paths.
- Idempotent entry detection (skip duplicates by UUID).

### Default Journal Path
```
/root/obsidian-vault-xuan/Journal/{year}/{month}/{day}/YYYY-MM-DD.md
```
完整路径示例: `/root/obsidian-vault-xuan/Journal/2026/03/26/2026-03-26.md`

### Example Usage

```bash
# Quick daily entry (使用 /daily 命令)
python3 skills/journal-manager/scripts/daily.py "今天完成了项目部署！"

# 追加内容到指定文件
python3 skills/journal-manager/scripts/append_entry.py \
  --file /root/obsidian-vault-xuan/Journal/2026/03/26/2026-03-26.md \
  --message "测试日记条目" \
  --tz china

# Preview last 10 entries
python3 skills/journal-manager/scripts/preview_entry.py /path/to/journal.md 10

# Convert timezone in journal file
python3 skills/journal-manager/scripts/convert_tz.py \
  --file /path/to/journal.md \
  --from-tz UTC \
  --to-tz "America/Los_Angeles"
```

### Entry Format
Default format for journal entries with **nested tags**:
```
- HH:MM 你的日记内容 #分类/子分类
  - 💡 旺财的想法：我的想法和见解。#标签
```

**Tag Guidelines** (嵌套标签规则):
- Use nested tags like `#运动/骑行`, `#家人/亲子`, `#休息/睡眠`
- Parent tags: `#运动`, `#家人`, `#休息`, `#生活`, `#社交`, `#感悟`, `#习惯`, `#学习`, `#工作`, `#工具`
- Child tags: `#运动/骑行`, `#家人/亲子`, `#休息/午休`, `#生活/下厨`, `#社交/朋友圈`, `#感悟/内心平静`, `#习惯/早起`
- Add `#成就` for achievements, `#反思` for reflections
- Keep tags clean - don't duplicate parent + child tags

**Important Rules** (IMPORTANT - follow strictly):
1. **读取模板**：如果是新的一天，先读取 `/root/obsidian-vault-xuan/Assets/_Templates/DailyNote.md` 获取完整模板结构
2. **添加主标签**：日记内容后面要加 `#分类/子分类` 标签
3. **添加想法**：以子列表形式添加 `💡 旺财的想法：...`
4. **想法标签**：💡 想法后面也要加 `#标签`
5. **Git 推送后返回链接**：格式 `https://github.com/zhaohongxuan/obsidian-vault-xuan/blob/main/{文件路径}`

Examples:
```
- 14:43 技能创建完成：journal-manager 已成功部署，支持安全日记管理。#工具/skill
  - 💡 旺财的想法：模块化设计让脚本职责清晰，便于维护和扩展。#技术/架构
- 09:51 环湖骑行完成！72.43 公里，3 小时骑行。#运动/骑行 #成就 🔥
  - 💡 旺财的想法：72公里骑行，体力与意志的双重考验，完成了就是英雄！#感悟
- 06:15 起床了，冲了冷水澡。#习惯/早起 💪
  - 💡 旺财的想法：冷水澡唤醒身体，新的一天从清醒开始。#习惯
```

### Image Upload Feature

**功能**：发送照片时自动上传到 GitHub Picgo 仓库，返回 Markdown 图片链接

**配置**：
- 仓库：`zhaohongxuan/picgo`
- 分支：`master`
- 目录：`images/`
- 文件名：时间戳（格式：`YYYYMMDD_HHmmss.jpg`）

**用法**：
```bash
# 上传图片到 Picgo
python3 skills/journal-manager/scripts/upload_pic.py /path/to/image.jpg
```

**输出**：
```
![20260329_063137.jpg](https://raw.githubusercontent.com/zhaohongxuan/picgo/master/images/20260329_063137.jpg)
```

**集成到日记（重要规则）**：
- 图片链接放在**主日记条目后面**（不是 💡 旺财的想法 后面）
- 格式：
```
- HH:MM 日记内容 #标签 ![图片](URL)
  - 💡 旺财的想法：...
```

### Git 链接展示规则

**重要规则**：展示 Git 链接时使用 Markdown 链接格式

**❌ 错误**：
```
🔗 https://github.com/zhaohongxuan/obsidian-vault-xuan/blob/main/Journal/2026/03/2026-03-29.md
```

**✅ 正确**：
```
🔗 [2026-03-29 日记](https://github.com/zhaohongxuan/obsidian-vault-xuan/blob/main/Journal/2026/03/2026-03-29.md)
```

**规则**：
- 所有 Git 链接都用 Markdown 格式 `[标题](URL)`
- 链接文本要简洁明了（如：日期、文件名）
- 不要直接暴露完整 URL

### Customization
Templates, backup policies, duplicate handling, and timezone settings can be configured by modifying the helper scripts in the skill folder.

### Dependencies
- Python 3.9+ (for `zoneinfo` module)
- Optional: `filelock` package for enhanced concurrency safety (`pip install filelock`)