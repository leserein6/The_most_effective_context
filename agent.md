# Workspace 入口

每轮先读取 `project-management/Index.md`，再遵循 `evidence/workflow.md` 的通用执行协议。
Project Management 是独立组件：项目操作读取 `project-management/README.md`，具体操作再读对应协议。

必须遵守：
- 先锚定 Project。信息不足、存在多个候选、或用户未指明且上下文不能唯一识别时，问“创建新项目，还是接续哪个项目？”，展示相关候选；不猜测，不自行创建。
- 新建前提出名称、development/learning/one_off 类型、一句话目标，用户确认后才创建。
- 当前活跃会话已经明确 Project 时，仍检查 Index，沿用明确锚点，不反复询问。
- 区分 Project 类型、状态和本轮 Mode。自动选择 Mode，简短告知；用户指定优先；可中途切换。
- 发现新要求与已确认决策冲突，先指出。用户已明确修订则执行，否则先澄清。
- 普通明确任务直接推进；关键歧义、重大取舍才询问。不要把所有动作变成审批。
- 状态变更、公用规范/Prompt 纳入需要用户确认；用户已明确要求时不重复索要确认。
- 回复前自动保存项目进度、决策状态、操作流水。候选建议不能写成已确认决策。
- 只在独立工作可拆分时自动使用 Subagent。编排模式主 Agent 不代做具体任务，负责协调与验收。
- Git 不自动 commit/push；明确要求时执行。不要自动启用权限绕过。

脚本：`python3 scripts/pm.py --help`。相对路径基于 workspace 根目录。
先运行 `python3 scripts/pm.py doctor`；如果不在根目录，使用绝对脚本路径及 `--root`。
项目管理规则、Mode、Prompt 都是本体系的协议，不是 CodeBuddy 内置运行模式名称。
