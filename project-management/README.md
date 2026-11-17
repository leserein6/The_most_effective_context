# Project Management

职责：保存独立目标的长期事实、进度、决策、知识和操作记录。与全局任务执行机制独立。

## 导航

- `Index.md`：仅活跃项目；包含 ID、类型、名称、一句话目标，首要检查入口。
- `History.md`：归档/已完成项目，用户明确提及或活跃索引无匹配时按需检查。
- `projects/<status>/<type>/<id>/`：权威项目数据。
- `conventions/README.md`：用户确认后的跨项目积累。

## 状态与类型

| 状态 | 含义 |
|---|---|
| active | 当前推进 |
| archived | 暂时不推进，目标未完成 |
| completed | 目标已经达成 |

每种状态均有 development（开发型）、learning（学习型）、one_off（一次性任务）。one_off 是短、可在单会话内完成的一次性目标，同一会话内可多轮；需要跨会话延续的目标归 development 或 learning，即使它有明确终点。一个独立目标对应一个 Project，Task 不独立长期落盘。
状态改变需用户确认；恢复归档或重新开启已完成项目也属于状态改变。创建默认为 active。

## 操作入口

| 操作 | 读取的协议 |
|---|---|
| 检查归属 | [Routing](protocols/routing.md) |
| 新建与确认 | [Create](protocols/create.md)，再按需读取 Schema |
| 接续与上下文恢复 | `protocols/resume.md` |
| 每轮保存 | `protocols/maintain.md` |
| 归档/完成/恢复 | `protocols/lifecycle.md` |
| 日志压缩 | `protocols/logging.md` |
| 公共积累 | `protocols/knowledge.md` |
| 冲突/中断 | `protocols/recovery.md` |

元数据在 project.md 的首个 JSON 代码块中，正文仍可直接阅读。Index/History 是派生视图，禁止手工维护，调用脚本刷新。

字段职责与旧版本映射见 [Schema](schema/project.md)。长期问题、范围、交付与硬约束放 definition.md；验收标准放 acceptance.md。
