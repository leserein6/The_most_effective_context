# Mac 安装与首次使用

## 1. 环境检查

按 [README 的用户拉取命令](../README.md#在-mac-上使用) 获取工作树，再在 The_most_effective_context 目录检查环境。

```bash
python3 --version
codebuddy --version
```

Python 需要 3.9+。不需 pip 安装第三方包；已有 CodeBuddy 和模型账号可以继续使用。如缺 Python，先安装 Python 3；本包不会替你更改机器环境。

## 2. 运行自检

```bash
python3 scripts/pm.py doctor
```

doctor 检查项目目录、索引和归档完整性。

## 3. 启动 CodeBuddy

```bash
codebuddy
```

首次输入：

> 请从 agent.md 开始，按需读取后续协议。我想做一个命令行待办工具，请先检查 Index，给出新 Project 的名称、类型和一句话目标，等我确认后创建。

确认后要求它明确验收条件，实际实现、验证并写回；不要只生成计划。完成本轮后检查项目 state.md、logs/current.md 是否出现实际进度。

## 4. 换会话验证恢复

关闭原 CodeBuddy 会话，再从同一 workspace 根目录运行 `codebuddy`，说：

> 接着做刚才的命令行待办项目。先恢复项目进度，说明已经完成什么、还剩什么，再继续。

它应读取 Index 与对应 Project 的状态；如果不能唯一识别，应询问候选。你无需重新粘贴全部历史。

## 5. 验证编排

> 在刚才的项目中使用编排模式：一个 Subagent 实现一个独立功能，另一个在它完成后独立审查。主 Agent 负责协调和验收，不亲自代做子任务。明确文件范围、依赖和证据。

使用 CodeBuddy `/agents` 检查 pm-worker、pm-reviewer 是否被识别。实际是否可调用依赖你的 CLI 版本和可用模型；不可用必须报告，不假装完成。不要为了本包开启 bypassPermissions。

## 6. 装入现有工作区（可选）

推荐先用仓库目录验收。安装器默认预览，遇同名不同内容拒绝覆盖；已有 agent.md 可以显式追加入口。

```bash
python3 scripts/install.py --target /绝对路径/你的workspace --merge-entry
python3 scripts/install.py --target /绝对路径/你的workspace --merge-entry --apply
```

已有 README.md、.gitignore 或其他不同内容会拒绝，需先决定如何合并；不要删除原文件来强行安装。安装到全新目录最直接。本脚本不会清空目录、强行替换用户规则或设置模型凭据。

## 7. 日常 Go/C++ Agent（按需启用）

默认在本项目的 `.codebuddy/agents/` 内提供 source-tutor、bug-investigator、change-impact、test-planner；在 CLI 里输入 `/agents` 查看。它们是主 Agent 的可选专业能力，不改变 Project/Task/Mode 的持久化方式。

若需要在其他 Go/C++ 仓库跨项目使用，请按 [Agent 安装和调用说明](Agents.md) 将所选文件复制到 `~/.codebuddy/agents/`。新的阅读/调查角色只读，不自动修改代码。

## 8. Git

自动保存是本地文件保存，不等于自动 commit。需要版本同步时，先检查 `git status` 与 diff，再明确要求 Agent 提交/推送。私密项目建议私有仓库；.pm-runtime、.env、CodeBuddy 本地配置已忽略。不要提交 API Key。

## 开发需求如何测试

先确认验收条件和关键不变量，再根据 [方法选择协议](../evidence/testing/selection.md) 选择适用的边界、状态、存储、并发、契约或故障检查。

可选：在**业务仓库**按 [testing_strategy.py](../scripts/testing_strategy.py) 的 `testing/strategy-input-v1` schema 编写包含 `change_id`、`claims` 的 JSON，然后运行：

```bash
python3 scripts/testing_strategy.py --input /路径/业务项目/strategy-input.json
```

输出 `DRAFT_UNREVIEWED` 只是候选方法，不是测试执行结果。实际测试运行方式见 [运行与证据](../evidence/testing/execution.md)，质量判定见 [充分性审查](../evidence/testing/adequacy.md)。维护者自身测试不提交到 Harness 仓库。
