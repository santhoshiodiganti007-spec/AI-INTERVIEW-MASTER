from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Roadmap, RoadmapTask, User, Profile
from app.schemas.all_schemas import RoadmapGenerate, RoadmapOut
from app.services.auth_service import get_current_user
from app.services.roadmap_service import generate_personalized_roadmap
from app.services.gamification_service import add_user_xp

router = APIRouter(prefix="/roadmap", tags=["Personalized Roadmap"])

@router.get("", response_model=RoadmapOut)
def get_current_roadmap(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == current_user.id).order_by(Roadmap.created_at.desc()).first()
    if not roadmap:
        # Generate default 30-day roadmap based on user profile
        profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
        target_role = profile.target_role if profile else "Software / Python Developer"
        data = generate_personalized_roadmap(target_role=target_role, duration_days=30, available_hours=2.0)
        
        roadmap = Roadmap(
            user_id=current_user.id,
            duration_days=data["duration_days"],
            title=data["title"]
        )
        db.add(roadmap)
        db.commit()
        db.refresh(roadmap)

        for t in data["tasks"]:
            task_obj = RoadmapTask(
                roadmap_id=roadmap.id,
                day_number=t["day_number"],
                topic=t["topic"],
                learning_objective=t["learning_objective"],
                questions=t["questions"],
                coding_problems=t["coding_problems"],
                revision_task=t["revision_task"],
                mock_interview_task=t["mock_interview_task"],
                estimated_minutes=t["estimated_minutes"],
                completed=t["completed"]
            )
            db.add(task_obj)
        db.commit()
        db.refresh(roadmap)

    return roadmap

@router.post("/generate", response_model=RoadmapOut)
def generate_new_roadmap(
    req: RoadmapGenerate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    target_role = profile.target_role if profile else "Software / Python Developer"
    
    data = generate_personalized_roadmap(
        target_role=target_role,
        duration_days=req.duration_days,
        available_hours=req.available_hours or 2.0
    )

    roadmap = Roadmap(
        user_id=current_user.id,
        duration_days=data["duration_days"],
        title=data["title"]
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)

    for t in data["tasks"]:
        task_obj = RoadmapTask(
            roadmap_id=roadmap.id,
            day_number=t["day_number"],
            topic=t["topic"],
            learning_objective=t["learning_objective"],
            questions=t["questions"],
            coding_problems=t["coding_problems"],
            revision_task=t["revision_task"],
            mock_interview_task=t["mock_interview_task"],
            estimated_minutes=t["estimated_minutes"],
            completed=t["completed"]
        )
        db.add(task_obj)
    db.commit()
    db.refresh(roadmap)

    add_user_xp(db, current_user.id, 30)

    return roadmap

@router.post("/task/{task_id}/toggle")
def toggle_roadmap_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(RoadmapTask).join(Roadmap).filter(RoadmapTask.id == task_id, Roadmap.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Roadmap task not found.")

    task.completed = not task.completed
    db.commit()
    
    if task.completed:
        add_user_xp(db, current_user.id, 15)

    return {"task_id": task.id, "completed": task.completed}
