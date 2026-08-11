import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from typing import Dict, Any

def generate_interview_workbook_pdf(candidate_data: Dict[str, Any]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Clean Palette
    primary_color = colors.HexColor("#1e293b") # Slate 800
    accent_color = colors.HexColor("#2563eb")  # Blue 600
    dark_gray = colors.HexColor("#334155")
    light_bg = colors.HexColor("#f8fafc")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=accent_color,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Heading2'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=dark_gray,
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
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=dark_gray,
        spaceAfter=6
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    story = []

    # Header / Title Page Element
    story.append(Paragraph("AI INTERVIEW MASTER", title_style))
    story.append(Paragraph("Personalized MNC Interview Preparation Workbook", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=accent_color, spaceBefore=0, spaceAfter=15))

    # Candidate Profile & Target Overview
    story.append(Paragraph("1. Candidate Overview & Readiness Score", heading2_style))
    
    candidate_name = candidate_data.get("full_name", "Candidate")
    target_role = candidate_data.get("target_role", "Software / Python Developer")
    exp_level = candidate_data.get("experience_level", "INTERMEDIATE")
    target_companies = ", ".join(candidate_data.get("target_companies", ["Google", "Meta"]))
    readiness_score = candidate_data.get("readiness_score", 76.5)
    label = candidate_data.get("readiness_label", "Strong Preparation")

    profile_table_data = [
        [Paragraph("Candidate Name:", bold_body), Paragraph(candidate_name, body_style)],
        [Paragraph("Target Role:", bold_body), Paragraph(target_role, body_style)],
        [Paragraph("Experience Level:", bold_body), Paragraph(exp_level, body_style)],
        [Paragraph("Target Companies:", bold_body), Paragraph(target_companies, body_style)],
        [Paragraph("AI Readiness Score:", bold_body), Paragraph(f"<b>{readiness_score}%</b> ({label})", body_style)],
    ]

    t_profile = Table(profile_table_data, colWidths=[140, 380])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 15))

    # Diagnostic Skill Radar Breakdown
    story.append(Paragraph("2. Skill Readiness Breakdown", heading2_style))
    cat_scores = candidate_data.get("category_scores", {
        "Python": 84, "DSA": 71, "ML": 79, "Deep Learning": 73,
        "GenAI": 65, "SQL": 68, "System Design": 55, "Behavioral": 85
    })
    
    score_table_data = [[Paragraph("Skill Category", bold_body), Paragraph("Preparation Score", bold_body), Paragraph("Status", bold_body)]]
    for cat, score in cat_scores.items():
        st_text = "Strong" if score >= 75 else ("Developing" if score >= 60 else "Weak Area")
        score_table_data.append([Paragraph(cat, body_style), Paragraph(f"{score}%", body_style), Paragraph(st_text, body_style)])

    t_scores = Table(score_table_data, colWidths=[180, 160, 180])
    t_scores.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#cbd5e1")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_scores)
    story.append(Spacer(1, 15))

    # Personalized Roadmap Summary
    story.append(Paragraph("3. Personalized Preparation Plan (Summary)", heading2_style))
    story.append(Paragraph("Follow this structured roadmap daily to bridge detected skill gaps prior to your target interview date:", body_style))
    
    roadmap_tasks = candidate_data.get("roadmap_tasks", [
        {"day": 1, "topic": "Python Core Memory & Concurrency (GIL, Generators)", "time": "120 mins"},
        {"day": 2, "topic": "OOP Pillars & Design Patterns (Encapsulation, Polymorphism)", "time": "120 mins"},
        {"day": 3, "topic": "DSA Pattern Mastery: Two Pointers & Sliding Window", "time": "120 mins"},
        {"day": 4, "topic": "Transformers, Self-Attention & RAG Architecture", "time": "120 mins"},
        {"day": 5, "topic": "Full MNC Dynamic AI Mock Interview & Weakness Drill", "time": "90 mins"},
    ])

    roadmap_table_data = [[Paragraph("Day", bold_body), Paragraph("Topic & Focus Area", bold_body), Paragraph("Est. Duration", bold_body)]]
    for task in roadmap_tasks[:10]:
        d = task.get("day", task.get("day_number", 1))
        top = task.get("topic", "Topic")
        tm = task.get("time", f"{task.get('estimated_minutes', 120)} mins")
        roadmap_table_data.append([Paragraph(f"Day {d}", body_style), Paragraph(top, body_style), Paragraph(tm, body_style)])

    t_road = Table(roadmap_table_data, colWidths=[60, 360, 100])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e2e8f0")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_road)
    story.append(Spacer(1, 15))

    # High Yield Practice Questions
    story.append(Paragraph("4. High-Yield Interview Question Bank", heading2_style))
    questions_list = candidate_data.get("questions", [
        {"q": "Explain Python GIL and its impact on multithreading.", "cat": "Python", "diff": "ADVANCED"},
        {"q": "Explain Scaled Dot-Product Attention in Transformers.", "cat": "Generative AI", "diff": "ADVANCED"},
        {"q": "Design a Production RAG System for Millions of Documents.", "cat": "System Design / RAG", "diff": "ADVANCED"},
        {"q": "Tell me about a time you faced a technical conflict.", "cat": "Behavioral", "diff": "INTERMEDIATE"}
    ])

    for i, item in enumerate(questions_list[:8], 1):
        q_text = f"<b>Q{i} [{item.get('cat', 'General')} - {item.get('diff', 'INT')}]:</b> {item.get('q', item.get('question', 'Question'))}"
        story.append(Paragraph(q_text, body_style))

    story.append(Spacer(1, 15))

    # Final Interview Checklist
    story.append(Paragraph("5. Final MNC Interview Day Checklist", heading2_style))
    checklist = [
        "✔ Review STAR framework examples for your top 3 resume projects.",
        "✔ Re-verify time & space complexity trade-offs for core DSA patterns.",
        "✔ Ensure clear verbalization of your thought process before writing code.",
        "✔ Prepare 3 strategic questions to ask your interviewer about team engineering culture.",
        "✔ Verify audio, video, and environment setup 15 minutes prior to mock/live interview."
    ]
    for chk in checklist:
        story.append(Paragraph(chk, body_style))

    doc.build(story)
    return buffer.getvalue()
