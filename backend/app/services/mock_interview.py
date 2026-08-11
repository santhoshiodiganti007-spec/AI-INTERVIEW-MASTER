from typing import Dict, Any, List

INTERVIEW_QUESTION_POOL = {
    "Python Interview": [
        "Welcome to your Python Technical Interview! Let's start: Explain Python's GIL and how it impacts CPU-bound vs I/O-bound multithreaded applications.",
        "Good. Now, how do Python Generators differ from Iterators, and how does lazy evaluation optimize memory usage?",
        "Excellent. Can you write or describe a decorator in Python that caches function results (memoization) and handles function metadata?"
    ],
    "DSA Interview": [
        "Welcome to the Data Structures & Algorithms Interview! Let's begin: Given an array of integers, how would you find two numbers that sum up to a target value in O(N) time?",
        "Great! Now let's move to Sliding Window: How do you find the length of the longest substring without repeating characters?",
        "Nice approach! For Binary Trees: How do you check if a binary tree is height-balanced?"
    ],
    "AIML Interview": [
        "Welcome to the AIML / Data Science Interview! First question: Explain the Bias-Variance tradeoff and how XGBoost hyperparameters control overfitting.",
        "Strong answer. In Deep Learning, why do vanishing gradients happen and how do Residual Skip Connections solve them?",
        "How do precision, recall, F1-score, and ROC-AUC differ when dealing with highly imbalanced datasets?"
    ],
    "GenAI Interview": [
        "Welcome to the Generative AI / LLM Interview! Let's start: Explain Scaled Dot-Product Attention in Transformers and why division by sqrt(d_k) is required.",
        "Superb! How would you design an Enterprise RAG Pipeline handling millions of PDF documents with Hybrid Search and Reranking?",
        "What are the trade-offs between Fine-Tuning an LLM with QLoRA versus using In-Context Retrieval (RAG)?"
    ],
    "Full MNC Interview": [
        "Welcome to the Full MNC Comprehensive Interview! Let's start with System Design & LLMs: Design a production-grade AI Code Assistant service for 10 million daily active users.",
        "Impressive. Moving to Core Python & Concurrency: How does asyncio event loop work under the hood compared to OS threads?",
        "Behavioral (STAR): Tell me about a critical production issue or outage you experienced and how you resolved it under pressure."
    ]
}

def get_initial_question(interview_type: str) -> str:
    pool = INTERVIEW_QUESTION_POOL.get(interview_type, INTERVIEW_QUESTION_POOL["Full MNC Interview"])
    return pool[0]

def get_next_question(interview_type: str, current_turn: int, user_last_answer: str) -> str:
    pool = INTERVIEW_QUESTION_POOL.get(interview_type, INTERVIEW_QUESTION_POOL["Full MNC Interview"])
    if current_turn < len(pool):
        return pool[current_turn]
    
    # Adaptive follow-up generator if past pre-seeded count
    return f"Building on your previous points about '{user_last_answer[:40]}...', how would you handle high concurrency, failure recovery, and real-time monitoring for this system?"
