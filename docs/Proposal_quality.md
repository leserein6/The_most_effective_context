# 方案质量与执行就绪：维护者设计记录

## 目标与边界

解决“方法文件各自正确，但最终方案不连贯、缺可执行第一步或陷入过度准备”的问题。保留现有 Project、Work Item、Turn Task、Mode 与 Verify，不引入独立规划数据库、Planning Agent 或强制的七步机器流程。

## 决策：统一叙事，按风险加载

- 方案叙事：问题与依据 → 目标/非目标/验收 → 现状/约束 → 方案/决策 → 依赖/第一步 → 验证 → 风险/回退。
- 低风险变更可简写；高风险/跨模块/迁移才显式展开不变量、关键假设、接口影响和独立方案审查。
- 结论 READY / EXPERIMENT / NEEDS_REVISION / BLOCKED 仅表示方案阶段可行动性。实现验收仍使用 Verify 的 PASS / FAIL / UNVERIFIED。
- 重要假设应有直接依据或 PoC。执行中事实变化时，只重新审视受影响的设计决定和验证。
- 持久化不变：definition.md 记问题/范围、acceptance.md 记判据、decisions.md 记有效决定、work-items.md 记可独立验收的 WI；方案正文按需放 work/。

## 外部实践依据及取舍

- [GitHub Spec Kit](https://github.com/github/spec-kit)：借鉴规格、计划、任务的跨产物一致性检查；不复制规格状态引擎。
- [OpenSpec](https://github.com/Fission-AI/OpenSpec)：借鉴 Proposal/Design/Task 的按需产物依赖；不增加固定目录层级。
- [Superpowers](https://github.com/obra/superpowers)：借鉴设计和计划的职责区分；不强制所有任务完整 Brainstorm。
- [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD)：借鉴按复杂度调整规划深度；不扩展固定 Agent 角色数。
- [GSD](https://github.com/gsd-build/get-shit-done)：借鉴独立计划审查和停止无效重写；不建立持久计划迭代数据库。

以上为设计借鉴，不构成在目标 CodeBuddy 模型上已验证效果的声明。

## 行为评价场景（当前未实测）

| 场景 | 正确行为 | 失败信号 |
|---|---|---|
| 一行 Markdown 修订 | 简短目标、改动、验证 | 强制七章和无关重构 |
| 普通后端功能 | 目标、设计、WI、验收双向追溯 | 漏项或多做无来源工作 |
| CKV 路由迁移 | 区分已知依赖与假设，设计 PoC/回退 | 编造下游路由能力、宣称已可上线 |
| 关键业务决定缺失 | BLOCKED，只问影响结果的决定 | 擅自补充业务语义 |
| 技术条件尚无依据 | EXPERIMENT，受控实验 | 无证据 READY 或无限改稿 |
| 执行时假设失效 | 局部修订受影响的 WI/决策 | 另建状态系统或丢失历史 |

真实验收需要固定客户端、模型、协议版本，用相同场景比较改造前后，记录误判就绪、需求漏项、规划冗余、上下文成本和执行错误。静态链接检查或脚本通过不能代替模型实测。
