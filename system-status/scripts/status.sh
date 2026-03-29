#!/bin/bash
# System Status Script - Clean table format

echo "=========================================="
echo "📊 System Status"
echo "=========================================="

# System info
echo ""
echo "🖥️  System"
echo "  Up:  $(uptime -p 2>/dev/null | sed 's/up //' || uptime | awk '{print $3,$4}' | sed 's/,//')"
echo "  Load: $(uptime | awk -F'load average:' '{print $2}')"

# Memory
echo ""
echo "💾  Memory"
free -h | awk 'NR==2 {printf "  %5s %5s %5s %s\n", "total", "used", "avail", "use%"
printf "  %5s %5s %5s %s\n", $2, $3, $7, $5}'

# Disk
echo ""
echo "💿  Disk"
df -h / | awk 'NR==2 {printf "  %5s %5s %5s %s\n", "total", "used", "avail", "use%"
printf "  %5s %5s %5s %s\n", $2, $3, $4, $5}'

# Top large dirs (exclude system dirs)
echo ""
echo "📁  Top 3 Large Dirs (user)"
du -hS / --exclude=/usr --exclude=/var --exclude=/boot --exclude=/lib --exclude=/sbin --exclude=/bin --exclude=/proc --exclude=/sys --exclude=/run 2>/dev/null | sort -rh | head -3 | awk '{printf "  %-30s %5s\n", $2, $1}'

# Top processes
echo ""
echo "🔥  Top 3 CPU"
ps aux --sort=-%cpu | tail -n +2 | head -3 | awk '{printf "  %-22s %4s %5s\n", $11, $3"%", $4"%"}'

echo ""
echo "=========================================="
