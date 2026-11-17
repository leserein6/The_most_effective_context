# The Most Effective Context

让 Agent 在正确时机加载最小充分上下文，执行当前任务，并可靠接续长期项目。

本次在原 V0.2 协议仓库上补齐 **V1 文件型 workspace 与项目管理脚本**：保留 `agent.md` 入口、Evidence 执行体系、独立 `project-management`，覆盖项目生命周期、七种模式、Subagent 协作、每轮日志、压缩归档、并发检查与进程中断恢复。

## 总体边界

| 层次 | 职责 |
|---|---|
| [agent.md](agent.md) | 轻量总入口：锚定项目，进入执行与项目管理路由 |
| [Evidence](evidence/README.md) | 按需加载工作方法；模式是其中的可变部分 |
| [Project Management](project-management/README.md) | 跨会话保存目标、进度、决策、知识与流水 |
| [scripts/pm.py](scripts/pm.py) | 真实文件操作、索引、版本检查与本地恢复 |

Project 按 **状态 → 类型 → 稳定 ID** 组织。三状态为活跃、归档（暂不推进但未完成）、已完成；每种状态均支持开发型、学习型、一次性任务。Task 不独立落盘。

## 先看什么

- [总体设计](docs/Architecture.md)
- [已确认需求](docs/Requirements.md)
- [安装与使用](docs/Getting_started.md)
- [验收清单](docs/Acceptance.md)与[实际测试结果](docs/Test_results.md)
- [命令与数据契约](docs/CLI.md)
- [与 V0.2 的迁移关系](docs/Migration.md)
- [实现与验证边界](docs/Verification.md)

## 在 Mac 上使用

已有仓库可先 `git pull`；首次使用：

```bash
git clone https://github.com/leserein6/The_most_effective_context.git
cd The_most_effective_context
python3 scripts/pm.py doctor
python3 -m unittest discover -s tests -v
python3 scripts/demo.py
codebuddy
```

需要 Python 3.9+ 和现有 CodeBuddy 账号。无需安装第三方 Python 包。

首次输入：

> 请读取 agent.md 并检查活跃 Index。我想新建一个开发型 Project，目标是实现命令行待办工具。先给我名称、类型和一句话目标确认，再创建、实现并验证。

`agent.md` 是规范入口；`AGENTS.md` 仅为支持该文件名的 CLI 提供薄适配，不含第二套规则。若 CLI 没自动加载适配文件，明确让它读取 agent.md。没有 CODEBUDDY.md 主入口。

## 验证范围

脚本行为、冲突拒绝、日志原文保留、进程中断回滚及安装器有自动测试。自然语言归属、模式选择、真实 Subagent 调度与每轮写回遵守率仍需要在你的 CodeBuddy 环境按清单实测，不能把文档要求当作程序强制保证。

不自动 commit/push；只在用户要求时进行。当前仓库没有真实用户项目或私密历史，示例只在临时目录运行。旧 YAML 模板保留作历史参考，不会被自动迁移或当作当前实例读取。
