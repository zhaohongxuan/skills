# Claude Code Skills

xuan 的自定义 [Claude Code](https://claude.ai/code) Skills 集合，用于增强日常学习、阅读和知识管理工作流。

## Skills

| Skill | 描述 | 用法 |
|-------|------|------|
| **reading** | 英文阅读学习 — 拆解外文文章，提取词汇句型，生成学习笔记 | `/reading <URL \| 双链 \| 文本>` |
| **til** | 知识内化 — 将文章转化为结构化 TIL 笔记，关联知识库 | `/til <URL \| 文件路径>` |
| **weread** | 微信读书助手 — 搜索书籍、书架、笔记划线、书评、阅读统计 | `/weread` |

### reading

- 支持 URL / 本地双链 / 直接粘贴文本三种输入
- 本地笔记直接读取文件，无需 WebFetch
- 自动提取核心词汇（含音标、释义、例句）、短语、句型
- 标注雅思考点（听力场景、同义替换、写作表达）
- 笔记输出到 `Areas/English/Reading/Notes/`

### til

- 将网页或文章内化成结构化 TIL（Today I Learned）笔记
- 自动关联已有知识库，追加到日记
- 笔记输出到 `Areas/TIL/`

### weread

- 搜索书籍、管理书架、查看笔记划线和书评
- 阅读统计与推荐
- 9 个子模块覆盖完整微信读书工作流

## 安装

Skills 放在 `~/.claude/skills/` 下即可被 Claude Code 自动加载：

```bash
git clone git@github.com:zhaohongxuan/skills.git /tmp/skills
cp -r /tmp/skills/* ~/.claude/skills/
```

## 开发

每个 Skill 由一个目录构成，核心文件是 `SKILL.md`：

```
skill-name/
└── SKILL.md    # frontmatter 声明 name/description，正文为执行指令
```

修改后提交 PR 即可。欢迎贡献。
