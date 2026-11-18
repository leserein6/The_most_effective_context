"""Deterministic method-routing regression, distinct from model behavior evals."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "testing_strategy.py"
spec = importlib.util.spec_from_file_location("strategy_module", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def claim(**overrides):
    base = {
        "id": "C1", "source": "requirement-1",
        "claim": "After a failed transaction no partial changes persist",
        "impact": "high", "features": ["persistence", "concurrency"],
        "oracle": "approved contract R1",
        "counterexample": "a partially committed batch",
        "environment": "real local database",
    }
    base.update(overrides)
    return base


def plan(*claims):
    return {"schema": "testing/strategy-input-v1", "change_id": "D-1", "claims": list(claims)}


class StrategyTests(unittest.TestCase):
    def run_plan(self, *claims):
        return module.build_strategy(plan(*claims))["claims"]

    def test_persistence_concurrency_selects_actual_failure_methods(self):
        one = self.run_plan(claim())[0]
        self.assertEqual([x["id"] for x in one["method_candidates"]], ["DB", "CON", "ST", "REV"])
        self.assertEqual(one["assurance_status"], "UNVERIFIED")

    def test_boolean_critical_includes_mcdc_independent_review(self):
        one = self.run_plan(claim(impact="critical", features=["boolean-decision", "critical-decision"]))[0]
        self.assertEqual([x["id"] for x in one["method_candidates"]], ["DT", "BR", "MCDC", "REV"])

    def test_lightweight_input_change_does_not_force_deep_methods(self):
        one = self.run_plan(claim(impact="low", features=["input-domain"]))[0]
        self.assertEqual([x["id"] for x in one["method_candidates"]], ["EP", "BVA"])

    def test_accessibility_routes_to_accessibility_evaluation(self):
        one = self.run_plan(claim(impact="medium", features=["accessibility"]))[0]
        self.assertEqual([m["id"] for m in one["method_candidates"]], ["ACC"])

    def test_missing_oracle_is_explicitly_unresolved(self):
        one = self.run_plan(claim(oracle=""))[0]
        self.assertTrue(any("oracle:" in text for text in one["unresolved"]))
        self.assertEqual(one["design_status"], "UNVERIFIED")

    def test_multi_feature_union_and_stable_order(self):
        one = self.run_plan(claim(features=["stateful", "concurrency", "remote-failure"]))[0]
        self.assertEqual([x["id"] for x in one["method_candidates"]], ["ST", "MBT", "CON", "FI", "REL", "REV"])

    def test_different_claims_are_not_collapsed(self):
        result = module.build_strategy(plan(claim(), claim(id="C2", features=["security"])))
        self.assertEqual(len(result["claims"]), 2)
        self.assertEqual(result["status"], "DRAFT_UNREVIEWED")
        self.assertEqual(result["claims"][1]["method_candidates"][0]["id"], "SEC")

    def test_rejects_invalid_or_ambiguous_data(self):
        invalid = [
            {}, plan(), plan(claim(features=[])), plan(claim(features=["impossible"])),
            plan(claim(features=["stateful", "stateful"])), plan(claim(), claim()),
            plan(claim(impact="very-high")), plan(claim(id="")),
        ]
        for value in invalid:
            with self.subTest(value=value), self.assertRaises(ValueError):
                module.build_strategy(value)

    def test_cli_outputs_draft_without_side_effects(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "request.json"
            path.write_text(json.dumps(plan(claim())), encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["status"], "DRAFT_UNREVIEWED")
            self.assertEqual([p.name for p in Path(directory).iterdir()], ["request.json"])


if __name__ == "__main__":
    unittest.main()
