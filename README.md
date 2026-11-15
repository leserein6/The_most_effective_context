# The Most Effective Context

> **让 AI 知道这轮要做什么、该遵守什么方法，以及一个长期项目究竟进展到哪里。**

The Most Effective Context 是一套面向 AI Agent 的 **上下文组织与协作协议**。它试图解决两个不同层次的问题：**单轮任务如何稳定执行**，以及**长期项目如何跨 Session 持续推进**。

项目的重点不是保存更多对话，也不是把所有 Prompt 塞进上下文，而是让 Agent 在正确时机读取**最小但充分**的指令、项目状态和相关资料。

目前是 **V0.2 协议 Demo**：仓库提供 Markdown 协议、Project 数据规范、示例和路由约定；尚无自动化运行时来保证每个 Agent 必然遵循。

## 1. 为什么需要这套体系？

与 AI 合作开发一个持续数周的项目时，常见情况是：

- 新开 Session 后，Agent 不清楚项目原本要解决什么，用户不得不重新解释。
- 做了许多局部任务，但重要决策、未完成事项和真实进度没有形成可信的项目状态。
- 用户只是讨论一个想法，Agent 却把推测写成已确定需求，甚至擅自变更项目方向。
- 查证、设计、调试和实际实施都套用同一套提示词；无关规则占用 Context，关键执行步骤反而容易遗漏。
- Agent 宣称“完成了”，但用户很难区分**提出方案、写入文件、验证通过**这三种不同结果。

因此，本项目希望提供两项能力：

**A. 可靠执行当前任务。** 每轮对话都有可见的 Task 锚点，Agent 根据任务类型按需加载相应方法论（Evidence）。

**B. 可靠管理长期项目。** Project 拥有独立于对话的身份、已确认的定义、当前状态和证据引用，使新 Session 能够恢复工作，而不是靠重读全部历史。

这两种能力相互配合，但**不是同一个系统**。

## 2. 系统全景

```text
                          AI Agent
                             │
                      agent.md（入口）
                             │
           ┌─────────────────┴──────────────────┐
           ▼                                    ▼
    Evidence / Task 执行体系              Project Management
    当前这轮该怎样完成任务                 长期项目如何被管理
           │                                    │
    ├─ research  查证                    ├─ create    创建与确认
    ├─ clarify   Grill-me                ├─ maintain  维护状态与决策
    ├─ design    设计                     ├─ resume    跨 Session 恢复
    ├─ execute   实施                     ├─ schema    数据及字段维护契约
    ├─ debug     调试                     └─ examples  按需 Few-shot
    └─ verify    完成验证                          │
                                                 ▼
                                    projects/<id>/project.yaml
                                    项目当前快照 + 资料引用
```

| 概念 | 解决的问题 | 生命周期 | 是否持久化 |
| --- | --- | --- | --- |
| **Task** | 本轮对话的主要预期结果是什么？ | 当前轮交互 | 不独立落盘 |
| **Evidence** | 当前任务应遵循哪套执行方法？ | 按任务阶段加载 | 协议本身保存在仓库 |
| **Project** | 长期工作是什么、做到哪里、如何接续？ | 跨多轮、跨 Session | 需要保存项目实例 |
| **agent.md** | 何时进入以上两个子系统？ | 每轮的轻量入口 | 全局协议文件 |

这里的 **Evidence** 特指“任务执行协议”，是本仓库自定义术语；它不等于 Project 实例中的**成果证明材料**（目前字段名仍为 `references.evidence`）。

## 3. Project Management：长期项目管理体系

这是本项目的一个**独立子系统**，不是简单的 Task 列表或聊天记录摘要。

### 3.1 它的存在价值

**Project 应当成为长期工作的稳定锚点。** Session 会结束，Task 会改变，甚至执行的 Agent 也可能更换；但已确认的项目意图、关键约束、决策理由、真实成果和下一步行动，不应该随之消失。

理想的恢复效果是：用户说「继续这个项目」，Agent 能回答：

