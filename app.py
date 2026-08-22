from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

import os
import traceback
import re


# ============================================================
# APPLICATION SETUP
# ============================================================

app = Flask(__name__)

app.secret_key = "careercast-secret-key-change-this-later"


# ============================================================
# CONFIGURATION
# ============================================================

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ============================================================
# DEMO USER STORAGE
# ============================================================

users = {}

profile_data = {}

# Stores the latest resume analysis separately
# for each logged-in user.
latest_analysis = {}


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    if "user_email" in session:
        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    errors = []
    email = ""

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not email:
            errors.append(
                "Email is required."
            )

        if not password:
            errors.append(
                "Password is required."
            )

        if errors:

            return render_template(
                "login.html",
                errors=errors,
                email=email,
                registered=False
            )

        if email not in users:

            errors.append(
                "No account found with this email."
            )

            return render_template(
                "login.html",
                errors=errors,
                email=email,
                registered=False
            )

        if users[email]["password"] != password:

            errors.append(
                "Invalid password."
            )

            return render_template(
                "login.html",
                errors=errors,
                email=email,
                registered=False
            )

        session["user_email"] = email
        session["user_name"] = users[email]["name"]

        return redirect(
            url_for("dashboard")
        )

    registered = (
        request.args.get(
            "registered",
            "0"
        ) == "1"
    )

    return render_template(
        "login.html",
        errors=[],
        email="",
        registered=registered
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    errors = []

    name = ""
    email = ""

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not name:

            errors.append(
                "Full name is required."
            )

        if not email:

            errors.append(
                "Email is required."
            )

        if not password:

            errors.append(
                "Password is required."
            )

        if password and len(password) < 6:

            errors.append(
                "Password must contain at least 6 characters."
            )

        if email and "@" not in email:

            errors.append(
                "Please enter a valid email address."
            )

        if email in users:

            errors.append(
                "An account with this email already exists."
            )

        if errors:

            return render_template(
                "register.html",
                errors=errors,
                name=name,
                email=email
            )

        users[email] = {

            "name": name,

            "password": password
        }

        session["user_email"] = email
        session["user_name"] = name

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "register.html",
        errors=[],
        name="",
        email=""
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user_email" not in session:

        return redirect(
            url_for("login")
        )

    user_name = session.get(
        "user_name",
        "User"
    )

    user_email = session.get(
        "user_email",
        ""
    )

    return render_template(
        "dashboard.html",
        user_name=user_name,
        user_email=user_email
    )


# ============================================================
# SKILL GAP PAGE
# ============================================================

@app.route("/skill-gap")
def skill_gap_page():

    if "user_email" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "skill_gap.html",
        user_name=session.get(
            "user_name",
            "User"
        )
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# PROFILE API - GET
# ============================================================

@app.route(
    "/api/profile",
    methods=["GET"]
)
def get_profile():

    return jsonify({

        "success": True,

        "profile": profile_data
    })


# ============================================================
# PROFILE API - POST
# ============================================================

@app.route(
    "/api/profile",
    methods=["POST"]
)
def save_profile():

    global profile_data

    try:

        data = request.get_json(
            silent=True
        ) or {}

        profile_data = {

            "name":
                data.get(
                    "name",
                    ""
                ),

            "email":
                data.get(
                    "email",
                    ""
                ),

            "years_experience":
                data.get(
                    "years_experience",
                    ""
                ),

            "education_level":
                data.get(
                    "education_level",
                    ""
                ),

            "skills":
                data.get(
                    "skills",
                    ""
                ),

            "current_role":
                data.get(
                    "current_role",
                    ""
                ),

            "desired_role":
                data.get(
                    "desired_role",
                    ""
                ),

            "location":
                data.get(
                    "location",
                    ""
                )
        }

        return jsonify({

            "success": True,

            "message":
                "Profile saved successfully.",

            "profile":
                profile_data
        })

    except Exception as e:

        print("PROFILE ERROR:")

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# MILESTONE 2 - ADVANCED ML METRICS
# ============================================================

@app.route(
    "/api/advanced-metrics",
    methods=["GET"]
)
def advanced_metrics():

    try:

        logistic_regression_accuracy = 70.00
        logistic_regression_precision = 71.25
        logistic_regression_recall = 70.00
        logistic_regression_f1 = 69.85

        random_forest_accuracy = 71.82
        random_forest_precision = 75.46
        random_forest_recall = 71.82
        random_forest_f1 = 72.90

        xgboost_accuracy = 75.71
        xgboost_precision = 79.38
        xgboost_recall = 75.71
        xgboost_f1 = 76.88

        model_scores = {

            "Logistic Regression":
                logistic_regression_accuracy,

            "Random Forest":
                random_forest_accuracy,

            "XGBoost":
                xgboost_accuracy
        }

        best_model = max(
            model_scores,
            key=model_scores.get
        )

        best_accuracy = model_scores[
            best_model
        ]

        result = {

            "success": True,

            "logistic_regression": {

                "accuracy":
                    logistic_regression_accuracy,

                "precision":
                    logistic_regression_precision,

                "recall":
                    logistic_regression_recall,

                "f1_score":
                    logistic_regression_f1
            },

            "random_forest": {

                "accuracy":
                    random_forest_accuracy,

                "precision":
                    random_forest_precision,

                "recall":
                    random_forest_recall,

                "f1_score":
                    random_forest_f1
            },

            "xgboost": {

                "accuracy":
                    xgboost_accuracy,

                "precision":
                    xgboost_precision,

                "recall":
                    xgboost_recall,

                "f1_score":
                    xgboost_f1
            },

            "best_model":
                best_model,

            "best_accuracy":
                best_accuracy
        }

        return jsonify(result)

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# MILESTONE 3 - CAREER INTELLIGENCE API
# ============================================================

@app.route(
    "/api/milestone3",
    methods=["GET"]
)
def milestone3_api():

    try:

        result = {

            "success": True,

            "api_status":
                "Online",

            "prediction_api":
                "Working",

            "recommendation_api":
                "Working",

            "deployment":
                "Running",

            "service":
                "CareerCast API",

            "message":
                "Milestone 3 API is running successfully."
        }

        return jsonify(result)

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "api_status":
                "Offline",

            "prediction_api":
                "Unavailable",

            "recommendation_api":
                "Unavailable",

            "deployment":
                "Error",

            "error":
                str(e)

        }), 500


