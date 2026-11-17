# 生命周期

active = 正在推进；archived = 未完成但暂不推进；completed = 目标已达成。允许在三者之间转换，转回 active 同样需用户确认。

Agent 可主动建议状态变化，不能自行据沉默执行。用户已明确要求则直接执行，不重复问。先 resume 获取 token，再 status --status ... --reason '实际用户确认依据' --confirmed。迁移保留稳定 ID、所有文件及执行权限，重建 Index/History。

完成前按 acceptance.md 检查目标达成依据，再由用户确认完成。用户确认与技术验证是两件事：未验证必须明确标注，不能制造证据。目标发生实质改变时更新一句话说明与验收条件并记录决策。
