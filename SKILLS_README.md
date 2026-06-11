# Claude Code Skills

本目录包含了 xuan 的自定义 Claude Code Skills，用于增强工作流程。

## 📚 Skills 列表

### 1. **reading** — 英文阅读学习
- **目标**: 辅助拆解外文文章，提取词汇句型，生成学习笔记
- **用法**: `/reading <URL 或 双链 或 文本>`
- **特性**:
  - 支持 URL、本地双链、直接文本三种输入
  - 本地笔记无需 WebFetch，直接读取文件
  - 生成结构化学习笔记
  - 追加到日记
  - 提取核心词汇、短语、句型
  - 标注雅思考点

**位置**: `Areas/English/Reading/Notes/YYYY-MM-DD_标题.md`

### 2. **til** — 知识内化
- **目标**: 将网页/文章转化为结构化 TIL（Today I Learned）笔记
- **用法**: `/til <URL 或 文件路径>`
- **特性**:
  - 快速内化知识
  - 生成结构化笔记
  - 关联知识库
  - 追加到日记

**位置**: `Areas/TIL/YYYY-MM-DD_标题.md`

### 3. **weread** — 微信读书助手
- **目标**: 处理微信读书笔记，提取洞察，关联知识库，生成写作选题
- **用法**: `/weread`
- **特性**:
  - 搜索书籍
  - 管理书架
  - 查看笔记划线
  - 浏览书评
  - 阅读统计
  - 发现推荐好书
  - 生成写作选题

## 🔧 安装与同步

所有 Skills 已同步到：
- **Claude Code**: `~/.claude/skills/`
- **版本管理**: `/Users/xuan/VSCodeProjects/skills/`（当前目录）

## 🚀 使用指南

### 在 Claude Code 中使用
```
/reading https://www.economist.com/article
/til [[Inbox/article]]
/weread
```

### 更新流程
1. 在本目录修改 SKILL.md 或其他文件
2. 通过 git 提交变更
3. 运行同步脚本更新到 ~/.claude/skills/

## 📝 版本历史

- **2026-06-11**: 从 iCloud~md~obsidian 迁移到 ~/.claude/skills/，添加 reading 和 til skills
- **之前**: weread skill 已存在

## 开发指南

### SKILL.md 结构
```markdown
---
name: skill_name
description: 简短描述
---

# /<skill_name> — 完整名称

## 输入
## 处理流程
## 输出示例
## 使用场景
```

### 关键文件
- `SKILL.md` — 主要文档，定义 Skill 的行为和配置
- `scripts/` — 如果有自定义脚本（可选）
- 相关辅助文件

## 联系方式

维护者: xuan
最后更新: 2026-06-11
