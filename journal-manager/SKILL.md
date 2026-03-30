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
  - 💡 旺财的想法：我的想法和见解。
```

**Note**: The 💡 thought line does NOT need a tag at the end.

### 自动想法生成器（Thought Generator）

**功能**：`daily.py` 会根据内容自动生成「旺财的想法」

**原理**：
- 维护一个关键词 → 想法的映射表
- 根据日记内容匹配关键词，生成个性化想法
- 未匹配时使用通用 fallback

**关键词映射示例**：
| 关键词 | 旺财的想法 |
|--------|-----------|
| 起床 | 新的一天从清醒开始，把握好早晨就是把握好人生 🌅 |
| 冷水澡 | 冷水唤醒身体，意志力就是在不舒服中坚持 💪 |
| 俯卧撑 | 龟仙流修行第一步，50个俯卧撑就是热身 💪 |
| 深蹲 | 腿部力量是龟仙流的基础，深蹲让人更有劲 🏋️ |
| 骑行 | 骑行是最自由的运动，边走边看风景 🚴 |
| 跑步 | 跑步是跟自己的对话，每一步都是修行 👟 |
| 五月天 | 五月天的歌是青春的记忆，每一首都是经典 🎸 |
| 加班 | 加班虽无奈，但每一步都是在为未来铺路 💪 |
| 提醒 | 小事情也要记下来，大脑是用来思考的不是用来记事的 📝 |
| 美津浓 | 好鞋配英雄，一双好鞋让训练更愉快 👟 |
| 读书 | 读书是与作者对话，启迪智慧的最好方式 📚 |
| 龙珠 | 龟仙流精神永不过时：基础+坚持+快乐修行 🐉 |

**通用 Fallback**：
```
每天都是新的一天，记录让生活更精彩 ✨
```

**如何扩展**：编辑 `daily.py` 中的 `thought_map` 字典即可添加新关键词

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
4. **Git 推送后返回链接**：格式 `https://github.com/zhaohongxuan/obsidian-vault-xuan/blob/main/{文件路径}`

Examples:
```
- 14:43 技能创建完成：journal-manager 已成功部署，支持安全日记管理。#工具/skill
  - 💡 旺财的想法：模块化设计让脚本职责清晰，便于维护和扩展。
- 09:51 环湖骑行完成！72.43 公里，3 小时骑行。#运动/骑行 🔥
  - 💡 旺财的想法：72公里骑行，体力与意志的双重考验，完成了就是英雄！
- 06:15 起床了，冲了冷水澡。#习惯/早起 💪
  - 💡 旺财的想法：冷水澡唤醒身体，新的一天从清醒开始。
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