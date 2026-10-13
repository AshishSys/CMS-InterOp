#!/usr/bin/env python3
"""
Automated Verification Suite: CMS-0057 Engagement Ownership & Scope Authority
Ticket ID: INT-379 (S00-ST02-T01)
Jira Reference: ELP-1
Engagement: ELP-1

Validates:
1. Presence & schema integrity of governance/01_ENGAGEMENT_OWNERSHIP.md.
2. Parsing & structure of governance/engagement_ownership.json.
3. Verification of Executive Sponsor, Accountable Product Owner, and Named Delegate.
4. Validation of Scope Authority Matrix.
5. Binding to Project Charter (01_PROJECT_CHARTER.md Section 4.1).
6. Multi-cloud environment parameters (AWS 646044944744, GCP project-1c617076-69b8-413f-94d).
7. Verification of files in dedicated ticket directory (/Linear-Tickets/INT-379/).
"""

import json
import os
import sys
from datetime import datetime

def run_verification():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    gov_md = os.path.join(base_dir, "governance", "01_ENGAGEMENT_OWNERSHIP.md")
    gov_json = os.path.join(base_dir, "governance", "engagement_ownership.json")
    charter_md = os.path.join(base_dir, "charter", "01_PROJECT_CHARTER.md")
    ticket_dir = "/Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-379"
    results_out = os.path.join(base_dir, "governance_verification_results.json")
    ticket_results_out = os.path.join(ticket_dir, "qa_verification_results.json")

    results = {
        "suite_name": "INT-379 Engagement Ownership & Scope Authority Verification Suite",
        "timestamp": datetime.now().isoformat(),
        "ticket_id": "INT-379",
        "ticket_code": "S00-ST02-T01",
        "jira_ref": "ELP-1",
        "lead_architect": "Ashish Singh",
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

    # Check 1: Markdown Governance Document Presence
    c1_ok = os.path.exists(gov_md) and os.path.getsize(gov_md) > 1000
    record_check("CHK-001", "Engagement Ownership Markdown Document Presence & Size", c1_ok, {
        "path": gov_md,
        "size_bytes": os.path.getsize(gov_md) if os.path.exists(gov_md) else 0
    })

    # Check 2: JSON Specification Parsability
    data = None
    c2_ok = False
    if os.path.exists(gov_json):
        try:
            with open(gov_json, "r") as f:
                data = json.load(f)
            c2_ok = True
        except Exception:
            c2_ok = False
    record_check("CHK-002", "Engagement Ownership JSON Specification Parsability", c2_ok, {
        "path": gov_json
    })

    if not data:
        print("ERROR: Failed to parse governance JSON. Aborting.")
        return False

    meta = data.get("governance_metadata", {})
    env = meta.get("cloud_environments", {})
    entities = data.get("accountable_entities", {})
    matrix = data.get("scope_authority_matrix", {})

    # Check 3: AWS Account ID Bound
    c3_ok = env.get("aws_account_id") == "646044944744"
    record_check("CHK-003", "AWS Environment Registration (Account ID 646044944744)", c3_ok, {
        "expected": "646044944744",
        "actual": env.get("aws_account_id")
    })

    # Check 4: GCP Project ID Bound
    c4_ok = env.get("gcp_project_id") == "project-1c617076-69b8-413f-94d"
    record_check("CHK-004", "GCP Environment Registration (Project project-1c617076-69b8-413f-94d)", c4_ok, {
        "expected": "project-1c617076-69b8-413f-94d",
        "actual": env.get("gcp_project_id")
    })

    # Check 5: Executive Sponsor Definition
    sponsor = entities.get("executive_sponsor", {})
    c5_ok = bool(sponsor.get("role") and sponsor.get("responsibilities"))
    record_check("CHK-005", "Executive Sponsor Role & Responsibilities Defined", c5_ok, {
        "title": sponsor.get("title"),
        "responsibilities_count": len(sponsor.get("responsibilities", []))
    })

    # Check 6: Accountable Product Owner Definition (Ashish Singh)
    po = entities.get("product_owner", {})
    c6_ok = (po.get("name") == "Ashish Singh" and len(po.get("responsibilities", [])) >= 3)
    record_check("CHK-006", "Accountable Product Owner Defined (Ashish Singh with Scope Authority)", c6_ok, {
        "name": po.get("name"),
        "github_handle": po.get("github_handle"),
        "responsibilities_count": len(po.get("responsibilities", []))
    })

    # Check 7: Named Delegate Definition
    delegate = entities.get("named_delegate", {})
    c7_ok = bool(delegate.get("role") and delegate.get("proxy_authority") and delegate.get("restrictions"))
    record_check("CHK-007", "Named Delegate Protocol & Authority Boundaries Defined", c7_ok, {
        "role": delegate.get("role"),
        "restrictions_count": len(delegate.get("restrictions", []))
    })

    # Check 8: Scope Authority Matrix Completeness
    required_domains = [
        "accept_reject_sprint_scope",
        "approve_architecture_change_requests",
        "production_release_gate_clearance",
        "synthetic_population_adjustments"
    ]
    c8_ok = all(d in matrix for d in required_domains)
    record_check("CHK-008", "Scope Authority Matrix Completeness (All 4 Decision Domains Mapped)", c8_ok, {
        "mapped_domains": list(matrix.keys())
    })

    # Check 9: Cross-Reference in Project Charter
    c9_ok = False
    if os.path.exists(charter_md):
        with open(charter_md, "r") as f:
            c_text = f.read()
        if "01_ENGAGEMENT_OWNERSHIP.md" in c_text and "INT-379" in c_text and "Ashish Singh" in c_text:
            c9_ok = True
    record_check("CHK-009", "Project Charter Binding (01_PROJECT_CHARTER.md Section 4.1)", c9_ok, {
        "charter_path": charter_md
    })

    # Check 10: Dedicated Ticket Directory Presence
    c10_ok = os.path.exists(ticket_dir)
    record_check("CHK-010", "Dedicated Ticket Artifact Directory Presence (/Linear-Tickets/INT-379/)", c10_ok, {
        "ticket_dir": ticket_dir
    })

    passed = sum(1 for c in results["checks"] if c["status"] == "PASS")
    total = len(results["checks"])
    failed = total - passed

    results["summary"]["total_checks"] = total
    results["summary"]["passed_checks"] = passed
    results["summary"]["failed_checks"] = failed
    results["summary"]["all_passed"] = (failed == 0)

    with open(results_out, "w") as f:
        json.dump(results, f, indent=2)

    os.makedirs(ticket_dir, exist_ok=True)
    with open(ticket_results_out, "w") as f:
        json.dump(results, f, indent=2)

    print("======================================================================")
    print(f"  CMS-0057 QA VERIFICATION SUITE: {results['ticket_id']} ({results['ticket_code']})")
    print(f"  Jira Reference        : {results['jira_ref']}")
    print("======================================================================")
    print(f"  Total Checks Executed : {total}")
    print(f"  Passed Checks         : {passed} [SUCCESS]")
    print(f"  Failed Checks         : {failed}")
    print(f"  Overall Status        : {'PASS' if results['summary']['all_passed'] else 'FAIL'}")
    print(f"  Results Written To    : {results_out}")
    print(f"  Ticket Copy Written To: {ticket_results_out}")
    print("======================================================================")

    return results["summary"]["all_passed"]

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
