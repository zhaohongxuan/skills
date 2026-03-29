#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime, timezone, timedelta

# 中国时区 (UTC+8)
CHINA_TZ = timezone(timedelta(hours=8))
# 默认日记路径
DEFAULT_JOURNAL_DIR = "/root/obsidian-vault-xuan/Journal"

def append_entry(file_path, message, use_china_tz=True):
    """
    追加日记条目到指定文件
    """
    # 获取当前时间
    if use_china_tz:
        now = datetime.now(CHINA_TZ)
    else:
        now = datetime.now()
    
    time_str = now.strftime('%H:%M')
    
    # 格式: - HH:mm {content}
    entry = f"- {time_str} {message}\n"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)
    
    print(f"✅ 已追加到 {file_path}")
    print(f"   内容: {entry.strip()}")
    return entry

def main():
    parser = argparse.ArgumentParser(description='追加日记条目')
    parser.add_argument('--file', '-f', required=True, help='日记文件路径')
    parser.add_argument('--message', '-m', required=True, help='要添加的内容')
    parser.add_argument('--tz', default='china', choices=['china', 'local'], 
                        help='时区: china (UTC+8) 或 local (服务器本地时间)')
    
    args = parser.parse_args()
    use_china_tz = (args.tz == 'china')
    append_entry(args.file, args.message, use_china_tz)

if __name__ == "__main__":
    main()