# 附录 A：史料与脚注——本书引用的论文与人物

> **本附录定位**：不是"分布式系统必读论文清单"，而是**正文的脚注集合**——只收录本书叙事中真正勾连了的论文、博客、人物。
>
> 读到正文某一段觉得"这个论断哪来的？"时，回到这里能找到来源。
>
> **写法约定**：每条由"史料 + 一句话注释 + 关联章节"三部分组成。注释解释的是"它为什么对本书叙事重要"，不是论文摘要。
>
> **配套阅读**：[章节分工矩阵](../chapters/CHAPTER_OWNERSHIP.md) · [设定圣经](../chapters/SETTING.md)

---

## A.1 使用说明

本附录分四个部分：

| 部分 | 内容 | 用法 |
|---|---|---|
| §A.2 论文 | 经典论文 11 篇 | 读到正文相关段落时回查"它的源头在哪" |
| §A.3 人物 | 关键人物 8 位 | 理解"这个观点是谁先提出的，他是什么背景" |
| §A.4 工程文档与技术博客 | 国内/业界一线材料 7 篇 | 论文太"学术"时的工程实践参照 |
| §A.5 反向索引 | 按章节查 | 读完某章想深挖时的入口 |

---

## A.2 论文

### A.2.1 共识与 CAP

#### **CAP Theorem**
- **作者**：Eric Brewer（提出，2000 PODC keynote）；Seth Gilbert & Nancy Lynch（证明，2002）
- **关键文献**：
  - Brewer (2000) "Towards Robust Distributed Systems" (PODC keynote)
  - Gilbert & Lynch (2002) "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services"
  - Brewer (2012) "CAP Twelve Years Later: How the 'Rules' Have Changed"
- **史料注释**：Brewer 2000 年只是在 keynote 上提出猜想，2002 年的 Gilbert-Lynch 论文给出了形式化证明。Brewer 2012 年的反思文章纠正了"三选二"的简化叙事——这一点本书第 11 章会还原 Brewer 自己的修正立场，不再讲"CAP 三选二"的教科书版。
- **关联章节**：第 2 章 2.6（缓存层 CAP 投影）· **第 11 章 11.3（CAP 的最严肃展开）** · 第 7 章 7.4（脑裂时的强约束）

#### **Paxos Made Simple**
- **作者**：Leslie Lamport（2001）
- **史料注释**：Lamport 1998 年发表的原始 Paxos 论文（"The Part-Time Parliament"）因为引入希腊议会的虚构故事而广受嘲笑——"看不懂"。2001 年这篇 "Made Simple" 是他的第二次尝试，但仍然不简单。本书第 7 章 7.5 引用它的目的不是讲算法，而是讲"为什么共识算法需要十几年才能让工业界用得起来"——Paxos 是这段历史的起点。
- **关联章节**：**第 7 章 7.5（共识算法）** · 第 3 章 3.6（Redlock 论战时一笔带过）

#### **In Search of an Understandable Consensus Algorithm (Raft)**
- **作者**：Diego Ongaro, John Ousterhout（USENIX ATC 2014）
- **史料注释**：论文标题就是它的故事——"我们想要一个能被理解的共识算法"。Raft 的工业界统治力（etcd、Consul、TiKV、CockroachDB……）证明了"可理解性"本身就是一种工程价值。本书第 7 章 7.5 用 Raft 而非 Paxos 作为共识算法的代表，原因就在这里。
- **关联章节**：**第 7 章 7.5（共识算法）**

#### **Dynamo: Amazon's Highly Available Key-value Store**
- **作者**：Giuseppe DeCandia 等（SOSP 2007）
- **史料注释**：Amazon 在 2007 年公开了支撑购物车的 Dynamo 设计——这是工业界第一次系统阐述"为了可用性放弃强一致"的实战做法。**最终一致性、向量时钟、读写仲裁（W+R>N）** 这些今天的常识都发源于此。本书第 11 章讲 BASE 哲学时，Dynamo 是它的工业落点。
- **关联章节**：**第 11 章 11.3（BASE 理论）** · 第 2 章 2.6

### A.2.2 缓存与数据结构

#### **Space/Time Trade-offs in Hash Coding with Allowable Errors**
- **作者**：Burton Howard Bloom（CACM 1970）
- **史料注释**：布隆过滤器的原始论文。一篇 1970 年的 5 页论文，定义了一个 50 多年后仍在用的数据结构。本书第 2 章 2.3 讲缓存穿透时引用——但**不讲它的数学推导**，只用几何直觉。原始论文留作有兴趣读者的史料链接。
- **关联章节**：**第 2 章 2.3（缓存穿透 + 布隆过滤器的几何直觉）**

### A.2.3 性能与延迟

