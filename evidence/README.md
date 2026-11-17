# 一级索引：按 Task 交付选择方法组

核心问题：**本轮用户要得到哪类结果，应进入哪个方法组？**

Task 是本轮预期结果；下表类型是临时路由标签，不是 Project 类型，也不是脚本 mode。不把每次阅读资料都另建一个调查 Task。

| 预期交付 | Task 类型 | 只读取这个二级索引 |
|---|---|---|
| 获得解释、事实、机制或调查结论 | 了解 answer | [answer](routes/answer.md) |
| 获得需求、设计、选型或实施计划 | 方案 proposal | [proposal](routes/proposal.md) |
| 获得实际代码、文件、配置或系统改动 | 修改 change | [change](routes/change.md) |
| 获得对既有产物的审查、合格性或完成判断 | 评估 assess | [assess](routes/assess.md) |
| 用户掌握知识、练习能力或继续课程 | 学习 learn | [learn](routes/learn.md) |

同一 Task 可经历多个方法；类型由主要交付决定，不随每个工具动作改变。不能判断时先简短重述结果，只有实质歧义才询问。

仅加载选中组及当前方法。例：“修复分页”属于 change，即使先读源码，也不换成 answer；“仅解释分页实现”属于 answer。用户转为只讨论方案时再改交付类型。

clarify 处理关键用户决定，research 处理事实缺口；verify 是完成检查，orchestrate 是协作方式，均可跨组使用。二级索引会给具体触发和路径，不需要再看十项平铺菜单。

Mode 仍是既有 clarify/research/plan/execute/review/learn/orchestrate；design→plan、debug→execute，verify沿用当前主模式，独立验收用review。Task 类型不写进 mode 字段。

操作参考：[workflow](workflow.md)；歧义示例：[routing](examples/routing.md)。项目状态按 [Project Management](../project-management/README.md) 管理；Prompt/参考材料仅在所选方法指向时读取，来源与eval不默认加载。
