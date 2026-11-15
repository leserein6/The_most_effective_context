# Project Schema · 字段索引

**加载条件**：要创建、校验或修改 `project.yaml` 时阅读；仅恢复项目摘要时通常可直接查看实例，不必读全字段契约。

## Canonical shape (V0)

```text
schema_version
id, name
intent: problem, desired_outcome, success_signals
scope: in, out
deliverables, constraints
state: phase, summary, verified_outputs, next_action, blockers, updated_at
references: decisions, journal, evidence
```

实例遵守 [模板](../templates/project.yaml)。字段命名应一致；不额外增设未经定义的“同义字段”。

## 字段规范按需加载

| 操作影响 | 读取 | 规范内容 |
| --- | --- | --- |
| 新建、改名、修改项目意图、交付物、范围 | [definition.md](definition.md) | **Definition / Extraction / Update / Constraints** |
| 更新阶段、进度、成果证据、阻塞、下一步、文件引用 | [progress.md](progress.md) | **Definition / Extraction / Update / Constraints** |
| 提取项目意图困难或需要变更对照案例 | [intent.md](../examples/intent.md) | 输入→判断→正确/错误示例 |
| 判断是否形成经过验证的进展 | [progress.md Few-shot](../examples/progress.md) | 进度更新/未验证/中断案例 |

## 不变量

1. `schema_version` 用于辨识数据结构；不允许用未知字段静默替换已有字段。
2. `id` 是稳定且唯一的项目标识。 `name` 是面向用户、可修改的标题。
3. **只有正式确认之后的 Project 才有正式持久化实例**；创建前草案在会话中呈现，不写入 `projects/`。
4. `state.phase` 只包含 `active | paused | completed | archived`。未确认草案不使用正式 `phase: draft` 实例伪装已创建。
5. **未知与否定不同**：未知内容使用 `null` 或明确标注待定；不能把不存在的事实填成空列表而暗示用户明确排除。
6. 在 Project 实例中保存**当前快照与引用**，不要复制完整聊天、所有操作过程或整套协议。
7. 所有链接/证据路径写入前应确认实际存在；路径引用只是定位方式，不代表已验证其内容。
