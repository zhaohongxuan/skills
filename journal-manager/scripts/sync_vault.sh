#!/bin/bash
# 定时同步 Obsidian 仓库脚本
# 用法: ./sync_vault.sh

VAULT_DIR="/root/obsidian-vault-xuan"
LOG_FILE="/root/.openclaw/logs/sync_vault.log"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 记录日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

cd "$VAULT_DIR" || exit 1

log "开始同步 Obsidian 仓库..."

# 检查是否是 git 仓库
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log "错误: $VAULT_DIR 不是 Git 仓库"
    exit 1
fi

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)
log "当前分支: $CURRENT_BRANCH"

# 检查远程仓库
REMOTE=$(git config --get branch.$CURRENT_BRANCH.remote)
if [ -z "$REMOTE" ]; then
    log "错误: 没有配置远程仓库"
    exit 1
fi

# 拉取远程更新
log "执行 git pull origin $CURRENT_BRANCH..."
git pull origin "$CURRENT_BRANCH" 2>&1 >> "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "同步成功!"
else
    # 检查是否有冲突
    if git status | grep -q "CONFLICT"; then
        log "检测到冲突，自动解决..."
        # 保留我们的版本（主要针对日记文件）
        git checkout --ours .
        git add -A
        git commit -m "chore: 自动解决同步冲突"
        git push origin "$CURRENT_BRANCH" 2>&1 >> "$LOG_FILE"
        log "冲突已解决并推送"
    else
        log "警告: git pull 失败"
    fi
fi

log "同步完成"
echo "" >> "$LOG_FILE"