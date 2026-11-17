# 二级索引：获得解释或调查结论

核心问题：**答案缺的是用户意图，还是可查证事实？**

| 当前情况 | 读取/执行 |
|---|---|
| 不清楚对象、范围或用户真正要问什么，且上下文无法消除 | [clarify](../../evidence/methods/clarify.md) |
| 需要版本、源码机制、当前状态或外部依据 | [research](../../evidence/methods/research.md) |
| 关键事实已在当前有效上下文，问题可直接回答 | 直接回答；不强制新一轮全仓研究 |
| 只是问故障原因，无修复授权 | research；需复现和因果定位再读 [debug](../../evidence/methods/debug.md)，不因此修改业务逻辑 |

取得足够依据即回答。发出可核实成功声明时按需读 [verify](../../evidence/methods/verify.md)；多个独立调查值得分工时读 [orchestrate](../../evidence/methods/orchestrate.md)，不扩大原调查范围。

例：“这个函数为什么返回空？”先定位实际分支与输入；不能直接改函数。用户明确要求修复后才转 change。
