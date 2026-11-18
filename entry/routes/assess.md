# 二级索引：判断既有产物

核心问题：**要寻找缺陷，还是证明某项交付声明成立？**

| 当前情况 | 读取/执行 |
|---|---|
| 检查代码/方案的缺陷、遗漏、误解或质量 | [review](../../evidence/methods/review.md) |
| 判断是否已创建、完成、修复、测试通过 | [verify](../../evidence/methods/verify.md) |
| 评估开发需求测试是否充分、能否交付 | [测试验收](../../evidence/testing/acceptance.md)与 verify 对照关键条件、候选版本和运行证据 |
| 为一个具体审查点查版本/源码事实 | 按需 [research](../../evidence/methods/research.md) |
| 审查对象/基线/标准实质不明且无法自行确认 | [clarify](../../evidence/methods/clarify.md)；缺规格时不假造需求符合结论 |

默认只读。已有有效检查不机械重跑；需要针对风险验证时遵守环境与副作用边界。发现问题返回证据，不自动修复或合并；用户授权修复才进入change。

例：“测试都过了，能交付吗？”用verify对照承诺；若要主动找遗漏/并发问题，再用review。多个独立审查轴值得拆分时按需orchestrate。
