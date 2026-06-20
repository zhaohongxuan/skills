---
name: hexo-publish
description: 将 Obsidian 笔记库中的写作草稿发布到 Hexo 博客，自动转换 frontmatter 为 Hexo 格式（categories/tags/date），清理 Obsidian 专有语法，提交并推送触发 CD 自动部署
---

# /hexo-publish — Hexo 博客发布 Skill

将 Obsidian Vault（`Writing/Draft/`）中的文章草稿迁移到 Hexo 博客，完成 frontmatter 转换、正文清理、提交推送全流程。

## 输入

```
/hexo-publish <一篇或多篇草稿文件路径>
```

| 类型 | 处理方式 |
|------|----------|
| **Vault 相对路径**（如 `Writing/Draft/2026-06-20-xxx.md`） | 从 Vault 根目录读取 |
| **@ 文件引用** | 直接使用被引用的文件 |

可一次传入多篇，批量处理。

## 关键路径

| 用途 | 路径 |
|------|------|
| Obsidian 草稿源 | Vault 内 `Writing/Draft/` |
| Hexo 博客仓库 | `/Users/xuan/VSCodeProjects/zhaohongxuan.github.io` |
| Hexo 文章目录 | `<博客仓库>/source/_posts/` |
| Hexo 配置 | `<博客仓库>/_config.yml`（`new_post_name` 决定文件命名规则） |
| 发布分支 | `src`（推送后 CD 自动部署） |

## 处理流程

### Step 1️⃣ — 读取草稿

逐篇读取输入的草稿文件，提取：
- 原始 frontmatter（title、date、tags、category、status、related 等）
- 正文内容

### Step 2️⃣ — 探测 Hexo 既有约定（关键）

**不要凭空生成 frontmatter，必须先探测博客现状**，否则会产出孤立分类、格式不统一。执行：

1. **命名规则**：读 `_config.yml` 的 `new_post_name`（本博客为 `:year-:month-:day-:title.md`）→ 文件名须为 `YYYY-MM-DD-英文slug.md`
2. **既有分类**：`grep -rh "^categories:" source/_posts/*.md | sort | uniq -c` → 得到**已使用的分类词表**
3. **格式样例**：取 `ls -t source/_posts/*.md | head -3` 最近几篇，看 `categories`/`tags`/`date`/`cover` 的写法

本博客既有的分类词表（持续探测，勿硬编码）：
- `散文随笔` — 随笔、思考、人生感悟
- `年终总结` — 年度复盘
- `工具效率` — Obsidian / 效率工具 / 插件
- `技术随笔`、`源码解析` — 技术类

### Step 3️⃣ — 转换 frontmatter

按探测到的格式生成 Hexo frontmatter：

| Obsidian 字段 | Hexo 处理 |
|---------------|-----------|
| `title` | 保留 |
| `date: 2026-06-20 07:24` | 转为 `date: YYYY-MM-DD HH:mm:ss` |
| `category: 思考` | **映射到既有分类词表**，写入 `categories: [散文随笔]` |
| `tags: [t1, t2]` | 转内联数组 `tags: [t1, t2]` |
| `excerpt` | 保留为 Hexo 摘要 |
| `aliases` / `status` / `publish` / `journal` / `related` / `updated` / `cover`（空） | **删除**（Obsidian 专有，Hexo 不需要） |

补齐 Hexo 必需字段：
```yaml
categories: [散文随笔]   # 从既有词表选，禁止自创孤立分类
tags: [思考, 行动]
date: 2026-06-20 07:24:00
cover:                    # 留空占位
```

**分类映射决策**：原 Obsidian 的 `category` 是个人随意写的（如 `思考`、`Obsidian微信读书插件`），不能直接照搬。必须归并到既有词表——随笔类→`散文随笔`，工具/插件类→`工具效率`，技术类→`技术随笔`。

### Step 4️⃣ — 清理正文

移除所有 Obsidian 专有、Hexo 无法渲染的语法：

| Obsidian 语法 | 处理 |
|---------------|------|
| `![[image.png]]`（本地双链嵌入） | 替换为标准 `![alt](url)` 或保留待人工补图 |
| `![image\|700](url)`（`\|700` 缩放） | 去掉 `|700` → `![image](url)` |
| `%% 隐藏注释 %%` | 删除整行 |
| `[[双链]]` | 保留文本、去双链语法，或转为普通文字 |
| `chrome-extension://...` iframe、不可用外链 | 删除 |
| 文末空 `## Reference` 占位区 | 删除 |

### Step 5️⃣ — 写入文件

文件名：`YYYY-MM-DD-英文slug.md`（日期取自 frontmatter date，slug 由标题音译/意译为英文连字符形式）。

写入 `source/_posts/`。一次多篇则逐个写入。

### Step 6️⃣ — 提交并推送

```bash
cd /Users/xuan/VSCodeProjects/zhaohongxuan.github.io
git add source/_posts/<新文件...>
git commit -m "publish: <标题1> / <标题2> / ..."
git push origin src
```

推送 `src` 分支即触发 CD 自动部署，**无需 `hexo deploy`**。

## 分类词表维护

若某篇确实无法归入既有分类（如全新主题），先与用户确认是否新增分类词表项，再使用。**默认禁止产出孤立新分类**，否则博客分类页会出现单篇孤立类目。

## 常见错误

| 错误 | 后果 | 正解 |
|------|------|------|
| 直接照搬 Obsidian 的 `category` 字段 | 产生 `思考` 等孤立分类 | 映射到既有词表 |
| 保留 `categories: 思考`（裸字符串）与 `categories: [散文随笔]`（数组）混用 | Hexo 分类页混乱 | 统一内联数组格式 |
| 文件名带中文/空格 | 部署 URL 异常 | `YYYY-MM-DD-英文slug.md` |
| 保留 `![[x|700]]` | Hexo 渲染为坏链 | 去 `|700`，改标准 markdown 图链 |
| 忘记 `git push origin src` | CD 不触发 | 必须推送 `src` 分支 |
| 跑 `hexo deploy` | 重复/冲突 | 本仓库靠 CD 自动部署，不要手动 deploy |
