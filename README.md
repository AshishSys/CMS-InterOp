# CMS-0057 Interoperability Platform: Multi-Cloud Enterprise Reference Architecture

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CMS Standard](https://img.shields.io/badge/CMS-CMS--0057--F-green.svg)](https://www.cms.gov)
[![HL7 FHIR](https://img.shields.io/badge/HL7-FHIR%20R4-orange.svg)](https://hl7.org/fhir/R4/)
[![AWS](https://img.shields.io/badge/AWS-HealthLake%20%7C%20S3%20%7C%20KMS-232F3E.svg?logo=amazon-aws)](https://aws.amazon.com)
[![GCP](https://img.shields.io/badge/GCP-Cloud%20Healthcare%20%7C%20Cloud%20SQL-4285F4.svg?logo=google-cloud)](https://cloud.google.com)
[![QA Status](https://img.shields.io/badge/QA%20Verification-12%2F12%20PASS-brightgreen.svg)]()

> **Enterprise Interoperability & Prior Authorization Engine for State Medicaid & Payer Networks**  
> Architected, engineered, and maintained by **Ashish Singh** ([@AshishSys](https://github.com/AshishSys)).

---

## 1. Executive Summary & Regulatory Mission

The **CMS-0057 Interoperability and Prior Authorization Final Rule** (CMS-0057-F) requires Medicare Advantage, state Medicaid FFS, Medicaid Managed Care plans, CHIP, and QHP payers to deploy modern API standards to streamline clinical care, enable member access, and automate prior authorization.

This repository serves as the **central, multi-cloud codebase, infrastructure definitions, data pipelines, and compliance verification engine** for the CMS-0057 platform across **AWS (Track A)**, **GCP (Track B)**, and **Local Developer Sandboxes**.

```mermaid
flowchart TB
    subgraph ExternalConsumers["External Consumers & Actors"]
        EHR["Provider EHR / Epic / Cerner<br/>(SMART on FHIR / CDS Hooks)"]
        MemberApp["Patient Mobile / Web App<br/>(Patient Access API)"]
        NewPayer["Gaining / Losing Payer<br/>(Payer-to-Payer Exchange)"]
    end

    subgraph EdgePerimeter["Edge Security & Ingress (Bridge VPC)"]
        Gateway["Apigee / APISIX API Gateway<br/>mTLS • OAuth 2.0 • WAF • Rate Limiting"]
    end

    subgraph CloudDataPlane["Private Multi-Cloud Data Plane (Zero Internet Ingress)"]
        subgraph TrackA["Track A: AWS Health Infrastructure (Account: 646044944744)"]
            HL["AWS HealthLake (FHIR R4 Store)"]
            S3["S3 Medallion Lakehouse<br/>Landing • Medallion • FHIR-Output"]
            KMS_A["AWS KMS (Customer Managed Key)"]
            Trail["AWS CloudTrail & CloudWatch Alarms"]
        end

        subgraph TrackB["Track B: GCP Healthcare Infrastructure (Project: project-1c617076-69b8-413f-94d)"]
            HAPI["GCP Cloud Healthcare API (FHIR R4)"]
            GCS["GCS Bucket Lakehouse<br/>Landing • Bronze • Silver"]
            CSQL["Cloud SQL Postgres<br/>(Sub-5s Decision Cache)"]
            Audit_G["GCP Cloud Audit Logs"]
        end

        subgraph DecisionEngine["Clinical & Attribution Engine"]
            Cache["Relational Lookup Cache (Postgres)<br/>Sub-5s CRD Evaluations"]
            Onyx["Onyx CQL & FHIR Translation Worker"]
            AuditMongo["Dedicated MongoDB Audit Store<br/>Count-Only / Zero PHI"]
        end
    end

    ExternalConsumers -->|mTLS / HTTPS| Gateway
    Gateway -->|VPC Peering| HL
    Gateway -->|VPC Peering| HAPI
    Gateway -->|CDS Hooks / P99 < 5s| Cache
    Onyx --> S3
    Onyx --> GCS
    Onyx --> AuditMongo
```

---

## 2. Cloud Environment Registry

| Environment Attribute | Specification / Identifier | Role & Security Invariant |
| :--- | :--- | :--- |
| **AWS Account ID** | **`646044944744`** | Primary Cloud Track A (HealthLake, S3 Lakehouse, CloudTrail, KMS) |
| **AWS Region** | `us-east-1` | Primary AWS deployment region |
| **GCP Project ID** | **`project-1c617076-69b8-413f-94d`** | Primary Cloud Track B (Cloud Healthcare API, GCS, Cloud SQL, BigQuery) |
| **GCP Region** | `us-central1` | Primary GCP deployment region |
| **Local FHIR Sandbox** | `http://localhost:4080` | Firely Server R4 developer test harness |
| **Synthetic Batch ID** | `SYN-ELP-EPA-01` | 50 synthetic longitudinal patients (`ms-pt-001` - `ms-pt-050`) |
| **Production Isolation** | `NONE` (Zero Prod Load) | Production is hard-gated (`abacus:production-tenant = none`) |

---

## 3. The Eight Binding Architectural Merge Decisions

Ratified under **Project Charter Document ID: `CHARTER-CMS0057-2026-V1`** (Linear Ticket **`INT-377`** / Jira **`ELP-1`**), these eight decisions serve as immutable build contracts:

| Decision ID | Focus Area | Selected Baseline Option | Immutable Invariant |
| :--- | :--- | :--- | :--- |
| **AMD-001** | **FHIR Store Selection** | **Dual-Track:** AWS HealthLake (Track A) & GCP Cloud Healthcare API (Track B) | Native HL7 FHIR R4 schema enforcement; no proprietary document stores. |
| **AMD-002** | **Edge Security & Gateway** | **Apigee / APISIX Gateway** with mTLS & SMART on FHIR OAuth 2.0 | Zero direct internet ingress to data subnets; public access blocked on all buckets. |
| **AMD-003** | **ePA Profile Selection** | **Profile A** (CSV/JSON Flat-File Ingestion to FHIR PAS with daily batch recon) | Excludes Option B and Hybrid profiles; no unapproved profile switching. |
| **AMD-004** | **Attribution & LOB Scope** | **Claims-Driven Attribution** (2-year lookback) on Medicaid FFS / Managed Care | Active treatment relationship required via `PDexProviderGroup`; member opt-out honored. |
| **AMD-005** | **Synthetic Data Isolation** | **Synthetic Batch `SYN-ELP-EPA-01`** (50 Patients); Empty Production Gate | Zero live PHI/PII in development/staging; production tenant remains empty. |
| **AMD-006** | **Pipeline Ingestion Cadence**| **Weekly Master Batch** + **Nightly Reconciliation Prefix** | Strict schema quarantine on bronze landings; row count equality checks required. |
| **AMD-007** | **CDS Hooks & CRD Latency** | **Six Mandatory CDS Hooks**; P99 Latency < 5.0 seconds | Dedicated relational cache; unlisted codes default to *"Prior Authorization Required"*. |
| **AMD-008** | **Privacy & Audit Invariants**| **Dedicated Audit DB (MongoDB)** + CloudTrail / Audit Logs | Count-only, latency, and status logging; zero member identifiers or payloads in logs. |

---

## 3.1 Canonical Kickoff Documentation Pack

Per ticket **INT-378** (`S00-ST01-T02` / Jira `DSP-6547`), all cross-functional squads are pinned to three canonical architectural specifications maintained under [`kickoff_pack/01_KICKOFF_PACK_MANIFEST.md`](file:///Users/ashishsingh/Projects/CMS-Interop/CMS-InterOp/kickoff_pack/01_KICKOFF_PACK_MANIFEST.md):

| Document Code | Document Title | Canonical Path | Checksum (SHA-256) | Squad Assignment |
| :--- | :--- | :--- | :--- | :--- |
| **DOC-01-ARCH** | **Consolidated Architecture Specification** | `kickoff_pack/docs/01-Patient-Access-API-From-Scratch-Plan.pdf` | `c33b328c789011bff...` | Access APIs, Lakehouse, Cloud Infra |
| **DOC-02-SETUP** | **Services Setup & Verification Log** | `kickoff_pack/docs/Environment_Setup_Verification_Log.pdf` | `4d4a4db07d4b2a6...` | Cloud Infra, FHIR & ePA, QA Squad |
| **DOC-03-STEPS** | **Kickoff Steps & Delivery Lifecycle** | `kickoff_pack/docs/03-Onyx-Sprints-and-Delivery-Lifecycle.pdf` | `d90535e5c09d659...` | Ingestion, Lakehouse, QA Squad |

---

## 4. SDLC DevOps Lifecycle Standard

Every ticket follows the standard DevOps progression across Linear, Git, and automated test runners:

```mermaid
flowchart LR
    Plan["1. PLAN<br/>(Scope & Arch)"] --> Run["2. RUN<br/>(Code & IaC)"]
    Run --> Artifacts["3. ARTIFACTS<br/>(Scripts & Config)"]
    Artifacts --> QA["4. QA<br/>(Automated Tests)"]
    QA --> MR["5. MR / PR<br/>(Peer & Lead Review)"]
    MR --> Approved["6. APPROVAL<br/>(Lead Sign-Off)"]
    Approved --> Release["7. RELEASE<br/>(Mainline Merge)"]
```

### Linear Ticket Status Alignment
1. **Selected for Development** &rarr; Ticket scheduled for current sprint.
2. **In Progress / In Dev** &rarr; Feature branch created (`feature/<ticket-id>-<slug>`), code authored.
3. **Dev Completed** &rarr; Code complete, unit tests pass.
4. **In QA / QA Done** &rarr; Verification script executed, evidence recorded in JSON.
5. **MR Created** &rarr; Pull Request / Merge Request opened with full audit trails.
6. **MR Approved** &rarr; Lead approval received.
7. **Released / Done** &rarr; Merged to `main`, documentation PDF archived to `Linear-Tickets`.

---

## 5. Verification & Quality Assurance Suite

Run the automated verification suite from the repository root:

```bash
# Execute the Charter & Merge Decisions QA Suite
python3 scripts/verify_charter_decisions.py
```

### Latest QA Verification Output
```text
======================================================================
  CMS-0057 QA VERIFICATION SUITE: INT-377 (S00-ST01-T01)
======================================================================
  Total Checks Executed : 12
  Passed Checks         : 12 [SUCCESS]
  Failed Checks         : 0
  Overall Status        : PASS
  Results Written To    : charter_verification_results.json
======================================================================
```

---

## 6. Directory Layout

```text
CMS-InterOp/
├── charter/
│   ├── 01_PROJECT_CHARTER.md          # Formal Ratified Architecture Contract
│   └── eight_merge_decisions.json     # Machine-Readable Decision Specifications
├── scripts/
│   └── verify_charter_decisions.py    # Automated Verification & Invariant Suite
├── charter_verification_results.json  # Latest Automated Verification Evidence
└── README.md                          # Repository Architecture & DevOps Documentation
```

---

## 7. Compliance & Certification Alignment

* **AWS Certified Data Engineer (DEA-C01):** Task 4.5 Data privacy & governance boundary contracts.
* **AWS Solutions Architect Professional (SAP-C02) / Associate (SAA-C03):** Task 1.3 Data security controls before resource inception.
* **AWS DevOps Engineer Professional (DOP-C02):** Task 6.2 Compliance gating and SDLC automation.
* **Google Cloud Professional Cloud Architect (PCA):** Domain 1.1 Business requirement scoping & stakeholder consensus.
* **Google Cloud Professional Data Engineer (PDE):** Domain 1.3 Translating regulatory mandates into multi-cloud architectures.

---

*Copyright &copy; 2026 Ashish Singh ([@AshishSys](https://github.com/AshishSys)). All rights reserved.*
