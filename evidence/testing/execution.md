# 运行与证据

在业务仓库确认测试入口、依赖和夹具，选与风险匹配的真实环境。复用已有测试框架。支持输出 JUnit XML 时，可用随安装提供的 [test_gate.py](../../scripts/test_gate.py) 将一组关键条件与本次运行绑定。其他框架保留原始报告并由 Verify 按同样的条件逐项核对。

## 测试方法建议辅助（可选，不替代设计）

使用标准库脚本 scripts/testing_strategy.py。输入 schema 为 testing/strategy-input-v1，包含 change_id 及 claims 数组；每项包括 id、source、claim、impact（low/medium/high/critical）和 features（参见脚本定义），另建议 oracle、counterexample、environment。

    python3 <Harness>/scripts/testing_strategy.py --input <业务仓库输入.json>

可从 [独立示例](examples/strategy-input.json) 参考格式。输出固定为 DRAFT_UNREVIEWED，仅给出候选方法和证明义务。审查者必须补齐规格、oracle、测试用例、覆盖分母。执行器不会核实是否漏掉受影响需求。

## 验收计划

```json
{
  "schema": "testing/v1",
  "criteria": [
    {
      "id": "BOOK-2",
      "source": "书单需求 R1：空书名使整批失败",
      "expected": "报告错误；重开书库仅见导入前内容",
      "cases": ["ReadingList::test_rejected_batch"]
    }
  ]
}
```

每项至少绑定一个真实 JUnit `classname::name`，映射多个用例表示全部必须成立。写计划时先核对测试框架报告里的实际名字。缺少关键手工检查或测试尚不可运行时，另列在总验收中。运行器不会自行发现计划漏写的要求。

在业务仓库工作目录使用以下调用形态。计划与测试入口使用真实路径；候选标识由调用端提供。干净 CI checkout 传运行中的提交 SHA，本地未提交改动应传能定位该工作树内容的快照标识。计划、命令参数和日志中不要放凭据。

```text
python3 <Harness>/scripts/test_gate.py --plan <计划.json> --candidate <候选版本> --out <全新目录> -- <仓库测试命令及参数>
```

程序直接传递参数，替换参数中的字面量 `{junit}`，同时设置 `HARNESS_JUNIT` 指向本次 XML。框架选项例如 pytest 的 `--junitxml={junit}`。只使用已核实的适配命令；结果要求无命名空间的 testsuite/testsuites XML，必测 testcase 有 classname、name 和标准的 failure/error/skipped 节点。其他报告格式先作明确适配。每次运行创建独占目录，保留 `plan.json`、`run.log`、框架生成的 `junit.xml` 及 `result.json`。后者包含计划哈希、候选标识、平台、命令、进程返回码、逐项结果；另记录影响结论的依赖版本、夹具和配置。中断未产生 result.json 时按未验证处理。

| 结果 | 程序退出码 | 处理 |
|---|---:|---|
| PASS | 0 | 命令成功且计划内全部用例获得唯一通过结果，报告中无错误或失败 |
| FAIL | 1 | 报告有断言失败，包括同轮检出的既有回归；查看实际差异和影响 |
| UNVERIFIED 或输入错误 | 2 | 命令、环境或报告有缺口，或必测项缺失、重复、跳过。阅读结果和日志；无有效结果文件也不能宣布通过 |

CI 使用程序退出码作为 job 状态，并在失败时保留产物。将 PR 检查设为必需由业务仓库的合入规则决定。独立核对断言、环境和报告来源仍是 [验收](acceptance.md) 的职责。
