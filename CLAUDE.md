# hankzhao-skills

自定义 Claude Code Skills 集合。

## Skills

通过 Skill 工具触发，按 `skills/` 目录下各 skill 的 `description` 匹配调用：

| Skill | 用途 |
|-------|------|
| **reading** | 英文阅读学习 |
| **til** | 知识内化 |
| **company-research** | 公司竞争分析 |
| **article-cover** | 文章封面提示词 |
| **hexo-publish** | Hexo 博客发布 |

## 开发

- 新增 skill：在 `skills/` 下创建目录，放入 `SKILL.md`
- 修改 skill：同时在 `CHANGELOG.md` 中记录变更，并按 [Semantic Versioning](https://semver.org/spec/v2.0.0.html) 升级版本号
- 注册 skill：在 `.claude-plugin/plugin.json` 中添加路径
- 详细规范见 [README.md](README.md)