# 更新日志

本项目的所有重要变更都会记录在此文件中。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，版本遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

## [1.2.0] - 2026-06-20

### 新增

- **hexo-publish**：将 Obsidian 写作草稿发布到 Hexo 博客，自动转换 frontmatter（categories/tags/date）、清理 Obsidian 专有语法、探测既有分类词表避免孤立分类，推送 `src` 分支触发 CD 自动部署

## [1.1.0] - 2026-06-20

### 新增

- **article-cover**：根据文章内容生成维多利亚时代黑白木刻/蚀刻风格的 16:9 横向封面绘画提示词，用于文章配图

## [1.0.0] - 2026-06-16

### 新增

- **Plugin 支持**：新增 `.claude-plugin/plugin.json`，支持以 Claude Code Plugin 方式加载 skills
- **company-research**：公司竞争分析与行业研究框架，从创业者/产业研究员/长期投资者三视角深度拆解
- **reading**：英文阅读学习 — 拆解外文文章，提取词汇句型，生成学习笔记
- **til**：知识内化 — 将文章转化为结构化 TIL 笔记，关联知识库