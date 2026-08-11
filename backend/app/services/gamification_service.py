from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.all_models import Progress, Achievement

BADGE_DEFINITIONS = {
    "python_master": {"title": "Python Master", "description": "Attempted 10+ Python conceptual questions"},
    "dsa_warrior": {"title": "DSA Warrior", "description": "Solved 5+ Data Structure & Algorithm coding challenges"},
    "ml_explorer": {"title": "ML Explorer", "description": "Completed machine learning diagnostic assessment"},
    "genai_engineer": {"title": "GenAI Engineer", "description": "Demonstrated expertise in LLMs and RAG system design"},
    "mock_champion": {"title": "Mock Interview Champion", "description": "Completed a full MNC AI interactive mock interview"},
    "streak_7": {"title": "7-Day Streak", "description": "Maintained a continuous 7-day preparation streak"},
    "hundred_club": {"title": "100 XP Club", "description": "Earned over 100 XP points"}
}

def add_user_xp(db: Session, user_id: int, xp_amount: int) -> Progress:
    prog = db.query(Progress).filter(Progress.user_id == user_id).first()
    if not prog:
        prog = Progress(user_id=user_id, total_xp=0, level=1, daily_streak=1)
        db.add(prog)
        db.commit()
        db.refresh(prog)

    prog.total_xp += xp_amount
    # Level formula: Level N = 1 + floor(XP / 100)
    prog.level = 1 + (prog.total_xp // 100)
    db.commit()
    db.refresh(prog)

    check_and_grant_badges(db, user_id, prog)
    return prog

def check_and_grant_badges(db: Session, user_id: int, prog: Progress):
    existing_badges = {a.badge_key for a in db.query(Achievement).filter(Achievement.user_id == user_id).all()}

    badges_to_award = []
    if prog.total_xp >= 100 and "hundred_club" not in existing_badges:
        badges_to_award.append("hundred_club")
    if prog.questions_attempted >= 5 and "python_master" not in existing_badges:
        badges_to_award.append("python_master")
    if prog.coding_solved >= 3 and "dsa_warrior" not in existing_badges:
        badges_to_award.append("dsa_warrior")
    if prog.mock_interviews_completed >= 1 and "mock_champion" not in existing_badges:
        badges_to_award.append("mock_champion")

    for key in badges_to_award:
        meta = BADGE_DEFINITIONS[key]
        ach = Achievement(
            user_id=user_id,
            badge_key=key,
            title=meta["title"],
            description=meta["description"]
        )
        db.add(ach)
    db.commit()
