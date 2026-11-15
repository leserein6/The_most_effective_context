# Project Maintain · 持续维护协议

**激活条件**：用户要求更新已有 Project，或已经产生了应同步到项目当前状态的真实成果/决策。普通聊天不必每轮强制写盘。

## 状态变更决策

1. **定位并核对现状**：读取目标 `projects/<id>/project.yaml`。未找到则说明；若多个候选项目，先确定身份。按本轮修改类型只读 [Definition](../schema/definition.md) 或 [Progress](../schema/progress.md)，必要时再读另一份。
2. **分类本轮变化**：`discussion`（讨论）、`proposal`（建议）、`confirmed-decision`（用户决定）、`verified-progress`（有证据的进展）、`blocker`（真实阻塞）。
3. **只改必要字段**：
   - 讨论或纯提议：通常不改持久化事实。
   - 进展/阻塞：依实际证据更新 `state` 与引用，下一步区分 confirmed/proposed。
   - 核心问题、期望成果、重大范围或硬约束变化：**展示旧值→新值→影响，用户确认后再写**。
4. **检查冲突**：写入前确认读取的版本仍为最新；若其他 Session 已改动，重新比较，避免覆盖他人更新。V0 仅是指令，没有事务锁保证。
5. **写入与核验**：修改受影响字段，保留未触及内容；重新读取，核对实际结果及所指证据文件。
6. **反馈**：说明变更了什么、是否确认、引用何处、未解决的问题；未写入不得声称更新成功。

## 判断边界

- 一项普通功能实现不自动改变长期项目意图。
- 只写了代码、未测试 → 最多记为待验证，不能列入 `verified_outputs` 的“测试通过”。
- 单轮 Task 不单独持久化；若未来启用详细项目日志，日志是 Project 的工作过程，不是 Task 数据库。
- 不要求把完整对话、所有工具输出塞进 `project.yaml`。

需要判断“这句话到底是变更意图还是普通任务”时，按需读取 [Intent Few-shot](../examples/intent.md)；需要判断成果是否可称验证完成时读 [Progress Few-shot](../examples/progress.md)。
