# The Most Effective Context

> 让 AI 在正确的时机，读取完成当前任务所需的**最小充分上下文**。

这是一个面向通用 AI Agent 的 Markdown 协议实验仓库（V0 Demo）。它不是某个 CLI 的专属配置，也不是已经具备自动调度能力的应用程序；它首先验证**协议分层、按需加载、长期项目连续性**是否有效。

## 为什么需要它？

- **上下文浪费**：把全部规则、历史和示例塞给每一轮任务，耗费上下文窗口，也会引入无关干扰。
- **任务执行不稳定**：查证、设计、实施、澄清等任务需要不同的方法与验证标准。
- **长期工作断裂**：新 Session 容易丢失项目意图、决策、进度和下一步。
- **AI 擅自推断**：需求不明确时直接创建项目，或在维护中悄悄改写重要约束。

目标不是压缩到最少 Token，而是提高**相关性、充分性、无冗余性、可追溯性**。

## 系统组成

```text
agent.md                         # 全局轻量入口：识别本轮 Task，按需路由
├── harness/README.md            # AI Execution Harness：任务执行协议索引
│   └── protocols/               # research / design / execute / clarify
└── project-management/README.md # 独立的长期 Project 管理入口
    ├── protocols/               # create / maintain / resume
    ├── schema/                  # Project 数据与字段维护契约
    ├── templates/               # Project 实例模板
    └── examples/                # 按需读取的 Few-shot
```

**两套系统互不等同。** Task 是单轮临时锚点，不因一次对话自动持久化；Project 是可跨 Session 保存和恢复的长期对象。全局入口仅负责发现并路由，不复制子系统规则。

## 渐进式加载

1. **入口（Discovery）**：先读取 [agent.md](agent.md)，获得最少的全局规则与子系统入口。
2. **路由（Activation）**：按本轮 Task 读取 [harness/README.md](harness/README.md)；仅在涉及 Project 时读取 [project-management/README.md](project-management/README.md)。
3. **专项（Execution）**：只加载当前操作对应的协议；遇到确切需要再读取 Schema、Few-shot、项目数据和历史证据。
4. **执行与验证**：遵守已加载协议，基于可核实结果答复；不把推测当成既成事实。

例如：
- 用户要求「查证某项框架机制」→ `agent.md` → `harness/README.md` → `harness/protocols/research.md`。
- 用户要求「创建长期项目」→ `agent.md` → `project-management/README.md` → `project-management/protocols/create.md`；当需求模糊时再加载 `harness/protocols/clarify.md`，确认前不得正式创建。
- 用户要求「继续上一个项目」→ `agent.md` → `project-management/README.md` → `project-management/protocols/resume.md` → 对应项目实例的最小状态。

## 如何试用 V0

将此仓库作为 Agent 可读取的工作目录，并在所用 CLI / Agent 的**实际入口配置**中显式指向 `agent.md`（不同产品不会自动识别同名文件）。在对话中分别尝试：

1. 「帮我查证一个技术结论」：检查是否只加载 research 相关协议。
2. 「我想做一个产品，但需求还不清楚，帮我创建 Project」：检查是否先澄清、展示草案并获得明确确认。
3. 「继续刚才的 Project」：检查是否从持久化状态恢复，而不是凭空补全进度。

仓库中的协议是 **可供 Agent 遵守的文本约定**，尚不能在运行时强制保证文件加载顺序、原子写入、跨进程并发一致性或自动日志归档；这些需要后续工程集成和测试。

## V0 边界与演进

V0 只覆盖任务识别与分类路由、四类执行协议、Project 创建/维护/恢复，以及 Project 最小数据与字段维护规则。不提前引入多 Agent 编排、后台任务、复杂日志压缩或通用平台。

后续优先评估：**所加载文件是否必要、是否遗漏关键约束、创建是否经过确认、项目能否真实恢复、执行结果是否可验证**。

## 导航

- [全局入口：agent.md](agent.md)
- [AI 执行协议索引](harness/README.md)
- [Project 管理索引](project-management/README.md)

---
**状态：V0 协议 Demo，仍需在真实 Agent 环境验证。**
