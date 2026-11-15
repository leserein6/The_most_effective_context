# Project Progress · 状态字段维护契约

**适用**：已有项目的进度刷新、恢复、阻塞、证据与资源引用。长期意图的修改见 [definition.md](definition.md)。

| 字段 | Definition（是什么） | Extraction（根据什么判断） | Update（何时更新）与 Constraints（禁忌） |
| --- | --- | --- | --- |
| `state.phase` | 生命周期阶段 `active/paused/completed/archived` | 用户指令 + 真实交付状态 | 未验收不能仅凭 Agent 宣称标 `completed`；停滞不自动算 paused |
| `state.summary` | 简洁、可信的目前情况 | 最近可确认的产物/决策与未完成点 | 只记录已知事实，保留限制；不复述完整会话 |
| `state.verified_outputs` | 已核实成果及其证明 | 文件存在检查、测试结果、提交/工具返回及必要人工核验 | 每项带 `description` 和 `evidence`；无证据的不列为 verified |
| `state.next_action` | 恢复时最合适的下一步，含来源性质 | 当前阻塞、用户优先级和依赖 | `status` 为 `confirmed/proposed`；AI 建议不能标 `confirmed` |
| `state.blockers` | 阻止下一步的真实依赖/问题 | 工具失败、资源缺失、待确认关键事项 | 已消除的阻塞及时更新；不可把猜测障碍写为确定事实 |
| `state.updated_at` | 当前快照最后实际维护时间 | 成功写入时可靠获得的 ISO 8601 时间 | 不能凭空编造时间；取不到就保持 `null` |
| `references.decisions` | 可检索的重大决策文档位置 | 已存在的项目内决策文件 | 路径必须可解析；记录重大决策须保留来由 |
| `references.journal` | 详细工作过程的可选日志位置 | 已存在的 Project 日志 | 当前 Demo 不强制每轮记录原始聊天；不因 Task 临时而保存 Task 实体 |
| `references.evidence` | 其他证据与资料的定位信息 | 实际文件/链接/提交编号 | 引用不等于内容真实性；必要时重新核实 |

## 维护分类

- **已验证进展** → 更新 `summary`、`verified_outputs`、`next_action`，保留依据。
- **已确认的新决策** → 更新相关字段并记录决策出处；重大定义变化应先经过用户确认。
- **仅讨论或 AI 建议** → 不当成已落实结果；下一步可标为 `proposed`，或暂不写。
- **执行失败/中断** → 写真实阻塞与部分结果，不伪造全部成功。

对更新判断有歧义时读取 [Few-shot：progress](../examples/progress.md)；普通状态读取不必加载示例。

注意：跨 Session 恢复首先依赖当前快照，但若快照显示“已完成”而实际文件已不存在，应以核验结果修正判断，而不是盲信摘要。
