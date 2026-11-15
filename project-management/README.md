# Project Management — 独立子系统入口

**职责**：持久化管理一个跨多轮对话、可能跨 Session 的长期 Project。它不负责所有用户对话的 Task 识别和通用执行方法；那些属于 [Agent Execution Harness](../harness/README.md)。

## Project 的定义

Project 是围绕长期意图与成果维护的**持久化工作单元**；不是每轮对话、每个临时 Task，也不是全部聊天记录的副本。

## 按需路由（只读匹配项）

| 用户意图 | 加载协议 | 进一步按需加载 |
| --- | --- | --- |
| 创建一个新 Project | [protocols/create.md](protocols/create.md) | 字段规范、模板、Few-shot；模糊时 Grill-me |
| 修改既有 Project、记录决策、更新进度 | [protocols/maintain.md](protocols/maintain.md) | 实例现状 + 涉及字段的维护规范 |
| 继续/恢复 Project | [protocols/resume.md](protocols/resume.md) | 实例摘要 → 必要的决策、证据与日志 |

## 数据入口

- [Project 字段契约](schema/project.md)：定义、提取、更新条件、限制。
- [Project 实例模板](templates/project.yaml)：生成实例时使用。
- [创建与变更 Few-shot](examples/intent.md)：仅需判断意图提取或重大变更时读取。
- `projects/<project-id>/project.yaml`：真实项目的最小持久化状态（V0 约定）；可以按需创建决策/日志文件，**不预加载全部历史**。

## 必守边界

1. **先展示草案并得到用户明确确认，再持久化创建 Project。**
2. 模糊需求使用 [Grill-me](../harness/protocols/clarify.md)；不是每个新需求都要长访谈。
3. 不擅自改写核心意图、范围或重要约束；提出重大变更时先让用户确认。
4. 项目事实必须有可回查依据；未核实的信息不能被写成已完成。
5. Project 只保存必要的当前状态和引用；详细历史与证据在引用文件中，按需读取。

**V0 限制**：这些是规范与模板，并非强制执行的状态机引擎；跨进程并发写入、事务性更新及自动恢复尚未实现。
