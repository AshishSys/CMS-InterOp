#!/usr/bin/env python3
"""
PDF Generator for Ticket INT-380 Completion Report
Saves to:
  1. /Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-380/INT-380_Record_a_lead_for_each_squad.pdf
  2. /Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-380_Record_a_lead_for_each_squad.pdf
"""

import os
import sys
import shutil
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(36, 580, "CMS-0057 Interoperability Architecture: Ticket INT-380 Completion Report (Sprint S00)")
            self.drawRightString(756, 580, "Governance: Squad Leads & Jira Lane Registry")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(36, 574, 756, 574)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(756, 25, page_text)
        self.drawString(36, 25, "Confidential - CMS-0057 Architecture Platform - Ashish Singh | AWS 646044944744 | GCP project-1c617076-69b8-413f-94d")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(36, 35, 756, 35)
        self.restoreState()

def build_pdf():
    ticket_dir = "/Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets/INT-380"
    general_dir = "/Users/ashishsingh/Projects/CMS-Interop/Linear-Tickets"
    os.makedirs(ticket_dir, exist_ok=True)
    os.makedirs(general_dir, exist_ok=True)

    pdf_in_ticket = os.path.join(ticket_dir, "INT-380_Record_a_lead_for_each_squad.pdf")
    pdf_in_general = os.path.join(general_dir, "INT-380_Record_a_lead_for_each_squad.pdf")

    doc = SimpleDocTemplate(
        pdf_in_ticket,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=3
    )

    sub_title_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=8
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=7,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor('#2D3748')
    )

    body_bold = ParagraphStyle(
        'TableBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    elements = []

    # Title & Metadata
    elements.append(Paragraph("CMS-0057 Interoperability Architecture — Formal Ticket Deliverable", title_style))
    elements.append(Paragraph(
        "<b>Ticket ID:</b> INT-380 &nbsp;|&nbsp; <b>Jira Ref:</b> SO / DSP / XPORT / CMS / ONYX / PRODOPS &nbsp;|&nbsp; "
        "<b>Sprint:</b> Sprint 00 (S00) Foundations & Governance &nbsp;|&nbsp; "
        "<b>Parent Story:</b> S00-ST02 (INT-303) Operational Governance & Ownership &nbsp;|&nbsp; "
        "<b>Generated:</b> " + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        sub_title_style
    ))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=7))

    # Executive Summary & Cloud Metadata Table
    summary_data = [
        [
            Paragraph("<b>Ticket Title</b>", body_bold),
            Paragraph("[S00-ST02-T02] Record a lead for each squad", body_style),
            Paragraph("<b>Target Environment</b>", body_bold),
            Paragraph("Multi-Cloud Hybrid (AWS & GCP)", body_style)
        ],
        [
            Paragraph("<b>Document Reference</b>", body_bold),
            Paragraph("DOC-GOV-SQUADS-V1 (governance/02_SQUAD_LEADS.md)", body_style),
            Paragraph("<b>AWS Account ID</b>", body_bold),
            Paragraph("646044944744", body_bold)
        ],
        [
            Paragraph("<b>SDLC DevOps State</b>", body_bold),
            Paragraph("QA Done -> MR Created -> MR Approved -> Released", body_style),
            Paragraph("<b>GCP Project ID</b>", body_bold),
            Paragraph("project-1c617076-69b8-413f-94d", body_bold)
        ],
        [
            Paragraph("<b>Git Repository / Branch</b>", body_bold),
            Paragraph("AshishSys/CMS-InterOp &nbsp;|&nbsp; feature/INT-380-record-squad-leads", body_style),
            Paragraph("<b>Verification Result</b>", body_bold),
            Paragraph("<font color='#22543D'><b>10/10 CHECKS PASSED (100% SUCCESS)</b></font>", body_style)
        ]
    ]

    t_summary = Table(summary_data, colWidths=[120, 240, 110, 250])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_summary)
    elements.append(Spacer(1, 6))

    # Section 1: The Six Engineering Squads & Jira Lane Registry
    elements.append(Paragraph("1. Six Engineering Squads & Jira Lane Registry (DOC-GOV-SQUADS-V1)", section_heading))

    squads_data = [
        [
            Paragraph("Squad ID & Name", table_header),
            Paragraph("Jira Lane", table_header),
            Paragraph("Named Lead", table_header),
            Paragraph("Contact Identity", table_header),
            Paragraph("Architectural Scope & Boundary", table_header)
        ],
        [
            Paragraph("<b>SQ-01: Cloud Foundation</b>", body_bold),
            Paragraph("<code>SO</code>", body_bold),
            Paragraph("<b>Ashish Singh</b>", body_bold),
            Paragraph("squad.cloud@cmsinterop.internal", body_style),
            Paragraph("Landing Zones (AWS 646044944744 & GCP project-1c617076-69b8-413f-94d), IAM policies, VPC peering, transit gateways, KMS keys, Terraform IaC.", body_style)
        ],
        [
            Paragraph("<b>SQ-02: Ingestion & Pipelines</b>", body_bold),
            Paragraph("<code>DSP</code>", body_bold),
            Paragraph("<b>Ashish Singh</b>", body_bold),
            Paragraph("squad.ingest@cmsinterop.internal", body_style),
            Paragraph("Clinical/claims ingestion (HL7 v2, X12 837/834/835, CCDA), Kinesis/PubSub event streams, Airflow/Composer DAGs, DLQ isolation.", body_style)
        ],
        [
            Paragraph("<b>SQ-03: Lakehouse & Platform</b>", body_bold),
            Paragraph("<code>XPORT</code>", body_bold),
            Paragraph("<b>Ashish Singh</b>", body_bold),
            Paragraph("squad.lakehouse@cmsinterop.internal", body_style),
            Paragraph("S3/GCS Medallion architecture (Bronze WORM lock, Silver Parquet, Gold Marts), Apache Iceberg formats, BigQuery/Athena, 7-yr retention.", body_style)
        ],
        [
            Paragraph("<b>SQ-04: FHIR & ePA Clinical</b>", body_bold),
            Paragraph("<code>CMS</code>", body_bold),
            Paragraph("<b>Ashish Singh</b>", body_bold),
            Paragraph("squad.fhir-epa@cmsinterop.internal", body_style),
            Paragraph("HL7 FHIR R4 & US Core v3.1.1/6.1.0, Da Vinci PAS STU 2.0.1 (FHIR to X12 278 engine), CRD CDS hooks, DTR CQL rules, 72h/7d turnaround.", body_style)
        ],
        [
            Paragraph("<b>SQ-05: Access APIs Gateway</b>", body_bold),
            Paragraph("<code>ONYX</code>", body_bold),
            Paragraph("<b>Ashish Singh</b>", body_bold),
            Paragraph("squad.apis@cmsinterop.internal", body_style),
            Paragraph("SMART on FHIR OAuth 2.0 / OIDC, Patient Access (45 CFR § 170.215), Provider Access, Payer-to-Payer, Provider Directory, mTLS gateway.", body_style)
        ],
        [
            Paragraph("<b>SQ-06: Quality & QA Conformance</b>", body_bold),
            Paragraph("<code>PRODOPS</code>", body_bold),
            Paragraph("<b>Ashish Singh</b>", body_bold),
            Paragraph("squad.quality@cmsinterop.internal", body_style),
            Paragraph("ONC Inferno & Touchstone conformance harnesses, Synthea EHR test beds, CI/CD automated gates (100% pass), HIPAA/HITRUST/SOC2 audit trails.", body_style)
        ]
    ]

    t_squads = Table(squads_data, colWidths=[120, 45, 85, 140, 330])
    t_squads.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1A365D')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_squads)
    elements.append(Spacer(1, 6))

    # Section 2: Certification & Industry Competency Alignment
    elements.append(Paragraph("2. Certification & Multi-Cloud Competency Alignment", section_heading))

    cert_data = [
        [
            Paragraph("Squad & Lane", table_header),
            Paragraph("AWS Certification Competency", table_header),
            Paragraph("Google Cloud Certification Competency", table_header),
            Paragraph("Governance Boundary Enforced", table_header)
        ],
        [
            Paragraph("<b>Cloud Foundation (SO)</b>", body_bold),
            Paragraph("<b>SAA-C03 Task 1.3:</b> Data security controls & boundaries<br/><b>DOP-C02 Task 6.2:</b> Automation for security controls", body_style),
            Paragraph("<b>Prof. Cloud Architect 1.1 & 4.2:</b> Business requirements & stakeholder decisions", body_style),
            Paragraph("Multi-cloud landing zone lockdown before resources are spun up.", body_style)
        ],
        [
            Paragraph("<b>Ingest & Pipelines (DSP)</b>", body_bold),
            Paragraph("<b>DEA-C01 Task 4.5:</b> Data privacy & governance in pipelines", body_style),
            Paragraph("<b>Prof. Data Engineer 1.3:</b> Map business requirements onto pipelines", body_style),
            Paragraph("Strict schema quarantine and DLQ isolation for clinical feeds.", body_style)
        ],
        [
            Paragraph("<b>Lakehouse (XPORT)</b>", body_bold),
            Paragraph("<b>DEA-C01 Task 4.5:</b> Storage governance, encryption & lifecycle", body_style),
            Paragraph("<b>Prof. Data Engineer 1.1:</b> Dev vs Prod segregation", body_style),
            Paragraph("Medallion WORM immutability; prod data store remains empty.", body_style)
        ],
        [
            Paragraph("<b>FHIR & ePA (CMS)</b>", body_bold),
            Paragraph("<b>SAA-C03 Task 1.3:</b> Secure PHI clinical processing", body_style),
            Paragraph("<b>Prof. Cloud Architect 1.1:</b> Regulatory compliance architecture", body_style),
            Paragraph("Profile A flat-file batch ingestion to FHIR PAS bundle engine.", body_style)
        ],
        [
            Paragraph("<b>Access APIs (ONYX)</b>", body_bold),
            Paragraph("<b>SAA-C03 Task 1.3:</b> Identity federation & OAuth scopes", body_style),
            Paragraph("<b>Prof. Cloud Architect 1.1:</b> Zero-trust doorway & API security", body_style),
            Paragraph("SMART on FHIR token introspection; no backend subnet exposure.", body_style)
        ],
        [
            Paragraph("<b>Quality & QA (PRODOPS)</b>", body_bold),
            Paragraph("<b>DOP-C02 Task 6.2:</b> Automated security & data protection gates", body_style),
            Paragraph("<b>Prof. Cloud Architect 4.2:</b> Auditing & operational excellence", body_style),
            Paragraph("100% automated test pass requirement for PR merge clearance.", body_style)
        ]
    ]

    t_cert = Table(cert_data, colWidths=[110, 220, 220, 170])
    t_cert.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B6CB0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_cert)
    elements.append(Spacer(1, 6))

    # Section 3: QA Automated Verification Results Table
    elements.append(Paragraph("3. QA Automated Verification & Test Results (10/10 Passed)", section_heading))

    checks_data = [
        [
            Paragraph("Test ID", table_header),
            Paragraph("Verification Focus", table_header),
            Paragraph("Target Rule / Standard", table_header),
            Paragraph("Status", table_header)
        ],
        [
            Paragraph("TC-SQL-01", body_bold),
            Paragraph("Squad Leads Markdown Charter", body_style),
            Paragraph("governance/02_SQUAD_LEADS.md exists, non-empty, and valid", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-02", body_bold),
            Paragraph("Structured JSON Registry Schema", body_style),
            Paragraph("governance/squad_leads.json is valid JSON with required schema", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-03", body_bold),
            Paragraph("Squad Count & Identifier Range", body_style),
            Paragraph("Exactly 6 squads present with IDs SQ-01 through SQ-06", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-04", body_bold),
            Paragraph("Jira Lane Mapping Completeness", body_style),
            Paragraph("All 6 Jira lanes mapped: SO, DSP, XPORT, CMS, ONYX, PRODOPS", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-05", body_bold),
            Paragraph("Named Squad Lead Identity", body_style),
            Paragraph("Ashish Singh assigned as lead across all active delivery lanes", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-06", body_bold),
            Paragraph("Squad Contact & Title Attributes", body_style),
            Paragraph("Email contacts and squad titles configured for all 6 squads", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-07", body_bold),
            Paragraph("AWS Account Reference Integrity", body_style),
            Paragraph("AWS Account 646044944744 present in all squad governance artifacts", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-08", body_bold),
            Paragraph("GCP Project Reference Integrity", body_style),
            Paragraph("GCP Project project-1c617076-69b8-413f-94d present in all squad governance artifacts", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-09", body_bold),
            Paragraph("Project Charter Cross-Reference", body_style),
            Paragraph("charter/01_PROJECT_CHARTER.md Section 4.2 cites DOC-GOV-SQUADS-V1", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ],
        [
            Paragraph("TC-SQL-10", body_bold),
            Paragraph("README System Map Synchronization", body_style),
            Paragraph("README.md Section 3.3 documents Six Squads & Jira Lane Ownership", body_style),
            Paragraph("<font color='#22543D'><b>PASSED</b></font>", body_style)
        ]
    ]

    t_checks = Table(checks_data, colWidths=[70, 180, 400, 70])
    t_checks.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2C5282')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_checks)
    elements.append(Spacer(1, 6))

    # Build Document
    doc.build(elements, canvasmaker=NumberedCanvas)
    shutil.copyfile(pdf_in_ticket, pdf_in_general)
    print(f"Successfully generated INT-380 Report PDF at:\n  - {pdf_in_ticket}\n  - {pdf_in_general}")

if __name__ == '__main__':
    build_pdf()
