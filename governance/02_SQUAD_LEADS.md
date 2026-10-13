# Squad Leadership & Jira Lane Governance Charter (DOC-GOV-SQUADS-V1)

**Document Reference:** `DOC-GOV-SQUADS-V1`  
**Parent Engagement:** CMS-0057 Interoperability Architecture Platform  
**Sprint / Track:** Sprint 00 (S00) — Foundations & Governance / Shared  
**Linear Ticket:** `INT-380` (`[S00-ST02-T02] Record a lead for each squad`)  
**Parent Story:** `INT-303` (`[S00-ST02] Record engagement owners and squad leads`)  
**Jira Reference:** `SO` / `DSP` / `XPORT` / `CMS` / `ONYX` / `PRODOPS` lanes  
**Effective Date:** October 13, 2026  
**Status:** Canonical / Approved  

---

## 1. Executive Context & Purpose

Under the CMS-0057 Federal Interoperability and Prior Authorization Rule mandate, enterprise execution requires clear division of labor, architectural ownership, and accountability across the entire clinical data lifecycle.

To mirror industry-standard enterprise Jira project lane topologies, the CMS-0057 program is organized into **six specialized engineering squads**. Each squad possesses an exclusive delivery lane, defined boundaries, regulatory responsibilities, and an accountable squad lead.

Per enterprise best practice:
- **One lead is formally named per squad lane**.
- While during initial phases or trial periods a single experienced technical leader may hold multiple squad lead roles, **each appointment is formally recorded and bounded** in this canonical register.
- Squad boundaries enforce data governance, privacy, and architectural control before cloud infrastructure resources are instantiated.

### Target Multi-Cloud Infrastructure Environments
- **Primary AWS Account ID:** `646044944744`
- **Primary GCP Project ID:** `project-1c617076-69b8-413f-94d`

---

## 2. Six Specialized Squads & Jira Lane Registry

| Squad ID | Squad Name | Jira Lane Key | Named Squad Lead | Contact Identity | Architectural Domain & Focus |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SQ-01** | **Cloud Foundation Squad** | `SO` | **Ashish Singh** | `squad.cloud@cmsinterop.internal` | Multi-Cloud Landing Zones, IAM, VPC, KMS, CI/CD, Network Peering |
| **SQ-02** | **Ingestion & Data Pipelines Squad** | `DSP` | **Ashish Singh** | `squad.ingest@cmsinterop.internal` | HL7 v2, X12 EDI (837/834/835), CCDA, Streaming Ingest, Airflow / Composer |
| **SQ-03** | **Lakehouse & Data Platform Squad** | `XPORT` | **Ashish Singh** | `squad.lakehouse@cmsinterop.internal` | S3 / GCS Medallion Lakehouse, Apache Iceberg, BigQuery / Athena, CMEK |
| **SQ-04** | **FHIR & Prior Authorization (ePA) Squad** | `CMS` | **Ashish Singh** | `squad.fhir-epa@cmsinterop.internal` | HL7 FHIR US Core 3.1.1/6.1.0, Da Vinci CRD, DTR, PAS (STU 2.0.1), X12 278 Engine |
| **SQ-05** | **Patient & Provider Access APIs Squad** | `ONYX` | **Ashish Singh** | `squad.apis@cmsinterop.internal` | SMART on FHIR OAuth 2.0 / OIDC, Patient Access, Provider Access, Payer-to-Payer |
| **SQ-06** | **Quality & Compliance Verification Squad** | `PRODOPS` | **Ashish Singh** | `squad.quality@cmsinterop.internal` | Inferno / Touchstone Conformance, Synthea EHR, HIPAA/HITRUST, SOC 2, Automated QA |

---

## 3. Detailed Squad Charters & Responsibilities

### 3.1 Squad 1: Cloud Foundation Squad (`SO`)
- **Jira Lane:** `SO` (Systems Operations & Cloud Platform)
- **Named Lead:** Ashish Singh (Cloud Infrastructure & Landing Zone Lead)
- **Primary Mission:** Establish and maintain zero-trust multi-cloud infrastructure, account segregation, and governance baselines.
- **Key Responsibilities:**
  - Multi-cloud Landing Zone management across AWS (`646044944744`) and GCP (`project-1c617076-69b8-413f-94d`).
  - IAM least-privilege role policies, Workload Identity federation, and cross-cloud authentication.
  - VPC network topologies, transit gateways, Cloud Interconnect, VPC peering, and firewall perimeter rules.
  - KMS encryption keyrings, CMEK rotation policies, and Secret Manager vaults.
  - Terraform / OpenTofu Infrastructure-as-Code modules and continuous drift detection.