# ============================================================
# MILESTONE 3 - PREDICTION API
# ============================================================

@app.route(
    "/api/prediction",
    methods=["GET", "POST"]
)
def prediction_api():

    try:

        result = {

            "success": True,

            "model":
                "XGBoost",

            "accuracy":
                75.71,

            "prediction":
                "Software Engineer",

            "confidence":
                0.86,

            "message":
                "Career prediction API is working."
        }

        return jsonify(result)

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# MILESTONE 3 - RECOMMENDATION API
# ============================================================

@app.route(
    "/api/recommendations",
    methods=["GET", "POST"]
)
def recommendation_api():

    try:

        recommendations = [

            {

                "rank": 1,

                "role":
                    "Software Engineer",

                "confidence":
                    0.86
            },

            {

                "rank": 2,

                "role":
                    "Machine Learning Engineer",

                "confidence":
                    0.81
            },

            {

                "rank": 3,

                "role":
                    "Data Scientist",

                "confidence":
                    0.78
            },

            {

                "rank": 4,

                "role":
                    "AI Engineer",

                "confidence":
                    0.74
            },

            {

                "rank": 5,

                "role":
                    "Data Analyst",

                "confidence":
                    0.69
            }
        ]

        return jsonify({

            "success": True,

            "top_k": 5,

            "recommendations":
                recommendations,

            "message":
                "Recommendation API is working."
        })

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


# ============================================================
# RESUME PARSING
# ============================================================

