# Evidence：给 AI 的工作方法库

核心问题：**选定当前工作后，AI 应用什么思想方法、怎样具体执行并检验结果？**

Task 路由由根 [agent.md](../agent.md) 负责，场景分支在 `entry/routes/`。本目录不再承载路由器；不要为选择方法先读完整个库。

| 目录 | 内容 | 读取时机 |
|---|---|---|
| [methods/](methods/) | 十份方法正文：clarify、research、design、plan、execute、debug、review、verify、orchestrate、learn | 二级路由选中当前方法时 |
| [prompts/](prompts/README.md) | 可填写的委派、实现、审查等输入/回传模板 | 当前方法要求某份模板时 |
| [references/](references/) | 工程检查点、协作约束、证据契约与来源记录 | 方法指向具体参考，或核对来源时 |
| [evals/](evals/README.md) | 场景输入、观察标准与效果评价说明 | 专门评估协议行为时 |

方法正文给出核心问题、思想工具、具体动作、示范和停止条件；模板组织执行输入，参考材料补充约束，验收材料用于观察效果。目录更整齐不等于目标模型效果已经通过测试。
