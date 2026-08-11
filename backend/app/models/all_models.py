import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False)
    resumes = relationship("Resume", back_populates="user")
    question_attempts = relationship("QuestionAttempt", back_populates="user")
    coding_attempts = relationship("CodingAttempt", back_populates="user")
    mock_interviews = relationship("MockInterview", back_populates="user")
    roadmaps = relationship("Roadmap", back_populates="user")
    progress = relationship("Progress", back_populates="user", uselist=False)
    achievements = relationship("Achievement", back_populates="user")
    study_sessions = relationship("StudySession", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    target_role = Column(String, default="Software / Python Developer") # "Software / Python Developer", "AIML / Data Science", "Generative AI / LLM"
    experience_level = Column(String, default="INTERMEDIATE") # BEGINNER, INTERMEDIATE, ADVANCED
    target_companies = Column(JSON, default=list) # ["Google", "Meta", "Amazon"]
    available_hours_per_day = Column(Float, default=2.0)
    target_date = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    raw_text = Column(Text, nullable=True)
    parsed_skills = Column(JSON, default=list)
    parsed_projects = Column(JSON, default=list)
    parsed_experience = Column(JSON, default=list)
    parsed_education = Column(JSON, default=list)
    generated_questions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    category = Column(String, index=True) # Python, OOP, DSA, SQL, ML, DL, GenAI, RAG, System Design, Behavioral, etc.
    topic = Column(String, index=True)
    difficulty = Column(String, default="INTERMEDIATE") # BEGINNER, INTERMEDIATE, ADVANCED
    role = Column(String, default="ALL")
    expected_answer = Column(Text, nullable=False)
    key_points = Column(JSON, default=list)
    common_mistakes = Column(JSON, default=list)
    follow_up_questions = Column(JSON, default=list)
    estimated_time_minutes = Column(Integer, default=10)
    tags = Column(JSON, default=list)

    attempts = relationship("QuestionAttempt", back_populates="question_obj")


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(Text, nullable=False)
    score = Column(Float, default=0.0)
    feedback = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="question_attempts")
    question_obj = relationship("Question", back_populates="attempts")


class CodingProblem(Base):
    __tablename__ = "coding_problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    topic = Column(String, index=True) # Arrays, Strings, Trees, Dynamic Programming, etc.
    difficulty = Column(String, default="INTERMEDIATE")
    problem_statement = Column(Text, nullable=False)
    examples = Column(JSON, default=list)
    constraints = Column(JSON, default=list)
    hint = Column(Text, nullable=True)
    brute_force_approach = Column(Text, nullable=True)
    optimized_approach = Column(Text, nullable=False)
    python_solution = Column(Text, nullable=False)
    time_complexity = Column(String, nullable=False)
    space_complexity = Column(String, nullable=False)
    explanation = Column(Text, nullable=False)
    follow_up_questions = Column(JSON, default=list)

    attempts = relationship("CodingAttempt", back_populates="problem")


class CodingAttempt(Base):
    __tablename__ = "coding_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("coding_problems.id"))
    user_code = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)
    execution_time_ms = Column(Float, default=0.0)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="coding_attempts")
    problem = relationship("CodingProblem", back_populates="attempts")


class MockInterview(Base):
    __tablename__ = "mock_interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    interview_type = Column(String, default="Full MNC Interview") # Python, DSA, AIML, GenAI, System Design, Behavioral, Resume, Full MNC
    target_role = Column(String, default="Software / Python Developer")
    status = Column(String, default="IN_PROGRESS") # IN_PROGRESS, COMPLETED
    overall_score = Column(Float, default=0.0)
    summary_evaluation = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="mock_interviews")
    questions = relationship("InterviewQuestion", back_populates="mock_interview")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    mock_interview_id = Column(Integer, ForeignKey("mock_interviews.id"))
    question_text = Column(Text, nullable=False)
    category = Column(String, default="General")
    difficulty = Column(String, default="INTERMEDIATE")
    sequence_order = Column(Integer, default=1)

    mock_interview = relationship("MockInterview", back_populates="questions")
    answers = relationship("InterviewAnswer", back_populates="question_obj")


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("interview_questions.id"))
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    question_obj = relationship("InterviewQuestion", back_populates="answers")
    evaluation = relationship("AnswerEvaluation", back_populates="answer_obj", uselist=False)


class AnswerEvaluation(Base):
    __tablename__ = "answer_evaluations"

    id = Column(Integer, primary_key=True, index=True)
    answer_id = Column(Integer, ForeignKey("interview_answers.id"), unique=True)
    technical_accuracy = Column(Float, default=0.0)
    completeness = Column(Float, default=0.0)
    depth = Column(Float, default=0.0)
    clarity = Column(Float, default=0.0)
    communication = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    what_was_good = Column(JSON, default=list)
    what_was_missing = Column(JSON, default=list)
    incorrect_statements = Column(JSON, default=list)
    better_answer = Column(Text, nullable=True)
    key_concepts_to_revise = Column(JSON, default=list)
    recommended_follow_up = Column(Text, nullable=True)

    answer_obj = relationship("InterviewAnswer", back_populates="evaluation")


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    duration_days = Column(Integer, default=30)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    tasks = relationship("RoadmapTask", back_populates="roadmap_obj")


class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"))
    day_number = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    learning_objective = Column(Text, nullable=False)
    questions = Column(JSON, default=list)
    coding_problems = Column(JSON, default=list)
    revision_task = Column(Text, nullable=True)
    mock_interview_task = Column(Text, nullable=True)
    estimated_minutes = Column(Integer, default=120)
    completed = Column(Boolean, default=False)

    roadmap_obj = relationship("Roadmap", back_populates="tasks")


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    readiness_score = Column(Float, default=0.0)
    python_score = Column(Float, default=0.0)
    dsa_score = Column(Float, default=0.0)
    aiml_score = Column(Float, default=0.0)
    genai_score = Column(Float, default=0.0)
    sql_score = Column(Float, default=0.0)
    system_design_score = Column(Float, default=0.0)
    behavioral_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    questions_attempted = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)
    coding_solved = Column(Integer, default=0)
    mock_interviews_completed = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    daily_streak = Column(Integer, default=0)
    last_activity_date = Column(String, nullable=True)

    user = relationship("User", back_populates="progress")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    badge_key = Column(String, nullable=False) # e.g. "python_master", "dsa_warrior"
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    earned_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="achievements")


class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    minutes_spent = Column(Integer, default=0)
    date_str = Column(String, nullable=False)

    user = relationship("User", back_populates="study_sessions")
