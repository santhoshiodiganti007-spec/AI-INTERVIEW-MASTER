from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import User, Profile, Progress, Question, RoadmapTask
from app.services.auth_service import get_current_user
from app.services.pdf_service import generate_interview_workbook_pdf

router = APIRouter(prefix="/pdf", tags=["PDF Generation"])

@router.post("/generate")
def generate_pdf_workbook(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    prog = db.query(Progress).filter(Progress.user_id == current_user.id).first()
    questions = db.query(Question).limit(10).all()
    tasks = db.query(RoadmapTask).limit(7).all()

    cat_scores = {
        "Python": prog.python_score if prog else 80.0,
        "DSA": prog.dsa_score if prog else 70.0,
        "AIML": prog.aiml_score if prog else 72.0,
        "GenAI": prog.genai_score if prog else 65.0,
        "System Design": prog.system_design_score if prog else 58.0,
        "Behavioral": prog.behavioral_score if prog else 82.0
    }

    q_data = [{"q": q.question, "cat": q.category, "diff": q.difficulty} for q in questions]
    t_data = [{"day": t.day_number, "topic": t.topic, "time": f"{t.estimated_minutes} mins"} for t in tasks]

    candidate_payload = {
        "full_name": current_user.full_name,
        "target_role": profile.target_role if profile else "Software / Python Developer",
        "experience_level": profile.experience_level if profile else "INTERMEDIATE",
        "target_companies": profile.target_companies if profile else ["Google", "Meta"],
        "readiness_score": prog.readiness_score if prog else 76.5,
        "readiness_label": "Strong Preparation" if (prog and prog.readiness_score >= 75) else "Developing",
        "category_scores": cat_scores,
        "roadmap_tasks": t_data,
        "questions": q_data
    }

    pdf_bytes = generate_interview_workbook_pdf(candidate_payload)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AI_Interview_Master_Workbook_{current_user.id}.pdf"
        }
    )
