#!/usr/bin/env python3
"""
Recap Skill - Generate daily or weekly summary from journal entries
"""
import os
import sys
import re
import argparse
from datetime import datetime, timezone, timedelta
from collections import defaultdict

# 中国时区 (UTC+8)
CHINA_TZ = timezone(timedelta(hours=8))
# 默认日记路径
DEFAULT_JOURNAL_DIR = "/root/obsidian-vault-xuan/Journal"

# 表情映射
EMOJIS = {
    "tech": "💻",
    "sport": "💪",
    "work": "📋",
    "mood": "🎭",
    "skill": "⚙️",
    "doc": "📝",
    "git": "🔀",
    "star": "⭐",
    "fire": "🔥",
    "book": "📓",
    "idea": "💡",
    "love": "❤️",
    "check": "✅",
}

def get_emoji(key):
    return EMOJIS.get(key, "👉")

def parse_journal_entry(line):
    """解析日记条目"""
    # 格式: - HH:mm 内容
    match = re.match(r'^- (\d{2}:\d{2})\s+(.+)$', line.strip())
    if match:
        return match.group(1), match.group(2)
    return None, None

def categorize_entry(content):
    """对日记内容进行分类"""
    content_lower = content.lower()
    categories = []
    
    tech_keywords = ["skill", "代码", "开发", "git", "commit", "push", "pull", 
                     "nvim", "neovim", "obsidian", "文档", "创建", "优化",
                     "修复", "bug", "feature", "workflow", "idev", "smart-commit"]
    sport_keywords = ["骑行", "跑步", "游泳", "深蹲", "俯卧撑", "引体向上", 
                     "卷腹", "运动", "训练", "健身房", "kg", "公里", "跑步"]
    work_keywords = ["工作", "任务", "项目", "会议", "需求", "产品", "产线",
                     "职级", "面试", "招聘", "团队"]
    mood_keywords = ["开心", "高兴", "焦虑", "累", "困", "压力", "兴奋", 
                      "成就感", "满足", "吐槽", "抱怨"]
    skill_keywords = ["skill", "技能", "工具"]
    doc_keywords = ["文档", "wiki", "readme", "笔记", "总结"]
    
    if any(k in content_lower for k in tech_keywords):
        categories.append("tech")
    if any(k in content for k in sport_keywords):
        categories.append("sport")
    if any(k in content_lower for k in work_keywords):
        categories.append("work")
    if any(k in content for k in mood_keywords):
        categories.append("mood")
    if any(k in content_lower for k in skill_keywords):
        categories.append("skill")
    if any(k in content_lower for k in doc_keywords):
        categories.append("doc")
    
    if not categories:
        categories.append("general")
    
    return categories

def generate_category_summary(entries):
    """生成各分类的汇总"""
    summary = {
        "tech": [],
        "sport": [],
        "work": [],
        "mood": [],
        "skill": [],
        "doc": [],
        "general": []
    }
    
    for time, content in entries:
        categories = categorize_entry(content)
        for cat in categories:
            if cat not in ["general"]:
                summary[cat].append(content)
    
    return summary

def format_recap(date_str, entries, summary):
    """格式化 recap 输出"""
    output = []
    output.append(f"\n{'='*50}")
    output.append(f"📊 Recap - {date_str}")
    output.append(f"{'='*50}\n")
    
    # 统计
    output.append(f"📝 共 {len(entries)} 条日记\n")
    
    # 分类汇总
    if summary["tech"]:
        output.append(f"{get_emoji('tech')} 技术产出:")
        for item in set(summary["tech"]):
            output.append(f"   • {item[:60]}...")
        output.append("")
    
    if summary["sport"]:
        output.append(f"{get_emoji('sport')} 运动:")
        for item in set(summary["sport"]):
            output.append(f"   • {item}")
        output.append("")
    
    if summary["work"]:
        output.append(f"{get_emoji('work')} 工作:")
        for item in set(summary["work"]):
            output.append(f"   • {item[:60]}...")
        output.append("")
    
    if summary["skill"]:
        output.append(f"{get_emoji('skill')} 技能开发:")
        for item in set(summary["skill"]):
            output.append(f"   • {item}")
        output.append("")
    
    # 生成亮点
    output.append(f"{get_emoji('star')} 今日亮点:")
    highlights = []
    for cat in ["skill", "tech", "sport"]:
        if summary[cat]:
            highlights.append(summary[cat][0])
    
    if highlights:
        for h in highlights[:3]:
            output.append(f"   • {h[:50]}...")
    else:
        output.append("   • 今天记录了一些想法和事项")
    
    output.append("")
    
    return "\n".join(output)

