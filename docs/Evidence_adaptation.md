# Evidence 方法论增强

本轮目标：将泛化原则改成适合需要明确步骤的执行模型直接使用的场景 Prompt。当前范围是 evidence 的方法、配套 Prompt、角色入口与行为验收材料，没有修改 Project 管理运行时。

## 变化

- 每个方法明确触发、必需输入、操作顺序、判断分支、输出、退出条件。
- Clarify 采用决策依赖与批量问题，区分自行调查的事实、用户决定和普通实现细节。
- Plan/Execute 明确文件、接口、验收与失败处理；Review 分需求/质量两轴；Verify 按声明绑定版本证据。
- Orchestrate 明确依赖、文件所有权、子 Agent 状态、补证据/修复/整体验收与失败停止条件。
- 六个可填 Prompt 与两个 CodeBuddy 角色定义衔接，避免只有目录没有使用入口。
- 按需提供后端风险检查，以及16项行为验收输入；不要求每轮加载全部材料。

## 来源与自定义边界

方法改写来源/采用与舍弃机制见 [SOURCES](../evidence/references/sources.md)，历史读取版本记录在 sources.json。外部原文资源库及固定 commit/许可另见 [Prompt 库](../evidence/prompts/README.md)，不再只有来源清单。已重新读取 Matt Pocock、Superpowers、Anthropic 和 Awesome Copilot 的具体文件，未将泛化研究列表作为完成依据。

模型适配基于用户实际反馈，不是关于 DeepSeek 性能的公开测试结论。协议不要求私有思维链；要求的是可观察事实、选择、操作与证据。Learn 和后端清单含明确的用户场景适配，不伪装成第三方已验证方案。

## 验证边界

已检查 Markdown 链接、来源 ID 与16项场景材料结构；独立审阅走查了已知CSV格式、RPC超时结果未知、子任务接口依赖、缺规格审查四个场景，未发现阻塞性流程问题。审阅提示的辅助方法→checkpoint mode映射已补齐，引用文件生成后已复查链接。目标 DeepSeek 模型下的行为、遵守率、质量变化与 Token 开销仍待独立对照测试；不能用项目文件管理检查代替。

本轮更新的是GitHub PR分支。用户Mac上的 `/Users/wangyingxin/workspace/github_projects/The_most_effective_context` 需同步对应分支后才包含变更，当前会话没有直接写入该Mac路径。
