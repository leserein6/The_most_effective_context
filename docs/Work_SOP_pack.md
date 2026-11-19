# Work SOP Pack：六个可选工作流程 Skill

这是 **Harness 维护者的能力说明**，不安装到用户 Workspace。六个 Skill 位于 `.codebuddy/skills/work-*/SKILL.md`；运行包携带原始文件以便选装，但 `install-manifest.json` 默认不列入它们。

## 目的与数据边界

- **Core**：Project / Work Item（持久工作事项）/ Turn Task（本轮交互）/ Mode（行为方法）不因 SOP 而变化。
- **Skill**：只定义触发条件、输入事实、决策步骤、输出与停止条件。不另造 Task 数据库，不绕过状态迁移、人员授权或消息发送权限。
- **安装**：零个或多个 SOP 均可运行；六个彼此独立；默认零个。已安装目标可用 `--skills-only --skill ...` 增量安装，不重建 Project。
- **自动触发不是定时调度**：Skill 被识别不代表每天自动执行或拥有聊天/日历工具；具体 CodeBuddy 的触发效果须实际验证。
- **安全**：公司内部数据、日志、代码和人员信息仅在已授权范围内读取、输出或发送；无法核实的事实标明未知。

## 六个 Skill

| Skill | 用户自然触发语句 | 必需事实 | 核心交付 |
|---|---|---|---|
| `work-new-task` | “领导交办一个需求，帮我确认和拆解” | 目标、交付对象、交付格式、截止和验收；未知标待确认 | 任务契约、关键追问、拆解与第一动作 |
| `work-report` | “向 leader 报一下本周进度/延期风险” | 经验证的交付、剩余任务、阻塞和受众 | 结果优先的汇报稿、风险/备选方案/请求 |
| `work-daily` | “今天我先做哪三件事” | 活跃 WI、时间、依赖和实际状态 | Top 3、派生四栏视图、待反馈 |
| `work-cross-team` | “联调团队还没回我，怎么催” | 对接人、请求内容、约定时间和项目影响 | 沟通草稿、阻塞解除或升级路径 |
| `work-meeting` | “准备评审议程/整理会议纪要” | 会议目的及真实资料、已表态的决定 | 待决策议程或决定/行动项纪要 |
| `work-error-response` | “操作出错了，帮我先处理/汇报” | 已知错误、真实影响、权限和应急流程 | 止损顺序、短报、补救和防复发行动项 |

没有“下班交接” Skill。

## 安装方式

首次安装时，在 `scripts/install.py` 原命令后添加选项，例如 `--skill work-meeting --skill work-report`。

对于 **已安装** 的业务仓库，重新下载的 Harness 安装包须包含选装的 Skill 文件，然后执行：

```bash
python3 scripts/install.py --target /绝对路径/业务仓库 --mode project --skills-only --skill work-report
python3 scripts/install.py --target /绝对路径/业务仓库 --mode project --skills-only --skill work-report --apply
```

仅会复制该 Skill 到目标 `.codebuddy/skills/`，不写 Project Index/History；发现目标已有不同内容则拒绝覆盖。仓库原有 `docs/` 和维护资料不会被安装。

## 设计参考（不是直接复制的上游原文）

1. [Agent Skills 规范](https://agentskills.io/specification) 与 [渐进式加载指导](https://github.com/agentskills/agentskills/blob/main/docs/client-implementation/adding-skills-support.mdx)：`name/description` 负责能力发现，正文在触发后加载。
2. [Anthropic engineering standup](https://github.com/anthropics/knowledge-work-plugins/blob/main/engineering/skills/standup/SKILL.md)：没有连接工具时退回用户提供的事实，有工具时按授权读取代码与任务数据。
3. [Anthropic task-management](https://github.com/anthropics/knowledge-work-plugins/blob/main/productivity/skills/task-management/SKILL.md)：任务状态、等待项与操作闭环；本项目 **不复制其 TASKS.md**，而复用 WI。
4. [GitHub roundup](https://github.com/github/awesome-copilot/blob/main/skills/roundup/SKILL.md)：按受众和时间区间收集真实证据，缺少数据要说明。
5. [GitHub meeting-minutes](https://github.com/github/awesome-copilot/blob/main/skills/meeting-minutes/SKILL.md)：区分决定与行动项，强调负责人、截止时间和后续动作。
6. [GitHub incident-postmortem](https://github.com/github/awesome-copilot/blob/main/skills/incident-postmortem/SKILL.md)：事实、时间线、影响、根因与防复发，不责怪个人；本项目把高风险时的止损与审批前置。
7. [Anthropic meeting-briefing](https://github.com/anthropics/knowledge-work-plugins/blob/main/legal/skills/meeting-briefing/SKILL.md)：行动项责任人、期限、依赖和跟进闭环。

以上借鉴的是工作流程结构，六份中文 Skill 依据本项目 Project/WI 约束独立编写，不照搬第三方系统状态与强制模板。

## 建议验证场景

- 新任务缺交期：应该问关键问题，不捏造日期。
- 领导汇报但项目无进度分母：不生成“80%完成”。
- 用户问今日 Top 3：从已有 WI 排序，不生成新任务数据库。
- 跨组联系人未知：标待确认，不捏造姓名/擅自发送。
- 会议记录有讨论但未拍板：不写成“已决定”。
- 生产误操作：优先提示止损与上报，不直接运行危险修复命令。
- 默认安装：六个 SOP 不出现；选装一个：只有一个出现。
- 重复选装：无新增更改；原有同名不同内容：拒绝覆盖。
