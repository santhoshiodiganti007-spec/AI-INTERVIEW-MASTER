from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.all_models import MockInterview, InterviewQuestion, InterviewAnswer, AnswerEvaluation, User, Progress
from app.schemas.all_schemas import MockInterviewStart, InterviewAnswerSubmit
from app.services.auth_service import get_current_user
from app.services.mock_interview import get_initial_question, get_next_question
from app.services.ai_evaluator import evaluate_answer
from app.services.gamification_service import add_user_xp

router = APIRouter(prefix="/mock-interview", tags=["AI Mock Interview"])

@router.post("/start")
def start_mock_interview(
    start_in: MockInterviewStart,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mock = MockInterview(
        user_id=current_user.id,
        interview_type=start_in.interview_type,
        target_role=start_in.target_role or "Software / Python Developer",
        status="IN_PROGRESS"
    )
    db.add(mock)
    db.commit()
    db.refresh(mock)

    q_text = get_initial_question(mock.interview_type)
    q_obj = InterviewQuestion(
        mock_interview_id=mock.id,
        question_text=q_text,
        category=mock.interview_type,
        sequence_order=1
    )
    db.add(q_obj)
    db.commit()
    db.refresh(q_obj)

    return {
        "mock_interview_id": mock.id,
        "interview_type": mock.interview_type,
        "status": mock.status,
        "question_id": q_obj.id,
        "question_number": 1,
        "question_text": q_obj.question_text
    }

@router.post("/{mock_id}/answer")
def submit_interview_answer(
    mock_id: int,
    ans_in: InterviewAnswerSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mock = db.query(MockInterview).filter(MockInterview.id == mock_id, MockInterview.user_id == current_user.id).first()
    if not mock:
        raise HTTPException(status_code=404, detail="Mock interview session not found.")

    latest_q = db.query(InterviewQuestion).filter(InterviewQuestion.mock_interview_id == mock.id).order_by(InterviewQuestion.sequence_order.desc()).first()
    if not latest_q:
        raise HTTPException(status_code=400, detail="No active question in session.")

    ans_obj = InterviewAnswer(
        question_id=latest_q.id,
        answer_text=ans_in.answer_text
    )
    db.add(ans_obj)
    db.commit()
    db.refresh(ans_obj)

    eval_result = evaluate_answer(
        question_text=latest_q.question_text,
        user_answer=ans_in.answer_text,
        category=latest_q.category
    )

    eval_obj = AnswerEvaluation(
        answer_id=ans_obj.id,
        technical_accuracy=eval_result["technical_accuracy"],
        completeness=eval_result["completeness"],
        depth=eval_result["depth"],
        clarity=eval_result["clarity"],
        communication=eval_result["communication"],
        overall_score=eval_result["overall_score"],
        what_was_good=eval_result["what_was_good"],
        what_was_missing=eval_result["what_was_missing"],
        incorrect_statements=eval_result["incorrect_statements"],
        better_answer=eval_result["better_answer"],
        key_concepts_to_revise=eval_result["key_concepts_to_revise"],
        recommended_follow_up=eval_result["recommended_follow_up"]
    )
    db.add(eval_obj)
    db.commit()

    current_count = db.query(InterviewQuestion).filter(InterviewQuestion.mock_interview_id == mock.id).count()
    
    if current_count >= 3:
        mock.status = "COMPLETED"
        # Calculate summary average
        all_evals = db.query(AnswerEvaluation).join(InterviewAnswer).join(InterviewQuestion).filter(InterviewQuestion.mock_interview_id == mock.id).all()
        avg_score = sum(e.overall_score for e in all_evals) / max(len(all_evals), 1)
        mock.overall_score = round(avg_score * 10, 1) # Scale to 0-100%
        mock.summary_evaluation = {
            "overall_performance": "Strong performance across technical and behavioral dimensions.",
            "average_score": round(avg_score, 1),
            "disclaimer": "AI Preparation Score is an internal diagnostic metric for interview preparation and does not represent an official company hiring decision."
        }
        db.commit()

        prog = db.query(Progress).filter(Progress.user_id == current_user.id).first()
        if prog:
            prog.mock_interviews_completed += 1
        db.commit()

        add_user_xp(db, current_user.id, 100)

        return {
            "status": "COMPLETED",
            "message": "Mock Interview completed!",
            "overall_score": mock.overall_score,
            "summary_evaluation": mock.summary_evaluation,
            "answer_evaluation": eval_result
        }
    else:
        next_q_text = get_next_question(mock.interview_type, current_count, ans_in.answer_text)
        next_q_obj = InterviewQuestion(
            mock_interview_id=mock.id,
            question_text=next_q_text,
            category=mock.interview_type,
            sequence_order=current_count + 1
        )
        db.add(next_q_obj)
        db.commit()
        db.refresh(next_q_obj)

        return {
            "status": "IN_PROGRESS",
            "question_id": next_q_obj.id,
            "question_number": current_count + 1,
            "question_text": next_q_obj.question_text,
            "previous_answer_evaluation": eval_result
        }

@router.get("/{mock_id}/evaluation")
def get_mock_interview_evaluation(
    mock_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mock = db.query(MockInterview).filter(MockInterview.id == mock_id, MockInterview.user_id == current_user.id).first()
    if not mock:
        raise HTTPException(status_code=404, detail="Mock interview session not found.")

    questions = db.query(InterviewQuestion).filter(InterviewQuestion.mock_interview_id == mock.id).order_by(InterviewQuestion.sequence_order).all()
    q_data = []
    for q in questions:
        ans = db.query(InterviewAnswer).filter(InterviewAnswer.question_id == q.id).first()
        eval_item = None
        if ans and ans.evaluation:
            e = ans.evaluation
            eval_item = {
                "technical_accuracy": e.technical_accuracy,
                "completeness": e.completeness,
                "depth": e.depth,
                "clarity": e.clarity,
                "communication": e.communication,
                "overall_score": e.overall_score,
                "what_was_good": e.what_was_good,
                "what_was_missing": e.what_was_missing,
                "better_answer": e.better_answer
            }
        q_data.append({
            "question": q.question_text,
            "user_answer": ans.answer_text if ans else None,
            "evaluation": eval_item
        })

    return {
        "mock_interview_id": mock.id,
        "interview_type": mock.interview_type,
        "status": mock.status,
        "overall_score": mock.overall_score,
        "summary_evaluation": mock.summary_evaluation,
        "questions_breakdown": q_data
    }
