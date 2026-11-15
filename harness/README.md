# AI Execution Harness — 路由入口

**职责**：决定“本轮 Task 属于哪种工作、应遵守什么执行方法”。Task 是一轮对话的工作锚点，**不落盘**；本模块不管理长期 Project 状态。

进入本目录时，先根据下面的路由表选择**一份主协议**，不要把所有协议同时读入 Context。

| Task 类型 | 典型触发 | 下一步加载 |
| --- | --- | --- |
| Research / 查证 | 求证事实、阅读来源、比较证据、调研 | [protocols/research.md](protocols/research.md) |
| Design / 设计 | 制定方案、架构设计、权衡选项 | [protocols/design.md](protocols/design.md) |
| Execute / 实施 | 修改文件、写代码、执行命令、交付产物 | [protocols/execute.md](protocols/execute.md) |
| Clarify / 澄清 | 需求含糊、关键决策缺失、Grill-me | [protocols/clarify.md](protocols/clarify.md) |

## 路由规则

1. 先判断本轮**主要预期结果**，不要只按关键词判断；这是 V0 可扩展分类，并不声称覆盖全部任务。
2. 单个 Task 若包括多步（例如先查证再设计），只加载执行**当前步骤**所需的协议；转到下一类工作时再加载。
3. 简单、无需专门方法的日常回复可以只遵守 [全局入口](../agent.md)，无需硬套四种分类。
4. 项目类操作在本系统之外：由 [Project Management](../project-management/README.md) 独立路由。一个项目类 Task 必要时仍可引用此处方法，如澄清。
5. 全局约束不在各协议重复定义；发现冲突时应暂停高风险动作并明确指出。

**输出要求**：用户能看见本轮 Task、关键结果与尚未完成之处；过程细节依据任务需要控制篇幅。