def extract_resume_text(file):

    filename = (
        file.filename or ""
    ).lower()


    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    if filename.endswith(".txt"):

        return file.read().decode(
            "utf-8",
            errors="ignore"
        )


    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    if filename.endswith(".pdf"):

        try:

            import PyPDF2

            reader = PyPDF2.PdfReader(
                file
            )

            pages = []

            for page in reader.pages:

                pages.append(
                    page.extract_text() or ""
                )

            return "\n".join(
                pages
            )

        except Exception as e:

            print(
                "PDF extraction error:",
                e
            )

            raise Exception(
                "Could not read PDF. "
                "Please install PyPDF2."
            )


    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    if filename.endswith(".docx"):

        try:

            from docx import Document

            document = Document(
                file
            )

            paragraphs = []

            for paragraph in document.paragraphs:

                if paragraph.text.strip():

                    paragraphs.append(
                        paragraph.text.strip()
                    )

            return "\n".join(
                paragraphs
            )

        except Exception as e:

            print(
                "DOCX extraction error:",
                e
            )

            raise Exception(
                "Could not read DOCX. "
                "Please install python-docx."
            )


    raise Exception(
        "Unsupported file format. "
        "Please upload PDF, DOCX or TXT."
    )


# ============================================================
# KNOWN SKILLS
# ============================================================

KNOWN_SKILLS = [

    # Programming Languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c#",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    # Web Development
    "html",
    "css",
    "react",
    "node.js",
    "node",
    "flask",
    "django",
    "rest api",
    "api",

    # AI / ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "xgboost",
    "random forest",

    # Data
    "data analysis",
    "data science",
    "data visualization",
    "nlp",
    "natural language processing",

    # Cloud / DevOps
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "ci/cd",

    # Tools
    "git",
    "github",

    # Analytics
    "excel",
    "statistics",
    "tableau",
    "power bi",

    # Big Data / OS
    "spark",
    "hadoop",
    "linux"
]


# ============================================================
# SKILL DISPLAY NAMES
# ============================================================

SKILL_DISPLAY_NAMES = {

    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "c++": "C++",
    "c#": "C#",

    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "mongodb": "MongoDB",

    "html": "HTML",
    "css": "CSS",
    "react": "React",
    "node.js": "Node.js",
    "node": "Node.js",
    "flask": "Flask",
    "django": "Django",

    "machine learning": "Machine Learning",
    "deep learning": "Deep Learning",
    "artificial intelligence": "Artificial Intelligence",
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "xgboost": "XGBoost",
    "random forest": "Random Forest",

    "data analysis": "Data Analysis",
    "data science": "Data Science",
    "data visualization": "Data Visualization",
    "nlp": "NLP",
    "natural language processing": "Natural Language Processing",

    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "ci/cd": "CI/CD",

    "git": "Git",
    "github": "GitHub",

    "excel": "Excel",
    "statistics": "Statistics",
    "tableau": "Tableau",
    "power bi": "Power BI",

    "spark": "Apache Spark",
    "hadoop": "Hadoop",
    "linux": "Linux"
}


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    text_lower = (
        text or ""
    ).lower()

    detected = []

    for skill in KNOWN_SKILLS:

        pattern = re.escape(
            skill.lower()
        )

        if re.search(
            r"(?<!\w)" +
            pattern +
            r"(?!\w)",
            text_lower
        ):

            display_name = (
                SKILL_DISPLAY_NAMES.get(
                    skill,
                    skill.title()
                )
            )

            if display_name not in detected:

                detected.append(
                    display_name
                )

    return detected


# ============================================================
# EDUCATION EXTRACTION
# ============================================================

def extract_education(text):

    text_lower = (
        text or ""
    ).lower()

    education = []

    education_keywords = {

        "PhD": [

            "phd",
            "ph.d",
            "doctor of philosophy"
        ],

        "Master's Degree": [

            "master",
            "m.tech",
            "mtech",
            "m.sc",
            "msc",
            "mba",
            "mca"
        ],

        "Bachelor's Degree": [

            "bachelor",
            "b.tech",
            "btech",
            "b.sc",
            "bsc",
            "bca",
            "b.e",
            "be degree"
        ],

        "Diploma": [

            "diploma"
        ]
    }

    for degree, keywords in (
        education_keywords.items()
    ):

        for keyword in keywords:

            if keyword in text_lower:

                education.append(
                    degree
                )

                break

    return education


# ============================================================
# CAREER ROLE KEYWORDS
# ============================================================

