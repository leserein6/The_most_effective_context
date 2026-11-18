# The Most Effective Context

让 Agent 在正确时机加载最小充分上下文，执行当前任务，并可靠接续长期项目。

本次在原 V0.2 协议仓库上迭代为 **V1.1 文件型 Workspace 与 Project Harness**：保留 `agent.md` 入口、Evidence 执行体系、独立 `project-management`，覆盖项目生命周期、七种模式、Subagent 协作、每轮日志、压缩归档、并发检查与进程中断恢复。

## 总体边界

| 层次 | 职责 |
|---|---|
| [agent.md](agent.md) | 总入口：锚定 Task/Project，内含一级 Task 路由 |
| [entry/routes/](entry/routes/) | 入口的二级场景路由，按预期交付选读 |
| [Evidence](evidence/README.md) | methods / prompts / references / testing，按需读取方法与测试工程知识 |
| [Project Management](project-management/README.md) | 跨会话保存目标、进度、决策、知识与流水 |
| [scripts/pm.py](scripts/pm.py) | 真实文件操作、索引、版本检查与本地恢复 |

Project 按 **状态 → 类型 → 稳定 ID** 组织。三状态为活跃、归档（暂不推进但未完成）、已完成；每种状态均支持开发型、学习型、一次性任务。Task 不独立落盘。

开发型需求通过[测试工程](evidence/testing/README.md)把业务承诺对应到可执行用例、候选版本、验收与回归。

完整的开发需求测试工程包含 [方法目录](evidence/testing/catalog.md)、[选择协议](evidence/testing/selection.md)、[充分性与双重门禁](evidence/testing/adequacy.md)、[具体模型](evidence/testing/models.md)和既有测试运行器。测试用例在业务仓库，Harness 不自动认定自己生成的测试充分。

## 先看什么

- [总体设计](docs/Architecture.md)
- [每轮Task与二级方法索引](docs/Task_routing.md)
- [CodeBuddy 专业 Agent 与 Go/tRPC-Go/金融 Review Skill](docs/Agents.md)
- [历史 Prompt 去重与复用决策](docs/Prompt_inventory.md)
- [外部 Skill / Prompt 资源库](evidence/prompts/README.md)
- [协议职责与去重](docs/Protocol_boundaries.md)
- [已确认需求](docs/Requirements.md)
- [安装与使用](docs/Getting_started.md)
- [验收与质量门禁](docs/Acceptance.md)
- [命令与数据契约](docs/CLI.md)
- [与 V0.2 的迁移关系](docs/Migration.md)
- [实现与验证边界](docs/Verification.md)

## 在 Mac 上使用

这个 GitHub 仓库是 **Harness 源码及维护资料**，并不等于普通用户的工作区。安装器使用 `install-manifest.json` 明确白名单：默认**不安装 `docs/`、根 `README.md`、安装器自身、安装清单、维护测试或源仓库 Project 数据**，仅向目标工作区复制运行时必需文件。日常使用只在目标工作区进行；升级或重新安装时才回到源码仓库。当前开发版本位于 `codex/project-workspace-v1-20261117`（未合并 main）。首次使用：

```bash
git clone -b codex/project-workspace-v1-20261117 https://github.com/leserein6/The_most_effective_context.git
cd The_most_effective_context
python3 scripts/install.py --target ~/my-ai-workspace --mode workspace
python3 scripts/install.py --target ~/my-ai-workspace --mode workspace --apply
cd ~/my-ai-workspace
python3 scripts/pm.py doctor
codebuddy
```

已有该分支的源码仓库使用 `git pull --ff-only` 同步。需要 Python 3.9+ 和 CodeBuddy；安装目标应是新的空目录。上述安装命令先预览、再执行；源码仓库与 `~/my-ai-workspace` 是两个不同目录。业务测试及 CI 留在业务仓库，Harness 的维护用例不随发行版本分发。

**装入已有 Go/C++ 业务仓库**（不修改业务根目录 README、`.gitignore` 或测试代码）：

```bash
python3 scripts/install.py --target /绝对路径/业务仓库 --mode project --merge-entry
python3 scripts/install.py --target /绝对路径/业务仓库 --mode project --merge-entry --apply
```

先预览后执行。Harness 协议位于业务仓库 `.codebuddy/harness/`，专用 Agent/Skill 放在业务仓库 `.codebuddy/agents/`、`.codebuddy/skills/`；原有 `CODEBUDDY.md` 或 `AGENTS.md` 仅在显式 `--merge-entry` 后追加带标记的入口，不覆盖原内容。全新独立目录安装用 `--mode workspace`，要求目标为空。详见 [安装说明](docs/Getting_started.md)。

首次输入：

> 请读取 agent.md 并检查活跃 Index。我想新建一个开发型 Project，目标是实现命令行待办工具。先给我名称、类型和一句话目标确认，再创建、实现并验证。

`agent.md` 是规范执行入口；`CODEBUDDY.md` 作为 CodeBuddy 推荐入口通过 `@agent.md` 导入，`AGENTS.md` 是兼容其他 CLI 的薄适配。两者不各自维护规则。使用 `/memory` 核实加载，不把文件存在当成已激活。

## 验证范围

脚本行为、冲突拒绝、日志原文保留、进程中断回滚及安装器已在开发过程中接受自动回归；维护用例不保留在本仓库。自然语言归属、模式选择、真实 Subagent 调度与每轮写回遵守率仍需要在你的 CodeBuddy 环境按清单实测，不能把文档要求当作程序强制保证。

不自动 commit/push；只在用户要求时进行。当前仓库没有真实用户项目或私密历史，示例只在临时目录运行。旧 YAML 模板保留作历史参考，不会被自动迁移或当作当前实例读取。