#### **The Tail at Scale**
- **作者**：Jeffrey Dean, Luiz André Barroso（CACM 2013）
- **史料注释**：**本书第 8 章的灵魂论文**。Jeff Dean 第一次系统阐述了"尾部延迟在大规模系统中是必然属性，不是 bug"——平均延迟会骗你，P99.9 才是用户感受到的延迟。本书第 8 章 8.4 的所有论述都建立在这篇论文之上，包括"对冲请求 (hedged requests)"、"备份请求 (tied requests)" 这些工程技巧也都来自这里。
- **关联章节**：**第 8 章 8.4（尾部延迟 / P99.9）** · 第 10 章 10.1（GC 是长尾的一个例子）

#### **Bigtable: A Distributed Storage System for Structured Data**
- **作者**：Fay Chang 等（OSDI 2006）
- **史料注释**：Google 2006 年的存储论文。本书引用它**不是讲 Bigtable 本身**，而是讲它隐含的工程哲学——LSM-Tree、SSTable、列式存储这些今天 NoSQL/NewSQL 的基础设施都源自这里。第 4 章讲分库分表的演化时作为对照（"如果当时我们看过 Bigtable……"的反事实假设）。
- **关联章节**：第 4 章（分库分表的对照）

### A.2.4 异步与系统设计

#### **End-to-End Arguments in System Design**
- **作者**：J. Saltzer, D. Reed, D. Clark（ACM TOCS 1984）
- **史料注释**：四十年前的系统设计经典——"功能应该实现在端到端，而不是中间层"。本书第 11 章 11.4 讲幂等性时回到这个原则：**网络重试不能保证幂等，幂等必须由业务端到端保证**。这条论断的源头在这里。
- **关联章节**：**第 11 章 11.4（幂等性原理）** · 第 9 章（异步化时的可靠投递）

#### **SAGAS**
- **作者**：Hector Garcia-Molina, Kenneth Salem（SIGMOD 1987）
- **史料注释**：Saga 模式的原始论文。1987 年——这是一个比绝大多数读者更老的概念。原本是为长事务（不能锁住资源等数小时）设计的，今天被拿来做微服务分布式事务，是一种巧妙的"老酒新瓶"。本书第 12 章讲分布式事务时，会还原这段"Saga 是怎么从数据库长事务被搬到微服务"的历史。
- **关联章节**：**第 12 章（分布式事务方案集）**

### A.2.5 可观测性

#### **Dapper, a Large-Scale Distributed Systems Tracing Infrastructure**
- **作者**：Benjamin H. Sigelman 等（Google Technical Report 2010）
- **史料注释**：Google Dapper 是几乎所有现代分布式追踪系统的祖宗——Zipkin / Jaeger / SkyWalking / OpenTelemetry 全都是它的精神后代。**TraceID、SpanID、采样率**这些概念都来自这里。本书第 13 章引用它时强调一点：Dapper 的核心创新不是技术，而是"低开销采样 + 不打扰业务代码"的工程权衡。
- **关联章节**：**第 13 章 13.4（链路追踪）**

### A.2.6 混沌工程

#### **Chaos Engineering: System Resiliency in Practice**
- **作者**：Casey Rosenthal, Nora Jones（O'Reilly 2020）
- **史料注释**：严格说这是一本书不是一篇论文，但它是混沌工程作为一门工程学科的奠基文本。它把 Netflix 从 2010 年开始的实践——Chaos Monkey、Chaos Kong、Failure Injection Testing——提炼成五条原则。本书第 14 章 14.3 的"五个步骤"是它的简化版。
- **关联章节**：**第 14 章（混沌工程整章）**

---

## A.3 关键人物

### A.3.1 学术界

#### **Leslie Lamport**（1941– ）
- **身份**：图灵奖得主（2013），分布式系统理论奠基人之一
- **本书相关贡献**：Paxos、逻辑时钟、拜占庭将军问题（与 Shostak、Pease 合作）、TLA+
- **本书引用语境**：第 7 章共识算法的引入——理解 Lamport 的工作有助于理解"为什么共识难"。Lamport 自己曾说："分布式系统是一个你都不知道存在的计算机的故障会让你的计算机崩溃的系统"——这句话本书会引用。
- **关联章节**：第 7 章 7.5

#### **Jeffrey Dean**（1968– ）
- **身份**：Google Senior Fellow / SVP，MapReduce、Bigtable、Spanner、TensorFlow 的核心设计者
- **本书相关贡献**：The Tail at Scale；MapReduce；Bigtable
- **本书引用语境**：第 8 章尾部延迟整章建立在 Dean 2013 年的论文之上。"Latency lies"（延迟的平均值会骗你）这句话基本上是 Dean 一手推广开的。
- **关联章节**：第 8 章 8.4 · 第 10 章 10.1