- **Certification & Competency Mapping:**
  - **AWS SAA-C03 Task 1.3:** Determine appropriate data security controls and infrastructure boundaries.
  - **AWS DOP-C02 Task 6.2:** Apply automation for security controls and data protection.
  - **Google Professional Cloud Architect 1.1 & 4.2:** Design business requirement architectures and stakeholder decisions.

---

### 3.2 Squad 2: Ingestion & Data Pipelines Squad (`DSP`)
- **Jira Lane:** `DSP` (Data Streaming & Pipelines)
- **Named Lead:** Ashish Singh (Data Ingestion & Integration Lead)
- **Primary Mission:** Author resilient, observable batch and streaming ingestion pipelines for clinical and financial healthcare datasets.
- **Key Responsibilities:**
  - Ingestion interfaces for HL7 v2 ADT/ORU messages, X12 EDI 837 (Claims), 834 (Enrollment), 835 (Remittance), and CCDA documents.
  - Event streaming through Amazon Kinesis Data Streams and Google Cloud Pub/Sub.
  - Orchestration DAGs in Apache Airflow and Google Cloud Composer.
  - Ingestion schema validation, data dead-letter queue (DLQ) quarantine, and schema evolution tracking.
  - Automated alerting for pipeline backpressure, late-arriving data, and unparseable clinical segments.
- **Certification & Competency Mapping:**
  - **AWS DEA-C01 Task 4.5:** Understand data privacy and governance in ingestion pipelines.
  - **Google Professional Data Engineer 1.3:** Map business requirements onto data pipeline architectures.

---

### 3.3 Squad 3: Lakehouse & Data Platform Squad (`XPORT`)
- **Jira Lane:** `XPORT` (Export & Lakehouse Storage)
- **Named Lead:** Ashish Singh (Lakehouse Architecture & Storage Lead)
- **Primary Mission:** Design and operate high-scale, immutable, cost-optimized healthcare lakehouse storage using medallion architecture.
- **Key Responsibilities:**
  - S3 / GCS Medallion architecture:
    - *Bronze Layer:* Raw payload capture with WORM object lock and compliance holds.
    - *Silver Layer:* Cleaned, deduplicated, schema-validated Parquet / FHIR NDJSON datasets.
    - *Gold Layer:* Curated analytical star/snowflake schemas, CMS-0057 compliance marts, and measure reporting.
  - Apache Iceberg open table format with metadata catalogs, partition evolution, and time-travel querying.
  - Serverless and distributed query engines (Google BigQuery, Amazon Athena, AWS Glue Data Catalog).
  - Lifecycle management: intelligent tiering to Glacier Flexible Archive / GCS Archive for 7-year regulatory retention.
- **Certification & Competency Mapping:**
  - **AWS DEA-C01 Task 4.5:** Storage governance, encryption, data lifecycle, and compliance archiving.
  - **Google Professional Data Engineer 1.1:** Segregation of development, staging, and production data tiers.

---

### 3.4 Squad 4: FHIR & Prior Authorization (ePA) Squad (`CMS`)
- **Jira Lane:** `CMS` (CMS Compliance & Clinical Services)
- **Named Lead:** Ashish Singh (Healthcare Interoperability & Clinical Lead)
- **Primary Mission:** Build end-to-end CMS-0057 compliant FHIR resources and automated Prior Authorization (ePA) workflows.
- **Key Responsibilities:**
  - Conformance with HL7 FHIR Release 4.0.1 and US Core Implementation Guide (v3.1.1 and v6.1.0).
  - Implementation of Da Vinci Prior Authorization Support (PAS - STU 2.0.1) FHIR-to-X12 278/275 bi-directional translation engine.
  - Implementation of Da Vinci Coverage Requirements Discovery (CRD) via CDS Hooks.
  - Implementation of Da Vinci Documentation Templates and Rules (DTR) using CQL (Clinical Quality Language).
  - FHIR Conformance Statements (`CapabilityStatement`, `StructureDefinition`, `OperationDefinition`).
  - Strict compliance with CMS statutory turnaround limits (72 hours expedited, 7 calendar days standard).
- **Certification & Competency Mapping:**
  - **Google Professional Cloud Architect 1.1:** Interoperability and federal regulatory compliance engineering.
  - **AWS SAA-C03 Task 1.3:** Secure processing of Protected Health Information (PHI).

