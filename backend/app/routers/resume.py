from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Resume, User
from app.services.auth_service import get_current_user
from app.services.resume_service import extract_text_from_pdf_bytes, parse_resume_content
from app.services.gamification_service import add_user_xp

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    pdf_bytes = await file.read()
    raw_text = extract_text_from_pdf_bytes(pdf_bytes)
    parsed = parse_resume_content(raw_text)

    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        raw_text=raw_text,
        parsed_skills=parsed["extracted_skills"],
        parsed_projects=parsed["extracted_projects"],
        parsed_experience=parsed["extracted_experience"],
        parsed_education=parsed["extracted_education"],
        generated_questions=parsed["generated_questions"]
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    add_user_xp(db, current_user.id, 50)

    return {
        "resume_id": resume.id,
        "filename": resume.filename,
        "parsed_skills": resume.parsed_skills,
        "parsed_projects": resume.parsed_projects,
        "generated_questions": resume.generated_questions
    }

@router.get("/questions")
def get_resume_questions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    latest_resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).first()
    if not latest_resume:
        return {
            "has_resume": False,
            "generated_questions": [
                "Built a Transformer-based behavioral authentication system: Why did you choose Transformer over LSTM?",
                "What pre-processing steps and dataset were used?",
                "How would you optimize latency and scale this architecture in production?"
            ]
        }

    return {
        "has_resume": True,
        "filename": latest_resume.filename,
        "parsed_skills": latest_resume.parsed_skills,
        "generated_questions": latest_resume.generated_questions
    }
