# Claude Code Skills

xuan 的自定义 [Claude Code](https://claude.ai/code) Skills 集合，用于增强日常学习、阅读和知识管理工作流。

## Skills

| Skill | 描述 | 用法 |
|-------|------|------|
| **reading** | 英文阅读学习 — 拆解外文文章，提取词汇句型，生成学习笔记 | `/reading <URL | 双链 | 文本>` |
| **til** | 知识内化 — 将文章转化为结构化 TIL 笔记，关联知识库 | `/til <URL | 文件路径>` |
| **company-research** | 公司竞争分析 — 三视角（创业者/产业研究员/长期投资者）深度拆解公司或行业 | `研究贵州茅台`、`分析台积电`、`从0做电商挑战亚马逊` |
| **article-cover** | 文章封面提示词 — 维多利亚黑白木刻/蚀刻风格 16:9 封面绘画提示词 | `/article-cover <文章文本>` |

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

## 安装

**方式一：Claude Code 内 `/plugin` 命令（推荐）**

在 Claude Code 会话中运行：

```
/plugin marketplace add zhaohongxuan/skills
/plugin install hankzhao-skills@zhaohongxuan/skills
```

之后按 `/skills` 管理已安装的 skills。

**方式二：直接从终端安装**

```bash
claude plugin marketplace add zhaohongxuan/skills
claude plugin install hankzhao-skills@zhaohongxuan/skills
```

**方式三：手动复制 skills 目录**

```bash
git clone git@github.com:zhaohongxuan/skills.git /tmp/skills
cp -r /tmp/skills/.claude-plugin ~/.claude-plugin
```

## 开发

```
skills-repo/
├── .claude-plugin/
│   └── plugin.json     # Plugin 清单，注册所有 skills
├── skills/
│   ├── reading/
│   │   └── SKILL.md
│   ├── til/
│   │   └── SKILL.md
│   └── company-research/
│       ├── SKILL.md
│       ├── PROMPT.md
│       └── EXAMPLES.md
└── README.md
```

修改 skills 后更新 `plugin.json` 中的路径列表，提交 PR 即可。欢迎贡献。