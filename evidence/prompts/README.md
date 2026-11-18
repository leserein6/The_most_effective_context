# Prompt 库：外部原文与本次任务输入

主 Agent 派发子任务时读本索引，按当前职责选择一份外部原文；已读且版本未变可复用。不把全库发送给子 Agent，不自动安装原生 Skill。库中有真正的上游原始 Skill/Prompt，独立保留在 `external/<owner>/<repo>/`，不是我们重新写的角色模板。

**与用户自有 Prompt 的区别**：本目录 `external/` 仅保存第三方固定版本原文；运行时适用的领域知识位于 [CodeBuddy Skills](../../.codebuddy/skills/)。历史 Prompt 的去重与整理记录保留在维护者源码仓库，不随运行包安装。不要把二者混入同一 catalog，也不在每轮同时加载。

## 按场景选择

| 当前需要 | 选取的原始资源 | 采用边界 |
|---|---|---|
| 派发明确的实现工作项 | `superpowers-implementer` | 参考实现/自查/回传；不继承原文自动 commit、模型参数或上游状态枚举 |
| 独立审查固定产物 | `superpowers-task-reviewer` | 参考规格/质量双轴；不假装上游 brief/diff 脚本已安装，不把所有警告机械判为缺陷 |
| 查具体事实、源码、文档 | `matt-research` | 参考一手来源和逐项引用；由主 Agent 派发，研究者不再次派发 |
| 编写/调整给 AI 的指令、Skill 或协议 | `matt-writing-for-agents` | 参考触发条件、完成条件与去重；作者经验未在目标模型验证，不每次委派都读 |
| 用户明确要求代码库级调查 | `copilot-acquire-codebase-knowledge` | 原文与全部相对依赖保留；窄修复不选它，不自动扫描全仓或生成七份文档 |

固定版本、原文位置、许可证、依赖、采用点和不兼容项以 [catalog.json](catalog.json) 为准。来源是 [Superpowers](https://github.com/obra/superpowers)、[Matt Pocock Skills](https://github.com/mattpocock/skills)、[Awesome Copilot](https://github.com/github/awesome-copilot)，每份原文按 commit 固定，保留 MIT 版权和许可。

可直接按 catalog 的 `local_path` 读取；也可用只读命令先筛选，再只展开选中正文：

```bash
python3 scripts/prompt_library.py list --scenario implement
python3 scripts/prompt_library.py show superpowers-implementer
python3 scripts/prompt_library.py check
```

`list` 只返回元数据，`show` 校验并显示原文/调用注意，`check` 校验所有已收录正文、附属文件和许可证的完整性；都不执行上游脚本或启动 Agent。命令从安装根目录运行，外部调用可用绝对脚本路径。

## 把参考变成本轮可执行指令

原文供主 Agent 选取方法和措辞；实际派发使用 [共用委派包](delegation.md) 加 [Orchestrate 的组装检查](../methods/orchestrate.md)。本地方法正文规定如何执行，原文不得改变用户授权、项目状态规则、工具可用性或写入范围。上游所称已安装工具/模型、自动提交和递归派发都不能凭资源文字成立。

多步骤计划的产物格式用 [plan](plan.md)；日志摘要的输入输出唯一由 [Project Logging](../../project-management/protocols/logging.md) 规定。实现/研究/审查共用委派字段，不再各复制一套执行步骤。

公共 Prompt 更新按 [知识积累协议](../../project-management/protocols/knowledge.md)；本次工作包留项目 `work/`，记录外部资源 ID/版本和采用点。原始快照只通过明确更新流程替换，不随 `main` 自动变化。收录/哈希通过不等于目标 DeepSeek 模型效果已通过。
