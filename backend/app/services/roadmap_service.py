from typing import List, Dict, Any

CURRICULUM_TRACKS = {
    "Software / Python Developer": [
        {"topic": "Python Core & Data Structures", "obj": "Master Python memory management, GIL, iterators, and generators.", "q": ["Explain Python GIL", "Iterators vs Generators"], "p": ["Two Sum (Hash Table Pattern)"]},
        {"topic": "Advanced OOP & Design Patterns", "obj": "Master 14 OOP pillars, magic methods, decorators, and composition.", "q": ["Method Overriding vs Overloading", "Encapsulation & Property Decorators"], "p": []},
        {"topic": "DSA - Arrays & Two Pointers", "obj": "Solve array manipulation and multi-pointer pattern problems.", "q": ["Time & Space Complexity analysis"], "p": ["Longest Substring Without Repeating Characters"]},
        {"topic": "DSA - Trees & Graphs", "obj": "Understand BFS, DFS, Tree Traversal, and Graph shortest path algorithms.", "q": ["Recursion vs Iteration in Trees"], "p": ["Invert Binary Tree"]},
        {"topic": "SQL & System Design Fundamentals", "obj": "Design relational schemas, indexing, and scalable web API architecture.", "q": ["ACID properties & Database Indexing"], "p": []},
        {"topic": "Behavioral STAR & Mock Interview", "obj": "Practice STAR framework responses and conduct a full mock interview.", "q": ["Tell me about a technical conflict"], "p": []}
    ],
    "AIML / Data Science": [
        {"topic": "Statistical Foundations & Regression", "obj": "Master probability distributions, linear/logistic regression, and loss functions.", "q": ["Bias-Variance Tradeoff"], "p": []},
        {"topic": "Tree-based Models & Ensemble Learning", "obj": "Master Decision Trees, Random Forest, and XGBoost hyperparameter tuning.", "q": ["XGBoost Overfitting & Regularization"], "p": []},
        {"topic": "Deep Learning & Neural Architectures", "obj": "Master ANN, CNN, ResNet skip connections, and Batch Normalization.", "q": ["Vanishing Gradient & ResNet"], "p": ["Invert Binary Tree"]},
        {"topic": "Feature Engineering & Cross Validation", "obj": "Implement robust preprocessing, target encoding, and K-Fold CV.", "q": ["Handling Class Imbalance & ROC-AUC"], "p": []},
        {"topic": "AIML System Design & Deployment", "obj": "Design scalable ML inference pipelines with feature stores.", "q": ["Model Drift & Monitoring"], "p": []},
        {"topic": "Full AIML Mock Interview & Portfolio", "obj": "Review resume projects and complete interactive AIML mock session.", "q": ["Explain your resume ML project architecture"], "p": []}
    ],
    "Generative AI / LLM": [
        {"topic": "Transformer Architecture & Self-Attention", "obj": "Master Scaled Dot-Product Attention, Multi-Head Attention, and RoPE.", "q": ["Self-Attention Q,K,V matrices"], "p": []},
        {"topic": "Enterprise RAG Systems", "obj": "Design RAG pipelines with Hybrid Search, BM25, HNSW, and Cross-Encoder Reranking.", "q": ["Design Production RAG System"], "p": ["Longest Substring Without Repeating Characters"]},
        {"topic": "LLM Fine-Tuning & Quantization", "obj": "Understand LoRA, QLoRA, NF4 quantization, and DPO alignment.", "q": ["Fine-Tuning vs RAG"], "p": []},
        {"topic": "AI Agents & Tool Calling", "obj": "Build autonomous agents using function calling, MCP, and guardrails.", "q": ["Agent Tool Calling & Loop Prevention"], "p": []},
        {"topic": "GenAI System Design & Latency Optimization", "obj": "Optimize LLM inference with FlashAttention, KV Caching, and vLLM.", "q": ["Production LLM Serving & KV Cache"], "p": []},
        {"topic": "GenAI Mock Interview & Defense", "obj": "Practice deep-dive GenAI questions and complete end-to-end evaluation.", "q": ["LLM Hallucination Prevention"], "p": []}
    ]
}

def generate_personalized_roadmap(
    target_role: str = "Software / Python Developer",
    duration_days: int = 30,
    available_hours: float = 2.0
) -> Dict[str, Any]:
    track = CURRICULUM_TRACKS.get(target_role, CURRICULUM_TRACKS["Software / Python Developer"])
    tasks = []
    
    for day in range(1, duration_days + 1):
        module = track[(day - 1) % len(track)]
        task = {
            "day_number": day,
            "topic": f"Day {day}: {module['topic']}",
            "learning_objective": module["obj"],
            "questions": module["q"],
            "coding_problems": module["p"],
            "revision_task": f"Revise key terms and flashcards for {module['topic']}",
            "mock_interview_task": "Complete 15-minute quick mock drill" if day % 5 == 0 else None,
            "estimated_minutes": int(available_hours * 60),
            "completed": False
        }
        tasks.append(task)

    return {
        "duration_days": duration_days,
        "title": f"Custom {duration_days}-Day Preparation Roadmap for {target_role}",
        "tasks": tasks
    }
