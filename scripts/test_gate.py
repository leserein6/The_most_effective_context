#!/usr/bin/env python3
"""Run a repository test command and match fresh JUnit evidence to its acceptance plan."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET


def read_plan(raw):
    plan = json.loads(raw)
    if not isinstance(plan, dict) or plan.get("schema") != "testing/v1":
        raise ValueError("expected plan schema testing/v1")
    criteria = plan.get("criteria")
    if not isinstance(criteria, list) or not criteria:
        raise ValueError("expected at least one acceptance criterion")
    ids = set()
    for item in criteria:
        for field in ("id", "source", "expected"):
            if not isinstance(item, dict) or not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError("criterion requires nonempty " + field)
        if item["id"] in ids:
            raise ValueError("duplicate criterion " + item["id"])
        ids.add(item["id"])
        cases = item.get("cases")
        if not isinstance(cases, list) or not cases or not all(
            isinstance(case, str) and "::" in case and all(case.split("::", 1)) for case in cases
        ) or len(set(cases)) != len(cases):
            raise ValueError("expected unique Class::case entries for " + item["id"])
    return criteria


def read_cases(path):
    root = ET.parse(path).getroot()
    if root.tag not in ("testsuites", "testsuite"):
        raise ValueError("expected JUnit testsuite or testsuites")
    results = {}
    run_statuses = []
    summaries = [node for node in root.iter() if node.tag in ("testsuite", "testsuites")]
    if any(int(node.get("errors", "0")) > 0 for node in summaries) or any(node.tag == "error" for node in root.iter()):
        run_statuses.append("UNVERIFIED")
    if any(int(node.get("failures", "0")) > 0 for node in summaries) or any(node.tag == "failure" for node in root.iter()):
        run_statuses.append("FAIL")
    for case in root.iter("testcase"):
        key = case.get("classname", "") + "::" + case.get("name", "")
        if case.find("failure") is not None:
            status = "FAIL"
        elif case.find("skipped") is not None or case.find("error") is not None:
            status = "UNVERIFIED"
        elif case.get("status", "").lower() not in ("", "run", "passed", "success") or case.get("result", "").lower() in ("skipped", "suppressed"):
            status = "UNVERIFIED"
        else:
            status = "PASS"
        # A duplicate does not establish which execution belongs to the criterion.
        results[key] = "UNVERIFIED" if key in results else status
    return results, run_statuses


def verdict(statuses):
    if "FAIL" in statuses:
        return "FAIL"
    if "UNVERIFIED" in statuses:
        return "UNVERIFIED"
    return "PASS"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--candidate", required=True, help="tested commit or immutable build identifier")
    parser.add_argument("--out", type=Path, required=True, help="new directory for this run")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or not args.candidate.strip():
        parser.error("candidate and repository test command are required")
    raw = args.plan.read_bytes()
    criteria = read_plan(raw)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=False)
    junit = output / "junit.xml"
    argv = [arg.replace("{junit}", str(junit)) for arg in command]
    record = {
        "schema": "testing/run-v1", "candidate": args.candidate,
        "started_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "cwd": str(Path.cwd()), "platform": platform.platform(), "command": command,
        "plan_sha256": hashlib.sha256(raw).hexdigest(), "exit_code": None,
        "notes": [], "criteria": [],
    }
    (output / "plan.json").write_bytes(raw)
    results, run_statuses = {}, []
    with (output / "run.log").open("wb") as log:
        try:
            run = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT,
                                 env={**os.environ, "HARNESS_JUNIT": str(junit)})
            record["exit_code"] = run.returncode
        except OSError as exc:
            record["notes"].append(str(exc))
    try:
        results, run_statuses = read_cases(junit)
    except (OSError, ValueError, ET.ParseError) as exc:
        record["notes"].append("JUnit unavailable: " + str(exc))
    for item in criteria:
        observations = {name: results.get(name, "UNVERIFIED") for name in item["cases"]}
        record["criteria"].append({"id": item["id"], "cases": observations,
                                   "status": verdict(observations.values())})
    statuses = [row["status"] for row in record["criteria"]]
    # Unmapped regressions still block the run; an infrastructure error alone
    # does not establish that any particular business requirement was violated.
    statuses.extend(run_statuses)
    if run_statuses:
        record["notes"].append("JUnit contains a failure or execution error; see junit.xml")
    if record["exit_code"] != 0:
        statuses.append("UNVERIFIED")
        record["notes"].append("test command did not exit successfully")
    record["status"] = verdict(statuses)
    (output / "result.json").write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(record["status"], output / "result.json")
    return {"PASS": 0, "FAIL": 1, "UNVERIFIED": 2}[record["status"]]


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
