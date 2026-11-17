# 通用任务执行机制

本文件只导航；不一次加载所有模式、所有项目、全部历史日志。

每轮顺序：
1. 检查 `project-management/Index.md`，按 [项目归属协议](../project-management/protocols/routing.md) 锚定项目。
2. 按 [上下文协议](../project-management/protocols/resume.md) 恢复目标、进度、已确认决策、验收条件、问题和下一步。
3. 明确本轮 Task 和可验证结果；Task 仅在本轮上下文存在，可在项目日志中留痕。
4. 根据 [模式索引](README.md) 选择/组合模式，只读相关模式协议；简短告知，不逐次请求批准。
5. 有关键歧义或决策冲突则先澄清，否则执行。多 Agent 按 [协作协议](protocols/delegation.md)。
6. 按 [证据协议](protocols/validation.md) 验证，不能直接采信 Subagent 的成功声明。
7. 按 [持久化协议](../project-management/protocols/maintain.md) 记录本轮进度与流水；阶段结束或容量达标时按 [日志协议](../project-management/protocols/logging.md) 判断压缩。
8. 回复结果、验证、剩余阻塞。建议第一行简短显示 `Project: ID | Task: … | Mode: …`，不要倾倒内部实现细节。

脚本写入失败必须明确告知“结果已产生但项目状态未保存”，解决失败后再声明保存成功。
