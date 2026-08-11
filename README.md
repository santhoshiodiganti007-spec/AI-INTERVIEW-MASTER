# AI INTERVIEW MASTER

**AI INTERVIEW MASTER** is a production-quality, full-stack AI-powered interview preparation platform designed to help software engineers, data scientists, and GenAI specialists ace technical interviews at **Google, Meta, Amazon, Microsoft, and top MNCs**.

---

## Architecture Overview

```
                          AI INTERVIEW MASTER
                                   │
                      ┌────────────┴────────────┐
                      │                         │
                  FRONTEND                   BACKEND
                      │                         │
                React + Vite                 FastAPI
                Tailwind CSS                    │
                Charts                          │
                      │                   ┌──────┴──────┐
                      │                   │             │
                      │               PostgreSQL      AI Layer
                      │                               │
                      │                    ┌──────────┼─────────┐
                      │                    │          │         │
                      │                  LLM       RAG      Evaluation
                      │                    │          │         │
                      │                    └──────────┼─────────┘
                      │                               │
                      └───────────────────────────────┘
```

---

## Key Features

1. **3 Career Tracks**:
   - Software / Python Developer (GIL, Concurrency, OOP 14 pillars, Iterators, Generators, Decorators)
   - AIML / Data Science (Statistics, XGBoost, Bias-Variance, Deep Learning, ResNet, BatchNorm, Imbalance)
   - Generative AI / LLM (Transformers, Scaled Dot-Product Self-Attention, Hybrid Search RAG, QLoRA, Agents, MCP)
2. **Interactive AI Mock Interviewer**: Multi-turn adaptive conversational interview room with dynamic follow-up questions and turn-by-turn evaluations.
3. **AI Answer Evaluation Engine**: 0–10 sub-scoring (Technical Accuracy, Completeness, Depth, Clarity, Communication), missing key point detection, STAR behavioral analysis, model answer recommendations, and AI Preparation Score disclaimers.
4. **DSA Pattern Mastery Lab**: Categorized coding challenges with hints, brute-force vs. optimized Python solutions, and time/space complexity breakdowns.
5. **PDF Resume Analyzer**: Extracts skills, projects, and generates targeted technical interview questions based on actual resume project content.
6. **Adaptive Roadmap Generator**: 7, 14, 30, 60, and 90-day study roadmaps tailored to role, level, target companies, and available daily hours.
7. **Downloadable PDF Interview Workbook**: Compiles candidate profile, readiness score, roadmap, high-yield track questions, weakness diagnosis, and interview checklist into a printable PDF.
8. **RAG Knowledge Engine**: Grounded semantic vector search over curated Google/MNC interview material.
9. **Gamification**: XP points, daily streaks, levels, and badges.

---

## Technology Stack

- **Frontend**: React 18, Vite, Tailwind CSS v4, Framer Motion, Lucide Icons, Chart.js / react-chartjs-2.
- **Backend**: FastAPI, Python 3.12, SQLAlchemy, Pydantic v2, PyJWT, Passlib, PyPDF, ReportLab.
- **Database**: PostgreSQL (Production) / SQLite (Local Development).
- **Deployment**: Vercel ready (`vercel.json`), serverless ASGI entry (`backend/api/index.py`).

---

## Quick Start (Local Setup)

### 1. Backend Setup
```bash
cd backend
py -3.12 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open application at: `http://localhost:3000`

---

## Testing

Run backend Pytest integration and unit test suite:
```bash
cd backend
.\venv\Scripts\pytest tests/ -v
```

---

## Environment Variables

Copy `.env.example` to `.env`:
```env
SECRET_KEY=super-secret-jwt-key-2026
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_interview_master
OPENAI_API_KEY=optional_openai_key
GEMINI_API_KEY=optional_gemini_key
VITE_API_URL=http://localhost:8000/api/v1
```

---

## Deployment Instructions

### Vercel Deployment
1. Connect repository to Vercel.
2. Vercel automatically uses root `vercel.json` to build the Vite React frontend static assets and serverless FastAPI backend functions at `/api/*`.

### Git Commit & Push
```bash
git add .
git commit -m "feat: complete AI INTERVIEW MASTER full-stack platform"
git push origin main
```

---

## API Documentation

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new candidate |
| `POST` | `/api/v1/auth/login` | Authenticate user & get JWT |
| `GET` | `/api/v1/dashboard` | Fetch readiness scores & daily prep checklist |
| `GET` | `/api/v1/questions` | List structured conceptual questions |
| `POST` | `/api/v1/questions/{id}/attempt` | Submit question answer for AI evaluation |
| `GET` | `/api/v1/coding-problems` | List DSA pattern coding challenges |
| `POST` | `/api/v1/mock-interview/start` | Start interactive multi-turn AI mock interview |
| `POST` | `/api/v1/mock-interview/{id}/answer` | Submit turn answer & receive dynamic follow-up |
| `POST` | `/api/v1/resume/upload` | Upload PDF resume & extract project questions |
| `POST` | `/api/v1/roadmap/generate` | Generate custom 7-90 day study plan |
| `POST` | `/api/v1/pdf/generate` | Download printable interview preparation PDF workbook |
| `POST` | `/api/v1/rag/query` | Grounded semantic search over knowledge base |

---

## Future Improvements

1. Live WebRTC Voice-to-Voice AI Interviewer agent with low-latency streaming.
2. Code Execution Sandbox using Isolated Docker/Wasm containers for live DSA unit test execution.
3. Collaborative Peer-to-Peer Mock Interview rooms with real-time video and shared whiteboards.