import io
import json
import re
import sqlite3
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import joblib
import spacy
from spacy.matcher import PhraseMatcher

BASE_DIR = Path(__file__).parent
MODELS_DIR = BASE_DIR / "models"
DB_PATH = BASE_DIR / "careercast.db"

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key-before-deploying"  # TODO: set a real secret

# ---------------------------------------------------------------------------
# Skills gazetteer / education patterns / role-skill profiles
# (same logic as the Streamlit version, ported here for the API)
# ---------------------------------------------------------------------------
SKILLS_GAZETTEER = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "SQL", "R",
    "Go", "Rust", "Scala", "PHP", "Ruby", "Swift", "Kotlin", "MATLAB",
    "Machine Learning", "Deep Learning", "Data Analysis", "Data Science",
    "Natural Language Processing", "Computer Vision", "TensorFlow", "PyTorch",
    "scikit-learn", "Pandas", "NumPy", "Data Visualization", "Statistics",
    "A/B Testing", "Tableau", "Power BI", "Excel",
    "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI",
    "REST API", "GraphQL", "HTML", "CSS", "Docker", "Kubernetes", "AWS",
    "Azure", "Google Cloud Platform", "CI/CD", "Git", "Microservices",
    "Agile", "Scrum",
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Snowflake", "BigQuery",
    "Spark", "Hadoop",
    "Project Management", "Product Management", "Leadership",
    "Communication", "Stakeholder Management", "Business Analysis",
    "Strategic Planning", "Negotiation", "Team Management",
    "Public Speaking", "Problem Solving", "Critical Thinking",
    "Digital Marketing", "SEO", "Content Marketing", "Social Media Marketing",
    "Salesforce", "CRM", "Lead Generation",
    "UX Design", "UI Design", "Figma", "Adobe Photoshop", "Adobe Illustrator",
]

DEGREE_PATTERNS = re.compile(
    r"\b(Bachelor(?:'s)?(?: of [A-Za-z]+)?|B\.?S\.?|B\.?A\.?|B\.?Tech|"
    r"Master(?:'s)?(?: of [A-Za-z]+)?|M\.?S\.?|M\.?A\.?|M\.?Tech|MBA|"
    r"Ph\.?D\.?|Doctorate|Associate(?:'s)?)\b",
    re.IGNORECASE,
)

ROLE_SKILL_PROFILES = {
    "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics",
                        "Pandas", "Deep Learning", "Data Visualization"],
    "Software Engineer": ["Python", "Java", "Git", "REST API", "Docker", "CI/CD"],
    "Machine Learning Engineer": ["Python", "Machine Learning", "TensorFlow",
                                   "PyTorch", "Deep Learning", "Docker", "AWS"],
    "Data Analyst": ["SQL", "Excel", "Data Analysis", "Data Visualization",
                      "Tableau", "Power BI", "Statistics"],
    "Product Manager": ["Product Management", "Stakeholder Management",
                         "Agile", "Business Analysis", "Communication",
                         "Strategic Planning"],
    "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Azure",
                         "Git", "Microservices"],
    "Business Analyst": ["Business Analysis", "SQL", "Excel",
                          "Stakeholder Management", "Communication", "Data Analysis"],
    "Marketing Manager": ["Digital Marketing", "SEO", "Content Marketing",
                           "Social Media Marketing", "Communication"],
}

# ---------------------------------------------------------------------------
# Model loading (loaded once at startup)
# ---------------------------------------------------------------------------
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("SKILL", [nlp.make_doc(skill) for skill in SKILLS_GAZETTEER])