---

### 3.5 Squad 5: Patient & Provider Access APIs Squad (`ONYX`)
- **Jira Lane:** `ONYX` (Onyx Interoperability API Gateway)
- **Named Lead:** Ashish Singh (Interoperability API & Gateway Lead)
- **Primary Mission:** Deliver high-performance, secure, standardized external APIs for patients, providers, and payers.
- **Key Responsibilities:**
  - SMART on FHIR OAuth 2.0 authorization server integration, OpenID Connect (OIDC), and token introspection.
  - CMS Patient Access API (45 CFR § 170.215) providing clinical data, claims, encounters, and formulary access.
  - CMS Provider Access API for treatment and care coordination queries.
  - CMS Payer-to-Payer Data Exchange API for continuous member longitudinal record transfer.
  - Provider Directory API for public, unauthenticated health system provider lookup.
  - API Gateway perimeter management: mutual TLS (mTLS), DDoS shielding (AWS Shield / Cloud Armor), and granular rate limiting.
- **Certification & Competency Mapping:**
  - **AWS SAA-C03 Task 1.3:** Identity federation, OAuth 2.0 scopes, and secure API perimeter controls.
  - **AWS DOP-C02 Task 6.2:** Continuous API gateway security policy enforcement.

---

### 3.6 Squad 6: Quality & Compliance Verification Squad (`PRODOPS`)
- **Jira Lane:** `PRODOPS` (Production Operations & QA)
- **Named Lead:** Ashish Singh (Quality Assurance & Regulatory Audit Lead)
- **Primary Mission:** Validate technical, clinical, and regulatory compliance through automated test harnesses and security audits.
- **Key Responsibilities:**
  - Automated FHIR testing via ONC Inferno Test Framework and Aegis Touchstone testing harnesses.
  - Maintenance of synthetic EHR patient populations (Synthea) representing diverse clinical cohorts.
  - Continuous integration QA test suites enforcing 100% compliance gate pass before production deployment.
  - HIPAA Security Rule compliance, HITRUST CSF validation, and immutable multi-cloud audit logging.
  - Incident response, site reliability engineering (SRE), synthetic uptime monitoring, and latency SLA adherence.
- **Certification & Competency Mapping:**
  - **AWS DOP-C02 Task 6.2:** Apply automation for security controls and regulatory data protection.
  - **Google Professional Cloud Architect 4.2:** Operational excellence, auditing, and compliance verification.

---

## 4. Multi-Squad RACI Matrix

| Program Lifecycle Activity | `SO` (Cloud) | `DSP` (Ingest) | `XPORT` (Lakehouse) | `CMS` (FHIR/ePA) | `ONYX` (APIs) | `PRODOPS` (QA) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Cloud VPC & Landing Zone Provisioning | **A / R** | C | C | I | C | C |
| Clinical Feed Ingestion & DLQ Isolation | I | **A / R** | C | C | I | C |
| Medallion Lakehouse & Retention Storage | C | C | **A / R** | C | I | C |
| FHIR Profile Authoring & ePA Translation | I | C | C | **A / R** | C | C |
| SMART on FHIR Gateway & External APIs | C | I | I | C | **A / R** | C |
| Conformance Verification & Audit Sign-Off | C | C | C | C | C | **A / R** |

*Key: **A** = Accountable, **R** = Responsible, **C** = Consulted, **I** = Informed*

---

## 5. Trial Leadership Holding Governance

Per standard enterprise transition models, technical leadership consolidation is permitted during Phase 0 / Sprint 00 discovery provided that:
1. **Explicit Separation of Concerns:** Lane responsibilities remain cleanly partitioned in Jira, Git repositories, and documentation.
2. **Independent Sign-Off Gates:** Work produced within a lane must still pass automated verification test suites before handoff to adjacent squads.
3. **Staffing Readiness:** As squads scale, individual lane leads will be transitioned with full handover documentation preserved in this repository.

---

## 6. Document Metadata & Authorization

- **Document ID:** `DOC-GOV-SQUADS-V1`
- **Product Owner:** Ashish Singh (`ashish.singh@cmsinterop.internal`)
- **AWS Account ID:** `646044944744`
- **GCP Project ID:** `project-1c617076-69b8-413f-94d`
- **Linear Issue:** `INT-380` (`b15b904a-2fe3-46f8-819e-6ef0ce0c8f76`)
- **Parent Story:** `INT-303` (`4e8bcb1d-bb91-4017-8ad8-2cc1f321b50e`)
