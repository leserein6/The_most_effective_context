# Project Create

先读活跃 [Index](../Index.md)，依 [归属协议](routing.md) 判断接续或新建；信息不足必须询问。

1. 从用户输入提炼名称、development/learning/one_off、一句话目标；类型按是否需跨会话延续选择：能在单会话内完成、无需跨会话的短目标选 one_off（同一会话内可多轮）；可能无法在一次会话内完成、需要跨会话延续的选 development 或 learning，即使它有明确终点。一个独立目标对应一个 Project。
2. 关键歧义才澄清，用户希望一次问完时集中列出；普通实现细节自行判断。按需读 [定义维护契约](../schema/definition.md)。
3. 展示具体草案，用户确认后才 create --confirmed。已明确给出全部字段并要求创建，不重复确认。
4. 脚本保存 Markdown 实例到 `project-management/projects/active/<type>/<id>/`，同时更新 Index。元数据结构见 [Schema](../schema/project.md)。
5. 先明确 definition.md 中的问题、结果、边界、交付、硬约束，以及 acceptance.md 的验收条件；未知可保留待定，不编造。
6. 实际检查创建结果；失败不得声称成功。本轮之后仍遵循 [每轮保存](maintain.md)。

没有自动导入旧 `projects/<id>/project.yaml`。旧实例若存在，按 [迁移说明](../../docs/Migration.md) 显式处理，不重建覆盖。