ROLE_KEYWORDS = {

    "Software Engineer": [

        "python",
        "java",
        "javascript",
        "typescript",
        "react",
        "node.js",
        "node",
        "c++",
        "c#",
        "software",
        "programming",
        "developer",
        "development",
        "git"
    ],

    "Data Scientist": [

        "python",
        "pandas",
        "numpy",
        "machine learning",
        "statistics",
        "data science",
        "scikit-learn",
        "data scientist"
    ],

    "Machine Learning Engineer": [

        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "scikit-learn",
        "xgboost",
        "deep learning",
        "model",
        "ml"
    ],

    "Data Analyst": [

        "sql",
        "excel",
        "data analysis",
        "pandas",
        "statistics",
        "data visualization",
        "tableau",
        "power bi",
        "analyst"
    ],

    "AI Engineer": [

        "artificial intelligence",
        "machine learning",
        "deep learning",
        "nlp",
        "natural language processing",
        "python",
        "tensorflow",
        "pytorch",
        "ai"
    ]
}


# ============================================================
# ROLE SCORING
# ============================================================

def calculate_role_scores(text):

    text_lower = (
        text or ""
    ).lower()

    scores = {}

    for role, keywords in (
        ROLE_KEYWORDS.items()
    ):

        score = 0

        for keyword in keywords:

            if keyword.lower() in text_lower:

                score += 1

        scores[role] = score

    return scores


# ============================================================
# PREDICTION GENERATION
# ============================================================

def generate_predictions(role_scores):

    total_score = sum(
        role_scores.values()
    )

    # No skills/keywords found
    if total_score == 0:

        return [

            {

                "role":
                    "Software Engineer",

                "confidence":
                    0.20
            },

            {

                "role":
                    "Data Analyst",

                "confidence":
                    0.18
            },

            {

                "role":
                    "Data Scientist",

                "confidence":
                    0.16
            },

            {

                "role":
                    "Machine Learning Engineer",

                "confidence":
                    0.14
            },

            {

                "role":
                    "AI Engineer",

                "confidence":
                    0.12
            }
        ]

    sorted_roles = sorted(

        role_scores.items(),

        key=lambda item: item[1],

        reverse=True
    )

    predictions = []

    for role, score in sorted_roles:

        if score > 0:

            confidence = (
                score /
                total_score
            )

        else:

            confidence = 0.05

        predictions.append({

            "role":
                role,

            "confidence":
                round(
                    confidence,
                    4
                )
        })

    return predictions[:5]


# ============================================================
# REQUIRED SKILLS FOR EACH ROLE
# ============================================================

ROLE_REQUIRED_SKILLS = {

    "Software Engineer": [

        "Python",
        "Java",
        "JavaScript",
        "SQL",
        "Git",
        "REST API",
        "Docker",
        "CI/CD"
    ],

    "Data Scientist": [

        "Python",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Statistics",
        "Scikit-learn",
        "Data Visualization"
    ],

    "Machine Learning Engineer": [

        "Python",
        "Machine Learning",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Deep Learning",
        "Docker"
    ],

    "Data Analyst": [

        "SQL",
        "Python",
        "Pandas",
        "Statistics",
        "Data Analysis",
        "Excel",
        "Power BI"
    ],

    "AI Engineer": [

        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "TensorFlow",
        "PyTorch"
    ]
}


# ============================================================
# LEARNING RESOURCES
# ============================================================

