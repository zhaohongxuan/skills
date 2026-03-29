#!/usr/bin/env python3
"""
TIL (Today I Learned) - Link Summarizer Skill
Fetches URL content, summarizes, and creates note cards as separate files with double links
"""
import os
import sys
import re
import subprocess
import html
from datetime import datetime, timezone, timedelta

# 中国时区 (UTC+8)
CHINA_TZ = timezone(timedelta(hours=8))
DEFAULT_JOURNAL_DIR = "/root/obsidian-vault-xuan/Journal"
DEFAULT_TIL_DIR = "/root/obsidian-vault-xuan/Resources/TIL"
VAULT_DIR = "/root/obsidian-vault-xuan"

EMOJIS = {
    "book": "📚",
    "link": "🔗",
    "tag": "🏷️",
    "check": "✅",
    "git": "📦",
    "push": "📤",
    "summary": "📝",
    "file": "📄",
}

def get_emoji(key):
    return EMOJIS.get(key, "👉")

def fetch_url_content(url):
    """获取 URL 内容"""
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
        return html_content
    except Exception as e:
        print(f"⚠️ 获取 URL 内容失败: {e}")
        return None

def extract_title(html_content):
    """从 HTML 中提取标题"""
    match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if match:
        return html.unescape(match.group(1).strip())
    
    match = re.search(r'<meta[^>]*name=["\']title["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    if match:
        return html.unescape(match.group(1).strip())
    
    match = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE)
    if match:
        return html.unescape(match.group(1).strip())
    
    return "未识别标题"

def extract_main_content(html_content):
    """提取正文内容（简单版本）"""
    # 移除 script 和 style 标签
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
    
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', ' ', html_content)
    
    # 解码 HTML 实体
    text = html.unescape(text)
    
    # 清理空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def summarize_content(text, max_length=300):
    """简单摘要内容"""
    # 移除常见网站导航文字
    nav_patterns = [
        r'Home Archives Tags Categories Weekly Recaps Links About',
        r'🍵',
        r'🍵\s*',
        r'\[[^\]]*\]',  # 移除 Markdown 链接
        r'\s+',  # 合并多余空格
    ]
    for pattern in nav_patterns:
        text = re.sub(pattern, ' ', text)
    
    text = text.strip()
    
    # 移除开头的标题重复
    lines = text.split('。')
    if len(lines) > 1:
        # 保留从正文开始的内容
        for i, line in enumerate(lines):
            if len(line) > 50:  # 跳过短行（通常是标题重复）
                text = '。'.join(lines[i:])
                break
    
    if len(text) <= max_length:
        return text
    
    # 取前 max_length 个字符
    summary = text[:max_length]
    
    # 尝试找到句子的断点
    last_period = summary.rfind('。')
    last_newline = summary.rfind('\n')
    cut_point = max(last_period, last_newline)
    
    if cut_point > 100:
        summary = summary[:cut_point + 1]
    else:
        summary = summary.rsplit(' ', 1)[0] + "..."
    
    return summary.strip()

def generate_tags(title, content):
    """根据标题和内容生成标签（不含#前缀）"""
    content_lower = (title + " " + content).lower()
    tags = []
    
    # 技术标签
    tech_keywords = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "rust": "Rust",
        "golang": "Golang",
        "docker": "Docker",
        "kubernetes": "K8s",
        "git": "Git",
        "linux": "Linux",
        "vim": "Vim",
        "neovim": "Neovim",
        "nvim": "Neovim",
        "ai": "AI",
        "llm": "LLM",
        "chatgpt": "ChatGPT",
        "openai": "OpenAI",
        "obsidian": "Obsidian",
        "react": "React",
        "vue": "Vue",
        "node": "NodeJS",
        "api": "API",
        "http": "HTTP",
        "database": "Database",
        "sql": "SQL",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "aws": "AWS",
        "cloud": "Cloud",
        "security": "Security",
        "algorithm": "算法",
        "machine learning": "ML",
        "deep learning": "深度学习",
        "spec driven": "工程思维",
        "specification": "工程思维",
        "软件工程": "工程思维",
    }
    
    for keyword, tag in tech_keywords.items():
        if keyword in content_lower:
            tags.append(tag)
    
    # 如果没有匹配到技术标签，添加通用标签
    if not tags:
        tags = ["技术", "学习"]
    
    # 限制标签数量
    tags = list(set(tags))[:5]
    
    return tags

def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    # 移除非法字符
    filename = re.sub(r'[\\/*?:"<>|]', '', title)
    # 移除 HTML 实体
    filename = html.unescape(filename)
    # 替换空格和特殊符号为下划线
    filename = re.sub(r'[\s\-\–\—]+', '_', filename)
    # 只保留字母、数字、中文和下划线
    filename = re.sub(r'[^\w\u4e00-\u9fff]', '', filename)
    # 限制长度
    if len(filename) > 50:
        filename = filename[:50]
    # 移除连续的下划线
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    
    return filename if filename else "untitled"

