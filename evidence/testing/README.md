# 开发型需求的测试工程

从每条业务承诺开始，追踪到能够揭露错误的场景、实际运行和交付结论。主 Agent 负责汇总，业务仓库拥有规格、测试及环境，Project 保存跨会话需要的索引与结果。

| 当前决定 | 入口 | 得到什么 |
|---|---|---|
| 怎样测这个变更 | [需求与测试设计](design.md) | 判据来源、风险、触发条件、观察位置及选用的检查 |
| 怎样取得可信的运行结果 | [执行与证据](execution.md) | 候选版本、计划快照、原始报告、执行日志、逐条件判定 |
| 能否交付，漏测后怎么办 | [验收与回归](acceptance.md) | 失败或未验证的影响、Project 记录、下一次回归入口 |

普通改动已有可靠测试时，直接引用既有检查。涉及用户数据、接口兼容、可恢复性等实质风险时，先固定关键判据，再改实现。按目标选择本地、PR、发布候选或实际平台验证；每个环境的结论只覆盖实际观察的条件。功能之外的性能、权限、隐私和无障碍承诺采用同一追溯方式，环境、阈值及来源随需求记录。

## 谁保存什么

- Project 的 `acceptance.md` 保存长期承诺与规格来源，按已有 edit 协议更新。单次开发工作只记与本次相关的项目产物。
- 业务仓库维护可执行用例、夹具和真实测试命令。复杂需求可把验收计划纳入业务仓库版本控制，已有测试平台也可以提供等价映射。
- 运行证据保存在有保留期保障的 CI 产物，或 Project 的 `work/testing/<run-id>/` 下。Project 状态及详细流水由主 Agent 按 [每轮保存](../../project-management/protocols/maintain.md) 写入。
- 方法和程序随 Harness 安装。维护者使用开发版的书单 CLI 回归与模型场景另行检验 Harness。

## 方法依据

从需求建立验证路径借鉴 [NASA 手册附录 D](https://www.nasa.gov/reference/system-engineering-handbook-appendix/)，判据来源见 [Barr 等的测试判据综述](https://discovery.ucl.ac.uk/id/eprint/1471263/)。用错误变体检验用例判别力借鉴 [DeMillo 等的变异测试研究](https://gse.ufsc.br/bezerra/disciplinas/Confiabilidade/docs/demillo-mutants.pdf)。AI 补丁通过既有用例仍可能有错的实证见 [UTBoost，ACL 2025](https://aclanthology.org/2025.acl-long.189/)。仓库的流程和运行器是基于这些研究作出的工程设计。
