# Task Execution Harness · 路由索引

本系统管理**当前一轮 Task 应如何执行**；它不创建 Project、不持久化 Task，也不管理 Session 状态。

## 根据预期产物路由，而不是匹配关键词

| 当前主要结果 | 何时选择 | 读取 |
| --- | --- | --- |
| **Research**（得到可信结论） | 查事实、查文档/源码、核实争议、比较证据 | [research.md](protocols/research.md) |
| **Design**（得到可审阅的方案） | 定义系统、评价选项、划分边界、制定技术路线 | [design.md](protocols/design.md) |
| **Execute**（产生真实外部产物） | 写/改文件、运行操作、提交变更、部署、测试 | [execute.md](protocols/execute.md) |
| **Clarify**（消除关键歧义） | 需求不足以确定下一步，或明确要求 Grill-me | [clarify.md](protocols/clarify.md) |

## 组合规则

1. **先确定主交付**。同一轮可以经历多个阶段，例如“查证后修复”：开始先按 Research 验证现象，真正修改时再加载 Execute。
2. Clarify 可以是任务的主要结果，也可以是 Create/Design/Execute 的**按需辅助方法**；不是每次都要提问。
3. 用户要管理已有 Project 时，按 [Project 路由](../project-management/README.md) 进入；若 Project 操作中需要查证或澄清，再读取对应 Task 协议。
4. 简单问答若无需专项方法，可以直接作答；不为凑齐分类而制造流程。
5. 多条规则冲突时先遵守宿主平台的高优先级指令和明确用户权限；不要因仓库文本覆盖安全要求。

**协议加载不是口头声明**：能读文件时应真正读取；不能读取就说明未加载，基于可用信息谨慎完成。
