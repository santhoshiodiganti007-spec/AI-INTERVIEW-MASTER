from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    target_role: Optional[str] = "Software / Python Developer"
    experience_level: Optional[str] = "INTERMEDIATE"
    target_companies: Optional[List[str]] = ["Google", "Meta"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    full_name: str
    email: str

class ProfileUpdate(BaseModel):
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    target_companies: Optional[List[str]] = None
    available_hours_per_day: Optional[float] = None
    target_date: Optional[str] = None

class ProfileOut(BaseModel):
    id: int
    user_id: int
    target_role: str
    experience_level: str
    target_companies: List[str]
    available_hours_per_day: float
    target_date: Optional[str] = None

    class Config:
        from_attributes = True

# --- Question Schemas ---
class QuestionOut(BaseModel):
    id: int
    question: str
    category: str
    topic: str
    difficulty: str
    role: str
    expected_answer: str
    key_points: List[str]
    common_mistakes: List[str]
    follow_up_questions: List[str]
    estimated_time_minutes: int
    tags: List[str]

    class Config:
        from_attributes = True

class QuestionAttemptCreate(BaseModel):
    user_answer: str

class QuestionAttemptOut(BaseModel):
    id: int
    question_id: int
    user_answer: str
    score: float
    feedback: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Coding Schemas ---
class CodingProblemOut(BaseModel):
    id: int
    title: str
    topic: str
    difficulty: str
    problem_statement: str
    examples: List[Dict[str, Any]]
    constraints: List[str]
    hint: Optional[str] = None
    brute_force_approach: Optional[str] = None
    optimized_approach: str
    python_solution: str
    time_complexity: str
    space_complexity: str
    explanation: str
    follow_up_questions: List[str]

    class Config:
        from_attributes = True

class CodingAttemptCreate(BaseModel):
    user_code: str

# --- Mock Interview Schemas ---
class MockInterviewStart(BaseModel):
    interview_type: str = "Full MNC Interview"
    target_role: Optional[str] = "Software / Python Developer"

class InterviewAnswerSubmit(BaseModel):
    answer_text: str

class EvaluationOut(BaseModel):
    technical_accuracy: float
    completeness: float
    depth: float
    clarity: float
    communication: float
    overall_score: float
    what_was_good: List[str]
    what_was_missing: List[str]
    incorrect_statements: List[str]
    better_answer: Optional[str] = None
    key_concepts_to_revise: List[str]
    recommended_follow_up: Optional[str] = None

# --- Roadmap Schemas ---
class RoadmapGenerate(BaseModel):
    duration_days: int = 30
    target_date: Optional[str] = None
    available_hours: Optional[float] = 2.0

class RoadmapTaskOut(BaseModel):
    id: int
    day_number: int
    topic: str
    learning_objective: str
    questions: List[str]
    coding_problems: List[str]
    revision_task: Optional[str] = None
    mock_interview_task: Optional[str] = None
    estimated_minutes: int
    completed: bool

    class Config:
        from_attributes = True

class RoadmapOut(BaseModel):
    id: int
    duration_days: int
    title: str
    tasks: List[RoadmapTaskOut]

    class Config:
        from_attributes = True

# --- Assessment Schemas ---
class AssessmentSubmit(BaseModel):
    answers: Dict[int, str] # question_id -> user_answer

# --- Analytics / Dashboard Out ---
class DashboardOut(BaseModel):
    readiness_score: float
    readiness_label: str # Foundation Required, Developing, Interview Practice Needed, Strong Preparation, Excellent Preparation
    disclaimer: str
    category_scores: Dict[str, float]
    todays_preparation: List[Dict[str, Any]]
    progress_stats: Dict[str, Any]
    streak: int
    xp: int
    level: int
    badges: List[Dict[str, Any]]
