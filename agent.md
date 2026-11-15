# Agent 全局入口（V0）

> 本文件是通用 **Agent 入口协议**，不是 Project 实例，也不是某个 CLI 专属文件。使用前须在 Agent/CLI 的实际配置中显式加载本文件；不同产品不保证自动识别 `agent.md`。

## 全局最小规则

1. **锚定本轮 Task**：结合用户当前输入和必要历史，提炼这一轮要达成的主要任务；不可凭空扩大范围。Task 是本轮临时工作锚点，不自动持久化。
2. **对用户可见**：在正式回答中简短标明 `本轮 Task：...`，让用户容易发现理解偏差。Task 发生变化时相应更新。
3. **按需加载**：先读 [harness/README.md](harness/README.md) 识别任务类型，然后只读匹配的执行协议；非当前任务所需文档不加载。
4. **独立的 Project 子系统**：只有用户意图涉及创建、维护、恢复或查询长期 Project 时，额外读 [project-management/README.md](project-management/README.md)，按该入口选择操作协议。不要把全局 Task 与 Project 混为一谈。
5. **可验证性**：明确区分用户确认、现有证据、待核实事实和建议；未真正执行/写入/验证时不能声称完成。

## 加载边界

- README / INDEX 提供路由与触发条件，不复制完整协议。
- 协议只在相关任务中激活；Few-shot、Schema、项目历史按执行步骤按需读取。
- 同时涉及多个任务类型时，先确定主任务；需要次级方法时再补载对应协议，避免全量预加载。
- 用户修改或否定 Task 理解时立即纠正，不把之前的错误理解持久化。

下一层入口：[AI 执行协议](harness/README.md) | [Project 管理协议](project-management/README.md)。
