# Project Work Items · 持久化实施工作项

## 三个概念必须分开

- **Project**：一个长期目标及其范围、验收和生命周期。
- **Work Item（WI）**：Project 为交付目标拆分出的、可独立验收的工作项，跨 Session 持久存在。只有值得追踪的工作才建 WI；简单对话和 one_off 不强制拆分。
- **Turn Task**：本轮用户交互的具体交付，不独立落盘；可通过 `work_item_ids` 关联零个或多个 WI。同一个 WI 可由多个 Turn Task 逐步完成。

`Mode` 是执行方法；不是 Task 或 WI 状态。

## 权威文件

`<project>/work-items.md` 是 WI 的唯一权威记录。格式为 `# Project Work Items` 标题后紧跟 `json` 代码块：

```json
{
  "schema_version": 1,
  "items": [
    {
      "id": "WI-01",
      "title": "实现双主体归并",
      "status": "pending",
      "depends_on": [],
      "acceptance": ["排序及游标边界符合已确认规格"],
      "evidence": [],
      "blocker": null,
      "next_action": "定位当前分页入口与复用点",
      "created_at": "由脚本生成",
      "updated_at": "由脚本生成"
    }
  ]
}
```

时间戳只是示意，不能原样作为实际实例写入。创建或更新时使用 `checkpoint` 的 `work_item_updates`，而不是手写全文；`pm.py` 负责生成与校验时间戳。

状态只有：`pending`（待开始）、`in_progress`（进行中）、`blocked`（阻塞）、`in_review`（待验收）、`completed`（具备本工作项完成证据）。**WI 完成不等于 Project completed**；项目状态仍由用户确认并通过 `status` 迁移。

- `depends_on`：引用本 Project 已存在或本轮一并创建的 WI-ID，不允许重复、引用自己、循环依赖；未完成前置项时不能开始实施/验收或标记完成。
- `acceptance`：至少一条可观察判据，不能以“代码写完”代替验收条件。
- `evidence`：`{kind, claim, source}` 列表，kind 为 `observed/cited/inferred/unverified`。新转为 `completed` 时，**本次更新必须新增 observed 证据**；脚本只校验结构与标记，真实性仍要由 Agent/审查者核验。
- `blocker`：仅 blocked 非空；解阻塞后清除。`next_action`：当前可执行动作，completed 时必须为空。
- 不自动删 WI。需求变更由 Agent 调整并在操作流水记录依据；无删除/重编号命令。

## 每轮 checkpoint（增量更新，不覆盖既有工作项）

普通 checkpoint 仍使用原有 `turn_id/mode/progress/next/operations/evidence/outcome` 字段，可额外写：

```json
{
  "work_item_ids": ["WI-01"],
  "work_item_updates": [
    {
      "op": "create",
      "id": "WI-01",
      "title": "实现双主体归并",
      "acceptance": ["满足已确认的游标和排序语义"],
      "depends_on": [],
      "next_action": "定位入口"
    }
  ]
}
```

下一轮可只更新其中一个工作项，例如：

```json
{
  "work_item_ids": ["WI-01"],
  "work_item_updates": [
    {
      "op": "update",
      "id": "WI-01",
      "status": "blocked",
      "blocker": "排序规则待用户确认",
      "next_action": "确认同时间戳记录的次级排序键"
    }
  ]
}
```

说明：两段是 checkpoint 的**局部字段示例**，调用脚本时仍须补齐原有必填字段。每轮同一 WI 最多更新一次，更新字段未指定时保留旧值；`evidence` 只追加，不清空。不存在的 WI 不能 update，重复 create 会拒绝；错误和版本冲突均在共享状态事务提交前检查。

`work_item_ids` 是当前 Turn Task 的关联，不代表状态变化；它也可以为空。没有 WI 的旧 Project 不会被推断为零剩余工作。第一次有 create 更新时才生成 `work-items.md`，**不要求重建已有项目**。

## 接续与验收

`resume ID` 返回 `work_items.tracked`、五类状态计数、未完成工作项和最近 10 个已完成工作项（最多展示 50 条）。更多条目按需读取文件；`work-items ID` 只读返回同样的工作项概览。

恢复时先读取 Project 定义、验收、决策、当前状态，再按依赖、阻塞和证据定位需要继续的 WI；不要根据 Turn Task 的完成自动推进 WI。若 WI 与真实代码/测试证据冲突，先复核再更新。

`state.md` 是项目级快照（整体进度、跨 WI 问题、下一步），不应重复维护另一份工作项列表；`logs/current.md` 保留每轮操作及 WI-ID 追溯。两者不能替代 `work-items.md`。