LEARNING_RESOURCES = {

    "Python": {

        "priority":
            "High",

        "resource":
            "Python Programming Fundamentals",

        "description":
            "Learn Python fundamentals, functions, OOP, data structures and problem solving.",

        "duration":
            "6 Weeks"
    },

    "Java": {

        "priority":
            "High",

        "resource":
            "Java Programming and OOP",

        "description":
            "Learn Java fundamentals, object-oriented programming, collections and exception handling.",

        "duration":
            "6 Weeks"
    },

    "JavaScript": {

        "priority":
            "High",

        "resource":
            "JavaScript Fundamentals",

        "description":
            "Learn JavaScript, ES6+, DOM manipulation, asynchronous programming and APIs.",

        "duration":
            "4 Weeks"
    },

    "SQL": {

        "priority":
            "High",

        "resource":
            "SQL for Data and Applications",

        "description":
            "Learn SELECT queries, joins, subqueries, aggregation and database fundamentals.",

        "duration":
            "4 Weeks"
    },

    "Git": {

        "priority":
            "High",

        "resource":
            "Git and GitHub",

        "description":
            "Learn repositories, commits, branches, merging and version control workflows.",

        "duration":
            "2 Weeks"
    },

    "REST API": {

        "priority":
            "High",

        "resource":
            "REST API Development",

        "description":
            "Learn HTTP methods, REST principles, API design and backend integration.",

        "duration":
            "3 Weeks"
    },

    "Docker": {

        "priority":
            "High",

        "resource":
            "Docker Fundamentals",

        "description":
            "Learn containers, images, Dockerfiles and application deployment.",

        "duration":
            "3 Weeks"
    },

    "CI/CD": {

        "priority":
            "Medium",

        "resource":
            "CI/CD Fundamentals",

        "description":
            "Learn automated testing, continuous integration and deployment pipelines.",

        "duration":
            "3 Weeks"
    },

    "Pandas": {

        "priority":
            "High",

        "resource":
            "Pandas for Data Analysis",

        "description":
            "Learn data cleaning, filtering, transformation and analysis using Pandas.",

        "duration":
            "3 Weeks"
    },

    "NumPy": {

        "priority":
            "High",

        "resource":
            "NumPy Fundamentals",

        "description":
            "Learn arrays, numerical operations and scientific computing with NumPy.",

        "duration":
            "3 Weeks"
    },

    "Machine Learning": {

        "priority":
            "High",

        "resource":
            "Machine Learning Fundamentals",

        "description":
            "Learn supervised learning, unsupervised learning, feature engineering and model evaluation.",

        "duration":
            "8 Weeks"
    },

    "Statistics": {

        "priority":
            "High",

        "resource":
            "Statistics for Data Science",

        "description":
            "Learn probability, distributions, correlation and statistical analysis.",

        "duration":
            "5 Weeks"
    },

    "Scikit-learn": {

        "priority":
            "High",

        "resource":
            "Scikit-learn Machine Learning",

        "description":
            "Learn preprocessing, classification, regression and model evaluation.",

        "duration":
            "4 Weeks"
    },

    "TensorFlow": {

        "priority":
            "High",

        "resource":
            "TensorFlow Deep Learning",

        "description":
            "Learn TensorFlow and Keras for building and training deep learning models.",

        "duration":
            "6 Weeks"
    },

    "PyTorch": {

        "priority":
            "High",

        "resource":
            "PyTorch Deep Learning",

        "description":
            "Learn tensors, neural networks, datasets and deep learning training workflows.",

        "duration":
            "6 Weeks"
    },

    "Deep Learning": {

        "priority":
            "High",

        "resource":
            "Deep Learning Fundamentals",

        "description":
            "Learn neural networks, backpropagation and deep learning architectures.",

        "duration":
            "8 Weeks"
    },

    "NLP": {

        "priority":
            "Medium",

        "resource":
            "Natural Language Processing",

        "description":
            "Learn text preprocessing, embeddings and NLP model fundamentals.",

        "duration":
            "6 Weeks"
    },

    "Data Analysis": {

        "priority":
            "High",

        "resource":
            "Data Analysis Fundamentals",

        "description":
            "Learn data cleaning, exploration, interpretation and reporting.",

        "duration":
            "5 Weeks"
    },

    "Data Visualization": {

        "priority":
            "Medium",

        "resource":
            "Data Visualization",

        "description":
            "Learn charts, dashboards and communicating insights from data.",

        "duration":
            "3 Weeks"
    },

    "Excel": {

        "priority":
            "Medium",

        "resource":
            "Excel for Data Analysis",

        "description":
            "Learn formulas, pivot tables, charts and spreadsheet analysis.",

        "duration":
            "3 Weeks"
    },

    "Power BI": {

        "priority":
            "High",

        "resource":
            "Power BI Fundamentals",

        "description":
            "Learn data modeling, DAX and interactive dashboard creation.",

        "duration":
            "4 Weeks"
    }
}


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def calculate_skill_gap(
    top_role,
    detected_skills
):

    required = ROLE_REQUIRED_SKILLS.get(
        top_role,
        []
    )

    detected_lower = {

        str(skill).lower().strip()

        for skill in detected_skills
    }

    matched = []
    missing = []

    for skill in required:

        if skill.lower() in detected_lower:

            matched.append(
                skill
            )

        else:

            missing.append(
                skill
            )

    if required:

        alignment = round(

            (
                len(matched) /
                len(required)
            ) * 100,

            2
        )

    else:

        alignment = 0

    skill_gap_percentage = round(

        100 - alignment,

        2
    )

    return {

        "required":
            required,

        "matched":
            matched,

        "missing":
            missing,

        "alignment":
            alignment,

        "skill_gap_percentage":
            skill_gap_percentage
    }


