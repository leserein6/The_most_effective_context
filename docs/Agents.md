# CodeBuddy CLI：常用专业 Sub-Agent

此页列出**日常使用角色**；它们是官方 `.codebuddy/agents/*.md` 子代理，不是新的 Project 类型、Task 类型或 Mode，也不是持久化任务。维护者测试代码不属于这些 Agent。

## 为什么需要它们

主 Agent 保持用户目标、交互、权限与 Project 记录；子 Agent 在独立上下文里做一项有边界的工作，返回源码证据与建议。不把整个 Go/C++ 大仓库的临时搜索记录灌入主会话。

| Agent | 触发场景 | 回传 | 与原角色的区别 |
|---|---|---|---|
| [source-tutor](../.codebuddy/agents/source-tutor.md) | 让我读某个 Go/C++ 函数、模块、RPC 调用链；继续源码学习 | 3–6 行全局路径、最小源码片段、必要前置、下一步 | 学习带读；主 Agent 维持对话节奏 |
| [bug-investigator](../.codebuddy/agents/bug-investigator.md) | panic、crash、编译/运行失败、日志、超时和并发异常 | 证据、候选根因、可区分的验证动作 | 诊断，不替 pm-worker 修复 |
| [change-impact](../.codebuddy/agents/change-impact.md) | 动老代码、迁移 RPC、接口、配置或存储前 | 调用方/下游、行为不变量、兼容/回归风险 | 改动前影响调查；pm-reviewer 负责改动后独立 CR |
| [test-planner](../.codebuddy/agents/test-planner.md) | 开发前明确验收、边界、异常、并发和测试策略 | Claim、Oracle、方法、层级及未验证项 | 制订验证策略；执行仍由主 Agent/业务测试工具完成 |

## 使用方式

CodeBuddy 官方支持 YAML frontmatter 的 Markdown 子代理；项目级目录为 `.codebuddy/agents/`，用户级为 `~/.codebuddy/agents/`。前者在**当前 CodeBuddy 工作目录对应的项目**中可用，不能因为这个 Harness 仓库存在就自动应用到所有其他源码仓库。

**只在此 Harness 工作区使用**：在该目录启动 CodeBuddy，输入 `/agents`，检查角色已被发现。可以明确说：

- “使用 source-tutor 带我读 `path/to/file.go` 的 `Function`，先讲整体再只讲第一个函数。”
- “使用 bug-investigator 调查这条 panic 和相关源码，只定位根因，不改代码。”
- “用 change-impact 梳理这个 C++ 接口改动涉及哪些调用方和错误处理。”
- “让 test-planner 为这次 RPC 兼容性改造设计关键验收和失败场景。”

**希望在所有 Go/C++ 仓库都可用（Mac）**：在本仓库根目录运行：

```bash
mkdir -p ~/.codebuddy/agents
cp .codebuddy/agents/{source-tutor,bug-investigator,change-impact,test-planner}.md ~/.codebuddy/agents/
```

这些用户级定义在所有 CodeBuddy 项目生效；将来仓库里的 Agent 更新时需要再次复制。也可以只选一个 `cp`。若目标仓库里有同名项目级 Agent，项目级定义优先。复制前请先检查你的用户级目录里是否已有同名文件，以免覆盖个人定制。使用 `/agents` 查看已生效的定义和工具权限。

**希望作为某个具体业务仓库的项目角色**：将所需 Markdown 放到该业务仓库的 `.codebuddy/agents/`，且仍应由该业务仓库管理和审核。

## 与现有 Harness 的关系

- `agent.md` 是主 Agent 的 Project/Task/Mode 总入口；主 Agent 在学习或开发任务中按需委派，不自动把用户当前互动交给子 Agent 取代。
- `source-tutor` 可以帮主 Agent 收集**真实源码证据**，但用户一轮只学一个最小知识点，主 Agent 继续与用户互动。
- 四个新角色默认只启用 `Read/Grep/Glob`，不提供 Edit 或 Bash，避免在调查/带读中意外写入。需要运行实验、修改或提交时另由主 Agent 在授权范围内执行。
- 子 Agent 不写 Project Index、日志或 checkpoint；主 Agent 负责整理必要结论并按原协议保存。
- 不强制任何模型版本，使用 `model: inherit`。CodeBuddy 是否正确识别与自动委派需在你安装的实际 CLI 中通过 `/agents` 验证；Markdown 存在不证明真实调度已成功。

官方参考：[CodeBuddy CLI Sub-Agents](https://www.codebuddy.ai/docs/cli/sub-agents)，[工具参考](https://www.codebuddy.ai/docs/cli/tools-reference)。
