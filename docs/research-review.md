# V0 外部研究与协议设计取舍

> 研究记录不是复制外部 Prompt。以下列明**参考来源 → 可借鉴机制 → 本仓库的选择/不采用项**；社区方案不能替代真实 Agent 验收。

## 参考来源（2026-11-15 查阅）

1. [Agent Skills 开放规范](https://github.com/agentskills/agentskills)：通过描述发现能力、激活时读主指令、必要时加载附属引用。**采用**三层渐进式加载的思想；**不宣称**本仓库的 `protocols/*.md` 已符合原生 `SKILL.md` 规范。
2. [Anthropic Skills：skill-creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) 与 [Skill 最佳实践](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)：强调描述的触发边界、短指令、外置参考与真实评估。**采用**清晰激活条件、具体例子、测试用例；**不采用**为了“兼容”而制造未实测的自动加载宣称。
3. [obra/superpowers](https://github.com/obra/superpowers)：brainstorming、writing-plans、verification-before-completion 等专门 Skill。**采用**澄清最影响决定的问题、先设计再实施、证据先于完成声明；**不采用**“所有任务必须走完整软件开发流程”的强制条件。
4. [GitHub Spec Kit](https://github.com/github/spec-kit/blob/main/docs/quickstart.md)：需求规格 → 澄清 → 计划 → 实施的分阶段衔接。**采用**区分用户意图、方案与实际产物；**不采用**它的完整命令/分支/规格文档体系（V0 没有这类基础设施）。
5. [GitHub Awesome Copilot](https://github.com/github/awesome-copilot) 与 [Agent Skills 文件指导](https://github.com/github/awesome-copilot/blob/main/instructions/agent-skills.instructions.md)：区分 Instructions、Prompts 与 Skills，并明确参考资源应按需加载。**采用**职责边界、指令可操作性；**不照搬** Copilot 专有的发现目录和触发机制。
6. [Claude Code Context 指导](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts)：不同平台可能有各自原生的配置文件和文件发现行为。**选择**保留用户指定的通用 `agent.md`，通过宿主适配层显式加载，而非宣称同名文件在任何 CLI 自动生效。

## 按文件审查的编辑准则

- 每份入口文件只回答：**我负责什么、何时读下一份、何时不要读**。
- 每份协议必须有：**激活条件、可执行步骤、完成/退出门槛、反例或重要限制**。
- Project Schema 单一事实来源：字段语义与数据形状放在 Schema，不在 create/maintain/resume 里重复描述。
- Few-shot 展示**输入 → 判断 → 正确行为**，并提供反例，避免从示例推断不存在的授权。
- 每次新增字段/规则，要补至少一个正例或反例测试；规则冲突和过度加载同样属于失败。
- 外部资料仅作为**可追溯的设计依据**，不得直接赋予仓库内容高于宿主指令的权限。

## 尚未验证的假设

- 明确 Task 锚点是否显著改善用户发现理解偏差的速度。
- 分层协议在不同模型/CLI 下是否能稳定被路由与按需读取。
- 与简短单文件协议相比，文件拆分的 Token、延迟与执行准确度净收益。
- Project 快照能否在中断、并行修改后保持可信且可恢复。

这些必须通过 [手工场景](../tests/manual-scenarios.md) 的实际记录判断，不能只看规范是否写得漂亮。
