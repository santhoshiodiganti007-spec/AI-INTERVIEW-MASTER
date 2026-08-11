from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import User, Profile, Progress
from app.schemas.all_schemas import UserRegister, UserLogin, Token, ProfileOut, ProfileUpdate
from app.services.auth_service import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered.")

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize Profile
    profile = Profile(
        user_id=user.id,
        target_role=user_in.target_role or "Software / Python Developer",
        experience_level=user_in.experience_level or "INTERMEDIATE",
        target_companies=user_in.target_companies or ["Google", "Meta"]
    )
    db.add(profile)

    # Initialize Progress & Scores
    progress = Progress(
        user_id=user.id,
        readiness_score=62.5,
        python_score=75.0,
        dsa_score=68.0,
        aiml_score=70.0,
        genai_score=60.0,
        sql_score=65.0,
        system_design_score=55.0,
        behavioral_score=80.0,
        communication_score=78.0,
        total_xp=50,
        level=1,
        daily_streak=1
    )
    db.add(progress)
    db.commit()

    token = create_access_token(data={"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": user.full_name,
        "email": user.email
    }

@router.post("/login", response_model=Token)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    token = create_access_token(data={"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "full_name": user.full_name,
        "email": user.email
    }

@router.get("/me/profile", response_model=ProfileOut)
def get_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("/me/profile", response_model=ProfileOut)
def update_user_profile(profile_in: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.add(profile)

    if profile_in.target_role is not None:
        profile.target_role = profile_in.target_role
    if profile_in.experience_level is not None:
        profile.experience_level = profile_in.experience_level
    if profile_in.target_companies is not None:
        profile.target_companies = profile_in.target_companies
    if profile_in.available_hours_per_day is not None:
        profile.available_hours_per_day = profile_in.available_hours_per_day
    if profile_in.target_date is not None:
        profile.target_date = profile_in.target_date

    db.commit()
    db.refresh(profile)
    return profile