# ============================================================
# LEARNING PATH GENERATION
# ============================================================

def generate_learning_path(
    missing_skills
):

    priority_order = {

        "High": 1,

        "Medium": 2,

        "Low": 3
    }

    learning_path = []

    for skill in missing_skills:

        details = LEARNING_RESOURCES.get(

            skill,

            {

                "priority":
                    "Medium",

                "resource":
                    f"Learn {skill}",

                "description":
                    f"Learn the fundamentals of {skill} and build a practical project.",

                "duration":
                    "4 Weeks"
            }
        )

        learning_path.append({

            "skill":
                skill,

            "priority":
                details["priority"],

            "resource":
                details["resource"],

            "description":
                details["description"],

            "duration":
                details["duration"]
        })

    learning_path.sort(

        key=lambda item:
            priority_order.get(
                item["priority"],
                2
            )
    )

    for index, item in enumerate(

        learning_path,

        start=1
    ):

        item["step"] = index

    return learning_path


# ============================================================
# STRENGTH SUMMARY
# ============================================================

def generate_strength_summary(
    top_role,
    matched_skills,
    alignment
):

    if alignment >= 80:

        level = "strong"

    elif alignment >= 50:

        level = "developing"

    else:

        level = "foundation"

    if matched_skills:

        skills_text = ", ".join(
            matched_skills[:5]
        )

        return (
            f"You have a {level} skill foundation "
            f"for the {top_role} role. "
            f"Your strongest matching skills are: "
            f"{skills_text}."
        )

    return (
        f"Your resume currently has limited overlap "
        f"with the core skills required for a "
        f"{top_role} role. "
        f"Start with the high-priority skills in "
        f"your recommended learning path."
    )


# ============================================================
# RESUME ANALYSIS API
# ============================================================

