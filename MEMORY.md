# 旺财的长期记忆

## 用户信息
- **名字**: hank zhao (hank_zhao)
- **Telegram ID**: 1429540570
- **主项目**: obsidian-weread-plugin (WeChat Reading Obsidian Plugin)
- **GitHub**: zhaohongxuan
- **日记路径**: /root/obsidian-vault-xuan/Journal
- **Obsidian 库**: /root/obsidian-vault-xuan

---

## 用户偏好与习惯

### 运动习惯
- 经常骑行（外环绿道 12 公里）
- 力量训练：深蹲最大 90kg，引体向上，卷腹
- 早起 Checklist：洗冷水澡、俯卧撑、深蹲、量体重

### 技术偏好
- Neovim 重度用户（有详细的 nvim 配置和快捷键速查表）
- 喜欢用 AI工具提升效率（minimax token 焦虑中 😅）
- 开发工作流：idev-workflow + smart-commit
- 订阅了 minimax 套餐

### 工作风格
- 团队技能开发：idev-workflow（自动创建分支和 MR）、smart-commit（自动生成 commit msg）
- 注重代码规范：feat: xxx 格式提交信息
- 技术文档整理

---

## 已创建的 Skills（2026-03-26）

### 1. journal-manager 📓
- **路径**: /root/.openclaw/workspace/skills/journal-manager/
- **功能**: 
  - `/daily xxx` 快速记日记
  - 自动 Git 提交推送
  - 添加到周记
  - 换行处理、时区处理（中国时区 UTC+8）
- **表情支持**: 根据内容自动添加表情 🔥⭐💪📚 等
- **Git 提交格式**: feat: xxx

### 2. recap 📊
- **路径**: /root/.openclaw/workspace/skills/recap/
- **功能**: 
  - `/recap` - 生成日报 recap
  - `/recap --week` - 生成周报 recap
  - 自动分类（技术产出💻、运动💪、工作📋、技能⚙️）
- **定时任务**: 每周六 20:00 自动执行

### 3. til 📚
- **路径**: /root/.openclaw/workspace/skills/til/
- **功能**: 
  - 发送链接 → 自动获取内容 → 生成摘要 → 添加 #TIL 标签到日记
  - 自动提取标题、来源、生成标签

### 定时任务
- 每 2 分钟同步 Obsidian 仓库
- 每周六 20:00 生成周报 recap
- **每周六/周日早上：根据一周日记自动更新周记**（重要！）

### 周记更新规则
- **周期**：周日到周六
- **更新时机**：周六或周日凌晨
- **内容**：根据日记生成周报，包含：技术产出、运动、亮点、数据统计
- **周记路径**：`Journal/YYYY/MM/YYYY-WXX.md`

---

## 项目：obsidian-weread-plugin

### 概述
- **描述**: Obsidian 插件，用于同步微信读书的笔记、高亮到 Obsidian
- **GitHub**: https://github.com/zhaohongxuan/obsidian-weread-plugin
- **开发语言**: TypeScript + Svelte
- **许可**: MIT

### 最新版本信息
- **当前版本**: 0.17.1（2026-03-24 发布）
- **版本规则**: semver

---

## 重要工作流程

### 日记记录流程（journal-manager）
1. `/daily xxx` → 执行 daily.py
2. **新的一天先读取模板**：`Assets/_Templates/DailyNote.md`
3. **自动生成标签和想法**：`generate_thought_and_tags()` 函数
4. 追加日记条目：`- HH:mm {content} #标签` + `💡 旺财的想法：...`
5. 自动 Git add → commit → push
6. 自动追加到周记 `YYYY-WXX.md`

### 日记模板结构
- frontmatter（aliases, date, tags, weekly）
- Planning（One Thing, 早起 Checklist, 工作事项）
- Journal（主内容 + 💡想法）

### 日记 Recap 流程（recap）
1. 读取日记文件
2. 分类条目（技术、运动、工作、技能、文档）
3. 生成格式化 recap
4. 可选：添加到周记

---

## 关键工具与命令

### 日记工具
```bash
# 记日记
python3 /root/.openclaw/workspace/skills/journal-manager/scripts/daily.py "内容"

# 生成日报
python3 /root/.openclaw/workspace/skills/recap/scripts/recap.py

# 生成周报
python3 /root/.openclaw/workspace/skills/recap/scripts/recap.py --week

# 同步仓库
/root/.openclaw/workspace/skills/journal-manager/scripts/sync_vault.sh
```

### Cron 任务
```bash
# 查看 cron
crontab -l

# 同步任务
*/2 * * * * /root/.openclaw/workspace/skills/journal-manager/scripts/sync_vault.sh

# 周 recap
0 20 * * 6 python3 /root/.openclaw/workspace/skills/recap/scripts/recap.py --week
```

---

## 今日重要事件（2026-03-26）

### 技术产出
- ✅ journal-manager 日记技能开发完成
- ✅ idev-workflow + smart-commit 团队技能完成
- ✅ recap 日报/周报技能完成
- ✅ til 链接摘要技能完成
- ✅ Claude-Nvim-Workflow 文档
- ✅ Nvim-Keymaps-Cheat-Sheet 文档

### 生活事件
- 🚴 外环绿道骑行 12 公里
- 🏋️ 深蹲 90kg x 10 组 + 卷腹 + 引体向上
- 📱 新 iPhone 17 Pro 摔了两次（自己和别人），非常心疼 😢
- 📦 订购了 minimax 套餐，开始有 token 焦虑

### 订阅与服务
- minimax 套餐（AI token 服务）

---

## OpenClaw 执行权限

### 配置文件: ~/.openclaw/exec-approvals.json

```json
{
  "agents": {
    "main": {
      "security": "allowlist",
      "allowlist": [
        { "pattern": "/bin/*" },
        { "pattern": "/usr/bin/*" },
        { "pattern": "/usr/local/bin/*" }
      ]
    }
  }
}
```

**注意**: 
- Git、npm、gh 命令都在 `/usr/bin/` 中
- 使用 `/bin/bash -c "..."` 方式运行复合命令

---

## 下次工作清单

### 技能维护
- [ ] 优化 journal-manager 的 TIL 格式
- [ ] 完善 recap 的 AI 生成能力
- [ ] 考虑添加更多日记模板

### 用户偏好记住
- [ ] 时区：中国时区 UTC+8
- [ ] 日记格式：`- HH:mm {content}`
- [ ] Git 提交格式：feat: xxx
- [ ] 运动习惯：骑行、深蹲、俯卧撑、引体向上

---

**最后更新**: 2026-03-26
**今日重点**: 完成日记技能全家桶（journal-manager + recap + til）
**状态**: 🚀 持续优化中