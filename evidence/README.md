# Evidence：给 AI 的工作方法库

核心问题：**选定当前工作后，AI 应用什么思想方法、怎样具体执行并检验结果？**

Task 路由由根 [agent.md](../agent.md) 负责，场景分支在 `entry/routes/`。本目录不再承载路由器；不要为选择方法先读完整个库。

| 目录 | 内容 | 读取时机 |
|---|---|---|
| [testing/](testing/README.md) | 开发型需求的测试设计、执行、验收与回归 | 开发和评估路由按当前阶段读取 |
| [methods/](methods/) | 十份方法正文：clarify、research、design、plan、execute、debug、review、verify、orchestrate、learn | 二级路由选中当前方法时 |
| [prompts/](prompts/README.md) | 可选外部 Skill/Prompt 原文库，以及共用委派/计划输入格式 | 主 Agent 派发时按职责选择一份；编写协议时选 author |
| [references/](references/) | 工程检查点、证据契约与方法来源记录 | 方法指向具体参考，或核对来源时 |
| `evals/`（开发版） | 场景输入、观察标准与效果评价说明 | 专门评估协议行为时 |

方法正文给出核心问题、思想工具、动作、示范和停止条件；共用委派包填写本次参数；外部原文是可选择参考，不是另一套自动生效的协议。Project 数据维护仅由 project-management/protocols/ 负责。目录整齐、原文收录与哈希通过都不等于目标模型效果已验证。
