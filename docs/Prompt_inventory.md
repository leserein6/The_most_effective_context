# 历史 Prompt 资产去重与接入清单（2026-11-18）

## 决策：把“角色”和“专业知识”拆开

- **Agent = 独立上下文中的职责**：源码带读、问题定位、改前影响、测试策略、实现与独立审查。Agent 只规定职责、权限、必要输入和回传。已有角色不重复新建。
- **CodeBuddy Skill = 某类场景才需要的专业方法**：Go 语言、tRPC/RPC、金融风险等；放在 `.codebuddy/skills/<name>/SKILL.md`，只在相关任务加载。
- **Evidence Method = Harness 通用工作方法**：Clarify/Research/Design/Plan/Execute/Debug/Review/Verify 等，仍由 `agent.md → entry/routes → evidence/methods` 路由。
- **外部原始 Prompt = 只读参考资料**：继续由 `evidence/prompts/catalog.json` 保存上游版本、许可证与哈希；**不把历史用户 Prompt 伪装成外部上游仓库**。

此清单对历史文件库中**实际能重新打开的原文**与对话中能定位的旧方案分类；不宣称覆盖所有历史对话或已把每份旧提示词逐字迁入 GitHub。原始个人文件不直接拷贝进公共仓库；新增 Skill 是复用方法、剔除过时/过强要求后的改写。

## A. 已重新核对原文并落实

| 历史文件/资产 | 复用的内容 | 当前位置 | 处理方式 |
|---|---|---|---|
| `go-code-review-skill.md` | error、typed nil、context、goroutine、channel、资源、RPC/DB 与边界风险 | [go-review](../.codebuddy/skills/go-review/SKILL.md) | **新增 Skill**。不重复 `evidence/methods/review.md` 的通用审查流程 |
| `trpc-go-review.md` | 请求/Filter/Handler/Proxy、超时、重试、错误码、Protobuf presence、服务发现、观测 | [trpc-go-review](../.codebuddy/skills/trpc-go-review/SKILL.md) | **新增专项 Skill**。修正“固定超时大小序列”等无条件规则，要求按版本核实 |
| `financial-system-review.md` | 资金不变量、事实源、状态机、幂等、事务、重复调用与异常恢复 | [financial-risk-review](../.codebuddy/skills/financial-risk-review/SKILL.md) | **新增专项 Skill**。业务规则须以真实规格为准，适用于 Go/C++ 等语言 |
| `spec_to_coding_task_skill.md` | 自然语言需求 → 项目事实 → 输入/输出/验收契约 → 可执行任务 | [Plan](../evidence/methods/plan.md)、[Clarify](../evidence/methods/clarify.md) 与 [共用委派包](../evidence/prompts/delegation.md) | **融入现有方法**，只补“验收约束反推输入/输出”的关键规则，不另造第二个 Task 工作流 |
| `开发型需求测试工程研究.md` | 测试依据、oracle、方法选择、证据与充分性 | [测试工程](../evidence/testing/README.md) 和 [test-planner](../.codebuddy/agents/test-planner.md) | **已覆盖**；不重新制作测试工程 Skill |

说明：旧文件是 ChatGPT 历史文件库的用户资料，不是当前 GitHub 分支里的文件。这里记录名称、主题和采用关系以便审计；新 Skill 不是旧全文备份。

## B. 既有职责已覆盖，不重复生成 Agent

| 历史能力（部分来自既有对话，未全部找回原文件） | 当前负责者 | 不重复建新角色的原因 |
|---|---|---|
| C++ Code Understanding、Go/tRPC-Go 源码带读、调用链逐层阅读 | [source-tutor](../.codebuddy/agents/source-tutor.md) + [Learn](../evidence/methods/learn.md) | 统一最小知识点/真实源码/前置补齐；不将每个语言建一个导师 |
| `business-reviewer`：从需求和契约推反例，回查执行路径 | [pm-reviewer](../.codebuddy/agents/pm-reviewer.md) + [Review](../evidence/methods/review.md) | 需求轴与质量轴已经覆盖；业务域专用风险再选 Skill |
| 自适应 Code Review、独立复查、多 Reviewer 协作 | [Review](../evidence/methods/review.md) + [Orchestrate](../evidence/methods/orchestrate.md) | 根据审查范围决定是否拆分；不在默认上下文加载多套相同的 Review Prompt |
| 假设驱动根因分析、日志与源码交叉核验 | [bug-investigator](../.codebuddy/agents/bug-investigator.md) + [Debug](../evidence/methods/debug.md) | 先缩小故障机制，再交给实现者修复 |
| 变更影响、架构调查与安全重构 | [change-impact](../.codebuddy/agents/change-impact.md) + [Design](../evidence/methods/design.md) | 改前调查，不与改后 pm-reviewer 重合 |
| Prompt Architect、编写 Agent/Skill/协议的元提示词 | [matt-writing-for-agents](../evidence/prompts/README.md) + [共用委派包](../evidence/prompts/delegation.md) | 现有外部原文及协议边界足够；未核实独立旧文件原文，因此不冒称已迁入 |
| Go 调用链/状态/数据/错误/副作用多维核对 | [go-review](../.codebuddy/skills/go-review/SKILL.md) + [review](../evidence/methods/review.md) | 历史曾形成多份子文件，但不默认引入冗长的七段同质检查 |

## C. 明确不纳入本次通用库

| 专用历史 Prompt | 原因 |
|---|---|
| `cpp_to_go_migration_review_prompt.md` | 针对迁移方案；需旧新实现、特定语义等价基线 |
| `cpp_to_go_equivalence_testing_prompt.md`、`cpp_go_single_interface_test_design_prompt.md` | 专门验证一次 C++→Go 迁移的等价性；非通用业务测试默认流程 |
| `lifeterm`、`CPP模块与限流体系研究提示词.md`、`Go限流体系研究提示词.md` | 对象是特定迁移或限流设计，用户已明确不再使用这类提示词 |

排除专用 Prompt **不代表**去掉通用的接口兼容、状态生命周期和数据一致性检查；这些只在相应业务特征真实存在时，由现有方法/Skill 触发。

## D. 如何决定本轮只加载什么

| 用户说 | 主路由 | 可选专业能力 |
|---|---|---|
| “带我读这个 Go/C++ 入口” | learn | source-tutor（不默认加载任何 Review Skill） |
| “这个 panic/超时怎么回事？” | change/debug | bug-investigator；若请求定位后 Review 再视技术栈选专业 Skill |
| “改这个接口会波及谁？” | proposal/change | change-impact |
| “给我做 Code Review” | assess/review | pm-reviewer + Go 时 go-review，实际涉及 RPC 才额外 trpc-go-review，涉及资金才额外 financial-risk-review |
| “我要新增一个功能，你先分析再开发” | proposal → change | Clarify/Plan 形成任务契约，必要时 test-planner；不新建 Task 持久化对象 |
| “帮我写一个通用 Skill/Agent” | proposal/change | 现有 `matt-writing-for-agents` 参考 + 协议边界检查，不默认调源代码 Reviewer |

**原则**：不管 Skill 数量多少，单轮只读和当前错误机理相关的材料。所有角色遵守最小权限、无自动 Git commit/push、不能把未验证的结论写成通过。

## E. 尚未实测

已完成当前分支的静态配置/链接核验后，还需要在 Mac 的 CodeBuddy CLI 用 `/skills`、`/agents` 检查实际注册，并用真实 Go/C++ 变更对照：是否正确触发、是否误加载无关 Skill、是否能给出代码证据与反例。无目标模型运行证据前不声明行为通过。
