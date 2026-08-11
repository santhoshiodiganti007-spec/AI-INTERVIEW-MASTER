import re
import random
from typing import Dict, Any, List

def evaluate_answer(
    question_text: str,
    user_answer: str,
    expected_answer: str = "",
    key_points: List[str] = None,
    category: str = "General"
) -> Dict[str, Any]:
    """
    Evaluates candidate's answer against expected criteria.
    Outputs scores (0-10) for: Technical Accuracy, Completeness, Depth, Clarity, Communication.
    Generates structured feedback breakdown.
    """
    if key_points is None:
        key_points = []

    answer_len = len(user_answer.strip().split())
    
    # Simple heuristic scoring based on key point overlap and response depth
    matched_points = []
    missing_points = []
    
    for kp in key_points:
        words = [w.lower() for w in re.findall(r'\w+', kp) if len(w) > 3]
        if any(w in user_answer.lower() for w in words):
            matched_points.append(kp)
        else:
            missing_points.append(kp)
            
    match_ratio = len(matched_points) / max(len(key_points), 1) if key_points else 0.7
    
    # Calculate sub-scores (0-10)
    if answer_len < 10:
        tech_score = round(min(match_ratio * 5.0, 4.0), 1)
        comp_score = round(min(match_ratio * 4.0, 3.5), 1)
        depth_score = 2.0
        clarity_score = 5.0
        comm_score = 4.0
    else:
        tech_score = round(min(6.0 + match_ratio * 3.8, 9.8), 1)
        comp_score = round(min(5.5 + match_ratio * 4.0, 9.5), 1)
        depth_score = round(min(5.0 + (answer_len / 50.0) * 1.5 + match_ratio * 2.5, 9.6), 1)
        clarity_score = round(min(7.0 + random.uniform(0.5, 2.0), 9.7), 1)
        comm_score = round(min(7.2 + random.uniform(0.5, 2.0), 9.6), 1)

    overall_score = round((tech_score * 0.35 + comp_score * 0.25 + depth_score * 0.20 + clarity_score * 0.10 + comm_score * 0.10), 1)

    what_was_good = []
    if matched_points:
        what_was_good.append(f"Correctly addressed core concept(s): {', '.join(matched_points[:2])}")
    if answer_len > 30:
        what_was_good.append("Provided a structured explanation with good technical context.")
    else:
        what_was_good.append("Responded promptly to the core question prompt.")

    incorrect_statements = []
    if answer_len < 15:
        incorrect_statements.append("Answer is too brief to demonstrate full technical mastery.")

    better_answer = expected_answer if expected_answer else "A thorough response should clearly state the definition, real-world trade-offs, internal mechanism, and time/space complexity implications."

    key_concepts_to_revise = missing_points if missing_points else ["Deep dive architecture", "Performance optimization trade-offs"]
    recommended_follow_up = f"How would you optimize or scale your approach in a production environment with millions of requests?"

    return {
        "technical_accuracy": tech_score,
        "completeness": comp_score,
        "depth": depth_score,
        "clarity": clarity_score,
        "communication": comm_score,
        "overall_score": overall_score,
        "what_was_good": what_was_good,
        "what_was_missing": missing_points if missing_points else ["Consider including more edge case analysis."],
        "incorrect_statements": incorrect_statements,
        "better_answer": better_answer,
        "key_concepts_to_revise": key_concepts_to_revise,
        "recommended_follow_up": recommended_follow_up,
        "disclaimer": "AI Preparation Score is an internal diagnostic metric for interview preparation and does not represent an official company hiring decision."
    }
