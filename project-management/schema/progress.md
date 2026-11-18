# Project Progress · 进度维护契约

| 位置 | 提取依据 | 不能怎样更新 |
|---|---|---|
| status | 用户已确认的活跃/归档/完成决定 | 不因长时间无操作自动归档，不因单轮完成自动 completed |
| state.md 进度 | 已实际产生的产物、检查及剩余工作 | 不能把讨论或未验证实现写成验证完成 |
| state.md 下一步 | 用户优先级、依赖或 Agent 建议 | 建议要明确标为建议，不能冒称用户决定 |
| state.md 未解决问题 | 项目级阻塞、待确认项与未验证部分 | 不把猜测写成确定故障 |
| work-items.md | 结构化工作项状态、依赖、验收和完成证据（可选） | 不把本轮 Turn Task 完成等同 WI 完成，也不在每轮覆盖整个工作项列表 |
| decisions.md | proposed / confirmed / superseded，带真实依据 | 不覆盖旧决定的来由；冲突先指出 |
| logs/current.md evidence | observed / cited / inferred / unverified，带出处 | 不编造命令输出或把引用当作验证 |
| updated_at / revision | 脚本成功写入时生成 | 不凭空预填未来时间 |

每轮结束前由主 Agent 调用 checkpoint 一次保存；Subagent 返回结果，不写共享状态。与其他会话冲突时读取最新版本、比较并合并，不只换 token 强行写。状态变更独立调用 status 并具备用户确认。

快照与实际证据不符时说明限制，回查现状后修正。当前数据契约见 [Schema](project.md)，实际步骤见 [Maintain](../protocols/maintain.md)。
