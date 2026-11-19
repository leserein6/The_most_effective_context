# Project Create

仅在已按 [归属协议](routing.md) 确定新建后读取本文件；不重新启动一轮相同归属询问。

1. 从用户输入提炼名称、development/learning/one_off、一句话目标；类型按任务规模与是否一次性选择：轻量、几轮交互即可完成的一次性目标选 one_off；需要持续迭代、分阶段推进或长期演进的选 development 或 learning，即使它有明确终点。跨会话不是判据。一个独立目标对应一个 Project。
2. 关键歧义才澄清，用户希望一次问完时集中列出；普通实现细节自行判断。按需读 [定义维护契约](../schema/definition.md)。
3. 展示具体草案，用户确认后才 create --confirmed。已明确给出全部字段并要求创建，不重复确认。`--confirmed` 仅表示调用者已有真实会话依据，脚本不能识别用户意图。
4. 脚本保存 Markdown 实例到 `project-management/projects/active/<type>/<id>/`，同时更新 Index。元数据结构见 [Schema](../schema/project.md)。
5. 先明确 definition.md 中的问题、结果、边界、交付、硬约束，以及 acceptance.md 的验收条件；未知可保留待定，不编造。
6. 实际检查创建结果；失败不得声称成功。本轮之后仍遵循 [每轮保存](maintain.md)。

不会自动导入旧 `projects/<id>/project.yaml`。发现旧实例时停止自动迁移并保留原始数据；需从 Harness 源码仓库查看 `docs/Migration.md`，制定显式迁移方案，不重建覆盖。该维护文档不随运行包安装。
