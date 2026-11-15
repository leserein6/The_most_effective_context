# Project Management · 操作路由

**仅在用户涉及长期 Project 时加载。** 本目录负责项目的持久化身份、意图、状态和恢复；不负责单轮 Task 锚定和通用任务执行方法（见 [Task Harness](../harness/README.md)）。

## 何为 Project

一个经用户确认、需要在多轮乃至多个 Session 持续推进的工作对象。它不是临时任务清单，也不是聊天归档。

## 一次只选当前操作的协议

| 当前意图 | 首先读取 | 随后按需读取 |
| --- | --- | --- |
| 新建长期 Project | [Create](protocols/create.md) | 定义字段、模板；有歧义时调用 Grill-me |
| 修改已有项目的意图、范围、决策或进度 | [Maintain](protocols/maintain.md) | 项目快照 + 受影响字段契约 |
| 恢复/继续已有项目 | [Resume](protocols/resume.md) | 项目快照 → 当前步骤所需证据 |

## 数据与维护规范的层次

- [Schema 索引](schema/project.md)：数据形状、不变量、字段规范路由。
- [Definition 字段契约](schema/definition.md)：项目身份、问题、期望成果、范围、验收与约束。
- [Progress 字段契约](schema/progress.md)：阶段、进度、证据、接续、引用。
- [实例模板](templates/project.yaml)：只有创建/迁移文件时才读取。
- [Few-shot：意图与变更](examples/intent.md)、[Few-shot：进度维护](examples/progress.md)：遇到提取或变更判断歧义时才读取，不每轮加载。
- 实际实例约定存放于仓库根 `projects/<id>/project.yaml`。**实例不存在不能冒充已创建。**

## 全局不变量

1. **创建前确认**：需求可不完美，但用户必须看过具体草案并明确确认后才能写入正式实例。
2. **重大变更前确认**：改变项目核心问题、期望成果、关键范围或硬约束，必须展示变更及影响。
3. **证据约束**：事实性进度只能来自可检查产物或可靠来源。提议不是已完成。
4. **最小加载**：进入本目录不意味着读全 Schema、所有例子或所有历史。
5. **容错**：文件缺失、权限不足、状态冲突时说明原因，不补写虚构项目数据。

> **V0 是协议约定**：没有内置事务/锁、后台守护或自动日志压缩。具体读写由宿主 Agent 工具完成。
