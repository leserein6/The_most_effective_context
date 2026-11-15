# Evidence · Task 执行协议路由

**Evidence = 按任务类型加载的执行方法论**，不是长期 Project 数据，也不是“事实证据仓库”。进入本目录先选当前需要的方法，只读**匹配的 README**，不遍历所有子目录。

| 当前要解决什么 | 触发信号 | 加载 | 非触发 |
| --- | --- | --- | --- |
| 得到可核实的结论 | 核查事实、版本、源码、资料 | [research](research/README.md) | 单纯头脑风暴 |
| 消除影响决定的歧义 | 关键需求不清、显式 Grill-me | [clarify](clarify/README.md) | 信息已足够、只需直接答复 |
| 给出可审阅的设计 | 架构/规格/选型/方案权衡 | [design](design/README.md) | 用户已明确要求立即执行既定方案 |
| 改变实际文件或系统 | 修改代码、文档、配置、提交 | [execute](execute/README.md) | 只要建议、不授权修改 |
| 查找故障根因 | bug、失败测试、异常行为 | [debug](debug/README.md) | 不涉及异常的普通新增功能 |
| 宣称完成或通过验证 | 要说“修复成功”“测试通过”“已交付” | [verify](verify/README.md) | 没有完成声明的纯讨论 |

## 路由与组合

1. 以**用户本轮要求的结果**而非关键词选主 Evidence。
2. 一个 Task 可以分阶段需要多个 Evidence，但**按实际阶段顺序补载**，不因为可能涉及执行就一开始读六份。
3. **依赖优先**：修 bug 时先加载 Debug 诊断，明确根因再按需加载 Execute 实施；完成声明前按需加载 Verify。Project 创建中的关键模糊先使用 Clarify。
4. 当两个协议都相关时，先加载当前步骤所需的一个；仅有实际依赖时加载第二个。项目生命周期仍由 [Project Management](../project-management/README.md) 负责。
5. 简单、低风险、无需专项方法的回答可以只遵守全局入口；不要让分类本身成为开销。

**有歧义的路由样例**再读 [examples/routing.md](examples/routing.md)。该文件不是每次强制加载。