def read_journal_file(file_path):
    """读取日记文件"""
    if not os.path.exists(file_path):
        return []
    
    entries = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            time, content = parse_journal_entry(line)
            if time and content:
                entries.append((time, content))
    
    return entries

def get_journal_path(journal_dir, date):
    """获取指定日期的日记文件路径"""
    year = date.strftime('%Y')
    month = date.strftime('%m')
    day = date.strftime('%d')
    
    return os.path.join(journal_dir, year, month, f"{year}-{month}-{day}.md")

def get_week_path(journal_dir, date):
    """获取周记文件路径"""
    year = date.strftime('%Y')
    week_num = date.isocalendar()[1]
    month = date.strftime('%m')
    
    return os.path.join(journal_dir, year, month, f"{year}-W{week_num:02d}.md")

def generate_daily_recap(journal_dir, date=None):
    """生成日报 recap"""
    if date is None:
        date = datetime.now(CHINA_TZ)
    
    date_str = date.strftime('%Y-%m-%d')
    file_path = get_journal_path(journal_dir, date)
    
    entries = read_journal_file(file_path)
    
    if not entries:
        print(f"📊 {date_str} 没有日记记录")
        return None
    
    summary = generate_category_summary(entries)
    recap = format_recap(date_str, entries, summary)
    
    return recap

def generate_weekly_recap(journal_dir, date=None):
    """生成周报 recap"""
    if date is None:
        date = datetime.now(CHINA_TZ)
    
    year = date.strftime('%Y')
    week_num = date.isocalendar()[1]
    date_str = f"{year} 第 {week_num} 周"
    
    # 获取本周所有日记
    all_entries = []
    
    # 计算本周起始日期
    start_of_week = date - timedelta(days=date.weekday())
    
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        file_path = get_journal_path(journal_dir, day)
        if os.path.exists(file_path):
            entries = read_journal_file(file_path)
            all_entries.extend(entries)
    
    if not all_entries:
        print(f"📊 {date_str} 没有日记记录")
        return None
    
    summary = generate_category_summary(all_entries)
    
    output = []
    output.append(f"\n{'='*50}")
    output.append(f"📊 Weekly Recap - {date_str}")
    output.append(f"{'='*50}\n")
    output.append(f"📝 本周共 {len(all_entries)} 条日记\n")
    
    # 技术产出
    if summary["tech"]:
        tech_items = list(set(summary["tech"]))
        output.append(f"{get_emoji('tech')} 技术产出 ({len(tech_items)} 项):")
        for item in tech_items[:5]:
            output.append(f"   • {item[:60]}...")
        output.append("")
    
    # 运动
    if summary["sport"]:
        sport_items = list(set(summary["sport"]))
        output.append(f"{get_emoji('sport')} 运动 ({len(sport_items)} 项):")
        for item in sport_items:
            output.append(f"   • {item}")
        output.append("")
    
    # 技能
    if summary["skill"]:
        skill_items = list(set(summary["skill"]))
        output.append(f"{get_emoji('skill')} 技能开发 ({len(skill_items)} 项):")
        for item in skill_items:
            output.append(f"   • {item}")
        output.append("")
    
    # 文档
    if summary["doc"]:
        doc_items = list(set(summary["doc"]))
        output.append(f"{get_emoji('doc')} 文档 ({len(doc_items)} 项):")
        for item in doc_items:
            output.append(f"   • {item}")
        output.append("")
    
    # 亮点总结
    output.append(f"{get_emoji('star')} 本周亮点:")
    highlights = []
    for cat in ["skill", "tech", "sport"]:
        for item in summary[cat][:2]:
            highlights.append(item)
    
    if highlights:
        for h in highlights[:5]:
            output.append(f"   • {h[:50]}...")
    else:
        output.append("   • 充实的一周！")
    
    output.append("")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='生成日记 Recap')
    parser.add_argument('--date', help='指定日期 (YYYY-MM-DD)')
    parser.add_argument('--week', action='store_true', help='生成周报')
    parser.add_argument('--journal-dir', default=DEFAULT_JOURNAL_DIR, help='日记目录')
    
    args = parser.parse_args()
    
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-%d')
        date = date.replace(tzinfo=CHINA_TZ)
    else:
        date = datetime.now(CHINA_TZ)
    
    if args.week:
        recap = generate_weekly_recap(args.journal_dir, date)
    else:
        recap = generate_daily_recap(args.journal_dir, date)
    
    if recap:
        print(recap)
        
        # 可选：添加到周记
        week_path = get_week_path(args.journal_dir, date)
        if os.path.exists(week_path):
            print(f"\n💡 周记已存在: {week_path}")
            print("   可以手动将上述 recap 内容添加到周记中")

if __name__ == "__main__":
    main()