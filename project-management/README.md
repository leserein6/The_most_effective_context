# Project Management · 长期项目专用路由

仅在涉及**经过确认或准备创建的长期 Project** 时加载。本系统不定义单轮 Task 的执行方法；Task 执行的专项方法统一由 [Evidence](../evidence/README.md) 提供。

| 操作 | 加载 | 按需资源 |
| --- | --- | --- |
| 创建长期项目 | [Create](protocols/create.md) | 核心字段定义、实例模板、必要时 Clarify |
| 修改项目定义/状态 | [Maintain](protocols/maintain.md) | 当前实例、受影响字段规范、必要时 Few-shot |
| 恢复已有项目 | [Resume](protocols/resume.md) | 当前快照 → 必要决策和证明材料 |

## 单一事实源

- [Schema 总索引](schema/project.md)
- [项目定义字段](schema/definition.md)
- [项目进度字段](schema/progress.md)
- [Project 实例模板](templates/project.yaml)
- [意图与变更示例](examples/intent.md)
- [进度更新示例](examples/progress.md)

正式实例约定为 `projects/<id>/project.yaml`，文件不存在不能声称已创建。正式创建之前，应先让用户看到具体草案并**明确确认**；修改核心方向和关键约束同样需要确认。

不要因进入 Project Management 就加载所有项目 Schema、Few-shot 和操作历史，也不要每轮自动创建 Task 记录。
