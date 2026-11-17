# Evidence · 执行方法与模式路由

沿用原仓库术语：Evidence 指按需加载的执行方法，不是项目证明材料仓库。Mode 决定当前怎样工作；证据验证是所有模式共同的要求。先读 [通用流程](workflow.md)，不一次遍历整个目录。

| 当前目标 | Mode / 路由 | 输出 |
|---|---|---|
| 解决影响执行的歧义 | [clarify](clarify/README.md) | 明确目标和关键选择 |
| 核实事实、来源、技术机制 | [research](research/README.md) | 有定位依据的结论 |
| 分步计划、依赖、验收 | [plan](plan/README.md)；具体架构取舍按需读 [design](design/README.md) | 可执行方案 |
| 真实修改与实施 | [execute](execute/README.md) | 实际产物和检查 |
| 独立审查既有方案/产物 | [review](review/README.md) | 具体触发场景、问题和证据 |
| 接续学习 | [learn](learn/README.md) | 合适单元、学习进度与疑问 |
| 多 Agent 拆分协作 | [orchestrate](orchestrate/README.md) | 委派、协调、验收汇总 |

主 Agent 自动选择并简短说明，用户指定优先，阶段变化可切换。

共用方法：异常时按需读 [debug](debug/README.md)；完成声明前读 [verify](verify/README.md) 与 [证据分类](protocols/validation.md)。Debug/Verify 是横跨模式的方法，不再额外造 Project 类型。

普通低复杂任务可以只读当前所需短协议；无论是否需要专项方法，仍遵守 agent.md 中 Index 锚定与每轮保存规则。项目生命周期由 [Project Management](../project-management/README.md) 独立负责。
