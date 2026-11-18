# The Most Effective Context

让 Agent 在正确时机加载最小充分上下文，执行当前任务，并可靠接续长期项目。

本次在原 V0.2 协议仓库上补齐 **V1 文件型 workspace 与项目管理脚本**：保留 `agent.md` 入口、Evidence 执行体系、独立 `project-management`，覆盖项目生命周期、七种模式、Subagent 协作、每轮日志、压缩归档、并发检查与进程中断恢复。

## 总体边界

| 层次 | 职责 |
|---|---|
| [agent.md](agent.md) | 总入口：锚定 Task/Project，内含一级 Task 路由 |
| [entry/routes/](entry/routes/) | 入口的二级场景路由，按预期交付选读 |
| [Evidence](evidence/README.md) | methods / prompts / references / evals，按需读取具体方法与材料 |
| [Project Management](project-management/README.md) | 跨会话保存目标、进度、决策、知识与流水 |
| [scripts/pm.py](scripts/pm.py) | 真实文件操作、索引、版本检查与本地恢复 |

Project 按 **状态 → 类型 → 稳定 ID** 组织。三状态为活跃、归档（暂不推进但未完成）、已完成；每种状态均支持开发型、学习型、一次性任务。Task 不独立落盘。

开发型需求通过[测试工程](evidence/testing/README.md)把业务承诺对应到可执行用例、候选版本、验收与回归。

完整的开发需求测试工程包含 [方法目录](evidence/testing/catalog.md)、[选择协议](evidence/testing/selection.md)、[充分性与双重门禁](evidence/testing/adequacy.md)、[具体模型](evidence/testing/models.md)和既有测试运行器。测试用例在业务仓库，Harness 不自动认定自己生成的测试充分。

## 先看什么

- [总体设计](docs/Architecture.md)
- [每轮Task与二级方法索引](docs/Task_routing.md)
- [外部 Skill / Prompt 资源库](evidence/prompts/README.md)
- [协议职责与去重](docs/Protocol_boundaries.md)
- [已确认需求](docs/Requirements.md)
- [安装与使用](docs/Getting_started.md)
- [验收清单](docs/Acceptance.md)与[实际测试结果](docs/Test_results.md)
- [命令与数据契约](docs/CLI.md)
- [与 V0.2 的迁移关系](docs/Migration.md)
- [实现与验证边界](docs/Verification.md)

## 在 Mac 上使用

用户可以只拉取使用 Harness 需要的工作树，省去开发测试和模型评测用例。**当前测试工程仍处于 PR #3 分支（其基线为 PR #2 → PR #1），main 尚未包含这些改动。** 要试用本次改造，在终端执行：

```bash
git clone --depth 1 --filter=blob:none --sparse -b codex/testing-methodology-v2-20261118 https://github.com/leserein6/The_most_effective_context.git
cd The_most_effective_context
git sparse-checkout set --no-cone '/*' '!/tests/' '!/evidence/evals/' '!/.github/workflows/harness-tests.yml'
python3 scripts/pm.py doctor
codebuddy
```

后续在该目录执行 `git pull` 会沿用本地稀疏检出设置。已有完整开发副本的用户也可直接用安装器，它会跳过测试目录。需要 Python 3.9+ 和 CodeBuddy。开发者使用普通 `git clone` 获取完整仓库，在源码目录运行 `python3 -m unittest discover -s tests -v`。

首次输入：

> 请读取 agent.md 并检查活跃 Index。我想新建一个开发型 Project，目标是实现命令行待办工具。先给我名称、类型和一句话目标确认，再创建、实现并验证。

`agent.md` 是规范入口；`AGENTS.md` 仅为支持该文件名的 CLI 提供薄适配，不含第二套规则。若 CLI 没自动加载适配文件，明确让它读取 agent.md。没有 CODEBUDDY.md 主入口。

## 验证范围

脚本行为、冲突拒绝、日志原文保留、进程中断回滚及安装器有自动测试。自然语言归属、模式选择、真实 Subagent 调度与每轮写回遵守率仍需要在你的 CodeBuddy 环境按清单实测，不能把文档要求当作程序强制保证。

不自动 commit/push；只在用户要求时进行。当前仓库没有真实用户项目或私密历史，示例只在临时目录运行。旧 YAML 模板保留作历史参考，不会被自动迁移或当作当前实例读取。
