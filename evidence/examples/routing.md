# Evidence Routing · Few-shot 边界案例

此文件仅在路由有歧义时打开；**例子不是当前用户的真实需求**。

| 用户话语 | 首要 Evidence | 下一阶段可选 | 不该做什么 |
| --- | --- | --- | --- |
| 「核查这个 Go 库的行为，给源码」 | Research | 无 | 不直接动用户仓库 |
| 「帮我设计项目的架构」 | Design | 关键歧义→Clarify | 不先写生产代码 |
| 「做个 AI 软件，我也不确定做什么」 | Clarify | Design | 不凭空决定全部需求 |
| 「按现有设计提交代码」 | Execute | Verify | 不重复 Grill-me 所有已确认需求 |
| 「我的测试挂了，修一下」 | Debug | Execute → Verify | 未定位故障前不猜式修复 |
| 「检查仓库是否已经可以交付」 | Verify | 必要时 Debug | 不只看仓库存在就说可交付 |
| 「创建一个长期 Project」 | Project Create | 关键不明→Clarify | 不把 Task 误当 Project |
| 「就聊聊项目方向」 | 可能不需专门 Evidence | 若请求方案→Design | 不自动创建 Project |

**主规则**：Evidence 是任务执行方法，不是标签集合。只有当前阶段真的需要时才读第二份文件。
