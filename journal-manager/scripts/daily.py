#!/usr/bin/env python3
import os
import sys
import subprocess
import re
from datetime import datetime, timezone, timedelta

# 中国时区 (UTC+8)
CHINA_TZ = timezone(timedelta(hours=8))
# 默认日记路径
DEFAULT_JOURNAL_DIR = "/root/obsidian-vault-xuan/Journal"
# Git 仓库路径
VAULT_DIR = "/root/obsidian-vault-xuan"

# 表情包
EMOJIS = {
    "success": "✨",
    "git": "📦",
    "push": "📤",
    "conflict": "⚠️",
    "fix": "🔧",
    "time": "🕐",
    "rocket": "🚀",
    "star": "⭐",
    "check": "✅",
    "book": "📓",
    "fire": "🔥",
    "idea": "💡",
    "love": "❤️",
    "week": "📅",
    "sport": "💪",
    "tech": "💻",
}

def get_emoji(key):
    return EMOJIS.get(key, "👉")

def run_git_command(args, cwd=None, check=True):
    """执行 git 命令并返回结果"""
    result = subprocess.run(
        args,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    if result.returncode != 0 and check:
        print(f"{get_emoji('conflict')} Git 命令失败: {' '.join(args)}")
        print(f"   错误: {result.stderr.strip()}")
    return result

def get_week_filename(journal_dir, date=None):
    """获取周记文件名"""
    if date is None:
        date = datetime.now(CHINA_TZ)
    
    year = date.strftime('%Y')
    week_num = date.isocalendar()[1]
    month = date.strftime('%m')
    
    week_filename = f"{year}-W{week_num:02d}.md"
    week_path = os.path.join(journal_dir, year, month, week_filename)
    
    return week_path, year, week_num

def ensure_weekly_note(week_path, year, week_num):
    """确保周记文件存在"""
    if not os.path.exists(week_path):
        # 创建周记
        week_content = f"""# Week {week_num}, {year}

## 日记总结

---

### 待补充...

"""
        os.makedirs(os.path.dirname(week_path), exist_ok=True)
        with open(week_path, 'w', encoding='utf-8') as f:
            f.write(week_content)
        print(f"   {get_emoji('week')} 已创建周记: {week_path}")
    return week_path

def add_to_weekly_note(journal_dir, date_str, summary):
    """将日记摘要添加到周记"""
    week_path, year, week_num = get_week_filename(journal_dir, datetime.now(CHINA_TZ))
    ensure_weekly_note(week_path, year, week_num)
    
    # 读取周记
    with open(week_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经有这天的记录
    if f"### 📅 {date_str}" in content:
        print(f"   {get_emoji('week')} 今天已添加到周记，跳过")
        return week_path
    
    # 构建新的摘要块
    new_summary = f"""### 📅 {date_str}

{summary}

"""
    
    # 插入到 "### 待补充..." 之前
    if "### 待补充..." in content:
        content = content.replace("### 待补充...", f"{new_summary}### 待补充...")
    else:
        content += "\n" + new_summary
    
    # 写回周记
    with open(week_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   {get_emoji('week')} 已添加到周记: {week_path}")
    return week_path

def git_add_and_commit(file_path, message):
    """Git 添加文件并提交"""
    print(f"\n{get_emoji('git')} 开始 Git 提交流程...")
    
    vault_dir = VAULT_DIR
    
    result = run_git_command(["git", "rev-parse", "--git-dir"], cwd=vault_dir, check=False)
    if result.returncode != 0:
        print(f"{get_emoji('conflict')} 当前目录不是 Git 仓库，跳过提交")
        return False
    
    rel_path = os.path.relpath(file_path, vault_dir)
    
    print(f"   {get_emoji('git')} git add {rel_path}")
    result = run_git_command(["git", "add", rel_path], cwd=vault_dir)
    if result.returncode != 0:
        print(f"   ❌ git add 失败: {result.stderr}")
        return False
    
    result = run_git_command(["git", "status", "--porcelain"], cwd=vault_dir, check=False)
    if not result.stdout.strip():
        print(f"   ℹ️ 没有需要提交的内容")
        return True
    
    commit_msg = f"feat: {message}"
    
    print(f"   {get_emoji('git')} git commit -m \"{commit_msg}\"")
    result = run_git_command(["git", "commit", "-m", commit_msg], cwd=vault_dir)
    
    if result.returncode != 0:
        if "nothing to commit" in result.stderr.lower():
            print(f"   ℹ️ 没有需要提交的内容")
            return True
        print(f"   ❌ git commit 失败: {result.stderr}")
        return False
    
    print(f"   {get_emoji('check')} 提交成功!")
    
    result = run_git_command(["git", "branch"], cwd=vault_dir, check=False)
    if result.returncode == 0:
        current_branch = result.stdout.strip().replace("* ", "")
        print(f"   {get_emoji('push')} 当前分支: {current_branch}")
        
        result = run_git_command(["git", "config", "--get", f"branch.{current_branch}.remote"], cwd=vault_dir, check=False)
        remote = result.stdout.strip() if result.returncode == 0 else ""
        
        if remote:
            print(f"   {get_emoji('push')} 推送到远程仓库...")
            
            result = run_git_command(["git", "pull", "origin", current_branch], cwd=vault_dir, check=False)
            
            if result.returncode != 0:
                if "CONFLICT" in result.stdout or "CONFLICT" in result.stderr:
                    print(f"   {get_emoji('conflict')} 检测到冲突，开始智能解决...")
                    resolve_git_conflicts(vault_dir)
                elif "Everything up-to-date" in result.stdout or "Already up to date" in result.stdout:
                    print(f"   ℹ️ 远程已是最新")
                else:
                    print(f"   ⚠️ pull 提示: {result.stderr.strip()}")
            
            result = run_git_command(["git", "push", "origin", current_branch], cwd=vault_dir, check=False)
            if result.returncode == 0:
                print(f"   {get_emoji('check')} push 成功!")
            else:
                print(f"   ⚠️ push 失败: {result.stderr.strip()}")
        else:
            print(f"   ℹ️ 没有配置远程仓库，跳过推送")
    
    return True

def resolve_git_conflicts(vault_dir):
    """智能解决 Git 冲突"""
    print(f"   {get_emoji('fix')} 开始解决冲突...")
    
    result = run_git_command(["git", "diff", "--name-only", "--diff-filter=U"], cwd=vault_dir, check=False)
    if result.returncode != 0:
        print(f"   ❌ 无法获取冲突文件列表")
        return False
    
    conflict_files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]
    
    if not conflict_files:
        print(f"   ℹ️ 没有冲突文件")
        return True
    
    print(f"   📋 发现 {len(conflict_files)} 个冲突文件:")
    
    for file_path in conflict_files:
        full_path = os.path.join(vault_dir, file_path)
        print(f"   处理: {file_path}")
        
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            parts = re.split(r'^<<<<<<<|^=======|^>>>>>>>', content, flags=re.MULTILINE)
            
            if len(parts) >= 3:
                ours = parts[1].strip() if len(parts) > 1 else ""
                theirs = parts[2].strip() if len(parts) > 2 else ""
                
                if len(ours) >= len(theirs):
                    resolved = ours
                else:
                    resolved = theirs
                
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(resolved)
                
                print(f"      {get_emoji('check')} 已解决 (保留 {len(resolved)} 字符)")
                run_git_command(["git", "add", file_path], cwd=vault_dir)
            else:
                print(f"      ⚠️ 无法解析冲突格式")
    
    result = run_git_command(["git", "rebase", "--continue"], cwd=vault_dir, check=False)
    if result.returncode == 0:
        print(f"   {get_emoji('check')} 冲突已解决，rebase 继续")
        return True
    else:
        print(f"   ⚠️ rebase --continue: {result.stderr.strip()}")
        return False

def analyze_day_content(message):
    """分析日记内容，生成摘要"""
    msg_lower = message.lower()
    
    tech_keywords = ["skill", "创建", "完成", "优化", "修复", "开发", "代码", "文档", "commit", "push"]
    sport_keywords = ["骑行", "跑步", "深蹲", "俯卧撑", "引体向上", "卷腹", "运动", "训练", "kg", "公里"]
    
    has_tech = any(k in msg_lower for k in tech_keywords)
    has_sport = any(k in message for k in sport_keywords)
    
    tech_emoji = get_emoji("tech") if has_tech else ""
    sport_emoji = get_emoji("sport") if has_sport else ""
    
    return f"{tech_emoji} {sport_emoji}".strip()

def add_daily_entry(message, journal_dir=None):
    if journal_dir is None:
        journal_dir = DEFAULT_JOURNAL_DIR
    
    now = datetime.now(CHINA_TZ)
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M')
    
    target_dir = os.path.join(journal_dir, year, month)
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, f"{year}-{month}-{day}.md")
    
    entry = f"- {time_str} {message}"
    
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            f.seek(max(0, os.path.getsize(file_path) - 1))
            last_char = f.read(1)
            if last_char not in (b'\n', b'\r'):
                entry = "\n" + entry
    
    entry += "\n"
    
    with open(file_path, "a", encoding="utf-8") as journal:
        journal.write(entry)
    
    # 根据内容匹配表情
    content_emoji = ""
    msg_lower = message.lower()
    if any(k in msg_lower for k in ["完成", "成功", "搞定", "解决了"]):
        content_emoji = get_emoji("fire")
    elif any(k in msg_lower for k in ["创建", "新增", "新建"]):
        content_emoji = get_emoji("star")
    elif any(k in msg_lower for k in ["测试", "调试"]):
        content_emoji = get_emoji("check")
    elif any(k in msg_lower for k in ["优化", "改进", "修复"]):
        content_emoji = get_emoji("rocket")
    elif any(k in msg_lower for k in ["焦虑", "累", "困"]):
        content_emoji = get_emoji("idea")
    elif any(k in msg_lower for k in ["骑行", "跑步", "运动", "训练", "深蹲"]):
        content_emoji = get_emoji("sport")
    else:
        content_emoji = get_emoji("book")
    
    print(f"\n{get_emoji('book')} 日记已记录!")
    print(f"   {get_emoji('time')} {time_str} {content_emoji} {message}")
    
    # 添加到周记
    summary_emoji = analyze_day_content(message)
    week_summary = f"**{date_str}** {summary_emoji} {message}"
    add_to_weekly_note(journal_dir, date_str, week_summary)
    
    # Git 提交
    git_add_and_commit(file_path, message)
    
    # 一些情绪价值鼓励
    encouragement = get_encouragement(message)
    if encouragement:
        print(f"\n   {encouragement}")
    
    return file_path, entry

def get_encouragement(message):
    """根据消息内容返回鼓励语"""
    msg_lower = message.lower()
    
    if "完成" in message or "成功" in message:
        return f"{get_emoji('star')}{get_emoji('fire')} 太棒了！继续保持！"
    elif "创建" in message or "新增" in message:
        return f"{get_emoji('rocket')} 创作力爆棚！👍"
    elif "测试" in message:
        return f"{get_emoji('check')} 测试通过就是进步！"
    elif "优化" in message or "改进" in message:
        return f"{get_emoji('rocket')} 越变越好！💪"
    elif "焦虑" in message:
        return f"{get_emoji('love')} 别担心，一切都会好的！"
    elif "累" in message or "困" in message:
        return f"{get_emoji('idea')} 休息一下，你已经很努力了！"
    elif "骑行" in message or "跑步" in message or "运动" in message:
        return f"{get_emoji('sport')} 运动让人更聪明！💪"
    else:
        return None

if __name__ == "__main__":
    if len(sys.argv) > 1:
        message = sys.argv[1]
    else:
        message = "今天完成了一些事情！"
    
    journal_dir = os.environ.get("JOURNAL_DIR", DEFAULT_JOURNAL_DIR)
    add_daily_entry(message, journal_dir)