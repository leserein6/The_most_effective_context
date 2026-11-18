# Task锚定与两级方法索引

## 规则放在哪里

Project、Task、Mode 的**唯一执行规则**见 [agent.md](../agent.md#每轮先锚定-task)，不在此页逐字重复。

关键边界：Project ID 必须是真实 active 项目；History 只用于经确认的归档恢复/完成重开；`待确认` 仅用于提出具体选择的当轮；之后需真实 active Project 或用户确认且写明理由的“无 Project”例外。没有真实 Project 时不运行 checkpoint，不能为满足显示要求创建虚构项目。

Task锚定与一级路由都属于入口职责；Project归属与本轮Task结果分开处理。

## 实际读取链

CODEBUDDY.md（CodeBuddy 优先）/ AGENTS.md（兼容） → agent.md（唯一规范正文）→ entry/routes/对应类型.md（二级场景路由）→ evidence/methods/当前方法.md → 必要Prompt/参考。委派额外进入 [Prompt 库](../evidence/prompts/README.md) 的场景索引，选一份外部原文，再填共用工作包；子 Agent 只读工作包指向的当前方法。

Project Index与项目状态是另一条数据加载线：每轮按用户要求检查Index，项目操作按需加载管理README。不会因为选了Task类型就新建Project或Task数据库。

一级类型：answer（理解/调查）、proposal（方案）、change（实际改动）、assess（评估）、learn（学习）。这是本仓库的工程设计，按交付结果而非动作分类；改功能时读源码不意味着Task变调查，用户改交付目标才重分类。

clarify/research可跨组解决意图/事实缺口；verify是完成检查；orchestrate是协作方式。两级索引只描述触发与去向，不复制正文，不强制一个Task把所有协议串行走完。

## Project、Task 与 Mode

Project 是跨交互保存的目标，Task 是本轮预期结果，Task 类型是入口临时标签，Mode 是当前工作方式；不能互相替代。checkpoint 的模式映射由根入口规定。Project 的恢复与写入动作只按管理协议执行，方法正文不重写它们。完整职责与删并记录见 [协议边界](Protocol_boundaries.md)。

## 上下文成本与限制

不把十份正文全量注入。已明确方法可直达；已加载且仍适用的静态规则可复用；压缩丢失或版本变化重新读取。分层文件结构不等于实际推理成本必然下降，需观察真实客户端读文件轨迹、错误路由与上下文开销。

## 设计依据

- [Agent Skills规范的渐进加载](https://agentskills.io/specification)：参考元信息、激活指令、必要附属资料的分层；Evidence不是原生Skill安装包。
- [Anthropic上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)：参考按任务相关性获取上下文，而非全量载入。

五类Task、文件名与跨组规则是本仓库适配，非上述来源的强制分类。仍由模型读取和遵守，未实现强制拦截器，不宣称目标模型效果已通过。
