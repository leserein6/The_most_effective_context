> 历史 V0.2 研究记录。下文“命名迁移”“尚待证明”描述当时状态。当前路由、文件布局和验证结果以 [总体设计](Architecture.md)、[迁移说明](Migration.md) 和 [测试记录](Test_results.md) 为准。外部来源并未在本次实现中重新逐项复核。

# Evidence 外部 Skill 调研与设计取舍（V0.2）

> 本文给出**具体参考文件**，区分开源 Skill 的原做法与本仓库的改写。参考源是方法论依据，不是自动生效的运行时依赖。

## 已核对的成熟来源

| 外部来源（源文件） | 原 Skill 的核心机制 | 我们如何采用 / 不采用 |
| --- | --- | --- |
| [Agent Skills 规范](https://agentskills.io/specification) | 描述用于发现，主指令在激活时加载，附属资源再按需加载 | 采用 Progressive Disclosure；不冒称 Evidence 为原生 `SKILL.md` 包 |
| [Anthropic skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) | 定义能力和触发，再使用测试提示评估 Skill 效果 | 用于设计 Evidence 的触发描述与路由测试；未运行其专用 eval 工具 |
| [Superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) | 先读上下文、追问真实动机、审批设计边界 | 用于 [Clarify](../evidence/methods/clarify.md) 与 [Design](../evidence/methods/design.md)；不强制所有创意任务走完整软件工作流 |
| [Superpowers writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) | 任务分解到足以实施，明确验收输出，避免重复代码 | 用于 Design 到 Execute 的交接；不引入其特定计划目录与命令 |
| [Superpowers executing-plans](https://github.com/obra/superpowers/blob/main/skills/executing-plans/SKILL.md) | 按计划执行、将真实检查结果与预期比较、记录偏差 | 用于 [Execute](../evidence/methods/execute.md)；不复制强制子 Agent 或专有辅助脚本 |
| [Superpowers systematic-debugging](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md) | 先调查根因，形成假设、验证后修复 | 用于 [Debug](../evidence/methods/debug.md)；不照搬其所有调试工具细节 |
| [Superpowers verification-before-completion](https://github.com/obra/superpowers/blob/main/skills/verification-before-completion/SKILL.md) | 将具体完成声明与最新检查结果绑定 | 用于 [Verify](../evidence/methods/verify.md)；扩展到文档、Project 文件与其他外部修改 |
| [GitHub Awesome Copilot doc-and-modernize](https://github.com/github/awesome-copilot/blob/main/skills/doc-and-modernize/SKILL.md) | 本地仓库优先调查、记录可追溯代码依据、再写架构文档 | [Research](../evidence/methods/research.md) 借鉴其代码调查分支；不直接声称它是通用网络事实查证 Skill |
| [Superpowers writing-skills](https://github.com/obra/superpowers/blob/main/skills/writing-skills/SKILL.md) | 使用失败场景和 Agent 行为测试迭代协议，减少冗余 | 作为后续人工评估方法的参考；当前尚未完成 RED/GREEN 实测 |

## 转化准则

1. **来源与我们自己的设计分开**：上述文件只作为启发；我们的 Evidence 采用不同名称、宿主无关步骤和自有边界。
2. **负面触发同样重要**：不仅写“何时加载”，还写“何时不要加载”，避免无关上下文。
3. **不把大 Skill 原文复制进 Context**：入口只保留索引，操作协议精简，复杂参考按需下钻。
4. **独立记录适配损失**：例如 Superpowers 用到的 subagent、特定目录、脚本、TDD 基建，不可假定你的 Agent 自带这些能力。
5. **真实测试优先**：提示词看起来规范，不等于能正确触发、避免问答过度或跨 Session 恢复。

## 命名迁移

旧 `harness/protocols/*.md` 的方法正文现收拢在 `evidence/methods/*.md`；一级路由在根 `agent.md`，二级路由在 `entry/routes/`。Project Management 保留自己的操作协议，并且仅在必要时调用 Evidence。

**注意**：项目 Schema 里的 `references.evidence` 原意是“证明材料引用”，不是本轮任务执行方法；该字段保留兼容性，避免因目录重命名破坏实例数据。

## 尚待证明

- Agent 是否真正加载被路由到的文件，而非只看目录名称猜内容？
- 触发与非触发准确率在不同任务/模型上如何？
- 是否能减少无关 Token，同时避免漏读关键方法？
- 正向场景通过的同时，是否能处理错误案例、执行中断和用户更正？

方法：记录文件访问轨迹和实际输出，先做无需 Evidence 的基线，再做开启 Evidence 的对照。未完成真实运行前，不得称协议已经经过验证。