def create_til_file(title, url, summary, tags):
    """创建独立的 TIL 笔记文件"""
    now = datetime.now(CHINA_TZ)
    date_str = now.strftime('%Y-%m-%d')
    
    # 创建文件名（不含非法字符）
    safe_title = sanitize_filename(title)
    filename = f"{date_str}_{safe_title}.md"
    
    # 确保目录存在
    os.makedirs(DEFAULT_TIL_DIR, exist_ok=True)
    
    file_path = os.path.join(DEFAULT_TIL_DIR, filename)
    
    # 构建笔记内容
    content = []
    content.append("---")
    content.append(f"title: {title}")
    content.append(f"source: {url}")
    content.append(f"date: {date_str}")
    # tags 不带 # 前缀
    content.append(f"tags: [{', '.join(tags)}]")
    content.append("---")
    content.append("")
    content.append(f"# {title}")
    content.append("")
    content.append(f"> **来源**: [{url}]({url})")
    content.append(f"> **标签**: {' '.join(f'#{t}' for t in tags)}")
    content.append("")
    content.append("## 总结")
    content.append("")
    content.append(summary)
    content.append("")
    content.append("---")
    # TIL 标签放在最后
    content.append("#TIL")
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    return file_path, filename

def add_link_to_journal(til_filename, title, url, tags):
    """在日记中添加双链"""
    now = datetime.now(CHINA_TZ)
    year = now.strftime('%Y')
    month = now.strftime('%m')
    day = now.strftime('%d')
    time_str = now.strftime('%H:%M')
    
    target_dir = os.path.join(DEFAULT_JOURNAL_DIR, year, month)
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, f"{year}-{month}-{day}.md")
    
    # 构建日记条目（使用双链）
    display_name = title[:30] + "..." if len(title) > 30 else title
    entry = f"- {time_str} 📚 TIL: [[Resources/TIL/{til_filename}|{display_name}]]"
    
    # 确保换行
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            f.seek(max(0, os.path.getsize(file_path) - 1))
            last_char = f.read(1)
            if last_char not in (b'\n', b'\r'):
                entry = "\n" + entry
    else:
        entry = "\n" + entry
    
    entry += "\n"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    return file_path

def git_add_and_commit(file_paths, message):
    """Git 提交"""
    print(f"\n{get_emoji('git')} 开始 Git 提交流程...")
    
    try:
        for file_path in file_paths:
            rel_path = os.path.relpath(file_path, VAULT_DIR)
            subprocess.run(["git", "add", rel_path], cwd=VAULT_DIR, check=True)
        
        commit_msg = f"feat: 添加 TIL - {message}"
        result = subprocess.run(["git", "commit", "-m", commit_msg], 
                               cwd=VAULT_DIR, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   {get_emoji('check')} 提交成功!")
            
            # Push
            result = subprocess.run(["git", "push", "origin", "main"], 
                                  cwd=VAULT_DIR, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   {get_emoji('push')} push 成功!")
            else:
                print(f"   ⚠️ push 失败")
        else:
            if "nothing to commit" in result.stderr.lower():
                print(f"   ℹ️ 没有需要提交的内容")
            else:
                print(f"   ⚠️ commit 失败")
    except Exception as e:
        print(f"   ⚠️ Git 操作失败: {e}")

def main():
    if len(sys.argv) < 2:
        print("用法: til.py <URL> [备注]")
        sys.exit(1)
    
    url = sys.argv[1]
    custom_note = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"\n{get_emoji('link')} 正在获取链接内容...")
    print(f"   URL: {url}")
    
    # 获取内容
    html_content = fetch_url_content(url)
    if not html_content:
        print("❌ 无法获取 URL 内容")
        sys.exit(1)
    
    # 提取信息
    print(f"{get_emoji('book')} 正在分析内容...")
    title = extract_title(html_content)
    content = extract_main_content(html_content)
    summary = summarize_content(content)
    tags = generate_tags(title, content)
    
    # 创建 TIL 文件
    print(f"{get_emoji('tag')} 生成标签: {', '.join(tags)}")
    print(f"{get_emoji('file')} 创建 TIL 笔记文件...")
    
    til_path, til_filename = create_til_file(title, url, summary, tags)
    print(f"   {get_emoji('check')} 已创建: {til_filename}")
    
    # 在日记中添加双链
    print(f"{get_emoji('book')} 在日记中添加双链...")
    journal_path = add_link_to_journal(til_filename, title, url, tags)
    print(f"   {get_emoji('check')} 已添加双链到日记")
    
    # Git 提交
    message = custom_note or title[:30]
    git_add_and_commit([til_path, journal_path], message)
    
    print(f"\n✅ 完成!")
    print(f"   📄 TIL 文件: [[Resources/TIL/{til_filename}]]")
    print(f"   📓 日记链接: 已添加双链")

if __name__ == "__main__":
    main()