1. **我们正在做什么？** 项目解决的问题、期望结果和边界。
2. **目前做到了哪里？** 哪些成果确实存在并已检查，哪些仍未完成。
3. **为什么会这样做？** 必要时回查先前的关键决策及依据。
4. **接下来做什么？** 当前阻塞和下一步行动，而不是从头设计。

**保存信息 ≠ 可靠恢复。** 如果只有一大段历史 Log，却没有可信的当前状态和可定位的证据，Agent 依然可能误判。

### 3.2 Project 如何被创建、维护和恢复？

**① 创建（Create）**

用户提出长期需求 → AI 根据已知信息提炼项目定义 → 如果核心需求模糊，按需调用 [Clarify / Grill-me](evidence/clarify/README.md) → 展示可修改的 Project 草案 → **用户确认具体草案** → 正式创建项目实例。

创建草案应当让用户看清：解决什么问题、希望达到什么结果、范围和不做的事、预期交付、关键约束、哪些尚未确定。非关键细节可以待定，不能为填满字段擅自编造。

**② 维护（Maintain）**

项目在一次次任务中推进时，AI 应区分：

- **普通任务或讨论**：不自动改变长期项目定义。
- **已确认的决策**：更新对应定义或记录决策来源；涉及核心方向、范围或硬约束的重大变化，先展示修改差异并请用户确认。
- **有实际证据的进展**：更新当前状态、经过验证的成果、阻塞与下一步；写入后核查结果。
- **仅是建议或尚未验证的工作**：保持其真实状态，不能写成“用户已决定”或“已完成”。

**③ 恢复（Resume）**

新 Session 关联 Project → 优先读取项目**当前快照** → 只在当前工作需要时，进一步读取相关决策、文件或历史依据 → 核实关键状态 → 告诉用户现状与下一步 → 继续当前 Task。

没有找到 Project 实例，或者引用已失效时，应说明限制，而不能假装恢复成功。

目前具体协议分别在 [Create](project-management/protocols/create.md)、[Maintain](project-management/protocols/maintain.md)、[Resume](project-management/protocols/resume.md)。

### 3.3 一个 Project 具体保存什么？

Project 分为两个部分，**数据实例**和**AI 字段维护契约**分离：

| 部分 | 内容 | 作用 |
| --- | --- | --- |
| Project Identity | `id`、`name` | 标识一个长期项目 |
| Project Definition | `intent`、`scope`、`deliverables`、`constraints` | 记录确认过的方向、边界与要求 |
| Project State | `phase`、`summary`、`verified_outputs`、`next_action`、`blockers` | 保存可信的当前进度 |
| References | `decisions`、`journal`、`evidence` | 指向详细决策、过程与证明资料 |

**数据实例**预计存放于 `projects/<id>/project.yaml`，记录每个项目自己的内容；**共享的字段契约**则规定字段是什么、如何从用户的话中提取、何时更新、不能如何擅自修改。遇到复杂提取或变更判断时，再按需加载 Few-shot。

例如，`intent.desired_outcome` 表示项目最终要达到的结果，**不是**这轮正在实现的某个功能，也不是 AI 自己建议的技术方案。

详见 [字段索引](project-management/schema/project.md)、[定义字段维护契约](project-management/schema/definition.md)、[进度字段维护契约](project-management/schema/progress.md) 和 [实例模板](project-management/templates/project.yaml)。

### 3.4 一个具体场景

假设用户想长期开发一个「AI 知识管理工具」：

- **第 1 次对话**：用户只提出模糊想法。Agent 先问最影响产品定位的问题，而不是自行生成完整功能表。形成草案，经确认后创建 Project。
- **第 2 次对话**：讨论并选择技术架构。Agent 可以调用 Design Evidence；确认的重要取舍由 Project Maintain 负责保存。
- **第 3 次对话**：实际开发并提交一个功能。Agent 调用 Execute，验证后才更新成果状态；没有通过的测试记录为阻塞，而不是“已完成”。
- **新 Session**：Agent 通过 Resume 读取项目快照，仅补读接下来开发所需的文档和源码，恢复工作。

