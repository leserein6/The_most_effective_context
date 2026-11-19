# 二级索引：形成需求、设计或计划

核心问题：**缺目标决定、实现方案，还是可执行工作安排？**

| 当前情况 | 读取/执行 |
|---|---|
| 关键目标、边界、验收或用户取舍未明确 | [clarify](../../evidence/methods/clarify.md) |
| 现有能力/技术事实尚无依据 | 按需 [research](../../evidence/methods/research.md)，不要求用户替你查代码 |
| 需要决定职责、接口、数据流或方案取舍 | [design](../../evidence/methods/design.md) |
| 需要选择测试方法、论证其充分性 | [方法选择协议](../../evidence/testing/selection.md)，按影响风险选择 EP/BVA、状态、组合、MC/DC 等，形成覆盖分母与独立判定依据 |
| 需要设计开发需求的验收条件、场景、判据和环境 | [测试设计](../../evidence/testing/design.md)，与 design / plan 共用同一套验收条件 |
| 方案已明，需要拆文件、依赖、动作和验收 | [plan](../../evidence/methods/plan.md) |

需要专门为开发需求推导测试策略且适合隔离上下文时，可选 [test-planner](../../.codebuddy/agents/test-planner.md) 辅助分析；它不生成验收结论、不改测试代码，主 Agent 仍核对需求与 Oracle。

## 统一方案故事线（只统一表达，不新建持久对象）

当用户需要完整方案时，按 **问题与证据 → 目标/非目标/验收 → 当前状态与约束 → 候选方案及选择理由 → 依赖与第一步 → 验证办法 → 风险/回退** 组织输出；关键假设独立标记。这是阅读结构，不是必须生成的七份文件，也不强制七种方法串行运行。简单或低风险任务可压缩为目标、动作和验证；跨模块、不可逆或高风险变更再展开详细设计与独立审查。

方案由 Clarify / Research / Design / Plan 按缺口组合；审查仍用 [Review](../../evidence/methods/review.md) 的方案分支，可按风险选只读 Reviewer，但不新建 Planning Agent、Project 状态或 Work Item 数据库。长文作为 Project work/ 的产物引用；权威定义、验收、决策和 WI 仍由原 Schema 管理。

只做当前缺失部分，不机械走完全部方法。方案产出不等于获得实现授权；用户要求“先给方案别改代码”时交付到此停止。用户已授权设计并实现时，完成必要方案后直接转 change，不反复问继续。

例：“设计书单批量导入”先确定非法行出现后旧书库与已读行应处于什么状态；“按既定方案列实施步骤”直接进入plan，不重新选择架构。