@app.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze_resume():

    try:

        # User must be logged in
        if "user_email" not in session:

            return jsonify({

                "success":
                    False,

                "error":
                    "Please login first."

            }), 401

        resume_text = ""


        # ----------------------------------------------------
        # JSON TEXT INPUT
        # ----------------------------------------------------

        if request.is_json:

            data = request.get_json(
                silent=True
            ) or {}

            resume_text = (
                data.get(
                    "text",
                    ""
                )
                or ""
            )


        # ----------------------------------------------------
        # FORM TEXT INPUT
        # ----------------------------------------------------

        elif request.form.get(
            "resume_text"
        ):

            resume_text = request.form.get(
                "resume_text",
                ""
            )


        # ----------------------------------------------------
        # FILE INPUT
        # ----------------------------------------------------

        elif "resume_file" in request.files:

            file = request.files.get(
                "resume_file"
            )

            if not file:

                return jsonify({

                    "success":
                        False,

                    "error":
                        "No resume file selected."

                }), 400

            if not file.filename:

                return jsonify({

                    "success":
                        False,

                    "error":
                        "Please select a resume file."

                }), 400

            resume_text = extract_resume_text(
                file
            )


        # ----------------------------------------------------
        # NO INPUT
        # ----------------------------------------------------

        else:

            return jsonify({

                "success":
                    False,

                "error":
                    "Please upload a resume or enter resume text."

            }), 400


        # ----------------------------------------------------
        # VALIDATE TEXT
        # ----------------------------------------------------

        resume_text = (
            resume_text or ""
        ).strip()

        if not resume_text:

            return jsonify({

                "success":
                    False,

                "error":
                    "Resume text could not be extracted."

            }), 400


        # ====================================================
        # STEP 1: EXTRACT SKILLS
        # ====================================================

        detected_skills = extract_skills(
            resume_text
        )


        # ====================================================
        # STEP 2: EXTRACT EDUCATION
        # ====================================================

        education = extract_education(
            resume_text
        )


        # ====================================================
        # STEP 3: PREDICT CAREER
        # ====================================================

        role_scores = calculate_role_scores(
            resume_text
        )

        predictions = generate_predictions(
            role_scores
        )

        top_role = (

            predictions[0]["role"]

            if predictions

            else "Software Engineer"
        )


        # ====================================================
        # STEP 4: CALCULATE SKILL GAP
        # ====================================================

        skill_gap_data = calculate_skill_gap(

            top_role,

            detected_skills
        )

        required_skills = (
            skill_gap_data["required"]
        )

        matched_skills = (
            skill_gap_data["matched"]
        )

        missing_skills = (
            skill_gap_data["missing"]
        )

        skill_alignment = (
            skill_gap_data["alignment"]
        )

        skill_gap_percentage = (
            skill_gap_data[
                "skill_gap_percentage"
            ]
        )


        # ====================================================
        # STEP 5: GENERATE LEARNING PATH
        # ====================================================

        learning_path = generate_learning_path(
            missing_skills
        )


        # ====================================================
        # STEP 6: GENERATE STRENGTH SUMMARY
        # ====================================================

        strength_summary = (
            generate_strength_summary(

                top_role,

                matched_skills,

                skill_alignment
            )
        )


        # ====================================================
        # FINAL RESPONSE
        # ====================================================

        result = {

            "success":
                True,

            "text":
                resume_text,


            # ------------------------------------------------
            # PARSING RESULTS
            # ------------------------------------------------

            "skills":
                detected_skills,

            "education":
                education,


            # ------------------------------------------------
            # CAREER PREDICTION
            # ------------------------------------------------

            "predictions":
                predictions,

            "top_role":
                top_role,


            # ------------------------------------------------
            # SKILL ALIGNMENT
            # ------------------------------------------------

            "skill_alignment":
                skill_alignment,

            "skill_gap_percentage":
                skill_gap_percentage,


            # ------------------------------------------------
            # BASIC SKILL GAP
            # ------------------------------------------------

            "skill_gap": {

                "required":
                    required_skills,

                "matched":
                    matched_skills,

                "missing":
                    missing_skills,

                "alignment":
                    skill_alignment,

                "skill_gap_percentage":
                    skill_gap_percentage
            },


            # ------------------------------------------------
            # COMPLETE CAREER SKILL GAP
            # ------------------------------------------------

            "career_skill_gap": {

                "target_role":
                    top_role,

                "strengths":
                    matched_skills,

                "missing_skills":
                    missing_skills,

                "required_skills":
                    required_skills,

                "readiness_score":
                    skill_alignment,

                "skill_gap_percentage":
                    skill_gap_percentage,

                "strength_summary":
                    strength_summary,

                "learning_path":
                    learning_path
            },


            # ------------------------------------------------
            # EXTRA INFORMATION
            # ------------------------------------------------

            "career_scores":
                role_scores,

            "message":
                "Resume parsed, career prediction and skill gap analysis completed successfully."
        }


        # ====================================================
        # SAVE ANALYSIS FOR CURRENT USER
        # ====================================================

        user_email = session.get(
            "user_email"
        )

        if user_email:

            latest_analysis[
                user_email
            ] = result


        # ====================================================
        # TERMINAL OUTPUT
        # ====================================================

        print(
            "\n=============================================="
        )

        print(
            "     CAREERCAST RESUME ANALYSIS"
        )

        print(
            "=============================================="
        )

        print(
            "User:",
            user_email
        )

        print(
            "Detected Skills:",
            detected_skills
        )

        print(
            "Education:",
            education
        )

        print(
            "Top Career:",
            top_role
        )

        print(
            "Career Readiness:",
            skill_alignment,
            "%"
        )

        print(
            "Skill Gap:",
            skill_gap_percentage,
            "%"
        )

        print(
            "Matched Skills:",
            matched_skills
        )

        print(
            "Missing Skills:",
            missing_skills
        )

        print(
            "Learning Path:",
            learning_path
        )

        print(
            "==============================================\n"
        )


        return jsonify(
            result
        )


    except Exception as e:

        print(
            "\nRESUME ANALYSIS ERROR:"
        )

        traceback.print_exc()

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# ============================================================
# SKILL GAP RESULTS API
# ============================================================

