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

def generate_thought_and_tags(message):
    """根据消息内容自动生成标签和想法"""
    msg_lower = message.lower()
    
    # 标签映射
    tag_map = {
        "健身": "#运动/健身",
        "骑行": "#运动/骑行",
        "跑步": "#运动/跑步",
        "深蹲": "#运动/力量",
        "俯卧撑": "#运动/力量",
        "引体向上": "#运动/力量",
        "游泳": "#运动/游泳",
        "篮球": "#运动/球类",
        "足球": "#运动/球类",
        "羽毛球": "#运动/球类",
        "乒乓球": "#运动/球类",
        "网球": "#运动/球类",
        "蹦床": "#运动/蹦床",
        "娃": "#家人/亲子",
        "孩子": "#家人/亲子",
        "女儿": "#家人/亲子",
        "儿子": "#家人/亲子",
        "老婆": "#家人/伴侣",
        "家庭": "#家人/家庭",
        "肯德基": "#生活/美食",
        "汉堡": "#生活/美食",
        "炸鸡": "#生活/美食",
        "做饭": "#生活/下厨",
        "早餐": "#生活/饮食",
        "午餐": "#生活/饮食",
        "晚餐": "#生活/饮食",
        "露营": "#生活/旅行",
        "旅游": "#生活/旅行",
        "郊游": "#生活/旅行",
        "公园": "#生活/旅行",
        "儿童乐园": "#家人/亲子",
        "游乐园": "#生活/娱乐",
        "龙珠": "#娱乐/动漫",
        "动漫": "#娱乐/动漫",
        "电影": "#娱乐/影视",
        "电视剧": "#娱乐/影视",
        "游戏": "#娱乐/游戏",
        "音乐": "#娱乐/音乐",
        "书": "#学习/阅读",
        "读书": "#学习/阅读",
        "背单词": "#学习/英语",
        "英语": "#学习/英语",
        "学习": "#学习/学习",
        "skill": "#技能/工具",
        "工作": "#工作/任务",
        "项目": "#工作/项目",
        "开会": "#工作/会议",
        "代码": "#技能/编程",
        "bug": "#技能/编程",
        "commit": "#技能/编程",
        "sleep": "#休息/睡眠",
        "睡觉": "#休息/睡眠",
        "午睡": "#休息/午休",
        "疲惫": "#休息/睡眠",
    }
    
    # 想法映射
    thought_map = {
        "起床": "新的一天从清醒开始，把握好早晨就是把握好人生 🌅",
        "冷水澡": "冷水唤醒身体，意志力就是在不舒服中坚持 💪",
        "俯卧撑": "龟仙流修行第一步，50个俯卧撑就是热身 💪",
        "深蹲": "腿部力量是龟仙流的基础，深蹲让人更有劲 🏋️",
        "骑行": "骑行是最自由的运动，边走边看风景 🚴",
        "跑步": "跑步是跟自己的对话，每一步都是修行 👟",
        "蹦床": "弹跳的快乐谁懂！运动也可以很有趣 💪",
        "游泳": "水中健身，全身都动起来的感觉真好 🏊",
        "娃": "陪伴是最长情的告白，孩子成长的速度比你想象的快 👶",
        "儿子": "小男孩的成长速度惊人，每一天都在变化 👦",
        "女儿": "小棉袄的温暖，陪伴是最好的爱 👧",
        "老婆": "家人的支持是最强的后盾 💕",
        "家庭": "家是温暖的港湾 💕",
        "儿童乐园": "儿童乐园是父母的休息站，也是孩子的快乐天地 🎠",
        "肯德基": "垃圾食品但真香！偶尔放纵一下也是生活的一部分 🍗",
        "汉堡": "简单粗暴的快乐，垃圾食品也有存在的意义 🍔",
        "炸鸡": "香脆可口，偶尔满足一下味蕾也是幸福 🍗",
        "做饭": "为家人做饭是一件幸福的事，大家吃得开心最重要 👨‍🍳",
        "早餐": "一日之计在于晨，早餐要吃好 🍳",
        "午餐": "午餐要吃饱，下午才有精力战斗 🍱",
        "晚餐": "晚餐要吃少，晚上才能睡得好 🍽️",
        "露营": "走出家门，亲近大自然，露营是最好的充电方式 ⛺",
        "郊游": "户外活动是最好的解压方式，新鲜空气和阳光 🌿",
        "公园": "城市里的绿洲，给身心放个假 🌳",
        "旅游": "读万卷书不如行万里路，旅行让人成长 ✈️",
        "龙珠": "龟仙流精神永不过时：基础+坚持+快乐修行 🐉",
        "动漫": "二次元的世界很美好，童心不灭 🎬",
        "电影": "电影是浓缩的人生，两个小时体验另一种生活 🎥",
        "读书": "读书是与作者对话，启迪智慧的最好方式 📚",
        "苏轼": "苏轼的豁达值得学习，人生起伏很正常 🍵",
        "背单词": "每天积累一点点，长期坚持就能看到巨大进步 📚",
        "英语": "英语是通向世界的桥梁，坚持学习才能掌握 💪",
        "学习": "学如逆水行舟，不进则退。每天进步一点点 💪",
        "skill": "工具提升效率，自动化是龟仙流的终极目标 🔧",
        "工作": "工作中的挑战是成长的机会 💪",
        "项目": "做好项目就是最好的作品 🚀",
        "代码": "代码是创造的工具，写代码是快乐的创造 🚀",
        "bug": "Bug是成长的阶梯，解决问题就是进步 🔧",
        "commit": "提交是进步的印记，每一个小commit都是前进 🚀",
        "睡眠": "睡眠是第一生产力，睡好才能干好 😴",
        "睡觉": "休息好才能工作好，睡眠是第一生产力 😴",
        "午睡": "20分钟小憩是恢复精力的好方法 😴",
        "疲惫": "累了就休息，身体是革命的本钱 😴",
        "提醒": "小事情也要记下来，大脑是用来思考的不是用来记事的 📝",
        "美津浓": "好鞋配英雄，一双好鞋让训练更愉快 👟",
        "必迈": "没有对比就没有伤害，质量才是王道 👟",
        "压缩毛巾": "出行必备，方便又实用 🧴",
    }
    
    # 查找匹配的标签
    found_tags = []
    for keyword, tag in tag_map.items():
        if keyword in message:
            found_tags.append(tag)
    
    # 查找匹配的想法
    found_thought = "每天都是新的一天，记录让生活更精彩 ✨"
    for keyword, thought in thought_map.items():
        if keyword in message:
            found_thought = thought
            break
    
    # 去重
    tags = " ".join(set(found_tags)) if found_tags else "#生活/日常"
    
    return tags, found_thought

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
    
    # 分析内容，自动添加标签和想法
    tags, thought = generate_thought_and_tags(message)
    
    entry = f"- {time_str} {message} {tags}\n"
    entry += f"  - 💡 旺财的想法：{thought} #感悟\n"
    
    # 检查是否是新的第一天（文件不存在或为空）
    is_new_file = not os.path.exists(file_path) or os.path.getsize(file_path) == 0
    
    if is_new_file:
        # 读取模板
        template_path = "/root/obsidian-vault-xuan/Assets/_Templates/DailyNote.md"
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            # 替换模板中的日期占位符
            template_content = template_content.replace("<% tp.file.creation_date() %>", date_str)
            template_content = template_content.replace("<% moment(tp.file.title, \"YYYY-MM-DD\").format(\"YYYY\") %>", year)
            template_content = template_content.replace("<% moment(tp.file.title, \"YYYY-MM-DD\").format(\"YYYY-[W]ww\") %>", f"{year}-W{now.isocalendar()[1]:02d}")
            template_content = template_content.replace("<% moment().format(\"HH:mm\") %>", time_str)
            # 移除 Poem 部分（不需要每日诗歌）
            template_content = re.sub(r'## Poem\n---?\n.*?\n---\n', '', template_content, flags=re.DOTALL)
            template_content = template_content.replace('<% await tp.user.daily_poem(tp) %>', '')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(template_content)
        else:
            # 如果没有模板，创建基本结构
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {date_str}\n\n## Journal\n---\n")
    elif os.path.exists(file_path):
        with open(file_path, "rb") as f:
            f.seek(max(0, os.path.getsize(file_path) - 1))
            last_char = f.read(1)
            if last_char not in (b'\n', b'\r'):
                entry = "\n" + entry
    else:
        entry = "\n" + entry
    
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
