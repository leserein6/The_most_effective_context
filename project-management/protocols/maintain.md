# 每轮持久化

本协议仅在已锚定真实 active Project 后执行。尚在归属澄清或用户明确确认“不归属任何 Project”的例外时，不能凭空创建状态或调用 checkpoint；允许按本轮授权回答，但须说明未做 Project 持久化。例外不能变成永久的伪 Project ID。

用户未明确改变 Project 状态时，完成本轮 Task 不等于 completed。每轮回复前由主 Agent 汇总一次写入；子 Agent 不写共享项目状态。

1. 首次 resume 保留 token 和读到的状态基线。
2. 本轮收集有意义的操作流水、产物、验证、决策和剩余问题。不要记录模型私有思维过程、凭据或无意义鼠标点击。
3. **优先通过标准输入**传入本轮 checkpoint JSON：`python3 scripts/pm.py checkpoint ID --expected TOKEN --payload -`（例如终端 heredoc），避免生成临时文件。字段参考 [WI 和 checkpoint 契约](../schema/work-items.md)；运行包不包含 docs/。必须使用文件时可传 `--payload FILE`，文件归调用方所有，脚本不会自行删除。历史 `.pm-runtime/turn-*.json` 可用 `pm.py clean` 预览；只有确认已持久化、超过保留时间的旧输入才列入清理候选。未知文件和目录永不自动清理。
4. 调用 checkpoint --expected TOKEN --payload -（或 FILE）。按需携带 `work_item_ids`（本轮 Turn Task 关联）和 `work_item_updates`（增量 WI 创建/更新）；自动更新状态、决策、知识、详细流水和 Index。重复 turn_id 被拒绝。
5. CONFLICT 时重新读取最新状态，比较基线与变化，合并自己与他人真实成果后再写；不能仅刷新 token 强行重试。
6. 已确认决策需 user_evidence，建议写 proposed，旧决定保留并标失效关系。创建/状态迁移分别按 [Create](create.md)/[Lifecycle](lifecycle.md)，不由 checkpoint 代替。
7. 工具失败时解决或报告未保存，不能对用户宣称记录成功。

元数据名称/一句话目标变化调用 describe，验收条件和资料索引用 edit；改名前先处理语义冲突。Project 类型创建后保持稳定，确需改类先做备份并制定显式迁移，不静默重建或丢历史。

开发型需求按[测试验收](../../evidence/testing/acceptance.md)在现有 checkpoint 的 evidence 中引用候选版本、测试方法选择与设计审查结论、运行报告以及残余风险；记录关键失败和待验证项。Project 不保存独立 Turn Task 数据库，也不复制业务测试代码。需要跨轮追踪的工作使用 `work-items.md`，只有明确证据并满足依赖时才标记 WI completed。项目级 `state.md` 不复制第二套 WI 状态。
