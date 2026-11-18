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

## 6. 发行安装（可选）

安装器从固定 `install-manifest.json` 的明确文件列表复制，**不会复制源项目已有 Project、日志、`.env`、维护者测试或原 `.gitignore`**，默认只预览。

**装到已有业务仓库**（推荐，`--mode project` 默认值）：

```bash
python3 scripts/install.py --target /绝对路径/业务仓库 --mode project --merge-entry
python3 scripts/install.py --target /绝对路径/业务仓库 --mode project --merge-entry --apply
```

业务仓库根目录的 `README.md`、`.gitignore` 和 `tests/` 原样保留。Harness 协议/Project 状态安装在 `.codebuddy/harness/`，CodeBuddy Agent/Skill 则进入根目录 `.codebuddy/agents/` 和 `.codebuddy/skills/`。若目标已有 `CODEBUDDY.md`，仅在 `--merge-entry` 时追加可识别的入口；若只有 `AGENTS.md` 则仅追加到它；若两者都没有则创建 `CODEBUDDY.md`。原内容不被替换。使用 CLI 的 `/memory` 检查实际入口加载。

**全新、单独的 Harness Workspace**：

```bash
python3 scripts/install.py --target /绝对路径/全新空目录 --mode workspace
python3 scripts/install.py --target /绝对路径/全新空目录 --mode workspace --apply
```

要求目标为空；生成受限 `.gitignore`（仅忽略本 Harness 运行产物）和空白 Project Index/History。不会带出源仓库自己的 Project 数据。

嵌入安装时，文档中指向 Agent/Skill 的 Markdown 相对链接会自动适配业务仓库的 `.codebuddy/agents/` 与 `.codebuddy/skills/` 位置；不创建重复副本。

若同名文件内容不一致，安装器中止而不是覆盖；再次安装相同版本应没有新改动。**安装新版本到已配置的目标时，需要先审阅并人工合并真实冲突，不等同自动升级。** 运行前检查预览，出现错误先保留现场。装好后在目标执行 `python3 .codebuddy/harness/scripts/pm.py doctor`（嵌入模式）或 `python3 scripts/pm.py doctor`（独立模式）。


## 7. 日常 Go/C++ Agent（按需启用）

默认在本项目的 `.codebuddy/agents/` 内提供 source-tutor、bug-investigator、change-impact、test-planner；在 CLI 里输入 `/agents` 查看。它们是主 Agent 的可选专业能力，不改变 Project/Task/Mode 的持久化方式。

若需要在其他 Go/C++ 仓库跨项目使用，请按 [Agent 安装和调用说明](Agents.md) 将所选文件复制到 `~/.codebuddy/agents/`。新的阅读/调查角色只读，不自动修改代码。

## 常用历史 Prompt 的 Skill 复用

原来编写过的通用 Go Review、RPC Review、金融风险 Review 已整理为独立可选 Skill；其它源码带读、需求契约、Prompt 编写与故障调查尽量复用已有 Agent/Method。完整分类见 [历史 Prompt 清单](Prompt_inventory.md)，跨项目安装与 `/skills` 验证见 [Agents](Agents.md)。

## 8. Git

自动保存是本地文件保存，不等于自动 commit。需要版本同步时，先检查 `git status` 与 diff，再明确要求 Agent 提交/推送。私密项目建议私有仓库；.pm-runtime、.env、CodeBuddy 本地配置已忽略。不要提交 API Key。

## 开发需求如何测试

先确认验收条件和关键不变量，再根据 [方法选择协议](../evidence/testing/selection.md) 选择适用的边界、状态、存储、并发、契约或故障检查。

可选：在**业务仓库**按 [testing_strategy.py](../scripts/testing_strategy.py) 的 `testing/strategy-input-v1` schema 编写包含 `change_id`、`claims` 的 JSON，然后运行：

```bash
python3 scripts/testing_strategy.py --input /路径/业务项目/strategy-input.json
```

输出 `DRAFT_UNREVIEWED` 只是候选方法，不是测试执行结果。实际测试运行方式见 [运行与证据](../evidence/testing/execution.md)，质量判定见 [充分性审查](../evidence/testing/adequacy.md)。维护者自身测试不提交到 Harness 仓库。
