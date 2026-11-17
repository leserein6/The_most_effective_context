# 实际验证结果

仓库整合版本：The_most_effective_context V1；入口 agent.md；运行时 project-management。

执行时间：2026-11-17T15:54:58+08:00（北京时间）

环境：Python 3.12.14 / Linux；Mac 真实 CLI 待实测。

## 19 项自动测试

```text
test_conflicts_reject_before_any_write (test_install.InstallTests.test_conflicts_reject_before_any_write) ... ok
test_preview_then_install_and_idempotent_merge (test_install.InstallTests.test_preview_then_install_and_idempotent_merge) ... ok
test_compaction_preserves_exact_bytes (test_pm.ProjectFlow.test_compaction_preserves_exact_bytes) ... ok
test_concurrent_updates_only_one_commits (test_pm.ProjectFlow.test_concurrent_updates_only_one_commits) ... ok
test_crash_requires_explicit_recovery (test_pm.ProjectFlow.test_crash_requires_explicit_recovery) ... ok
test_document_edit_and_index_regeneration (test_pm.ProjectFlow.test_document_edit_and_index_regeneration) ... ok
test_duplicate_turn_rejected_after_refresh (test_pm.ProjectFlow.test_duplicate_turn_rejected_after_refresh) ... ok
test_full_lifecycle_and_cross_session (test_pm.ProjectFlow.test_full_lifecycle_and_cross_session) ... ok
test_invalid_payload_has_no_partial_writes (test_pm.ProjectFlow.test_invalid_payload_has_no_partial_writes) ... ok
test_long_term_definition_survives_progress_updates (test_pm.ProjectFlow.test_long_term_definition_survives_progress_updates) ... ok
test_no_unconfirmed_create_or_status (test_pm.ProjectFlow.test_no_unconfirmed_create_or_status) ... ok
test_public_promotion_requires_confirmation (test_pm.ProjectFlow.test_public_promotion_requires_confirmation) ... ok
test_recovery_rejects_path_escape (test_pm.ProjectFlow.test_recovery_rejects_path_escape) ... ok
test_stale_state_and_direct_file_edit_conflict (test_pm.ProjectFlow.test_stale_state_and_direct_file_edit_conflict) ... ok
test_status_preserves_executable_permissions (test_pm.ProjectFlow.test_status_preserves_executable_permissions) ... ok
test_summary_update_refreshes_index (test_pm.ProjectFlow.test_summary_update_refreshes_index) ... ok
test_symlink_and_traversal_rejected (test_pm.ProjectFlow.test_symlink_and_traversal_rejected) ... ok
test_three_types_and_unique_identity (test_pm.ProjectFlow.test_three_types_and_unique_identity) ... ok
test_work_outputs_do_not_invalidate_shared_state_token (test_pm.ProjectFlow.test_work_outputs_do_not_invalidate_shared_state_token) ... ok

----------------------------------------------------------------------
Ran 19 tests in 4.329s

OK
```

## 三类型项目及真实代码产物演示

```text
{
  "demo_passed": true,
  "projects": [
    {
      "schema_version": "1.0",
      "id": "rpc-report",
      "name": "rpc-report",
      "type": "one_off",
      "summary": "演示目标：rpc-report",
      "status": "active",
      "revision": 1,
      "created_at": "2026-11-17T07:54:58+00:00",
      "updated_at": "2026-11-17T07:54:58+00:00"
    },
    {
      "schema_version": "1.0",
      "id": "go-study",
      "name": "go-study",
      "type": "learning",
      "summary": "演示目标：go-study",
      "status": "archived",
      "revision": 2,
      "created_at": "2026-11-17T07:54:58+00:00",
      "updated_at": "2026-11-17T07:54:58+00:00"
    },
    {
      "schema_version": "1.0",
      "id": "calculator",
      "name": "calculator",
      "type": "development",
      "summary": "演示目标：calculator",
      "status": "completed",
      "revision": 4,
      "created_at": "2026-11-17T07:54:58+00:00",
      "updated_at": "2026-11-17T07:54:58+00:00"
    }
  ],
  "artifact_check": "2 checks passed",
  "archive_verified": true,
  "note": "独立临时目录演示；未创建真实用户项目，未启动模型或 CodeBuddy。"
}
```

## 仓库自检

```text
{
  "ok": true,
  "projects": 0,
  "codebuddy_installed": false,
  "agent_behavior_verified": false
}

```

全体 Markdown 本地链接检查通过。没有在仓库中创建真实用户 Project；示例仅在临时目录中运行。