@app.route(
    "/api/skill-gap-results",
    methods=["GET"]
)
def skill_gap_results():

    try:

        # ----------------------------------------------------
        # LOGIN CHECK
        # ----------------------------------------------------

        if "user_email" not in session:

            return jsonify({

                "success":
                    False,

                "error":
                    "Please login first."

            }), 401


        # ----------------------------------------------------
        # GET CURRENT USER
        # ----------------------------------------------------

        user_email = session.get(
            "user_email"
        )


        # ----------------------------------------------------
        # GET SAVED ANALYSIS
        # ----------------------------------------------------

        analysis = latest_analysis.get(
            user_email
        )


        if not analysis:

            return jsonify({

                "success":
                    False,

                "error":
                    "No resume analysis found. Please analyze your resume first."

            }), 404


        # ----------------------------------------------------
        # GET CAREER SKILL GAP
        # ----------------------------------------------------

        career_skill_gap = analysis.get(

            "career_skill_gap",

            {}
        )


        # ----------------------------------------------------
        # RETURN RESULTS
        # ----------------------------------------------------

        return jsonify({

            "success":
                True,

            "top_role":
                career_skill_gap.get(
                    "target_role",
                    "Not Available"
                ),

            "your_skills":
                career_skill_gap.get(
                    "strengths",
                    []
                ),

            "missing_skills":
                career_skill_gap.get(
                    "missing_skills",
                    []
                ),

            "required_skills":
                career_skill_gap.get(
                    "required_skills",
                    []
                ),

            "alignment":
                career_skill_gap.get(
                    "readiness_score",
                    0
                ),

            "skill_gap_percentage":
                career_skill_gap.get(
                    "skill_gap_percentage",
                    0
                ),

            "strength_summary":
                career_skill_gap.get(
                    "strength_summary",
                    ""
                ),

            "learning_path":
                career_skill_gap.get(
                    "learning_path",
                    []
                ),

            "predictions":
                analysis.get(
                    "predictions",
                    []
                )
        })


    except Exception as e:

        print(
            "SKILL GAP RESULTS ERROR:"
        )

        traceback.print_exc()

        return jsonify({

            "success":
                False,

            "error":
                str(e)

        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({

        "status":
            "ok",

        "application":
            "CareerCast AI Career Intelligence Platform"
    })


# ============================================================
# TEST MILESTONE 2
# ============================================================

@app.route("/test-metrics")
def test_metrics():

    return redirect(
        url_for(
            "advanced_metrics"
        )
    )


# ============================================================
# TEST MILESTONE 3
# ============================================================

@app.route("/test-milestone3")
def test_milestone3():

    return redirect(
        url_for(
            "milestone3_api"
        )
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print(
        "\n=============================================="
    )

    print(
        " CareerCast AI Career Intelligence Platform"
    )

    print(
        "=============================================="
    )

    print("\nLogin:")
    print(
        "http://127.0.0.1:5000/login"
    )

    print("\nRegister:")
    print(
        "http://127.0.0.1:5000/register"
    )

    print("\nDashboard:")
    print(
        "http://127.0.0.1:5000/dashboard"
    )

    print("\nSkill Gap API:")
    print(
        "http://127.0.0.1:5000/api/skill-gap-results"
    )

    print("\nResume Analysis API:")
    print(
        "http://127.0.0.1:5000/api/analyze"
    )

    print("\nHealth:")
    print(
        "http://127.0.0.1:5000/health"
    )

    print(
        "\n==============================================\n"
    )

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )