# 测试计划和证据追踪契约（不创建持久化 Task 实体）

**设计原则：** 真正的业务规格、测试代码、夹具和 CI 保留在被开发业务仓库。Harness 的 Project 仅保存验收依据与跨会话可恢复的证据索引，不复制整个业务代码仓库、不创建 Task 数据库。

## 建议的受影响需求映射

对每项 Claim（可以是一条需求或风险控制）记录：

| 字段 | 作用 |
|---|---|
| claim_id / source_ref / spec_version | 需求来源与稳定 ID，不可从生成代码猜出 |
| precondition / stimulus / expected / invariant | 可证伪的行为命题 |
| oracle_ref / oracle_independence | 预期来源及与实现的独立性 |
| impact / uncertainty / change_surface | 风险与错误机理 |
| methods / why_selected / not_selected | 方法选择和排除理由 |
| model_ref / coverage_items / denominator | 测试模型、枚举覆盖义务和分母 |
| case_refs / layer / fixture / environment | 可执行测试或手工/静态检查 |
| counterexample / valid_alternative | 错误实现能否检出、合法实现能否通过 |
| design_review / run_evidence / decision | 设计充分性、执行结果、交付结论 |
| residual_risk / regression_trigger | 未解决项与复用失效条件 |

单个简单变更可以在开发计划里记录上述最小信息，复杂变更将版本化测试计划与报告放在业务仓库；不要求固定文件名。Harness 的 test_gate.py 仍接受旧版 testing/v1 的 criteria 列表用于**运行映射**。这些附加字段**当前没有被运行器自动验证**，不得因文档出现而宣称程序已经强制质量门禁。

## 双向追踪检查

- 前向：每条受影响需求/风险 → 方法/用例 → 结果/版本 → 验收结论；
- 反向：每个新增高成本用例 → 对应风险/义务；无必要性说明的多余用例可移除；
- 缺需求判据：先处理规格，不能由测试自动补造；
- 有需求无测试：记录可接受的静态/形式/人工检查，或者标 UNVERIFIED；
- 有执行通过但方法不足：EXECUTION PASS、DESIGN UNVERIFIED、ASSURANCE UNVERIFIED；
- 变更影响：候选、oracle、模型、测试、依赖、环境改变时重新判断哪些证据失效。

## 安装、恢复与审计

安装包应包含 evidence/testing/ 方法文档、scripts/test_gate.py 和可选 scripts/testing_strategy.py；**不要把仓库维护者的 tests/ 和 evidence/evals/ 放入用户安装包**。Harness 维护回归保留在开发仓库，由 CI 运行。

Project checkpoint 的 evidence 写入候选 SHA/工作树快照、计划与模型版本、设计审查结果、实际 run-id 和持久报告链接。日志记录动作与重要异常；恢复时按影响分析定位所需结果，不加载全部历史测试。
