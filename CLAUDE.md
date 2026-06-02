# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这不是软件仓库，是一本**中文技术书**的写作工程：《三高之下——电商系统设计与治理的演化之旅》（高并发 / 高可用 / 高性能 + 数据一致性 + 体系化治理）。

- 输出物：Markdown 章节稿 + PDF（移动端阅读用）
- 读者目标：读完记住"下次遇到类似问题我知道怎么思考"，不是技术 checklist
- 叙事铁律：**场景 → 朴素方案 → 撞墙 → 调查 → 演化 → 原理沉淀** 六段式，不写"正确结论汇编"

## 常用命令

PDF 导出走 `~/.claude/skills/md2pdf`（pandoc + Chrome headless，自动生成左侧大纲、Water.css 排版、CJK 字体注入）。

```bash
# 单章导出
bash ~/.claude/skills/md2pdf/scripts/md2pdf.sh chapters/01-flash-sale-crash.md pdf_output/01.pdf

# 多章合并导出（先合并 + 剥离写作元数据 blockquote，再交给 skill）
python3 scripts/merge_chapters.py chapters/00-prologue.md chapters/01-flash-sale-crash.md -o /tmp/part1.md
bash ~/.claude/skills/md2pdf/scripts/md2pdf.sh /tmp/part1.md pdf_output/序幕+第1章.pdf
```

`scripts/merge_chapters.py` 是本书特化的预处理：合并多章节 + 剥离 H1 之后的写作元数据 blockquote（**所属部** / **主讲** / **引用** / **叙事设计** 这块对读者无意义）。

`scripts/md2pdf.py` 已废弃（fpdf2 实现，渲染质量低），保留作为历史记录。

`pdf_output/` 已被 `.gitignore` 忽略。

## 三件套权威文件（写每一节正文之前**按顺序**查）

本书的核心架构是**单一来源原则**——每一类信息只有一个权威文件，其他地方只引用、不重复。这是项目最初最大的痛点（catalog.md 597 行里把节标题、写作提示、TODO 和章节文件四处重复）的根治方案。

| 顺序 | 文件 | 职责 | 写作前查什么 |
|---|---|---|---|
| 1 | [`chapters/CHAPTER_OWNERSHIP.md`](./chapters/CHAPTER_OWNERSHIP.md) | 40+ 技术概念的"主讲章 / 引用章"分工矩阵 | 本节涉及的概念是不是别章主讲？是的话只能一两句话点到 + 锚点链接，**不要展开** |
| 2 | [`chapters/SETTING.md`](./chapters/SETTING.md) | 虚拟公司"橙舟"设定圣经（人物 / 服务 / 事故年表 / 对话语调示范） | 要用的人物、服务名、事故是否都在表里？不在的**先回这里加再用**，绝不临时造 |
| 3 | [`catalog.md`](./catalog.md) | 全书骨架 + 章级进度速查表 | 章节定位、整书进度。**只到章不到节** |

每个章节文件顶部都有元数据块声明本章的"主讲 / 引用"——和 `CHAPTER_OWNERSHIP.md` 保持一致。

### 反模式（绝不允许）

- 在某章正文里临时造一个新人物名（"老李"）、新服务名（"inventory-service"）、新事故（"2017 年那次缓存事故"）——必须先回 `SETTING.md` 加。
- 在引用章里把别章主讲的概念**展开**（比如在第 1 章把 Redlock 论战讲完整，那是 3.6 的事）。
- 在 `catalog.md` 里写节级标题或 TODO——节级 TODO 在各章节文件里以 `- [ ]` 维护。

## 文件结构（与单一来源职责对应）

```
catalog.md                       # 全书骨架 + 章级进度速查表（v2.1）
chapters/
  CHAPTER_OWNERSHIP.md           # 谁讲什么矩阵
  SETTING.md                     # 橙舟设定圣经
  00-prologue.md ~ 16-epilogue.md  # 17 章正文
appendices/
  a-papers-and-people.md         # 史料与脚注（11 论文 + 8 人物 + 7 工程文档）
  b-glossary.md                  # 术语对照表（75 个术语，卡片式）
  c-postmortem-template.md       # 故障复盘模板（橙舟版）
attachments/                     # 图、图谱等
pdf_output/                      # 导出产物，gitignored
scripts/md2pdf.py                # Markdown → PDF（中文字体自动适配）
```

## 设定速查（节省 SETTING.md 翻阅）

写场景前必须用以下固定符号，不要造同义词：

- **公司**：橙舟 / ChengZhou / OrangeBoat（杭州主 + 上海双活 + 张北灾备）
- **5 人团队**：老张（SRE TL，灵魂角色）/ 小林（业务 TL）/ 小赵（SRE on-call，老张徒弟）/ 小周（实习生，读者代入镜子）/ 王姐（DBA TL）
- **12 个核心服务**：`api-gateway` / `auth-service` / `user-service` / `product-service` / `stock-service` / `price-service` / `order-service` / `payment-service` / `payment-notify` / `notify-service` / `recommend-service` / `member-service`
- **6 个共享事故**（章节叙事的弹药库）：2016 行锁雪崩 / 2018 缓存血案 / 2019 重复下单 / 2022 张北脑裂 / 2025 对账日 / 2026 47 分钟尾延迟（序幕复盘对象）

详细人物画像、服务职责、事故时间线、对话语调示范见 `chapters/SETTING.md`。

## 写作维护规则

### 章节状态推进
每完成或推进一个章节，回 `catalog.md` 的进度速查表更新状态符号（✅ 完稿 / ✏️ 写作中 / 📋 大纲完成 / 🔲 待写）和"最近动作"。**粒度到章不到节**——节级 TODO 在章节文件内的 `- [ ]` 里维护。

### 节粒度的"叙事张力"原则
节级粒度按"读者会不会记住"决定，不按"教科书是否需要这个标题"决定。如果某节明显比相邻节重 2 倍 / 轻一半，先想"是不是该拆 / 该合并"，再写。

### 工具书层（附录 A/B/C）的差异化
**为本书读者服务，不为搜索引擎服务**：
- 附录 A 只收录正文实际引用的论文/人物，不做"分布式系统必读论文清单"
- 附录 B 只收录正文真出现的术语，不做"分布式系统术语百科"
- 附录 C 是橙舟版模板，预设了本书的人物/服务/事故约定

### Session 收尾
- 不要主动 `git commit`（用户没要求时不提交）
- 重要决策（新增设定、新风格规则）回写到 `~/.claude/projects/.../memory/feedback_writing_workflow.md`
- 检查 `catalog.md` 进度速查表是否更新

## 输出语言

中文。脚本注释、PDF 元信息也是中文。
