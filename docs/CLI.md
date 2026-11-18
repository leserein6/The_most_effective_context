# 命令与数据契约

所有命令默认以 pm.py 上一级 workspace 为根；也可用 `python3 /绝对路径/scripts/pm.py --root /workspace路径 COMMAND`。示例 ID 和 token 是占位，正常由 Agent 读取实际值。

| 命令 | 用途 |
|---|---|
| init | 初始化或重建索引，不删除现有项目 |
| index / index --history | 读取活跃/非活跃 Index |
| list / list --all | 输出活跃/全部元数据 |
| create | 用户确认后新建 |
| resume ID | 恢复包、token、压缩提醒 |
| describe ID | 更新名称/一句话目标，并刷新索引 |
| checkpoint ID | 每轮保存当前状态、决策、知识、流水 |
| edit ID | 更新验收条件、知识或资料索引（项目状态迁移使用 status） |
| status ID | 用户确认后迁移状态，保留 ID 和内容 |
| compact ID | 原文归档、追加摘要、重置活跃日志 |
| promote ID | 确认后将公共知识纳入 conventions |
| doctor | 结构、索引、日志归档校验；报告本机 CLI 是否存在 |
| recover --rollback | 检查未完成事务后恢复原始文件 |

## 新建与写入示例

```bash
python3 scripts/pm.py create --id todo-cli --name '命令行待办工具' --type development --summary '支持添加、列出和完成本地待办' --confirmed
python3 scripts/pm.py resume todo-cli
python3 scripts/pm.py checkpoint todo-cli --expected 实际TOKEN --payload .pm-runtime/turn-001.json
python3 scripts/pm.py describe todo-cli --expected 实际TOKEN --summary '修订后的独立目标' --reason '用户明确修订目标'
python3 scripts/pm.py edit todo-cli --expected 实际TOKEN --document acceptance.md --file .pm-runtime/acceptance.md --reason '根据需求明确验收'
python3 scripts/pm.py status todo-cli --expected 实际TOKEN --status archived --reason '用户明确要求暂停' --confirmed
python3 scripts/pm.py compact todo-cli --expected 实际TOKEN --summary-file .pm-runtime/summary.md
python3 scripts/pm.py promote todo-cli --expected 实际TOKEN --title '可复用经验' --file .pm-runtime/candidate.md --reason '用户确认纳入' --confirmed
```

命令行静态例子的用户确认标志只是示范，不应未获真实确认就照抄执行。所有 shared-state 写入都要求 resume token；每次成功返回新 token。发生冲突要比较和合并，不盲目重试。

## checkpoint JSON

真实示例见 `examples/checkpoint.json`。其中：

| 字段 | 规则 |
|---|---|
| turn_id | Project 内唯一，小写字母数字/下划线/连字符，1..80字符 |
| mode | clarify/research/plan/execute/review/learn/orchestrate |
| progress / next / outcome | 必填非空文字 |
| operations | 必填非空字符串数组，详细有意义的操作 |
| evidence | 必填数组，可为空；每条 kind、claim、source |
| open_questions / notes / candidates | 可选字符串数组 |
| decisions | 可选；status 为 proposed/confirmed/superseded；text；确认或失效需 user_evidence |
| phase_end | 可选布尔值，重要阶段结束时触发压缩判断 |

confirmed 决策的 user_evidence 是调用者提供的依据，脚本不能识别真假。旧决策不删除，新增 superseded 记录说明被哪个决定替代。字段不认识会拒绝；进度描述未验证部分应明确标记。

输出为 UTF-8 JSON（index 输出 Markdown），错误写 stderr 并返回 2。写入有进程锁和事务回滚，失败后检查返回码。日志重复 turn_id 会拒绝，防止同轮重复追加。

## 文件约束

Project ID 全局唯一、稳定；状态目录迁移不改 ID。managed 路径不支持符号链接。外部源码仓库可在 work/README.md 登记绝对路径或仓库地址，不要靠符号链接接入。

脚本当前不提供 Project 类型重分类命令；创建时确认类型。若日后确需改类，先设计显式迁移与回归验证，不直接改目录与元数据使之失配。

## 外部 Prompt 资源（只读）

```bash
python3 scripts/prompt_library.py list --scenario implement
python3 scripts/prompt_library.py show superpowers-implementer
python3 scripts/prompt_library.py check
```

场景为 implement/review/research/author。list 只读元数据；show 校验正文、相对依赖及许可后显示选中原文和采用注意；check 校验全库。支持 `--root` 指定安装根目录，不依赖运行时网络。未知 ID、无匹配和哈希/路径异常返回非零。命令不执行上游脚本，不安装原生 Skill，也不代替主 Agent 填写授权与验收。

## 安装入口（scripts/install.py）

`--entry` 只决定生成哪个宿主入口，不复制规则正文：

| 值 | 生成文件 | 内容 |
|---|---|---|
| `codebuddy`（默认） | `CODEBUDDY.md` | `@agent.md`（嵌入模式为 `@.codebuddy/harness/agent.md`） |
| `agents` | `AGENTS.md` | 指向 `agent.md` 的入口说明 |
| `both` | 两个都生成 | 同上 |
| `none` | 不生成 | 只安装 `agent.md`，由用户自行改名/适配 |

`--mode workspace` 要求目标为空；`--mode project` 写入 `.codebuddy/harness/`，已有入口文件只有在 `--merge-entry` 时才追加受管块，否则拒绝覆盖。
