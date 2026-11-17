# 实现与验证边界

## 分工

| 能力 | 实现方式 | 可验证程度 |
|---|---|---|
| 识别 Project、语义冲突、自动选模式 | agent.md + 模式/协议 | 需要真实 CLI 对话验收 |
| 新建和状态变更确认 | 协议要求 + 脚本 --confirmed 门槛 | 脚本可拒绝无标志调用；无法证明对话授权真实 |
| Project 文件/索引更新 | pm.py | 自动测试 |
| 每轮写回 | Agent 必须调用 checkpoint | 数据写入可测；遵守率未在 CLI 验证 |
| 七模式 | Markdown 工作协议 | 不是独立执行引擎；CLI 实测 |
| Subagent | 官方格式配置 + 委派/验收契约 | 文件存在；实际调度未实测 |
| 证据正确性 | Agent 审查与实际命令 | 结构可验；真实性需具体任务验收 |
| 日志压缩 | Agent 生成摘要；脚本归档和校验 | 原文字节/哈希可测；摘要语义需复核 |
| 并发 | 本地 flock + shared-state token | 仅脚本调用；代码文件需分工/worktree |
| 恢复 | 写前日志与回滚 | 进程中断已测；不宣称断电数据库语义 |
| Git | 协议明确仅按要求提交/推送 | 本包不调用 Git 网络写入 |

## 环境限制

本环境没有 CodeBuddy 运行会话，未使用你的 Mac、模型账号或真实项目验证。Python 代码依赖 macOS/Linux 的 fcntl，不声称原生 Windows 可用；Windows 可考虑 WSL，另行验收。

共享状态 token 遍历目录并哈希 metadata/日志等管理内容，不哈希普通 work/source 产物；大型历史仍有扫描开销。源码仓库建议外置登记，状态文件保持简洁。

初版安装器不强行合并任意既有同名文件，冲突会停止；新目录解压运行是推荐路径。已有 Project 类型重分类尚无专用命令。

## 官方接口依据（核对日期：2026-11-17）

- [CodeBuddy Memory](https://www.codebuddy.ai/docs/cli/memory)：AGENTS.md 入口适配（转引本仓库 agent.md）。
- [CodeBuddy Sub-Agents](https://www.codebuddy.ai/docs/cli/sub-agents)：项目目录 agents Markdown 定义与 /agents 管理。

本包只使用这些基础入口，没有配置自动执行 Hook、未核实 API 或默认绕过权限。研究/规划等模式是我们设计的协议，不是官方内置命令。

## 独立审查

独立审查复现的执行权限丢失与回滚路径越界问题已修复并增加回归测试。实际测试结果见 Test_results.md。所有示例运行在临时目录，不冒充用户真实项目进度。
