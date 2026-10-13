#!/usr/bin/env python3
"""
Automated Verification Suite: CMS-0057 Architecture Charter & Merge Decisions
Ticket ID: INT-377 (S00-ST01-T01)
Engagement: ELP-1

Validates:
1. Integrity and presence of Project Charter (01_PROJECT_CHARTER.md).
2. Completeness and validity of eight_merge_decisions.json.
3. Verification of all eight Architectural Merge Decisions (AMD-001 through AMD-008).
4. Enforcement of immutable constraints, status LOCK, and governing sprint mappings.
5. Cloud environment registration (AWS 646044944744, GCP project-1c617076-69b8-413f-94d).
6. Synthetic population boundary isolation (SYN-ELP-EPA-01).
"""

import json
import os
import sys
from datetime import datetime

def run_charter_verification():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    charter_md_path = os.path.join(base_dir, "charter", "01_PROJECT_CHARTER.md")
    charter_json_path = os.path.join(base_dir, "charter", "eight_merge_decisions.json")
    results_out_path = os.path.join(base_dir, "charter_verification_results.json")

    results = {
        "suite_name": "INT-377 Architectural Merge Decisions QA Verification",
        "timestamp": datetime.now().isoformat(),
        "ticket_id": "INT-377",
        "ticket_code": "S00-ST01-T01",
        "lead_engineer": "Ashish Singh",
        "checks": [],
        "summary": {
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "all_passed": False
        }
    }

    def record_check(check_id, description, status, details=None):
        results["checks"].append({
            "check_id": check_id,
            "description": description,
            "status": "PASS" if status else "FAIL",
            "details": details or {}
        })

    # Check 1: Charter Markdown Document exists and has content
    c1_ok = os.path.exists(charter_md_path) and os.path.getsize(charter_md_path) > 1000
    record_check("CHK-001", "Project Charter Markdown Document Presence & Minimum Size", c1_ok, {
        "path": charter_md_path,
        "size_bytes": os.path.getsize(charter_md_path) if os.path.exists(charter_md_path) else 0
    })

    # Check 2: JSON Specification Document exists and parses
    json_data = None
    c2_ok = False
    if os.path.exists(charter_json_path):
        try:
            with open(charter_json_path, "r") as f:
                json_data = json.load(f)
            c2_ok = True
        except Exception as e:
            c2_ok = False
    record_check("CHK-002", "Eight Merge Decisions JSON Specification Parsability", c2_ok, {
        "path": charter_json_path
    })

    if not json_data:
        print("ERROR: Failed to load JSON data. Aborting verification.")
        return False

    meta = json_data.get("project_metadata", {})
    env = meta.get("environments", {})

    # Check 3: AWS Account ID verification
    c3_ok = env.get("aws_account_id") == "646044944744"
    record_check("CHK-003", "AWS Environment Registration (Account ID 646044944744)", c3_ok, {
        "expected": "646044944744",
        "actual": env.get("aws_account_id")
    })

    # Check 4: GCP Project ID verification
    c4_ok = env.get("gcp_project_id") == "project-1c617076-69b8-413f-94d"
    record_check("CHK-004", "GCP Environment Registration (Project project-1c617076-69b8-413f-94d)", c4_ok, {
        "expected": "project-1c617076-69b8-413f-94d",
        "actual": env.get("gcp_project_id")
    })

    # Check 5: Synthetic Batch Isolation
    c5_ok = env.get("synthetic_batch_id") == "SYN-ELP-EPA-01"
    record_check("CHK-005", "Synthetic Batch Constraint (SYN-ELP-EPA-01)", c5_ok, {
        "batch_id": env.get("synthetic_batch_id")
    })

    # Check 6: Production Tenant Isolation Tag
    c6_ok = "none" in env.get("production_tenant_isolation", "").lower()
    record_check("CHK-006", "Production Zero-Load Gate Policy (abacus:production-tenant = none)", c6_ok, {
        "policy": env.get("production_tenant_isolation")
    })

    # Check 7: Count of Decisions exactly 8
    decisions = json_data.get("decisions", [])
    c7_ok = len(decisions) == 8
    record_check("CHK-007", "Exact Count of Eight Merge Decisions (AMD-001 through AMD-008)", c7_ok, {
        "count": len(decisions)
    })

    # Check 8: Validate Each Decision (AMD-001 to AMD-008)
    expected_ids = [f"AMD-00{i}" for i in range(1, 9)]
    actual_ids = [d.get("id") for d in decisions]
    c8_ok = actual_ids == expected_ids
    record_check("CHK-008", "Sequential Decision Identifier Integrity", c8_ok, {
        "expected": expected_ids,
        "actual": actual_ids
    })

    # Check 9: Status LOCK on all 8 decisions
    all_locked = all(d.get("status") == "LOCKED" for d in decisions)
    record_check("CHK-009", "Immutable Status LOCK Enforced on All 8 Decisions", all_locked, {
        "statuses": {d.get("id"): d.get("status") for d in decisions}
    })

    # Check 10: Invariants Present on All 8 Decisions
    all_invariants = all(len(d.get("immutable_invariants", [])) >= 2 for d in decisions)
    record_check("CHK-010", "Robust Invariant Definitions on All Decisions", all_invariants, {
        "invariant_counts": {d.get("id"): len(d.get("immutable_invariants", [])) for d in decisions}
    })

    # Check 11: Governing Sprints Defined
    all_sprints = all(len(d.get("governing_sprints", [])) >= 1 for d in decisions)
    record_check("CHK-011", "Governing Sprint Traceability Across All Decisions", all_sprints, {
        "sprint_maps": {d.get("id"): d.get("governing_sprints") for d in decisions}
    })

    # Check 12: Specific Architectural Constraints Verification
    amd_map = {d.get("id"): d for d in decisions}
    c12_sub1 = "HealthLake" in amd_map.get("AMD-001", {}).get("selected_options", {}).get("track_a_aws", "")
    c12_sub2 = "Healthcare API" in amd_map.get("AMD-001", {}).get("selected_options", {}).get("track_b_gcp", "")
    c12_sub3 = "Profile A" in amd_map.get("AMD-003", {}).get("selected_options", {}).get("selected_profile", "")
    c12_sub4 = len(amd_map.get("AMD-007", {}).get("selected_options", {}).get("supported_hooks", [])) == 6
    c12_ok = c12_sub1 and c12_sub2 and c12_sub3 and c12_sub4
    record_check("CHK-012", "Specific Domain Architectural Invariants (FHIR Store, Profile A, 6 CDS Hooks)", c12_ok, {
        "AMD-001_HealthLake": c12_sub1,
        "AMD-001_HealthcareAPI": c12_sub2,
        "AMD-003_ProfileA": c12_sub3,
        "AMD-007_SixHooks": c12_sub4
    })

    # Summarize
    passed = sum(1 for c in results["checks"] if c["status"] == "PASS")
    total = len(results["checks"])
    failed = total - passed

    results["summary"]["total_checks"] = total
    results["summary"]["passed_checks"] = passed
    results["summary"]["failed_checks"] = failed
    results["summary"]["all_passed"] = (failed == 0)

    with open(results_out_path, "w") as f:
        json.dump(results, f, indent=2)

    print("======================================================================")
    print(f"  CMS-0057 QA VERIFICATION SUITE: {results['ticket_id']} ({results['ticket_code']})")
    print("======================================================================")
    print(f"  Total Checks Executed : {total}")
    print(f"  Passed Checks         : {passed} [SUCCESS]")
    print(f"  Failed Checks         : {failed}")
    print(f"  Overall Status        : {'PASS' if results['summary']['all_passed'] else 'FAIL'}")
    print(f"  Results Written To    : {results_out_path}")
    print("======================================================================")

    return results["summary"]["all_passed"]

if __name__ == "__main__":
    success = run_charter_verification()
    sys.exit(0 if success else 1)
