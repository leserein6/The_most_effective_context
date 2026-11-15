# The Most Effective Context

> **让 AI 在正确的时机得到正确的上下文，而不是得到最多的上下文。**

面向通用 AI Agent 的 **Context Engineering / Agent Protocol V0 实验仓库**。它包含两个独立系统：**单轮任务执行协议**与**跨 Session 的 Project 管理协议**。二者只通过轻量入口关联，不共享生命周期。

## 1. 要解决的问题

| 真实失效 | 所需机制 | 如何判断有效 |
| --- | --- | --- |
| 所有规则常驻 Context，干扰当前任务 | 轻入口 + 按需路由 | 简单查证不加载 Project 全部结构 |
| Agent 忘记本轮要做什么 | 每轮明确一个可见 Task | 用户能立即指出理解偏差 |
| 不同任务使用同一套路 | 依主要交付类型选择执行协议 | 查证有证据，实施有可核实产物 |
| 需求没说清楚便擅自设计 | 按需 Grill-me 与确认门槛 | 不凭空增加关键需求 |
| 新 Session 无法继续长期工作 | 持久化 Project 当前快照与引用 | 不依赖旧对话也能恢复状态 |
| 把“写了文件”等同“功能完成” | 证据先于完成声明 | 每个关键结论都有实际核实方式 |

**优化目标**是最小**充分**上下文，而不是最少 Token：缺失必要协议比多读几行更危险。

## 2. 架构及职责

```text
agent.md                     全局入口：锚定本轮 Task，指向路由器
├── harness/README.md        单轮 Task 的协议路由
│   └── protocols/           research / design / execute / clarify
└── project-management/
    ├── README.md            Project 专用操作路由
    ├── protocols/           create / maintain / resume
    ├── schema/
    │   ├── project.md       字段索引和全局不变量
    │   ├── definition.md    项目意图、边界与成果字段
    │   └── progress.md      状态、证据与接续字段
    ├── examples/            只有需要时才读 Few-shot
    └── templates/           项目实例模板
projects/                    未来实际创建的 Project 实例；V0 不预置假项目
tests/                       手工行为测试与文件引用检查
docs/                        设计依据、取舍和外部研究
```

**Task ≠ Project**：Task 是本轮可见、临时的执行锚点，不要求写盘；Project 是经过用户确认、跨 Session 持续维护的对象。即使当前 Task 是“创建一个 Project”，两者也不是同一份数据。

## 3. 加载契约

- **L0：入口**。Agent 运行环境显式加载 [agent.md](agent.md)。这里只保留跨任务通用的不变量和路由地址。
- **L1：路由**。依据意图读取 [harness/README.md](harness/README.md)；涉及长期 Project 时额外读取 [project-management/README.md](project-management/README.md)。
- **L2：执行协议**。选当前操作对应的一个协议。跨步骤任务只在进入下一步骤时补载需要的协议。
- **L3：具体资源**。Schema、示例、项目状态和证据只有在此步骤需要时才读；加载了入口不代表必须读完子树。

例如：
- 「核对 Go 某个实现是否线程安全」→ `agent.md` → `harness/README.md` → `research.md`。
- 「帮我创建一个长期项目」→ `agent.md` → Project README → `create.md` → 必要时 `clarify.md` → 定义 Schema/模板 → **用户确认后才落盘**。
- 「继续项目 X」→ `agent.md` → Project README → `resume.md` → 项目快照 → 仅所需引用。

**限制**：这是遵循 Agent Skills *渐进披露思想* 的 Markdown 协议，不是原生 Skill 包（没有宣称所有文件符合 `SKILL.md` 格式）。`agent.md` 也不是跨工具统一自动发现的标准文件名。某些工具需要显式配置启动入口或采用各自的适配文件。当前没有运行时调度器能强制 Agent 按上述顺序读取。

## 4. 开始使用

1. 在支持读取工作区文件的 Agent 中打开本仓库。
2. 在该 Agent/CLI 的实际入口配置中**显式引用** `agent.md`；不要假定单凭文件名就会自动生效。
3. 按 [tests/manual-scenarios.md](tests/manual-scenarios.md) 分别测试查证、模糊创建、确认后写入、跨 Session 恢复。
4. 用文件访问日志/实际回复核实行为；记录额外读取和漏读，不靠 Prompt 自我宣称有效。

文档引用可执行 `python3 tests/check_docs.py` 检查（仅做静态文件引用校验，不验证 Agent 行为）。

## 5. V0 范围

**已定义**：Task 锚定、任务协议路由、Project 创建/维护/恢复、项目字段提取与更新契约、Few-shot、手工验收条件。

**尚未实现**：CLI 原生适配、自动加载强制执行、Agent 真实行为测试、并发写入控制、运行时状态机、复杂 Log 压缩、多 Agent 调度。因此 V0 是**协议样机**而不是已验证的 Agent 产品。

设计依据与适用边界见 [docs/research-review.md](docs/research-review.md)。协议和外部来源会迭代；修改前先看验证用例是否要同步更新。
