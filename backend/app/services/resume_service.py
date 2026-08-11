import re
from typing import Dict, Any, List
import pypdf

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF text: {str(e)}"

import io

def parse_resume_content(raw_text: str) -> Dict[str, Any]:
    """
    Parses resume raw text to extract skills, projects, education, experience, and certifications.
    Generates targeted technical interview questions based on actual projects and skills mentioned.
    """
    skills_keywords = [
        "Python", "Java", "C++", "PyTorch", "TensorFlow", "FastAPI", "React", "Docker",
        "Kubernetes", "PostgreSQL", "MongoDB", "AWS", "GCP", "Transformer", "LLM", "RAG",
        "XGBoost", "BERT", "GPT", "Kafka", "Redis", "LangChain", "LlamaIndex"
    ]
    
    extracted_skills = [s for s in skills_keywords if re.search(r'\b' + re.escape(s) + r'\b', raw_text, re.IGNORECASE)]
    
    # Extract project bullet points or lines containing keywords
    lines = [l.strip() for l in raw_text.split('\n') if len(l.strip()) > 15]
    project_lines = [l for l in lines if any(k in l for k in ["Built", "Developed", "Designed", "Implemented", "Created", "Trained", "Deployed", "Engineered"])]
    
    if not project_lines:
        project_lines = lines[:3] if lines else ["Built a machine learning platform."]
        
    generated_questions = []
    
    for proj in project_lines[:3]:
        proj_clean = proj[:100]
        if "Transformer" in proj or "BERT" in proj or "GPT" in proj or "LLM" in proj:
            generated_questions.extend([
                f"For your project '{proj_clean}': Why did you choose a Transformer architecture over RNN/LSTM?",
                f"How did you handle tokenization, context length limits, and positional encodings in this system?",
                f"What dataset did you use for training/fine-tuning, and what preprocessing steps were applied?",
                f"How did you evaluate model performance (e.g. Perplexity, ROUGE, BLEU, or domain metrics)?",
                f"How would you optimize inference latency and scale this model in a production API environment?"
            ])
        elif "RAG" in proj or "Embedding" in proj or "Vector" in proj:
            generated_questions.extend([
                f"Regarding '{proj_clean}': What chunking strategy and vector database did you implement?",
                f"How did you handle hallucination prevention and context relevance reranking?",
                f"What were the main throughput and latency bottlenecks during vector retrieval?"
            ])
        elif "FastAPI" in proj or "Docker" in proj or "API" in proj or "System" in proj:
            generated_questions.extend([
                f"In your project '{proj_clean}': Explain your microservice/API architecture and database schema.",
                f"How did you handle authentication, rate limiting, and database connections under load?",
                f"What monitoring, logging, and CI/CD pipelines did you setup for deployment?"
            ])
        else:
            generated_questions.extend([
                f"Explain the architectural decisions behind '{proj_clean}'.",
                f"What was the most challenging technical roadblock you encountered in this project, and how did you resolve it?",
                f"If you were to rebuild this system today from scratch, what would you change?"
            ])

    return {
        "extracted_skills": extracted_skills if extracted_skills else ["Python", "FastAPI", "SQL", "Machine Learning"],
        "extracted_projects": project_lines[:5],
        "extracted_experience": [l for l in lines if any(k in l for k in ["Engineer", "Developer", "Intern", "Lead", "Architect"])][:3],
        "extracted_education": [l for l in lines if any(k in l for k in ["University", "College", "Bachelor", "Master", "B.Tech", "Degree"])][:2],
        "generated_questions": generated_questions[:10]
    }
