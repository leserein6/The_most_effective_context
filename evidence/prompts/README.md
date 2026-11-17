# 场景 Prompt 索引

对应 README 是方法主体，这里的文件是可填写的执行输入/回传模板。按职责读一份；发给 Agent 前全部替换占位符。未知必须明确标 UNKNOWN，并依必需程度查证或询问，不能用空白暗示不存在。

| 时机 | 模板 |
|---|---|
| 拆分并派发研究/实现等子任务 | [delegation](delegation.md) |
| 实现一个已经明确的工作项 | [implementer](implementer.md) |
| 独立审查产物 | [review](review.md) |
| 多步骤方案交给执行者 | [plan](plan.md) |
| 查事实/源码的工作包 | [research](research.md) |
| 日志压缩与下一会话恢复 | [compression](compression.md) |

公共 Prompt 更新需用户确认；本轮用户已经明确要求完善这些文件。后续任务产生的临时 Prompt 放项目 work 内，提炼为公共候选后再确认纳入。来源和改写说明见 [SOURCES](../SOURCES.md)。
