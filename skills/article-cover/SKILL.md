---
name: article-cover
description: 根据文章内容生成维多利亚时代黑白木刻/蚀刻风格的16:9横向封面绘画提示词，用于文章配图
---

# /article-cover — 文章封面提示词 Skill

将一篇文章的核心观点，转化为 Gustave Doré 式黑白木刻/蚀刻风格的超现实隐喻封面提示词。

## 角色定位

精通维多利亚时代版画美学的概念视觉设计师，专注把抽象观点转化为黑白木刻/蚀刻风格的 16:9 横向文章封面。用超现实隐喻手法，通过交叉影线和点画技法，创造具有叙事性和哲学深度的视觉作品。

## 输入

```
/article-cover <文章文本 或 URL 或 文件路径>
```

| 类型 | 处理方式 |
|------|----------|
| **文本** | 直接分析 |
| **URL** | `WebFetch` 抓取正文后分析 |
| **文件路径** | 读取文件内容后分析 |

## 处理流程

### Step 1️⃣ — 分析内容

从文章中提炼四要素：

- **核心主题**（1 个名词）
- **核心观点**（1 句话）
- **情绪基调**（六选一：`inspirational` / `mysterious` / `protective` / `breakthrough` / `contemplative` / `rebellious`）
- **关键视觉锚点**（文中可转化为意象的具象事物）

### Step 2️⃣ — 设计隐喻方案

确定三件事：

- **前景主体物**：与主题强关联的**具体物体**（不要抽象概念直接上场）
- **隐喻转化机制**：如何**超现实地**表达观点（but… 的转折）
- **2-3 个象征性辅助细节**：点缀隐喻，不超过 3 个

### Step 3️⃣ — 输出提示词

严格按以下模板填空（方括号为占位，需替换为实际内容）：

```
A horizontal black and white [woodcut/etching] banner (16:9 ratio), depicting [前景主体物详细描述], but [超现实转化描述]. The [主体物] rendered in detailed cross-hatching showing [质感], the [隐喻元素] in lighter stippling creating [感觉]. [光源描述] against pure black void. [装饰细节] in negative space. [文字区域位置] pure black for text overlay. [情绪] mood in Victorian illustration/Gustave Doré style.
```

### Step 4️⃣ — 解释隐喻

用 1-2 句话说明：图片如何视觉化文章观点。

## 负向约束（严格遵守）

生成提示词时，以下一律禁止出现：

- ❌ 风格：彩色 / 渐变 / 灰度照片 / 扁平化 / 3D 渲染 / 卡通 / 水彩 / 油画
- ❌ 技法：阴影渐变 / 模糊 / 光晕 / 滤镜感 / 平涂黑色
- ❌ 构图：竖版 / 方形 / 非 16:9 / 对称居中 / 无文字预留区
- ❌ 内容：字面翻译 / 无关装饰 / 超过 3 个主要元素 / 过度抽象
- ❌ 调性：可爱 / 卡通 / 恐怖 / 血腥 / 广告感
- ❌ 其他：添加文字 / 照片拼贴 / 低分辨率

## 输出格式

```
## 内容分析
- 核心主题：<名词>
- 核心观点：<一句话>
- 情绪基调：<六选一>
- 视觉锚点：<具象事物>

## 隐喻方案
- 前景主体物：<具体物体>
- 转化机制：<超现实转折>
- 辅助细节：<2-3 个>

## Prompt
<填好的模板提示词>

## 隐喻说明
<1-2 句话>
```

## 使用场景

- 写完一篇文章，需要一张封面配图
- 公众号 / 博客 / Newsletter 封面生成
- 想用统一视觉语言建立系列文章的封面体系

## 注意事项

- 主体物必须是**具体物体**，不要让"自由""成长"这类抽象词直接进 prompt
- `but` 后的转折是灵魂——没有超现实转化就不算达标
- 文字预留区（pure black for text overlay）必须保留，用于后期叠标题
- 风格关键词锁定 `Victorian illustration / Gustave Doré / cross-hatching / stippling / pure black void`，不可漂移
