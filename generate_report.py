import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def build_pdf():
    pdf_path = os.path.join(os.path.dirname(__file__), "CCA2_SUBMISSION_REPORT.pdf")
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0f172a")
    accent_color = colors.HexColor("#0284c7")
    success_color = colors.HexColor("#16a34a")
    danger_color = colors.HexColor("#dc2626")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=1,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_color,
        alignment=1,
        spaceAfter=15
    )

    heading2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'CodeStyleCustom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=1,
        borderPadding=6,
        spaceAfter=8
    )

    elements = []

    # PAGE 1: TITLE & STUDENT DETAILS
    elements.append(Paragraph("MIT World Peace University, Pune", subtitle_style))
    elements.append(Paragraph("Department of Computer Engineering and Technology", ParagraphStyle('Dept', alignment=1, fontSize=10, textColor=colors.HexColor("#64748b"))))
    elements.append(Paragraph("Cloud Computing and DevOps (CSE30040)", ParagraphStyle('Course', alignment=1, fontSize=10, textColor=colors.HexColor("#64748b"), spaceAfter=15)))
    elements.append(HRFlowable(width="100%", thickness=2, color=accent_color, spaceAfter=20))

    elements.append(Paragraph("CCA 2 INDIVIDUAL ASSESSMENT SUBMISSION REPORT", title_style))
    elements.append(Paragraph("Dynamic Web Application & Automated Git CI/CD Pipeline", subtitle_style))
    elements.append(Spacer(1, 15))

    # Student Details Table
    table_data = [
        [Paragraph("<b>Field</b>", body_style), Paragraph("<b>Student Details</b>", body_style)],
        [Paragraph("Student Name", body_style), Paragraph("[Your Full Name]", body_style)],
        [Paragraph("PRN", body_style), Paragraph("[Your PRN]", body_style)],
        [Paragraph("Roll No. / Panel", body_style), Paragraph("[Your Roll No / Panel]", body_style)],
        [Paragraph("Project Title", body_style), Paragraph("Cosarc - Cinematic Fitness & Discipline Portal", body_style)],
        [Paragraph("GitHub Repository URL", body_style), Paragraph("https://github.com/anisherande23-lab/Web-Gym-", body_style)],
        [Paragraph("Live Application URL", body_style), Paragraph("https://web-gym-rvze.onrender.com", body_style)],
        [Paragraph("Date of Submission", body_style), Paragraph("September 24, 2026", body_style)],
        [Paragraph("Course Faculty", body_style), Paragraph("Pranati Waghodekar", body_style)]
    ]

    t = Table(table_data, colWidths=[2.2*inch, 4.8*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.HexColor("#0284c7")),
        ('TEXTCOLOR', (0,0), (1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("1. Problem Statement & System Overview", heading2_style))
    elements.append(Paragraph(
        "Modern web applications require reliable release mechanisms that guarantee zero-downtime deployment, code quality verification, and automated safety gates. "
        "The <b>Cosarc Dynamic Web Application</b> was developed as a dynamic fitness and discipline contract logging portal. "
        "Every page request dynamically renders server-side data, calculates live completion metrics, and validates incoming user input before storing entries in memory.",
        body_style
    ))
    elements.append(Paragraph(
        "Key Features of the Cosarc Web Portal:<br/>"
        "• <b>Server-Side Dynamic Rendering:</b> Dynamic calculation of total contracts, completion rate percentage, average discipline score, and active commit ID.<br/>"
        "• <b>Form Input Validation:</b> Quality gate enforcing mandatory title, category selection, target string, and rating between 1 and 5.<br/>"
        "• <b>JSON API Route:</b> Public <code>/api/contracts</code> endpoint exposing formatted contract data.<br/>"
        "• <b>Container Health Route:</b> <code>/health</code> endpoint returning HTTP 200 OK and running Git commit SHA.<br/>"
        "• <b>Commit Tracking Footer:</b> Footer displaying <code>commit &lt;sha&gt;</code> injected via environment variables.",
        body_style
    ))

    elements.append(PageBreak())

    # PAGE 2: ARCHITECTURE & PIPELINE
    elements.append(Paragraph("2. Architecture & CI/CD Pipeline Design", heading2_style))
    elements.append(Paragraph(
        "The application architecture separates quality validation, container packaging, and deployment into sequential stages defined in GitHub Actions (<code>.github/workflows/ci-cd.yml</code>).",
        body_style
    ))

    pipeline_table = [
        [Paragraph("<b>Pipeline Stage</b>", body_style), Paragraph("<b>Tools & Command</b>", body_style), Paragraph("<b>Trigger & Safety Condition</b>", body_style)],
        [Paragraph("1. Quality Gates (CI)", body_style), Paragraph("ESLint 9, node:test<br/><code>npm run lint && npm test</code>", body_style), Paragraph("Runs on every push & pull request. Any error blocks build.", body_style)],
        [Paragraph("2. Docker Build & Smoke Test", body_style), Paragraph("Docker Desktop / Alpine<br/><code>docker build --build-arg GIT_SHA</code>", body_style), Paragraph("Needs Stage 1. Launches container locally & tests <code>/health</code>.", body_style)],
        [Paragraph("3. Render CD Release", body_style), Paragraph("Render Deploy Webhook<br/><code>curl -X POST RENDER_DEPLOY_HOOK</code>", body_style), Paragraph("Needs Stage 2. Triggers <i>only</i> on <code>push</code> to <code>main</code> branch.", body_style)]
    ]
    t_pipe = Table(pipeline_table, colWidths=[2.0*inch, 2.5*inch, 2.5*inch])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_pipe)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("3. Detailed Pipeline Stage Explanation", heading2_style))
    elements.append(Paragraph("<b>Stage 1: Linting & Automated Testing</b>", body_style))
    elements.append(Paragraph(
        "Code style is verified using ESLint. Four automated tests are executed using Node.js native test runner (<code>node:test</code>):<br/>"
        "1. <code>GET /health</code> returns 200 OK and valid health payload.<br/>"
        "2. <code>POST /contracts</code> with valid input creates contract and updates API.<br/>"
        "3. <code>POST /contracts</code> with invalid input (e.g. missing title) is rejected with 400 Bad Request.<br/>"
        "4. <code>GET /api/contracts</code> returns valid JSON schema and stats.",
        body_style
    ))

    elements.append(Paragraph("<b>Stage 2: Docker Containerization & Smoke Test</b>", body_style))
    elements.append(Paragraph(
        "The application is packaged inside a lightweight <code>node:22-alpine</code> Docker container. "
        "The build argument <code>GIT_SHA</code> is passed dynamically from <code>${{ github.sha }}</code> to embed the commit hash inside the container environment. "
        "A smoke test spins up the container, waits 5 seconds, and verifies HTTP status 200 from <code>http://localhost:3000/health</code> before stopping.",
        body_style
    ))

    elements.append(PageBreak())

    # PAGE 3: FAILURE DEMO & PREVENTING BAD DEPLOYS
    elements.append(Paragraph("4. Failure Demo: Preventing Bad Deployments", heading2_style))
    elements.append(Paragraph(
        "To satisfy assessment requirements, the CI/CD pipeline was tested under a intentional code failure scenario on a feature branch (<code>feature/broken-test-demo</code>).",
        body_style
    ))

    elements.append(Paragraph("<b>Failure Simulation Scenario:</b>", body_style))
    elements.append(Paragraph(
        "In <code>test/app.test.js</code>, an assertion was modified to intentionally expect <code>status: 'error'</code> instead of <code>status: 'ok'</code>.",
        code_style
    ))

    elements.append(Paragraph("<b>Observed Pipeline Behavior:</b>", body_style))
    elements.append(Paragraph(
        "1. The <code>test</code> job ran in GitHub Actions and failed during <code>npm test</code>.<br/>"
        "2. GitHub Actions immediately terminated the workflow with exit code 1.<br/>"
        "3. Because downstream jobs declared <code>needs: test</code> and <code>needs: build</code>, both the <b>Docker Build</b> and <b>Deploy</b> stages were automatically <b>SKIPPED</b>.<br/>"
        "4. Render was never pinged by the deploy hook, ensuring the live production app remained stable on the previous passing commit.",
        body_style
    ))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>Success Pipeline Verification:</b>", body_style))
    elements.append(Paragraph(
        "When the broken assertion was reverted and pushed to <code>main</code>, all stages ran in sequence:<br/>"
        "<code>Lint & Test (Pass) → Docker Build (Pass) → Render Deploy Webhook (Triggered)</code>.<br/>"
        "The live application immediately updated to reflect the new Git commit ID in the footer.",
        body_style
    ))

    elements.append(Spacer(1, 15))
    elements.append(Paragraph("5. Challenges Faced & Key Learnings", heading2_style))
    elements.append(Paragraph(
        "• <b>Environment Variable Resolution:</b> Ensuring the commit SHA was visible required configuring Docker build args (<code>ARG GIT_SHA</code>) and mapping them to process environment variables in Express.<br/>"
        "• <b>Asynchronous Test Setup:</b> Adapting <code>node:test</code> required using native Promises for server startup/shutdown to avoid race conditions.<br/>"
        "• <b>Render Auto-Deploy vs Webhook:</b> Turning Auto-Deploy <i>OFF</i> in Render ensured deployment occurred strictly when GitHub Actions CI quality checks passed.",
        body_style
    ))

    elements.append(PageBreak())

    # PAGE 4: VIVA PREPARATION & LINKS
    elements.append(Paragraph("6. Project Links & Verification Details", heading2_style))

    links_table = [
        [Paragraph("<b>Resource</b>", body_style), Paragraph("<b>Link / Path</b>", body_style)],
        [Paragraph("GitHub Repository", body_style), Paragraph("https://github.com/anisherande23-lab/Web-Gym-", body_style)],
        [Paragraph("Live Render Application", body_style), Paragraph("https://web-gym-rvze.onrender.com", body_style)],
        [Paragraph("GitHub Actions Pipeline", body_style), Paragraph("https://github.com/anisherande23-lab/Web-Gym-/actions", body_style)],
        [Paragraph("Workflow Configuration File", body_style), Paragraph("<code>.github/workflows/ci-cd.yml</code>", body_style)]
    ]
    t_links = Table(links_table, colWidths=[2.5*inch, 4.5*inch])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0284c7")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(t_links)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("7. Viva Questions & Answers Summary", heading2_style))
    elements.append(Paragraph(
        "<b>Q1: What is the difference between CI and CD?</b><br/>"
        "<i>Answer:</i> Continuous Integration (CI) automatically builds, lints, and runs tests on every commit to catch errors early. Continuous Deployment (CD) automatically releases passing code to production without human intervention.<br/><br/>"
        "<b>Q2: What does the <code>needs:</code> keyword do in GitHub Actions?</b><br/>"
        "<i>Answer:</i> It defines job dependencies. A job with <code>needs: test</code> will only run if the <code>test</code> job succeeds, enforcing sequential execution and blocking deployments on failure.<br/><br/>"
        "<b>Q3: Why store deploy hook URLs in GitHub Secrets?</b><br/>"
        "<i>Answer:</i> Exposing deploy hooks in public repositories allows anyone to trigger deployments. Storing them in Secrets hides credentials while keeping workflow files public.<br/><br/>"
        "<b>Q4: Why package the application in Docker?</b><br/>"
        "<i>Answer:</i> Docker guarantees environment parity between local development, CI testing, and production servers, preventing dependency mismatch issues.",
        body_style
    ))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceBefore=20, spaceAfter=15))
    elements.append(Paragraph("<b>End of CCA 2 Submission Report — Cosarc Web Portal</b>", ParagraphStyle('End', alignment=1, fontSize=10, textColor=colors.HexColor("#64748b"))))

    doc.build(elements)
    print(f"Report generated successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
