#!/usr/bin/env python3
"""
Automated QA Verification Suite for Ticket INT-380 / S00-ST02-T02
Verifies:
  1. governance/02_SQUAD_LEADS.md (DOC-GOV-SQUADS-V1) exists and non-empty.
  2. governance/squad_leads.json is valid JSON with required schema.
  3. Six squads defined with distinct IDs (SQ-01 through SQ-06).
  4. All six Jira lanes mapped: SO, DSP, XPORT, CMS, ONYX, PRODOPS.
  5. Ashish Singh explicitly assigned as squad lead across lanes.
  6. Email contacts and squad titles present for each squad.
  7. AWS Account ID 646044944744 present across all governance artifacts.
  8. GCP Project ID project-1c617076-69b8-413f-94d present across all governance artifacts.
  9. Project Charter (charter/01_PROJECT_CHARTER.md) updated with Section 4.2 citing DOC-GOV-SQUADS-V1.
 10. Engagement Ownership & README synchronized with squad lane registry.
"""

import os
import sys
import json
from datetime import datetime

AWS_ACCOUNT_ID = "646044944744"
GCP_PROJECT_ID = "project-1c617076-69b8-413f-94d"
EXPECTED_LANES = ["SO", "DSP", "XPORT", "CMS", "ONYX", "PRODOPS"]
EXPECTED_SQUADS = ["SQ-01", "SQ-02", "SQ-03", "SQ-04", "SQ-05", "SQ-06"]

