---
name: system-status
description: "Display current machine status including CPU, memory, and disk usage. Use when asked about system resources, VPS performance, or server health."
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["df", "free", "top"] } } }
---

## Summary

Quick command to check VPS/ server status with clean table format.

## Usage

```bash
bash skills/system-status/scripts/status.sh
```

## Status Report Format

```
🖥️ System
  OS: Linux racknerd-e45ccf 6.12.43
  Uptime: 24 days 5h
  Load: 0.19

💾 Memory
  total  used  avail  use%
  715MB 589MB 125MB  82%

💿 Disk  
  total  used  avail  use%
  14GB  6.8GB 7.1GB  49%

🔥 Top Processes
  openclaw-gateway  8.2%  44.5%
  couchdb           2.1%   8.0%

📁 Large Dirs (/)
  /usr/lib/x86_64-linux-gnu   510MB
  /var/log/journal            288MB
  /opt/Obsidian              240MB
```

## Cleanup Commands

| Cleanup | Command | Space |
|---------|---------|-------|
| pip cache | `rm -rf ~/.cache/pip` | ~1.5GB |
| npm cache | `npm cache clean --force` | varies |
| journal logs | `journalctl --vacuum-time=7d` | ~300MB |
| apt cache | `apt clean` | ~100MB |
