# V0.2 → V1 整合说明

本次在原仓库上迭代，没有把独立压缩包放进仓库充当源码，也没有建立第二套并行生效的 Harness。

## 保留

- agent.md 规范入口；Evidence 与 Project Management 分离。
- evidence 的研究、澄清、设计、执行、调试、验证方法的职责；补充七模式路由与通用协作。
- 原外部研究记录和意图/进度示例，明确标注其历史数据表示。
- 先读路由、按需读协议/Schema/Few-shot 的加载原则。

## 本轮确认覆盖的旧规则

| 旧 V0.2 | V1 |
|---|---|
| 只有长期项目操作才进入项目管理 | 每轮先检查活跃 Index，归属不足就问，不猜测 |
| 仅长期目标是 Project | 一次性任务也属于 Project，可在单会话内多轮完成；需要跨会话延续的目标归 development/learning |
| active/paused/completed/archived | active/archived/completed；归档=未完成但暂不推进 |
| projects/ID/project.yaml | project-management/projects/状态/类型/ID/，Markdown 多文件 |
| 普通讨论不要求每轮写入 | 每轮回复前记录有意义流水和真实状态，提议仍保持提议 |
| 澄清强制一次一个问题 | 根据用户偏好可集中问完关键问题 |
| 并发、压缩、编排仅协议设想 | 增加脚本可验证部分和需要 CLI 实测的行为协议 |

## 数据迁移边界

读取的远端基线没有真实 projects 实例，因此本次没有待迁移的用户数据，也没有创建虚构项目。旧 templates/project.yaml 明确标为历史参考，不被当前脚本加载。

如果用户本地已有 V0.2 YAML 实例：先备份和列清单，展示状态/类型映射与目标，获得确认后显式迁移，逐项核对定义、约束、进度、决策与引用；保留原文件。当前不提供未经验证的自动 YAML 导入。

## CLI 入口

agent.md 继续是规范执行入口；`CODEBUDDY.md` 通过 `@agent.md` 导入它，`AGENTS.md` 仅作兼容其他 CLI 的薄适配。不维护两套工作流。CodeBuddy 对两个入口同时存在时优先读取 CODEBUDDY.md；需在 CLI `/memory` 核验。

## 验证

历史维护验证在临时环境执行，原始用例和日志不随仓库发布；脚本测试不替代真实模型对话。旧研究记录不构成当前效果已验证的证据。
