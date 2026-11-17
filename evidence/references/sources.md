# 方法来源与适配记录

核对日期：2026-11-17。源文件 URL 与读取时 Git blob SHA 在 [sources.json](sources.json)。这里记录采用了哪些机制，不把一张参考列表当成已经验证的能力。链接 main 会变化，可用 blob SHA 核对读取版本。下表记录此前改写所读取的具体文件。运行时可选的外部原文、固定 commit、许可与完整性记录另见 [Prompt 库](../prompts/README.md) 及其 catalog.json；不把历史来源清单全量载入。

| ID | 原仓库文件 | 采用机制 → 当前文件 | 没有照搬 / 本地改变 |
|---|---|---|---|
| S01 | mattpocock/skills · skills/productivity/grilling/SKILL.md | 决策依赖、同批可回答的问题集中询问、事实自行查 → clarify | 不要求无止境问完全部枝节；关键分歧消除即止；不把每次调查都强制委派 |
| S02 | mattpocock/skills · skills/engineering/code-review/SKILL.md | 固定审查基线、需求与标准双轴 → review / 共用委派包的审查字段 | 不绑定特定 issue tracker；没有规格不虚构；小审查可一人分两遍，不强制双 Agent |
| S03 | mattpocock/skills · skills/productivity/handoff/SKILL.md | 为接续保留必要状态、引用已有文档、去除敏感信息 → Project Logging | 不存临时目录作为唯一长期锚点；仍由 Project 管理摘要与完整原文 |
| S04 | obra/superpowers · skills/brainstorming/SKILL.md | 先调查现状、厘清目标和边界、具体取舍 → clarify / design | 不采用固定单题访谈、不为全部小修改强制设计审批、不启用视觉服务或自动 commit |
| S05 | obra/superpowers · skills/writing-plans/SKILL.md | 具体文件/接口/依赖/验证、可独立验收的工作项 → plan / plan Prompt | 不要求频繁提交、不把代码全文提前写入计划；工作项属于 Project 产物 |
| S06 | obra/superpowers · skills/executing-plans/SKILL.md | 按步执行、结果记录和接续 → execute | 不采用对全部冲突自行裁决的规则；已确认方向冲突先指出，关键未决问用户 |
| S07 | obra/superpowers · skills/systematic-debugging/SKILL.md | 复现、边界调查、可证伪假设、最小修复与复验 → debug | 连续两次无效修复回到调查是本地防循环约定，不是通用科学阈值 |
| S08 | obra/superpowers · skills/verification-before-completion/SKILL.md | 按声明寻找直接证据 → verify | 同一版本充分证据可复用，避免无变化仍机械重跑；区分脚本与真实模型效果 |
| S09 | obra/superpowers · skills/subagent-driven-development/implementer-prompt.md | 实现工作包、先查输入、实施/自查/回传，执行者不自行安排审查 → delegation | 不采用来源中的自动提交或绑定其任务脚本；无主会话上下文需具体输入包 |
| S10 | obra/superpowers · skills/subagent-driven-development/task-reviewer-prompt.md | 独立只读、报告待核、需求符合与代码质量分别判断 → review / orchestrate | 有具体风险可补查/运行针对性检查，不死守只看 diff；不把警告全视为缺陷 |
| S11 | anthropics/skills · skills/skill-creator/SKILL.md | 真实测试输入、旧版/新版对照、评价与迭代 → evals | 不宣称跑过其工具或目标模型；只有真实执行后才填写效果数据 |
| S12 | github/awesome-copilot · skills/acquire-codebase-knowledge/SKILL.md | 限定调查范围、可核实事实、未知显式记录 → research | 不要求每个窄问题都生成七份全仓文档，不依赖未安装扫描脚本 |

## 改写范围

本次是基于来源机制的中文场景化改写，不是直接安装来源 Skill。专用 Skill 工具名、宿主参数、状态存储、用户确认与 Git 权限按当前 workspace 实际能力改写。

工程风险清单、Project 锚定与状态、输出状态枚举和具体默认分支属于本地设计。Learn 的前置/复习/独立练习边界来自用户要求，示例交替、具体与抽象连接、解释性问题参考 IES 指南；Go例子对应官方语言规范。方法依据不证明目标模型教学效果。上述本地方法是中文适配；新增外部原始资源库另行保留完整原文、必要依赖与各上游 MIT 版权和许可证，不改写原始快照。

## 模型适配假设

用户目标环境是 CodeBuddy 中使用 DeepSeek V4.1 Flash 系列（名称按用户表述记录）。本次针对“执行能力足够、需要明确推断和交接步骤”的使用反馈设计，不据此作公开性能结论或推定 API 模型 ID。

具体设计：一次选当前方法；输入列出实际值与来源；判断写成条件分支；依赖不满足不得抢跑；结果有固定格式；证据绑定产物版本；失败有恢复位置。无需展示私有思维链，不要求模型自己补全缺失业务规则。

所有新规则仍需目标模型场景验证；增加字数本身不代表提高效果。若实测显示多余步骤造成负担，依据失败轨迹精简相应段落。

## 方法知识与索引设计的补充依据

以下与Prompt仓库机制分开：属于方法知识/规范参考，不是当前客户端已安装的Skill。

| ID | 一手/权威资料 | 对应内容与边界 |
|---|---|---|
| S13 | [FActScore](https://aclanthology.org/2023.emnlp-main.741/) | Research按原子事实核实；未运行评分器，不推广原论文实验指标 |
| S14 | [CoVe](https://aclanthology.org/2024.findings-acl.212/) | Research独立验证问题；模型自答不等于外部证据 |
| S15 | [SEP Abduction](https://plato.stanford.edu/entries/abduction/) | 区分解释性推断与确定证明；具体工程规则是操作化适配 |
| S16 | [IES学习指南](https://ies.ed.gov/ncee/WWC/PracticeGuide/1) | Learn中的示例/练习交替、抽象具体联系、解释性问题；用户练习偏好优先 |
| S17 | [Go Calls](https://go.dev/ref/spec#Calls) | Learn的参数绑定例子，不预设用户已经掌握全部语法 |
| S18 | [Agent Skills规范](https://agentskills.io/specification) | 入口/正文/附属资源渐进加载；Evidence并非原生Skill包 |
| S19 | [Anthropic上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 按相关性获取上下文；五类Task和两级索引为本地设计，效果待实测 |
