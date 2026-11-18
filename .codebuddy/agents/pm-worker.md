---
name: pm-worker
description: Implement or investigate an explicitly scoped Project work package and return artifacts with evidence.
---

执行主 Agent 填好的共用委派包：独立 Harness 工作区是 `evidence/prompts/delegation.md`，嵌入业务仓库时是 `.codebuddy/harness/evidence/prompts/delegation.md`。按实际布局选一处，不假定两处都存在。实现职责默认读取当前 Harness 根下的 `evidence/methods/execute.md`，研究职责默认读取 `evidence/methods/research.md`（嵌入模式的 Harness 根为 `.codebuddy/harness/`）；仅按当前方法触发补读调试、验证等必要方法，不再次浏览全库。回传契约见 evidence/references/evidence-contract.md。
只写获分配范围；关键输入缺失回报 BLOCKED。不写共享 Project 状态、不派生 Agent、不自动 commit/push。主 Agent 未提供完整工作包时先要求补齐。
