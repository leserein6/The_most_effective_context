# The Most Effective Context

> 让 AI 在正确时机加载正确的方法和项目上下文，而不是每轮灌入全部 Prompt。

这是一个 **Agent Context Engineering V0.2 协议 Demo**，包含两个独立子系统：

1. **Evidence（任务执行协议）**：围绕本轮 Task 选择恰当的执行方法；不持久化 Task。
2. **Project Management（长期项目管理）**：围绕经用户确认的 Project 保存定义、状态、决策和接续位置；跨 Session 存在。

`agent.md` 是全局轻量入口，负责 Task 锚定和两个子系统的路由，**不承载全部方法论**。

## 架构

```text
agent.md                           全局最小入口
├── evidence/README.md             Task → Evidence 分类与触发
│   ├── research/README.md          查证：结论有来源
│   ├── clarify/README.md           Grill-me：澄清关键需求
│   ├── design/README.md            设计：明确取舍与边界
│   ├── execute/README.md           执行：真实产物与检查
│   ├── debug/README.md             调试：先查根因再修复
│   ├── verify/README.md            验证：完成声明的证据门槛
│   └── examples/routing.md         边界案例，按需读取
└── project-management/README.md   独立的长期 Project 管理
    ├── protocols/                 创建、维护、恢复
    ├── schema/                    字段定义与更新契约
    ├── templates/                 项目实例模板
    └── examples/                  Project Few-shot
```

## 概念边界

- **Task**：本轮对话的主要预期结果，应对用户可见；不自动落盘。
- **Evidence**：完成某种 Task 时，Agent 需要加载并遵守的执行协议。它是本仓库的术语，并不表示已经符合外部 `SKILL.md` 包格式。
- **Project**：经确认的长期工作对象，有持久化状态，与单轮 Task 生命周期不同。
- **验证凭据**：证明某事已发生的测试、文件或记录。它与名为 Evidence 的**方法论目录**是两个不同概念；Project 模型里历史存在的 `references.evidence` 指后者意义上的证明材料，暂不做破坏性字段迁移。

## Progressive Disclosure

| 层级 | 读取内容 | 为什么 |
| --- | --- | --- |
| L0 | [agent.md](agent.md) | 只定义跨任务不变量和子系统入口 |
| L1 | [evidence/README.md](evidence/README.md)，或项目管理 README | 识别**此时**要使用的执行协议 |
| L2 | 某个 Evidence 的 `README.md` 或具体 Project 操作协议 | 按当前问题执行 |
| L3 | 按需引用的 Few-shot、Schema、真实项目文件与证明材料 | 解开歧义、完成具体步骤 |

**入口不是整棵目录的预加载指令**。可以先按 Research 查证、然后按 Execute 修改、在声明成功前按 Verify 验证；只在进入相应阶段时加载。

## 试用

- 在宿主 Agent/CLI 中**显式配置**读取 `agent.md`。不同工具不会因为该文件名就必然自动识别。
- 先看 [Evidence 路由](evidence/README.md)，在实际任务中追踪所加载的文件路径。
- 涉及长期项目时看 [Project Management](project-management/README.md)。项目需求模糊则按需调用 Clarify；用户**确认具体草案前不创建正式实例**。
- 用 [测试场景](tests/manual-scenarios.md) 记录路由是否正确、是否多读/漏读、成果是否有实际验证。
- 可用 `python3 tests/check_docs.py` 检查相对链接（只是静态检查，不证明 Agent 已遵守）。

## 外部借鉴与约束

V0.2 **改写并借鉴** Agent Skills 规范、Anthropic `skill-creator`、Superpowers 的 `brainstorming`、`writing-plans`、`executing-plans`、`systematic-debugging`、`verification-before-completion` 等。映射和取舍见 [来源分析](docs/research-review.md)。

借鉴的是**触发条件、工作步骤、失败门槛、分层引用和测试方法**，不照搬外部工具专用命令、强制子 Agent 假设或大段 Prompt。

**已实现**：文本协议、路由目录、Project 核心规范、静态验证脚本和手工评估用例。  
**未实现**：宿主 CLI 适配、保证文件加载的运行时机制、真实模型 A/B 测试、自动并发一致性/日志压缩。V0.2 不是已验证的生产框架。