#### **Eric Brewer**（1967– ）
- **身份**：UC Berkeley 教授 / Google VP，CAP 定理提出者
- **本书相关贡献**：CAP 定理（2000 提出，2012 自我修正）；Inktomi 联合创始人（搜索引擎先驱）
- **本书引用语境**：本书第 11 章 11.3 在讲 CAP 时**特意还原 Brewer 2012 年自己的修正**——他认为 "CAP 三选二" 是过度简化，真实情况是"分区发生时如何选择"。这一点很多教科书没讲。
- **关联章节**：第 11 章 11.3 · 第 2 章 2.6

#### **Werner Vogels**（1958– ）
- **身份**：Amazon CTO（2005 至今）
- **本书相关贡献**：推动 Amazon 服务化架构；2008 年那篇影响深远的博客 "Eventually Consistent" 把 BASE 哲学带进了主流视野
- **本书引用语境**：BASE 哲学的工业界推手。本书第 11 章 11.3 引用 Vogels 那句"几乎所有大型分布式系统都是最终一致的"——这是 BASE 取代 ACID 在大规模系统中地位的标志性表态。
- **关联章节**：第 11 章 11.3

### A.3.2 工业界 / 工程实践

#### **Martin Kleppmann**（1980– ）
- **身份**：剑桥大学 senior researcher，《Designing Data-Intensive Applications (DDIA)》作者
- **本书相关贡献**：DDIA（2017）——可能是过去十年分布式系统领域最有影响力的一本书；2016 年公开质疑 Redlock 安全性的博客
- **本书引用语境**：第 3 章 3.6 Redlock 论战——Kleppmann 是论战的一方。他的批评不是"Redlock 不能用"，而是"Redlock 不是真正的分布式锁；如果你需要正确性，请用 ZooKeeper / etcd"。本书会还原这场论战的两边立场。
- **关联章节**：**第 3 章 3.6（Redlock 论战）**

#### **Salvatore Sanfilippo (antirez)**（1977– ）
- **身份**：Redis 作者（2009 创建，2020 退出维护）
- **本书相关贡献**：Redis；Redlock 算法
- **本书引用语境**：第 3 章 3.6 Redlock 论战的另一方。antirez 对 Kleppmann 批评的回应是："你们用错场景了，Redlock 是为可用性优先的场景设计的，不是为正确性。" 这场论战的精彩之处在于双方都对——只是预设了不同的场景前提。
- **关联章节**：**第 3 章 3.6（Redlock 论战）**

#### **Adrian Cockcroft & Yury Izrailevsky**（Netflix 工程文化奠基人）
- **身份**：Netflix 早期云架构师（Cockcroft 现在 AWS）
- **本书相关贡献**：Netflix 微服务架构 + Chaos Monkey 的工程文化推广者；Hystrix 设计参与
- **本书引用语境**：第 14 章混沌工程的源头是 Netflix 2010 年迁移 AWS 时的工程决策——这一决策的推动者就是 Cockcroft 团队。本书 14.1 的开篇场景围绕这段历史展开。
- **关联章节**：**第 14 章 14.1** · 第 6 章 6.3（Hystrix → Resilience4j 代际故事）

#### **Martin Thompson**（LMAX Disruptor 设计者）
- **身份**：高性能 Java 领域代表人物，Mechanical Sympathy 理念推广者
- **本书相关贡献**：LMAX Disruptor（2011）；机械同理心（Mechanical Sympathy）的工程化
- **本书引用语境**：第 10 章 10.5 "机械同理心 / 缓存行 / 伪共享" 整节建立在 Thompson 的工作之上。"Mechanical Sympathy" 这个词他借自 F1 赛车手 Jackie Stewart——驾驶员理解机械才能跑得快。
- **关联章节**：**第 10 章 10.5（机械同理心）**

---

## A.4 工程文档与技术博客

> 论文太"学术"时，工业界的一线材料往往更接地气。下列条目是本书直接引用的工程文档/技术博客。

#### **"How to do distributed locking" — Martin Kleppmann**
- **链接**：https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
- **史料注释**：Redlock 论战的开端——Kleppmann 2016 年这篇博客质疑 Redlock 在 GC pause / 时钟漂移下的安全性。今天读起来仍然是一份"分布式锁陷阱"的最佳入门教材。
- **关联章节**：**第 3 章 3.6**

#### **"Is Redlock safe?" — antirez**
- **链接**：http://antirez.com/news/101
- **史料注释**：antirez 对 Kleppmann 的回应。如果说 Kleppmann 的文章是"理论家的批评"，这篇就是"工程师的反驳"——读完两篇你才能理解为什么"分布式锁"这件事没有银弹。
- **关联章节**：**第 3 章 3.6**