**Task 执行方法可以切换，Project 本身保持连续。** 这就是两个子系统协作的方式。

## 4. Evidence：按任务加载的执行协议

Evidence 不是把现有开源 Skill 整份复制给 AI，而是借鉴成熟方法，将其改写为适合本体系的执行契约。

| Evidence | 典型用途 | 关键行为 |
| --- | --- | --- |
| [Research](evidence/research/README.md) | 查证事实与技术机制 | 找可定位来源，区分事实和推断 |
| [Clarify](evidence/clarify/README.md) | 需求不明确、Grill-me | 优先问最影响决定的问题，及时停止追问 |
| [Design](evidence/design/README.md) | 架构、方案、技术取舍 | 先问题和边界，后设计与权衡 |
| [Execute](evidence/execute/README.md) | 写文件、改代码、提交成果 | 核对现状、实施、检查真实结果 |
| [Debug](evidence/debug/README.md) | Bug、失败测试、异常 | 先定位根因，再修复 |
| [Verify](evidence/verify/README.md) | 声明任务完成前 | 将每项完成声明与实际检查绑定 |

路由由 [evidence/README.md](evidence/README.md) 负责。例如一个“修复错误”的 Task，可以先读 Debug，确定根因后读 Execute，准备宣称修复完成时再读 Verify；**不需要一开始读取全部六份**。

## 5. Context 设计：渐进式加载

Context 是有限资源。我们采用 **Progressive Disclosure（渐进式披露/加载）**：

```text
L0  agent.md                        只有最小通用规则和子系统指引
L1  对应子系统 README               决定当前操作读取哪份协议
L2  当前 Evidence / Project 协议     指导本次具体动作
L3  Schema / Few-shot / 项目资料     确实需要时才进一步加载
```

遵守三个原则：**相关性、充分性、非冗余性**。不要为了省 Token 漏掉必要约束；也不要把整棵目录、所有项目日志和所有例子一次性塞进 Context。

同时区分：

- **协议上下文**：指导 Agent *应该怎样工作*，由 `agent.md`、Evidence 和 Project 协议提供。
- **项目上下文**：说明 *这个具体项目当前是什么情况*，由 Project 实例及必要的引用提供。

## 6. 仓库目录

```text
.
├── README.md                      面向开发者的项目总览
├── agent.md                       面向 Agent 的轻量入口
├── evidence/
│   ├── README.md                  Evidence 路由
│   ├── research/ clarify/ design/
│   ├── execute/ debug/ verify/
│   └── examples/                  按需读取的路由案例
├── project-management/
│   ├── README.md                  Project 操作路由
│   ├── protocols/                 create / maintain / resume
│   ├── schema/                    定义与进度字段维护契约
│   ├── templates/                 Project 数据模板
│   └── examples/                  意图提取与进度判断案例
└── docs/
    └── research-review.md         外部 Skill 的研究和取舍
```

正式项目实例在执行创建流程并获得用户确认后，才会按协议生成到 `projects/<id>/`；当前仓库不预置虚构项目。

## 7. 使用与当前边界

**使用方式**：将仓库放到 Agent 可读的工作区，并通过对应 CLI/Agent 的实际配置指向 [agent.md](agent.md)（这个文件名并非所有产品通用的自动入口）。日常执行由它按需导向 Evidence 或 Project Management 的 README；开发者阅读本根 README 即可了解整体设计。

**V0.2 已提供**：可阅读的执行协议、项目创建/维护/恢复规则、Project Schema、Few-shot 与外部研究记录。

**V0.2 尚未提供**：跨 CLI 的自动入口适配、强制加载调度器、真实 Agent 效果验证、并发安全的项目写入、自动日志压缩与多 Agent 编排。协议描述了期望行为，并不等于已有可运行的自动化服务。

外部研究和具体取舍见 [docs/research-review.md](docs/research-review.md)。
