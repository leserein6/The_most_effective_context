# 协议职责与收拢记录

入口、方法、任务参数、外部参考、项目数据各有不同职责；相同规则不在多处维护正文。本页面向维护者，不加入每轮必读链。

| 唯一正文位置 | 负责的问题 | 其他位置怎样引用 |
|---|---|---|
| agent.md / entry/routes/ | 本轮做什么、归属与何时读哪个方法 | 不另写一套全局 workflow |
| evidence/methods/ | 当前问题怎样思考、执行和判断 | 角色入口与模板只指向对应方法 |
| evidence/prompts/delegation.md | 本次工作项的真实输入、权限、验收与交付格式 | 实现/研究/审查仅列必要差异，不各抄执行步骤 |
| evidence/prompts/catalog.json 与 external/ | 外部原始 Skill/Prompt 的选择、固定版本与许可 | 原文只读参考，不自动激活；不能覆盖本地授权 |
| .codebuddy/skills/*/SKILL.md | 按 Go/RPC/金融领域触发的用户历史 Prompt 改编专项知识 | Review 按需链接，不重复规格/证据两轴流程；映射见 docs/Prompt_inventory.md |
| evidence/references/evidence-contract.md | 回传证据分类和状态含义 | 方法与工作包引用同一契约 |
| project-management/protocols/ | 长期记录的归属、创建、恢复、写入、迁移与压缩 | 方法收尾链接操作协议，不重写脚本事务细节 |

本次删除 entry/workflow.md、evidence/references/collaboration.md 两份重复说明；实现/研究/审查三份包装模板合为共用委派包；压缩 Prompt 的四栏输入输出归入 Project Logging。原生 worker/reviewer 只保留职责路由和独立调用所需权限边界。Project Routing 不再复制 Create 的字段与确认步骤。

保留的相近词并非重复职责：Verify 判断“完成声明有无证据”，Lifecycle 处理“已确认状态怎样迁移”；Research 查事实，Project source/INDEX 只登记资料；审查结论与 DONE 等回传状态也不同。不能为了少文件而把它们合成一份大协议。

外部库首批五份来自三个上游仓库，正文、相对依赖和 MIT 许可原样保留；catalog 记录固定 commit、Git blob SHA、SHA256、采用点和不兼容项。方法来源清单记录历史改写依据，catalog 负责运行时可选资源，不混成一套全量必读来源。

原有外部上游原文和用户历史 Prompt 需区别对待：用户历史资产整理在 [复用清单](Prompt_inventory.md)，三份通用专业内容以本地原生 Skill 提供；针对一次迁移/限流改造的 Prompt 不引入。

此前只调整协议职责与外部资源选择；首次保存位置配置、选择性安装、Project 创建模板外置未在本次实现。仍不能把 Prompt 中的 HARD GATE 当作程序拦截，也没有目标模型效果数据。
