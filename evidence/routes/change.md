# 二级索引：产生实际改动

核心问题：**目标清楚后，当前缺事实、方案、故障定位还是实施？**

| 当前情况 | 读取/执行 |
|---|---|
| 关键需求/授权/已确认约束存在分歧 | [clarify](../clarify/README.md) |
| 需要核实现有行为或依赖版本 | 仅为该缺口读 [research](../research/README.md) |
| 需要作关键设计取舍/安排复杂实施 | 分别按需读 [design](../design/README.md) / [plan](../plan/README.md) |
| 已有异常、失败测试或错误行为 | [debug](../debug/README.md)，定位后再实施 |
| 目标/边界清楚，可以实际修改 | [execute](../execute/README.md) |

值得独立委派且工具可用 → [orchestrate](../orchestrate/README.md)；具体任务仍执行对应方法，不是只有调度没有产物。
改动完成并准备声明成功 → [verify](../verify/README.md)；需要独立审查再读 [review](../review/README.md)。这些都按实际阶段补载，不一开始全部读取。

例：“给既有CSV增加注册时间列”若格式/权限已明，读相关实现后直接execute；不重新访谈整套产品。
