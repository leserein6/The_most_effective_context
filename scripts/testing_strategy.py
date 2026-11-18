#!/usr/bin/env python3
"""Suggest testing techniques from explicit change claims; never certify adequacy.

Input schema testing/strategy-input-v1; output testing/strategy-v1.
Only standard-library dependencies. This tool selects candidate methods using
declared failure mechanisms; it cannot derive missing requirements or an oracle.
"""
import argparse
import json
from pathlib import Path
import sys

FEATURES = {
    "input-domain", "boolean-decision", "stateful", "persistence", "concurrency",
    "remote-failure", "api-compatibility", "config-interaction", "algorithmic",
    "untrusted-input", "migration", "security", "performance", "recovery",
    "critical-decision", "weak-tests", "user-journey", "accessibility",
}
IMPACTS = {"low", "medium", "high", "critical"}

# Explicit methodology rules, not learned guesses. Evidence must be designed
# and independently reviewed for each candidate method.
RULES = (
    ("input-domain", ("EP", "BVA"), "Partition inputs and probe each known boundary."),
    ("boolean-decision", ("DT", "BR"), "Map feasible rules to outcomes; inspect structural branches."),
    ("stateful", ("ST", "MBT"), "Cover allowed/forbidden transitions and important event sequences."),
    ("persistence", ("DB",), "Observe committed and rolled-back state using the real store."),
    ("concurrency", ("CON", "ST"), "Target interleavings, duplicate effects and state invariants."),
    ("remote-failure", ("FI", "REL"), "Inject known failure windows and observe recovery."),
    ("api-compatibility", ("CT",), "Check producer/consumer compatibility using versioned contracts."),
    ("config-interaction", ("CMB",), "Define factors, constraints and t-way coverage."),
    ("algorithmic", ("PROP", "MET"), "Check independent mathematical properties and transformations."),
    ("untrusted-input", ("FUZZ", "BVA"), "Explore adversarial/invalid input shapes and boundaries."),
    ("migration", ("CT", "DB", "DIFF"), "Check old/new representation and persisted data compatibility."),
    ("security", ("SEC", "SA"), "Map trust boundaries and negative authorization cases."),
    ("performance", ("PERF",), "Measure the specified workload and SLO in a suitable environment."),
    ("recovery", ("REL", "FI"), "Observe reboot/retry/rollback under a stated failure model."),
    ("critical-decision", ("DT", "MCDC", "REV"), "Review boolean independence for critical decisions."),
    ("weak-tests", ("MUT",), "Check whether representative faulty implementations are rejected."),
    ("user-journey", ("SC",), "Observe the user-visible flow and error/recovery path."),
    ("accessibility", ("ACC",), "Use the applicable accessibility standard and user tasks."),
)
LIMITS = {
    "EP": "Partitions can omit relevant distinctions.",
    "BVA": "Boundary samples do not cover multi-factor interactions.",
    "DT": "Decision rules do not by themselves establish temporal or concurrent safety.",
    "BR": "Executing branches does not establish correct assertions.",
    "ST": "Transition coverage does not establish all event sequences.",
    "MBT": "A wrong state model can generate consistently wrong tests.",
    "DB": "Results apply to the tested engine, isolation and configuration.",
    "CON": "Sampled interleavings do not exhaust all possible schedules.",
    "FI": "Only injected failure points and windows are exercised.",
    "REL": "Recovery evidence is limited to the exercised topology and duration.",
    "CT": "Contract compatibility does not prove service internals.",
    "CMB": "t-way coverage does not cover all higher-order interactions.",
    "PROP": "Generated samples do not prove a universal property.",
    "MET": "A wrong metamorphic relation invalidates the oracle.",
    "FUZZ": "Exploration duration and corpus cannot establish no remaining defects.",
    "DIFF": "Two implementations may share a wrong behavior.",
    "SEC": "The threat model and tool rules may omit relevant attacks.",
    "SA": "Static analysis depends on rules, assumptions and false positives.",
    "PERF": "Load results may not generalize to production topology.",
    "MCDC": "Independent influence must be shown per atomic condition; coupling matters.",
    "REV": "Review is evidence only for its documented scope.",
    "MUT": "Mutation score concerns only the selected non-equivalent mutants.",
    "SC": "A few journeys do not cover all internal states.",
    "ACC": "Automated checks alone do not establish real usability or accessibility.",
}


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def build_strategy(payload):
    if not isinstance(payload, dict) or payload.get("schema") != "testing/strategy-input-v1":
        raise ValueError("expected schema testing/strategy-input-v1")
    if not _nonempty(payload.get("change_id")):
        raise ValueError("change_id is required")
    claims = payload.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims must be a nonempty array")
    result = []
    ids = set()
    for index, item in enumerate(claims):
        if not isinstance(item, dict) or not all(_nonempty(item.get(k)) for k in ("id", "source", "claim")):
            raise ValueError("each claim requires id, source and claim")
        if item["id"] in ids:
            raise ValueError("duplicate claim id " + item["id"])
        ids.add(item["id"])
        impact = item.get("impact")
        features = item.get("features")
        if impact not in IMPACTS or not isinstance(features, list) or not features or not all(
            isinstance(f, str) and f in FEATURES for f in features
        ):
            raise ValueError("claim " + item["id"] + ": invalid impact/features")
        if len(set(features)) != len(features):
            raise ValueError("claim " + item["id"] + ": duplicate feature")
        chosen = {}
        for feature, methods, rationale in RULES:
            if feature in features:
                for method in methods:
                    chosen.setdefault(method, {"id": method, "triggered_by": [], "why": [], "limitation": LIMITS[method]})
                    chosen[method]["triggered_by"].append(feature)
                    chosen[method]["why"].append(rationale)
        # High consequences demand independent model/oracle review, not a fixed
        # quota of tests or an arbitrary numeric coverage target.
        if impact in ("high", "critical") and "REV" not in chosen:
            chosen["REV"] = {"id": "REV", "triggered_by": ["high-impact"],
                             "why": ["Independently review specification, oracle and residual risks."],
                             "limitation": LIMITS["REV"]}
        oracle = item.get("oracle")
        unresolved = []
        if not _nonempty(oracle):
            unresolved.append("oracle: independent expected-result source is missing")
        if not _nonempty(item.get("counterexample")):
            unresolved.append("counterexample: name a wrong behavior that should fail")
        if not _nonempty(item.get("environment")):
            unresolved.append("environment: document the smallest credible execution environment")
        result.append({
            "id": item["id"], "source": item["source"], "claim": item["claim"],
            "impact": impact, "features": features,
            "oracle": oracle if _nonempty(oracle) else None,
            "method_candidates": list(chosen.values()),
            "unresolved": unresolved,
            "proof_obligations": [
                "review source, expected behavior and oracle independently of implementation",
                "list model coverage items, their denominator and any excluded/unreachable item",
                "bind test cases and observations to a candidate snapshot, fixture and environment",
                "record a faulty implementation that must fail and a conforming alternative that must pass",
                "document the result scope, residual risk and evidence invalidation trigger",
            ],
            "design_status": "UNVERIFIED",
            "execution_status": "UNVERIFIED",
            "assurance_status": "UNVERIFIED",
        })
    return {
        "schema": "testing/strategy-v1",
        "change_id": payload["change_id"],
        "purpose": "method candidates only; no cases executed and no adequacy claim",
        "status": "DRAFT_UNREVIEWED",
        "claims": result,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, help="write JSON result; default stdout")
    args = parser.parse_args(argv)
    try:
        result = build_strategy(json.loads(args.input.read_text(encoding="utf-8")))
    except (OSError, ValueError, TypeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.out is None:
        print(data, end="")
    else:
        try:
            args.out.write_text(data, encoding="utf-8")
        except OSError as exc:
            print("ERROR: " + str(exc), file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
