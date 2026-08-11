import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "AI INTERVIEW MASTER"
    assert data["status"] == "online"

def test_user_registration_and_login():
    email = "pytest_candidate@google.com"
    password = "securePassword123"
    
    # 1. Register
    reg_res = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test Candidate",
        "target_role": "Software / Python Developer"
    })
    assert reg_res.status_code in [200, 400] # 200 OK or 400 if already exists

    # 2. Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_res.status_code == 200
    token_data = login_res.json()
    assert "access_token" in token_data
    return token_data["access_token"]

def test_questions_endpoint():
    res = client.get("/api/v1/questions")
    assert res.status_code == 200
    questions = res.json()
    assert isinstance(questions, list)
    assert len(questions) > 0

def test_coding_problems_endpoint():
    res = client.get("/api/v1/coding-problems")
    assert res.status_code == 200
    problems = res.json()
    assert isinstance(problems, list)
    assert len(problems) > 0

def test_rag_query_endpoint():
    res = client.post("/api/v1/rag/query", json={
        "query": "Explain Scaled Dot-Product Attention in Transformers"
    })
    assert res.status_code == 200
    data = res.json()
    assert "grounded_answer" in data
    assert "retrieved_documents" in data