print("Loading role classifier...")
clf = joblib.load(MODELS_DIR / "role_classifier.joblib")
tfidf = joblib.load(MODELS_DIR / "role_tfidf_vectorizer.joblib")
print("Models loaded.")


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS profiles (
            user_id INTEGER PRIMARY KEY,
            profile_json TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------
def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------------------------------------------------------------------------
# Resume parsing / prediction logic (ported from the Streamlit app)
# ---------------------------------------------------------------------------
def extract_all(text):
    doc = nlp(text)
    matches = matcher(doc)
    spans = sorted(
        [(start, end) for _, start, end in matches],
        key=lambda s: (s[0], -(s[1] - s[0])),
    )
    filtered = []
    last_end = -1
    for start, end in spans:
        if start >= last_end:
            filtered.append((start, end))
            last_end = end

    html_parts, skills = [], []
    cursor = 0
    for start, end in filtered:
        span = doc[start:end]
        html_parts.append(doc[cursor:start].text)
        html_parts.append(
            f'<span class="skill-highlight">{span.text}</span>'
        )
        skills.append(span.text)
        cursor = end
    html_parts.append(doc[cursor:].text)
    highlighted_html = "".join(html_parts)

    education = []
    for m in DEGREE_PATTERNS.finditer(text):
        degree = m.group(0)
        window_text = text[m.end():m.end() + 120]
        window_doc = nlp(window_text)
        institution = next((e.text for e in window_doc.ents if e.label_ == "ORG"), None)
        education.append({"degree": degree, "institution": institution})

    return highlighted_html, sorted(set(skills)), education


def predict_roles(text, top_k=5):
    X = tfidf.transform([text])
    proba = clf.predict_proba(X)[0]
    classes = clf.classes_
    ranked = sorted(zip(classes, proba), key=lambda x: -x[1])[:top_k]
    return [{"role": r, "confidence": float(p)} for r, p in ranked]


def skill_gap(role, extracted_skills):
    required = ROLE_SKILL_PROFILES.get(role)
    if not required:
        return None
    extracted_lower = {s.lower() for s in extracted_skills}
    matched = [s for s in required if s.lower() in extracted_lower]
    missing = [s for s in required if s.lower() not in extracted_lower]
    return {"matched": matched, "missing": missing}


def extract_text_from_file(file_storage):
    filename = file_storage.filename.lower()
    data = file_storage.read()

    if filename.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)

    if filename.endswith(".docx"):
        import docx
        doc = docx.Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)

    return ""


# ---------------------------------------------------------------------------
# Routes: auth
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    errors = []
    if not name:
        errors.append("Name is required.")
    if not EMAIL_RE.match(email):
        errors.append("A valid email is required.")
    if len(password) < 6:
        errors.append("Password must be at least 6 characters.")

    if errors:
        return render_template("register.html", errors=errors, name=name, email=email)

    conn = get_db()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
    if existing:
        conn.close()
        return render_template(
            "register.html", errors=["An account with that email already exists."],
            name=name, email=email,
        )

    conn.execute(
        "INSERT INTO users (name, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (name, email, generate_password_hash(password), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("login", registered="1"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", registered=request.args.get("registered"))

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", errors=["Invalid email or password."], email=email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Routes: dashboard (protected)
# ---------------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user_name=session.get("user_name"))


# ---------------------------------------------------------------------------
# API: resume analysis
# ---------------------------------------------------------------------------
@app.route("/api/analyze", methods=["POST"])
@login_required
def api_analyze():
    resume_text = ""

    if "resume_file" in request.files and request.files["resume_file"].filename:
        resume_text = extract_text_from_file(request.files["resume_file"])
    elif request.is_json:
        resume_text = (request.get_json() or {}).get("text", "")
    else:
        resume_text = request.form.get("text", "")

    if not resume_text.strip():
        return jsonify({"error": "No resume text found."}), 400

    highlighted_html, skills, education = extract_all(resume_text)
    ranked = predict_roles(resume_text, top_k=5)
    top_role = ranked[0]["role"] if ranked else None
    gap = skill_gap(top_role, skills) if top_role else None

    return jsonify({
        "highlighted_html": highlighted_html,
        "skills": skills,
        "education": education,
        "predictions": ranked,
        "top_role": top_role,
        "skill_gap": gap,
    })


# ---------------------------------------------------------------------------
# API: profile save/load
# ---------------------------------------------------------------------------
@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def api_profile():
    user_id = session["user_id"]
    conn = get_db()

    if request.method == "GET":
        row = conn.execute(
            "SELECT profile_json FROM profiles WHERE user_id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if row:
            return jsonify(json.loads(row["profile_json"]))
        return jsonify({})

    data = request.get_json() or {}
    errors = []
    if not data.get("name", "").strip():
        errors.append("Name is required.")
    if not EMAIL_RE.match(data.get("email", "")):
        errors.append("Email is invalid.")
    years = data.get("years_experience")
    if years is None or not (0 <= float(years) <= 60):
        errors.append("Years of experience must be between 0 and 60.")
    if not data.get("skills"):
        errors.append("At least one skill is required.")

    if errors:
        conn.close()
        return jsonify({"errors": errors}), 400

    conn.execute(
        """
        INSERT INTO profiles (user_id, profile_json, updated_at) VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET profile_json = excluded.profile_json,
                                            updated_at = excluded.updated_at
        """,
        (user_id, json.dumps(data), datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "saved"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)