# The Most Effective Context

一个面向 CodeBuddy CLI / AI Agent 的 Project 与任务执行 Harness：**让 AI 知道当前要做什么、按什么方法执行，以及长期项目进行到哪里。**

你可以直接提出开发、学习、调研或审查任务；Agent 按需读取执行方法、恢复 Project 状态，并记录有证据的进展。它不是 AI 模型，也不会自动获得更高的系统权限。

## 主要能力

- **Project 管理**：开发型、学习型、一次性项目；活跃、归档、已完成三种状态；跨会话恢复。复杂项目支持持久化 Work Item（拆分、依赖、待办、阻塞、完成证据），与每轮 Turn Task 区分。复杂项目可持久追踪 Work Items（需求拆分、依赖、待办、阻塞、完成证据）；每轮 Turn Task 与之区分。
- **任务执行**：针对需求澄清、调研、设计、实施、审查、测试、学习及编排等场景按需加载方法；复杂方案支持实施前的完整性、可行性和执行就绪审查。
- **协作与验证**：可选专业 Agent、Go / tRPC-Go / 金融审查 Skill、证据与测试工程协议。
- **持续记录**：每轮写回真实进度、决策与操作流水，支持日志压缩、归档及本地冲突检测。

**普通用户不需要 clone 这个源码仓库。** 用户安装的是精简的运行包，里面没有维护者的 `docs/`、测试、根 README、源码仓库 Project 实例和 Git 历史。

## 安装（Mac）

准备：Python 3.9+、CodeBuddy CLI，以及该 GitHub 仓库的访问权限。目前仓库为 **Private**，因此下载 GitHub Actions 安装包需要登录有权限的 GitHub 账号；如果你让 AI 帮忙安装，也仍需由你完成账号授权。

### 1. 获取精简运行包（无需 git clone）

在 GitHub 仓库打开 **Actions → Build minimal Harness runtime → 最近一次成功运行 → Artifacts → harness-runtime**，下载并解压 Artifact。里面有：

```text
harness-runtime.zip
harness-runtime.zip.sha256
```

核对 SHA-256 后再解压 `harness-runtime.zip`，其中只有安装器、安装白名单和运行所需文件；不含 `docs/`。

也可以让 AI 运行下面的命令，以 GitHub CLI 自动获取最新一次**成功**的构建产物：

```bash
# 安装过 gh 并登录后即可使用（首次执行 gh auth login）
REPO=leserein6/The_most_effective_context
BRANCH=codex/project-workspace-v1-20261117
RUN_ID=$(gh run list --repo "$REPO" --workflow runtime-package.yml --branch "$BRANCH" --limit 20 --json databaseId,conclusion --jq '[.[] | select(.conclusion == "success")][0].databaseId')
test -n "$RUN_ID" || { echo "没有找到成功的运行包构建，请查看仓库 Actions"; exit 1; }

DL_DIR=$(mktemp -d)
gh run download "$RUN_ID" --repo "$REPO" --name harness-runtime --dir "$DL_DIR"
(cd "$DL_DIR" && shasum -a 256 -c harness-runtime.zip.sha256)
unzip -q "$DL_DIR/harness-runtime.zip" -d "$DL_DIR/runtime"
```

上面使用的 `$DL_DIR/runtime` 是临时解压的安装包目录，不是日常 Workspace。GitHub Actions 产物可能按仓库保留策略过期；需要时由维护者重新运行打包流程。

### 2. 安装到你的工作区

**方式 A：创建全新的独立 Workspace**（目标目录必须为空）：

```bash
python3 "$DL_DIR/runtime/scripts/install.py" --target ~/my-ai-workspace --mode workspace --entry codebuddy
python3 "$DL_DIR/runtime/scripts/install.py" --target ~/my-ai-workspace --mode workspace --entry codebuddy --apply
python3 ~/my-ai-workspace/scripts/pm.py doctor
cd ~/my-ai-workspace
codebuddy
```

**方式 B：安装到已有业务代码仓库**（将目标换成你的真实路径）：

```bash
python3 "$DL_DIR/runtime/scripts/install.py" --target /绝对路径/业务仓库 --mode project --entry codebuddy --merge-entry
python3 "$DL_DIR/runtime/scripts/install.py" --target /绝对路径/业务仓库 --mode project --entry codebuddy --merge-entry --apply
python3 /绝对路径/业务仓库/.codebuddy/harness/scripts/pm.py doctor
```

两种方式都是**先预览、后明确执行**，遇到同名内容冲突会拒绝覆盖。嵌入业务仓库时，Harness 运行文件集中在 `.codebuddy/harness/`，专业 Agent / Skill 位于 `.codebuddy/agents/`、`.codebuddy/skills/`；不改动你的业务 README、测试或原有 `.gitignore`。

**入口约定：规则正文只有 `agent.md`。** 安装器按 `--entry` 生成你实际使用的那一个宿主入口，不把入口当成第二份规则：

- `codebuddy`（默认）：生成 `CODEBUDDY.md`，内容 `@agent.md`；
- `agents`：生成 `AGENTS.md`，指向 `agent.md`；
- `both`：两个都生成；
- `none`：只放 `agent.md`，由你自行改名或适配。

嵌入业务仓库时，入口指向 `.codebuddy/harness/agent.md`。入口文件是生成物，修改规则请改 `agent.md`，然后用同一 `--entry` 重新安装。

如手动在网页下载了运行包，命令里的 `"$DL_DIR/runtime/scripts/install.py"` 改为实际解压位置。正常安装无需执行 `git clone` 或 `pip install`。

### 3. 日常使用

在已安装的 Workspace / 业务仓库中启动 `codebuddy`，例如：

> 我想新建一个开发型 Project，目标是实现一个命令行待办工具。请先确认名称、类型和一句话目标，再创建、实现并验证。

下次会话直接说「继续这个 Project」，Agent 应检查索引、恢复现状并按需读取资料。可以使用 CodeBuddy 的 `/memory`、`/agents` 检查入口和专业 Agent 是否真实可用；**只看到文件存在并不代表模型行为已验收**。

自动保存 Project 状态不等于自动 `git commit` / `git push`；这些操作只在用户明确要求时进行。遇到版本升级冲突需要审查差异，不能自动覆盖现有项目记录。

## 工作方法插件

从 Harness 根运行以下命令。独立 Workspace 的根是安装目录，嵌入模式的根为 `.codebuddy/harness/`。随包提供的全景图方法默认启用。

```bash
python3 scripts/extensions.py list --task proposal
python3 scripts/extensions.py disable panorama
python3 scripts/extensions.py enable panorama
```

新增方法包、为已有包补充资料及旧工作区接入见[方法插件设计与实施](docs/Method_extensions.md)。

## 可选 Work SOP Skills

默认安装不包含办公 SOP；需要时可逐个选择 `work-new-task`（接新任务）、`work-report`（向上汇报）、`work-daily`（日常安排）、`work-cross-team`（跨团队）、`work-meeting`（会议）、`work-error-response`（差错处理）。**没有下班交接 Skill**。六份完整流程和公开参考来源见 [Work SOP Pack](docs/Work_SOP_pack.md)（仅维护者文档，不安装）。

首次安装时，在安装器命令中追加 `--skill work-report` 等选项即可选装。已经安装到业务仓库后，可以只增量安装一项，不重装核心和用户 Project：

```bash
python3 "$DL_DIR/runtime/scripts/install.py" --target /绝对路径/业务仓库 --mode project --skills-only --skill work-report
python3 "$DL_DIR/runtime/scripts/install.py" --target /绝对路径/业务仓库 --mode project --skills-only --skill work-report --apply
```

运行包包含这六份**待选装文件**，但默认不会复制到用户 Workspace。选择性安装遇到同名文件内容不同会停止，不覆盖用户修改；安装后用 CodeBuddy `/skills` 核实发现情况。Skills 不自带消息发送、定时提醒或生产操作授权。

## 常见边界

- 项目状态写回、冲突检测、日志归档由本地 Python 脚本完成；自然语言路由、模式选择、多 Agent 调度以及实际测试质量还需要真实 CodeBuddy 环境验证。
- 不会自动上传公司源码、敏感业务日志或密钥。请按所在组织的权限与数据处理要求使用外部 AI 工具。
- 运行包只复制安装白名单中的文件；日志、Project 数据以及用户业务代码保存在**用户自己的 Workspace** 中。
- GitHub Actions 尚未成功构建时，不能把运行包描述为已发布。开发者可从源仓库构建，下文提供命令。

## 开发与维护（普通用户无需阅读）

这里是**源码仓库**，包含架构、研究、维护说明及打包工具；日常用户只安装上面的运行包。

- [架构](docs/Architecture.md) · [需求及约束](docs/Requirements.md) · [协议边界](docs/Protocol_boundaries.md)
- [任务路由](docs/Task_routing.md) · [Agent 设计](docs/Agents.md) · [实现边界](docs/Verification.md)
- [安装/命令契约](docs/CLI.md) · [迁移](docs/Migration.md) · [验收](docs/Acceptance.md)

维护者 clone 源码后可构建和校验安装包：

```bash
python3 scripts/build_runtime.py --output dist/harness-runtime.zip
python3 scripts/build_runtime.py --output dist/harness-runtime.zip --verify
```

核心按 `install-manifest.json` 打包，方法插件按各自的 `extension.json` 打包；`scripts/install.py` 和白名单是用户运行包所必需的，`docs/`、维护者资料和源项目数据永远不进入包。对应工作流为 `.github/workflows/runtime-package.yml`。
