#!/usr/bin/env python3
"""
Automated Verification Suite: CMS-0057 Kickoff Pack Manifest & Document Integrity
Ticket ID: INT-378 (S00-ST01-T02)
Jira Reference: DSP-6547
Engagement: ELP-1

Validates:
1. Presence & schema integrity of kickoff_pack/01_KICKOFF_PACK_MANIFEST.md.
2. Parsing & structure of kickoff_pack/kickoff_pack_manifest.json.
3. Physical existence and SHA-256 integrity of the three canonical PDFs.
4. Completeness of squad implementation directives across all 6 squads.
5. Binding to Project Charter (01_PROJECT_CHARTER.md).
6. Multi-cloud environment parameters (AWS 646044944744, GCP project-1c617076-69b8-413f-94d).
7. Verification of files in dedicated ticket directory (/Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-378/).
"""

import hashlib
import json
import os
import sys
from datetime import datetime

EXPECTED_DOCS = {
    "DOC-01-ARCH": {
        "filename": "01-Patient-Access-API-From-Scratch-Plan.pdf",
        "expected_sha256": "c33b328c789011bff255e707cf1dd02d4e2fe2de2594d99fefef75efef25ae66",
        "min_size": 20000
    },
    "DOC-02-SETUP": {
        "filename": "Environment_Setup_Verification_Log.pdf",
        "expected_sha256": "4d4a4db07d4b2a6ab4cd160b20ca90689527d9cdf70598a44c351bfb69dad2e1",
        "min_size": 15000
    },
    "DOC-03-STEPS": {
        "filename": "03-Onyx-Sprints-and-Delivery-Lifecycle.pdf",
        "expected_sha256": "d90535e5c09d6595ae31d98e2cde9e599ae96e522652670d6475b1c0d4729942",
        "min_size": 20000
    }
}

def compute_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def run_verification():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_md = os.path.join(base_dir, "kickoff_pack", "01_KICKOFF_PACK_MANIFEST.md")
    manifest_json = os.path.join(base_dir, "kickoff_pack", "kickoff_pack_manifest.json")
    charter_md = os.path.join(base_dir, "charter", "01_PROJECT_CHARTER.md")
    ticket_dir = "/Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-378"
    results_out = os.path.join(base_dir, "kickoff_pack_verification_results.json")
    ticket_results_out = os.path.join(ticket_dir, "qa_verification_results.json")

    results = {
        "suite_name": "INT-378 Kickoff Documentation Pack Verification Suite",
        "timestamp": datetime.now().isoformat(),
        "ticket_id": "INT-378",
        "ticket_code": "S00-ST01-T02",
        "jira_ref": "DSP-6547",
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

    # Check 1: Markdown Manifest Presence
    c1_ok = os.path.exists(manifest_md) and os.path.getsize(manifest_md) > 1000
    record_check("CHK-001", "Kickoff Pack Markdown Manifest Presence & Size", c1_ok, {
        "path": manifest_md,
        "size_bytes": os.path.getsize(manifest_md) if os.path.exists(manifest_md) else 0
    })

    # Check 2: JSON Manifest Parsability
    data = None
    c2_ok = False
    if os.path.exists(manifest_json):
        try:
            with open(manifest_json, "r") as f:
                data = json.load(f)
            c2_ok = True
        except Exception:
            c2_ok = False
    record_check("CHK-002", "Kickoff Pack JSON Manifest Parsability", c2_ok, {
        "path": manifest_json
    })

    if not data:
        print("ERROR: Failed to parse manifest JSON. Aborting.")
        return False

    meta = data.get("manifest_metadata", {})
    env = meta.get("cloud_environments", {})

    # Check 3: AWS Account ID
    c3_ok = env.get("aws_account_id") == "646044944744"
    record_check("CHK-003", "AWS Environment Registration (Account ID 646044944744)", c3_ok, {
        "expected": "646044944744",
        "actual": env.get("aws_account_id")
    })

    # Check 4: GCP Project ID
    c4_ok = env.get("gcp_project_id") == "project-1c617076-69b8-413f-94d"
    record_check("CHK-004", "GCP Environment Registration (Project project-1c617076-69b8-413f-94d)", c4_ok, {
        "expected": "project-1c617076-69b8-413f-94d",
        "actual": env.get("gcp_project_id")
    })

    # Check 5: Three Canonical PDFs existence in repo docs
    repo_docs_dir = os.path.join(base_dir, "kickoff_pack", "docs")
    c5_all = True
    c5_details = {}
    for code, info in EXPECTED_DOCS.items():
        doc_path = os.path.join(repo_docs_dir, info["filename"])
        exists = os.path.exists(doc_path)
        sz = os.path.getsize(doc_path) if exists else 0
        c5_details[code] = {"exists": exists, "size": sz}
        if not exists or sz < info["min_size"]:
            c5_all = False
    record_check("CHK-005", "Canonical Kickoff PDFs Physical Presence in Repository", c5_all, c5_details)

    # Check 6: SHA-256 Checksum Verification
    c6_all = True
    c6_details = {}
    for code, info in EXPECTED_DOCS.items():
        doc_path = os.path.join(repo_docs_dir, info["filename"])
        actual_sha = compute_sha256(doc_path)
        match = (actual_sha == info["expected_sha256"])
        c6_details[code] = {"match": match, "actual_sha256": actual_sha}
        if not match:
            c6_all = False
    record_check("CHK-006", "Cryptographic SHA-256 Checksum Verification of All Three PDFs", c6_all, c6_details)

    # Check 7: Dedicated Ticket Directory Presence (/Linear-Tickets/INT-378/)
    c7_all = os.path.exists(ticket_dir)
    c7_details = {}
    for code, info in EXPECTED_DOCS.items():
        t_path = os.path.join(ticket_dir, info["filename"])
        exists = os.path.exists(t_path)
        c7_details[code] = {"ticket_folder_exists": exists}
        if not exists:
            c7_all = False
    record_check("CHK-007", "Dedicated Ticket Folder Asset Presence (/Linear-Tickets/INT-378/)", c7_all, c7_details)

    # Check 8: Squad Directives Completeness
    directives = data.get("squad_directives", {})
    required_squads = [
        "cloud_infrastructure_squad",
        "data_ingestion_squad",
        "lakehouse_analytics_squad",
        "fhir_epa_squad",
        "access_apis_squad",
        "quality_compliance_squad"
    ]
    c8_ok = all(sq in directives for sq in required_squads)
    record_check("CHK-008", "Squad Implementation Directives Completeness (All 6 Squads Mapped)", c8_ok, {
        "mapped_squads": list(directives.keys())
    })

    # Check 9: Project Charter Cross-Reference
    c9_ok = False
    if os.path.exists(charter_md):
        with open(charter_md, "r") as f:
            c_content = f.read()
        if "PACK-CMS0057-KICKOFF-V1" in c_content or "DOC-01-ARCH" in c_content or "INT-378" in c_content:
            c9_ok = True
    record_check("CHK-009", "Project Charter Binding & Canonical Link Verification", c9_ok, {
        "charter_path": charter_md
    })

    # Check 10: Synthetic Isolation & Hard Prod Gate
    c10_ok = (env.get("synthetic_batch_id") == "SYN-ELP-EPA-01" and "none" in env.get("production_isolation", "").lower())
    record_check("CHK-010", "Synthetic Isolation & Hard-Gated Production Policy", c10_ok, {
        "batch": env.get("synthetic_batch_id"),
        "prod_policy": env.get("production_isolation")
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
