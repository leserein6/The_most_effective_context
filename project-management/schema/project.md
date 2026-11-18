# Project Schema · V1 文件映射

仅在创建、编辑定义或校验实例时加载；普通恢复用 resume 即可。

当前实例路径：`project-management/projects/<status>/<type>/<id>/`。不再使用 V0.2 YAML 实例作为运行时数据。三种 status 是 active/archived/completed；没有独立 paused，归档即未完成但暂停推进。

| 文件 | 当前职责 | V0.2 对应概念 |
|---|---|---|
| project.md | 首个 JSON 代码块保存 schema_version、id、name、type、summary、status、revision、created_at、updated_at | Identity 与简短目标/生命周期 |
| definition.md | 问题、期望结果、范围、交付物、硬约束；未知显式待定 | intent / scope / deliverables / constraints |
| acceptance.md | 可观察验收条件 | intent.success_signals |
| state.md | 真实进度、未解决问题、下一步；建议须标建议 | state.summary / next_action / blockers |
| decisions.md | proposed/confirmed/superseded 与真实用户依据 | references.decisions |
| logs/current.md | 操作流水、验证证据、结果与限制 | references.journal / verified_outputs |
| logs/summary.md 与 archive/ | 可恢复摘要、完整原文与哈希 | 历史引用 |
| source/INDEX.md | 可定位资料、版本、用途 | references.evidence |
| notes.md / knowledge-candidates.md | 项目知识 / 公共积累候选 | 新增分离职责 |

## 不变量

稳定 ID 全局唯一，名称可修改。Index/History 由 project.md 派生；修改名称或一句话目标用 describe，更新长定义与验收用 edit。所有共享状态写入需 expected token，冲突重读比较合并。

正式创建需用户确认；未知不等于否定；建议不等于确认；写了文件不等于通过验证；完成本轮不等于项目完成。引用不是真实性证明，需要时回查实际内容。

项目管理命令通过 `python3 scripts/pm.py --help` 查看；字段提取见 [Definition](definition.md)，进度判断见 [Progress](progress.md)。旧 YAML 模板仅历史参考，旧示例中的字段名按本表理解。
