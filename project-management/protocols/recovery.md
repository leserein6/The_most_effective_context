# 冲突、故障与恢复

共享状态写入：全局本地 flock 串行化脚本操作；读取 token 后写入采用内容版本检查，拒绝旧 token。token 包括状态与日志、source/INDEX，不含 work 和其他 source 内容。因此正常产物修改不会阻断状态回写。

此保护面向遵守脚本的会话；不阻止编辑器直接写文件。代码/产物并发必须隔离文件范围或 worktree。跨机器/同步工具不共享本地 flock，Git 冲突由人工/Agent 显式合并；不要把工作区放实时双向同步盘并在两台机器同时写。

事务写前持久化 before-image；脚本异常自动回滚。进程中断留下 `.pm-runtime/pending.json` 时拒绝继续读写，先检查再运行 `recover --rollback`。回滚幂等，恢复原始内容和权限；随后 doctor。遇到完整目录操作中断，可留下空目录，不代表存在 Project。

这是本地进程中断恢复机制，不宣称数据库级跨设备事务或断电持久性。外部 API、邮件、付费调用等副作用不在回滚范围，重试前核对是否已生效。

Git 默认手动：检查 diff/status → 用户要求时 commit/push。冲突时比较各方项目状态与决策，合并 project.md 等权威文件后运行 init 重建派生索引、doctor，不能任选 ours/theirs 抹掉进度。不要自动 force push。
