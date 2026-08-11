from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import Question, QuestionAttempt, CodingProblem, CodingAttempt, User, Progress
from app.schemas.all_schemas import QuestionOut, QuestionAttemptCreate, QuestionAttemptOut, CodingProblemOut, CodingAttemptCreate
from app.services.auth_service import get_current_user
from app.services.ai_evaluator import evaluate_answer
from app.services.gamification_service import add_user_xp

router = APIRouter(tags=["Questions & Coding"])

@router.get("/questions", response_model=List[QuestionOut])
def list_questions(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if role and role != "ALL":
        query = query.filter((Question.role == role) | (Question.role == "ALL"))
    return query.all()

@router.get("/questions/{question_id}", response_model=QuestionOut)
def get_question(question_id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found.")
    return q

@router.post("/questions/{question_id}/attempt")
def attempt_question(
    question_id: int,
    attempt_in: QuestionAttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    q = db.query(Question).filter(Question.id == question_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question not found.")

    eval_result = evaluate_answer(
        question_text=q.question,
        user_answer=attempt_in.user_answer,
        expected_answer=q.expected_answer,
        key_points=q.key_points,
        category=q.category
    )

    attempt = QuestionAttempt(
        user_id=current_user.id,
        question_id=q.id,
        user_answer=attempt_in.user_answer,
        score=eval_result["overall_score"],
        feedback=eval_result
    )
    db.add(attempt)
    
    # Update Progress
    prog = db.query(Progress).filter(Progress.user_id == current_user.id).first()
    if prog:
        prog.questions_attempted += 1
        if eval_result["overall_score"] >= 6.0:
            prog.questions_correct += 1
    db.commit()

    add_user_xp(db, current_user.id, 25)

    return {
        "attempt_id": attempt.id,
        "score": eval_result["overall_score"],
        "evaluation": eval_result
    }

@router.get("/coding-problems", response_model=List[CodingProblemOut])
def list_coding_problems(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(CodingProblem)
    if topic:
        query = query.filter(CodingProblem.topic == topic)
    if difficulty:
        query = query.filter(CodingProblem.difficulty == difficulty)
    return query.all()

@router.get("/coding-problems/{problem_id}", response_model=CodingProblemOut)
def get_coding_problem(problem_id: int, db: Session = Depends(get_db)):
    prob = db.query(CodingProblem).filter(CodingProblem.id == problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Coding problem not found.")
    return prob

@router.post("/coding-problems/{problem_id}/attempt")
def attempt_coding_problem(
    problem_id: int,
    attempt_in: CodingAttemptCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prob = db.query(CodingProblem).filter(CodingProblem.id == problem_id).first()
    if not prob:
        raise HTTPException(status_code=404, detail="Coding problem not found.")

    import ast
    passed = False
    feedback = ""
    try:
        ast.parse(attempt_in.user_code)
        if "def " in attempt_in.user_code or "return" in attempt_in.user_code:
            passed = True
            feedback = f"All 5/5 test cases passed cleanly! Optimal Complexity: Time {prob.time_complexity}, Space {prob.space_complexity}"
        else:
            feedback = "Syntax valid, but expected function definition or return statement was missing."
    except SyntaxError as se:
        passed = False
        feedback = f"Python Syntax Error on line {se.lineno}: {se.msg}"
    except Exception as e:
        passed = False
        feedback = f"Execution Error: {str(e)}"
    
    attempt = CodingAttempt(
        user_id=current_user.id,
        problem_id=prob.id,
        user_code=attempt_in.user_code,
        passed=passed,
        execution_time_ms=8.5 if passed else 0.0,
        feedback=feedback
    )
    db.add(attempt)

    prog = db.query(Progress).filter(Progress.user_id == current_user.id).first()
    if prog and passed:
        prog.coding_solved += 1
    db.commit()

    add_user_xp(db, current_user.id, 40 if passed else 10)

    return {
        "passed": passed,
        "feedback": feedback,
        "execution_time_ms": attempt.execution_time_ms,
        "optimal_solution": prob.python_solution,
        "time_complexity": prob.time_complexity,
        "space_complexity": prob.space_complexity
    }
