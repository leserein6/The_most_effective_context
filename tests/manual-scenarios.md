# V0 手工验收场景

> 用能展示文件读取记录的真实 Agent/CLI 运行；仓库本身没有运行时加载器或自动化测试。记录实际读取路径与用户可见行为。

| 场景 | 输入 | 预期加载（示例） | 成功判定 |
| --- | --- | --- | --- |
| A 技术查证 | 「核实某框架的超时传播机制，给出处」 | `agent.md` → `harness/README.md` → `research.md` | 本轮 Task 可见；有来源；无关协议未读 |
| B 模糊创建 | 「我想做个 AI 工具，帮我建 Project」 | `agent.md` → Project README → `create.md` → 必要时 `clarify.md` | 优先澄清；草案未经确认**不落盘** |
| C 确认创建 | 「以上草案确认，创建吧」 | Project README → `create.md` → Schema/Template | 创建真实实例；字段忠实、路径有效 |
| D 普通维护 | 「把已经验证的功能写进项目进度」 | Project README → `maintain.md` → 项目当前状态 | 只更新证据支持的字段，不修改长期意图 |
| E 跨 Session 恢复 | 「继续 Project X」 | Project README → `resume.md` → 当前实例 → 必要引用 | 不读完整历史也能说明可靠状态与下一步 |

## 应记录的观察

- 实际读取了哪些协议文件？是否遗漏必需协议或读取无关协议？
- Task 是否在用户可见回复中明确？
- 是否在需要 Grill-me 时提问，在不需要时停止追问？
- Project 创建/重大变更是否经过明确确认？
- 文件写入和恢复是否用实际证据验证？

不应因为 README 或示例写得完整，就声称 Agent 已自动遵循协议；必须有运行记录。