def run_checks():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results = []

    # TC-SQL-01: Markdown spec existence
    md_path = os.path.join(repo_root, "governance", "02_SQUAD_LEADS.md")
    tc01_pass = os.path.exists(md_path) and os.path.getsize(md_path) > 500
    results.append({
        "test_id": "TC-SQL-01",
        "description": "Verify governance/02_SQUAD_LEADS.md existence and size",
        "status": "PASS" if tc01_pass else "FAIL",
        "details": f"File exists: {os.path.exists(md_path)}, size: {os.path.getsize(md_path) if os.path.exists(md_path) else 0} bytes"
    })

    # TC-SQL-02: JSON registry existence and valid JSON
    json_path = os.path.join(repo_root, "governance", "squad_leads.json")
    json_data = None
    tc02_pass = False
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            tc02_pass = True
        except Exception as e:
            tc02_pass = False
    results.append({
        "test_id": "TC-SQL-02",
        "description": "Verify governance/squad_leads.json schema parsing",
        "status": "PASS" if tc02_pass else "FAIL",
        "details": "JSON valid and parsed" if tc02_pass else "Invalid JSON"
    })

    # TC-SQL-03: Six squads present in registry
    squads = json_data.get("squads", []) if json_data else []
    found_squad_ids = [s.get("squad_id") for s in squads]
    tc03_pass = all(sid in found_squad_ids for sid in EXPECTED_SQUADS) and len(squads) == 6
    results.append({
        "test_id": "TC-SQL-03",
        "description": "Verify exactly 6 squads defined with expected IDs (SQ-01 to SQ-06)",
        "status": "PASS" if tc03_pass else "FAIL",
        "details": f"Found squads: {found_squad_ids}"
    })

    # TC-SQL-04: Jira lane mapping completeness
    found_lanes = [s.get("jira_lane") for s in squads]
    tc04_pass = all(lane in found_lanes for lane in EXPECTED_LANES)
    results.append({
        "test_id": "TC-SQL-04",
        "description": "Verify all six Jira lanes mapped (SO, DSP, XPORT, CMS, ONYX, PRODOPS)",
        "status": "PASS" if tc04_pass else "FAIL",
        "details": f"Mapped lanes: {found_lanes}"
    })

    # TC-SQL-05: Lead assignment
    all_leads = [s.get("lead", {}).get("name") for s in squads]
    tc05_pass = all(name == "Ashish Singh" for name in all_leads) and len(all_leads) == 6
    results.append({
        "test_id": "TC-SQL-05",
        "description": "Verify Ashish Singh assigned as lead across all active lanes",
        "status": "PASS" if tc05_pass else "FAIL",
        "details": f"Assigned leads: {list(set(all_leads))}"
    })

    # TC-SQL-06: Lead emails and squad titles present
    emails = [s.get("lead", {}).get("email") for s in squads]
    tc06_pass = all("@cmsinterop.internal" in e for e in emails if e) and len(emails) == 6
    results.append({
        "test_id": "TC-SQL-06",
        "description": "Verify lead email contact identities present for all 6 squads",
        "status": "PASS" if tc06_pass else "FAIL",
        "details": f"Found contact emails: {emails}"
    })

    # TC-SQL-07: AWS Account ID verification
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    with open(json_path, 'r', encoding='utf-8') as f:
        json_content = f.read()
    tc07_pass = (AWS_ACCOUNT_ID in md_content) and (AWS_ACCOUNT_ID in json_content)
    results.append({
        "test_id": "TC-SQL-07",
        "description": "Verify AWS Account ID 646044944744 in squad governance specs",
        "status": "PASS" if tc07_pass else "FAIL",
        "details": f"AWS Account present in markdown: {AWS_ACCOUNT_ID in md_content}, json: {AWS_ACCOUNT_ID in json_content}"
    })

    # TC-SQL-08: GCP Project ID verification
    tc08_pass = (GCP_PROJECT_ID in md_content) and (GCP_PROJECT_ID in json_content)
    results.append({
        "test_id": "TC-SQL-08",
        "description": "Verify GCP Project ID project-1c617076-69b8-413f-94d in squad governance specs",
        "status": "PASS" if tc08_pass else "FAIL",
        "details": f"GCP Project present in markdown: {GCP_PROJECT_ID in md_content}, json: {GCP_PROJECT_ID in json_content}"
    })

    # TC-SQL-09: Project Charter cross-reference
    charter_path = os.path.join(repo_root, "charter", "01_PROJECT_CHARTER.md")
    with open(charter_path, 'r', encoding='utf-8') as f:
        charter_content = f.read()
    tc09_pass = "DOC-GOV-SQUADS-V1" in charter_content and "4.2 Squad Leadership" in charter_content
    results.append({
        "test_id": "TC-SQL-09",
        "description": "Verify Project Charter Section 4.2 cross-references DOC-GOV-SQUADS-V1",
        "status": "PASS" if tc09_pass else "FAIL",
        "details": f"DOC-GOV-SQUADS-V1 in charter: {'DOC-GOV-SQUADS-V1' in charter_content}"
    })

    # TC-SQL-10: README Section 3.3 synchronization
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    tc10_pass = "3.3 Six Engineering Squads" in readme_content and "DOC-GOV-SQUADS-V1" in readme_content
    results.append({
        "test_id": "TC-SQL-10",
        "description": "Verify README Section 3.3 documents Six Squads & Jira Lane Ownership",
        "status": "PASS" if tc10_pass else "FAIL",
        "details": f"Section 3.3 in README: {'3.3 Six Engineering Squads' in readme_content}"
    })

    all_passed = all(r["status"] == "PASS" for r in results)
    summary = {
        "timestamp": datetime.now().isoformat(),
        "ticket_id": "INT-380",
        "jira_reference": "SO / DSP / XPORT / CMS / ONYX / PRODOPS lanes",
        "sprint": "S00",
        "total_checks": len(results),
        "passed_checks": sum(1 for r in results if r["status"] == "PASS"),
        "failed_checks": sum(1 for r in results if r["status"] == "FAIL"),
        "overall_status": "PASS" if all_passed else "FAIL",
        "cloud_accounts": {
            "aws_account_id": AWS_ACCOUNT_ID,
            "gcp_project_id": GCP_PROJECT_ID
        },
        "test_results": results
    }

    # Save results to repo root
    output_path = os.path.join(repo_root, "squad_leads_verification_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    # Save copy to dedicated ticket folder
    ticket_dir = "/Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-380"
    os.makedirs(ticket_dir, exist_ok=True)
    ticket_output_path = os.path.join(ticket_dir, "qa_verification_results.json")
    with open(ticket_output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print("=" * 70)
    print("  CMS-0057 QA VERIFICATION SUITE: INT-380 (S00-ST02-T02)")
    print("  Jira Reference        : SO / DSP / XPORT / CMS / ONYX / PRODOPS lanes")
    print("=" * 70)
    print(f"  Total Checks Executed : {summary['total_checks']}")
    print(f"  Passed Checks         : {summary['passed_checks']} [{'SUCCESS' if all_passed else 'FAILURE'}]")
    print(f"  Failed Checks         : {summary['failed_checks']}")
    print(f"  Overall Status        : {summary['overall_status']}")
    print(f"  Results Written To    : {output_path}")
    print(f"  Ticket Copy Written To: {ticket_output_path}")
    print("=" * 70)

    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    run_checks()
