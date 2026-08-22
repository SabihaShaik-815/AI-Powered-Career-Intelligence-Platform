from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


# ============================================================
# TEST ROOT
# ============================================================

def test_root():

    response = client.get("/")

    assert response.status_code == 200


# ============================================================
# TEST HEALTH
# ============================================================

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


# ============================================================
# TEST METRICS
# ============================================================

def test_metrics():

    response = client.get("/metrics")

    assert response.status_code == 200


# ============================================================
# TEST PREDICTION VALIDATION
# ============================================================

def test_predict_validation():

    response = client.post(
        "/predict",
        json={
            "text": "short",
            "top_k": 5
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST PREDICTION
# ============================================================

def test_predict():

    resume_text = """
    Python developer with experience in machine learning,
    data analysis, SQL, pandas, NumPy and scikit-learn.
    """

    response = client.post(
        "/predict",
        json={
            "text": resume_text,
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data is not None


# ============================================================
# TEST RECOMMENDATION
# ============================================================

def test_recommend():

    resume_text = """
    Software engineer with Python, Java, SQL, Docker,
    REST API and Git experience.
    """

    response = client.post(
        "/recommend",
        json={
            "text": resume_text,
            "top_k": 5
        }
    )

    assert response.status_code == 200


# ============================================================
# TEST SKILL GAP
# ============================================================

def test_skill_gap():

    response = client.post(
        "/skill-gap",
        json={
            "role": "Data Scientist",
            "skills": [
                "Python",
                "SQL",
                "Machine Learning"
            ]
        }
    )

    assert response.status_code == 200


# ============================================================
# TEST REPORT
# ============================================================

def test_report():

    resume_text = """
    Data analyst with Python, SQL, Excel, statistics,
    Tableau and Power BI experience.
    """

    response = client.post(
        "/report",
        json={
            "text": resume_text,
            "top_k": 5
        }
    )

    assert response.status_code == 200