#### **"Eventually Consistent" — Werner Vogels**
- **链接**：https://www.allthingsdistributed.com/2008/12/eventually_consistent.html （2008 年原始版本；2009 年 ACM Queue 修订版）
- **史料注释**：Vogels 把"最终一致性"从一个学术概念变成了工业界的主流叙事。2008 年这篇博客是分水岭——之前讲 ACID 是政治正确，之后 BASE 成了大规模系统的默认假设。
- **关联章节**：第 11 章 11.3

#### **Google SRE Book**
- **链接**：https://sre.google/books/ （免费在线）
- **史料注释**：MTBF、MTTR、Error Budget、SLO/SLI 这些今天的 SRE 常识都在这本书里被系统化。本书第 5 章建立"故障观"时引用的几乎所有数学工具都源自这本书第 4-5 章。
- **关联章节**：**第 5 章 5.2 / 5.5** · 第 13 章 13.5（告警）

#### **阿里 Sentinel 设计文档**
- **链接**：https://github.com/alibaba/Sentinel/wiki
- **史料注释**：Sentinel 不只是 Hystrix 的中国版本——它的设计哲学不同。Hystrix 把熔断 / 限流 / 隔离揉在一起，Sentinel 拆开做"流量控制 + 系统保护 + 熔断降级"三件事。这种拆分背后是阿里在双十一场景下的实战教训。本书第 6 章 6.5 讲 Sentinel 设计哲学时引用。
- **关联章节**：**第 6 章 6.5**

#### **阿里 RocketMQ 设计文档 / 双十一技术总结**
- **链接**：https://rocketmq.apache.org/docs/
- **史料注释**：RocketMQ 在事务消息这件事上的设计是国内特色——本地事务 + 半消息 + 回查的方案。本书第 12 章讲分布式事务方案集时，"事务消息"这一支的工程化主要参考 RocketMQ 的实现。
- **关联章节**：**第 12 章** · 第 9 章 9.3

#### **"Chaos Engineering: Building Confidence in System Behavior through Experiments" — Netflix**
- **链接**：https://principlesofchaos.org/ + Netflix Tech Blog 2014-2017 多篇
- **史料注释**：principlesofchaos.org 是混沌工程的"原则宣言"——五条原则成为后续 ChaosBlade、Litmus 等工具设计的纲领。本书第 14 章 14.2-14.3 的理念铺底基于这份宣言。
- **关联章节**：**第 14 章 14.2-14.3**

---

## A.5 反向索引：按章节查史料

> 读完某章想深挖时，从这里入口。

| 章节 | 论文 / 博客 | 人物 |
|---|---|---|
| **序幕** | Dapper | Jeff Dean |
| **第 1 章** 秒杀崩溃 | — | — |
| **第 2 章** 缓存 | Bloom (1970) · CAP (Brewer/Gilbert-Lynch) | Burton Howard Bloom · Eric Brewer |
| **第 3 章** 分布式锁 | Kleppmann 博客 · antirez 反驳 · Paxos Made Simple | Martin Kleppmann · antirez · Lamport |
| **第 4 章** 分库分表 | Bigtable（对照） | — |
| **第 5 章** 故障观 | Google SRE Book | — |
| **第 6 章** 限流降级熔断 | Netflix Hystrix 文档 · 阿里 Sentinel 文档 | Adrian Cockcroft |
| **第 7 章** 冗余/脑裂 | Paxos · Raft · CAP | Lamport · Ongaro |
| **第 8 章** 延迟解剖 | The Tail at Scale | Jeff Dean |
| **第 9 章** 异步化 | End-to-End Arguments · RocketMQ 文档 | — |
| **第 10 章** 优化极限 | Tail at Scale（GC 视角） | Martin Thompson |
| **第 11 章** 事务的黄昏 | CAP · Dynamo · Eventually Consistent · End-to-End Arguments | Brewer · Vogels |
| **第 12 章** 分布式事务 | SAGAS (1987) · RocketMQ 事务消息 | Garcia-Molina |
| **第 13 章** 可观测性 | Dapper · Google SRE Book | — |
| **第 14 章** 混沌工程 | Chaos Engineering (O'Reilly) · principlesofchaos.org | Adrian Cockcroft / Nora Jones |
| **第 15 章** 技术债 | Conway's Law（1968 原始论文） | Melvin Conway |

---

## A.6 维护说明

- 本附录条目**只在正文实际引用时增减**——不收录"应该读但本书没引"的论文
- 写作各章时如引用了新的史料，回本附录登记一条；删除引用时同步删条目
- 如某条引用降级为"一笔带过"，可保留但在注释里标注"仅在 X.Y 节脚注出现一次"

---

*附录 A 版本：v1.0（史料与脚注模式） | 最后更新：2026-06-02*
