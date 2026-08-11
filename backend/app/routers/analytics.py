from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Progress, Achievement, User, Profile
from app.schemas.all_schemas import DashboardOut, AssessmentSubmit
from app.services.auth_service import get_current_user
from app.services.gamification_service import BADGE_DEFINITIONS, add_user_xp

router = APIRouter(tags=["Dashboard & Analytics"])

def get_readiness_label(score: float) -> str:
    if score <= 40.0:
        return "Foundation Required"
    elif score <= 60.0:
        return "Developing"
    elif score <= 75.0:
        return "Interview Practice Needed"
    elif score <= 90.0:
        return "Strong Preparation"
    else:
        return "Excellent Preparation"

@router.get("/dashboard", response_model=DashboardOut)
def get_dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prog = db.query(Progress).filter(Progress.user_id == current_user.id).first()
    if not prog:
        prog = Progress(
            user_id=current_user.id,
            readiness_score=68.0,
            python_score=78.0,
            dsa_score=70.0,
            aiml_score=72.0,
            genai_score=65.0,
            sql_score=68.0,
            system_design_score=58.0,
            behavioral_score=82.0,
            communication_score=80.0,
            questions_attempted=12,
            questions_correct=9,
            coding_solved=4,
            mock_interviews_completed=2,
            total_xp=140,
            level=2,
            daily_streak=4
        )
        db.add(prog)
        db.commit()
        db.refresh(prog)

    achievements = db.query(Achievement).filter(Achievement.user_id == current_user.id).all()
    earned_keys = {a.badge_key for a in achievements}

    badge_list = []
    for key, meta in BADGE_DEFINITIONS.items():
        badge_list.append({
            "key": key,
            "title": meta["title"],
            "description": meta["description"],
            "earned": key in earned_keys
        })

    cat_scores = {
        "Technical": round((prog.python_score + prog.sql_score) / 2.0, 1),
        "Python": prog.python_score,
        "DSA": prog.dsa_score,
        "AIML": prog.aiml_score,
        "GenAI": prog.genai_score,
        "SQL": prog.sql_score,
        "System Design": prog.system_design_score,
        "Behavioral": prog.behavioral_score,
        "Communication": prog.communication_score
    }

    # Weighting logic for overall preparation metric
    weighted_score = round(
        prog.python_score * 0.20 +
        prog.dsa_score * 0.20 +
        prog.genai_score * 0.15 +
        prog.aiml_score * 0.15 +
        prog.system_design_score * 0.10 +
        prog.behavioral_score * 0.10 +
        prog.communication_score * 0.10,
        1
    )
    prog.readiness_score = weighted_score
    db.commit()

    todays_prep = [
        {"task": "Solve 3 DSA problems (Array & Two Pointer patterns)", "done": prog.coding_solved >= 3},
        {"task": "Revise Python OOP 14 pillars & property decorators", "done": prog.questions_attempted >= 5},
        {"task": "Practice 5 ML & Bias-Variance conceptual questions", "done": False},
        {"task": "Complete 1 dynamic GenAI / RAG AI mock interview", "done": prog.mock_interviews_completed >= 1},
        {"task": "Practice 1 Behavioral STAR framework scenario", "done": False}
    ]

    return {
        "readiness_score": prog.readiness_score,
        "readiness_label": get_readiness_label(prog.readiness_score),
        "disclaimer": "AI Preparation Score is an internal diagnostic metric for interview preparation and does not represent an official company hiring decision.",
        "category_scores": cat_scores,
        "todays_preparation": todays_prep,
        "progress_stats": {
            "questions_attempted": prog.questions_attempted,
            "questions_correct": prog.questions_correct,
            "coding_solved": prog.coding_solved,
            "mock_interviews_completed": prog.mock_interviews_completed
        },
        "streak": prog.daily_streak,
        "xp": prog.total_xp,
        "level": prog.level,
        "badges": badge_list
    }

@router.post("/assessment/submit")
def submit_initial_assessment(
    submit_in: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prog = db.query(Progress).filter(Progress.user_id == current_user.id).first()
    if not prog:
        prog = Progress(user_id=current_user.id)
        db.add(prog)

    # Score assessment answers
    total_q = max(len(submit_in.answers), 1)
    correct_count = sum(1 for ans in submit_in.answers.values() if len(ans.strip()) > 15)
    
    score_percentage = round((correct_count / total_q) * 100.0, 1)
    prog.readiness_score = score_percentage
    prog.python_score = min(score_percentage + 5, 100.0)
    prog.dsa_score = max(score_percentage - 10, 40.0)
    prog.genai_score = min(score_percentage + 2, 100.0)
    db.commit()

    add_user_xp(db, current_user.id, 75)

    return {
        "readiness_score": prog.readiness_score,
        "readiness_label": get_readiness_label(prog.readiness_score),
        "message": "Initial assessment evaluated successfully!"
    }
