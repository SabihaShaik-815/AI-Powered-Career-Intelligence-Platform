from pathlib import Path
from datetime import datetime
from io import BytesIO
import json
import os
import re

import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# OPTIONAL IMPORTS
# ============================================================

try:
    import joblib
except ImportError:
    joblib = None

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        PageBreak,
    )

    REPORTLAB_AVAILABLE = True

except ImportError:
    REPORTLAB_AVAILABLE = False


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
ADVANCED_MODELS_DIR = BASE_DIR / "advanced_models"

POSTINGS_FILE = DATA_DIR / "postings.csv"

ROLE_MODEL_FILE = MODELS_DIR / "role_classifier.joblib"
ROLE_VECTORIZER_FILE = MODELS_DIR / "role_tfidf_vectorizer.joblib"

RF_MODEL_FILE = ADVANCED_MODELS_DIR / "random_forest_model.pkl"
XGB_MODEL_FILE = ADVANCED_MODELS_DIR / "xgboost_model.pkl"

ADVANCED_METRICS_FILE = (
    ADVANCED_MODELS_DIR / "advanced_metrics.json"
)

ROLE_METRICS_FILE = MODELS_DIR / "role_metrics.json"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerCast - Milestone 4",
    page_icon="CC",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(37, 99, 235, 0.16),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(234, 179, 8, 0.10),
            transparent 25%
        ),
        linear-gradient(
            135deg,
            #07111f 0%,
            #0b1728 45%,
            #111827 100%
        );
    color: #f8fafc;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

p, label, span {
    color: #dbeafe;
}

.hero {
    padding: 28px;
    border-radius: 22px;
    margin-bottom: 25px;

    background:
        linear-gradient(
            135deg,
            rgba(15, 23, 42, 0.96),
            rgba(30, 41, 59, 0.92)
        );

    border: 1px solid rgba(148, 163, 184, 0.20);

    box-shadow:
        0 20px 50px rgba(0, 0, 0, 0.30);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    color: #94a3b8 !important;
    font-size: 17px;
}

.card {
    background: rgba(15, 23, 42, 0.82);
    border: 1px solid rgba(148, 163, 184, 0.18);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 20px;

    box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.20);
}

.metric-card {
    background:
        linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.95),
            rgba(15, 23, 42, 0.90)
        );

    border: 1px solid rgba(96, 165, 250, 0.20);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    min-height: 135px;
}

.metric-title {
    color: #94a3b8 !important;
    font-size: 14px;
}

.metric-value {
    color: #f8fafc !important;
    font-size: 31px;
    font-weight: 800;
    margin-top: 8px;
}

.status-complete {
    color: #4ade80 !important;
    font-weight: 700;
}

.status-progress {
    color: #facc15 !important;
    font-weight: 700;
}

.status-pending {
    color: #f87171 !important;
    font-weight: 700;
}

.section-title {
    font-size: 25px;
    font-weight: 750;
    margin-top: 12px;
    margin-bottom: 15px;
}

.small-text {
    color: #94a3b8 !important;
    font-size: 13px;
}

.info-box {
    background: rgba(30, 41, 59, 0.65);
    border-left: 4px solid #60a5fa;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.success-box {
    background: rgba(22, 101, 52, 0.18);
    border-left: 4px solid #4ade80;
    padding: 15px;
    border-radius: 10px;
}

.warning-box {
    background: rgba(161, 98, 7, 0.18);
    border-left: 4px solid #facc15;
    padding: 15px;
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #64748b !important;
    padding: 30px;
    margin-top: 30px;
}

div[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.75);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(148, 163, 184, 0.15);
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def file_exists(path: Path):
    """Return True when a file exists."""
    return path.exists() and path.is_file()


def percentage(value):
    """Convert decimal metrics to percentage."""
    if value is None:
        return 0.0

    try:
        value = float(value)
    except (ValueError, TypeError):
        return 0.0

    if value <= 1:
        return value * 100

    return value


def safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def load_json_file(path: Path):
    """Load JSON file safely."""
    if not file_exists(path):
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def load_postings():
    """
    Load postings.csv.

    Only a limited number of columns are loaded where possible
    to avoid unnecessarily large memory usage.
    """

    if not file_exists(POSTINGS_FILE):
        return pd.DataFrame()

    try:
        return pd.read_csv(
            POSTINGS_FILE,
            low_memory=False,
        )
    except Exception as error:
        st.warning(
            f"Unable to load postings.csv: {error}"
        )
        return pd.DataFrame()


@st.cache_data
def get_postings():
    return load_postings()


def get_column(df, possible_names):
    """Return the first matching column."""
    if df.empty:
        return None

    normalized = {
        str(column).lower().strip(): column
        for column in df.columns
    }

    for name in possible_names:
        key = name.lower().strip()

        if key in normalized:
            return normalized[key]

    return None


def extract_role_column(df):
    return get_column(
        df,
        [
            "title",
            "job_title",
            "role",
            "career",
        ],
    )


def extract_description_column(df):
    return get_column(
        df,
        [
            "description",
            "job_description",
            "text",
            "job_text",
        ],
    )


def normalize_role(role):
    if role is None:
        return ""

    role = str(role).strip()

    role = re.sub(
        r"\s+",
        " ",
        role,
    )

    return role


# ============================================================
# MODEL METRICS
# ============================================================

def load_model_metrics():

    advanced_metrics = load_json_file(
        ADVANCED_METRICS_FILE
    )

    role_metrics = load_json_file(
        ROLE_METRICS_FILE
    )

    metrics = {
        "logistic_regression": 0.0,
        "random_forest": 0.0,
        "xgboost": 0.0,
    }

    # --------------------------------------------------------
    # Advanced metrics
    # --------------------------------------------------------

    if isinstance(advanced_metrics, dict):

        for key in [
            "logistic_regression",
            "random_forest",
            "xgboost",
        ]:

            value = advanced_metrics.get(key)

            if isinstance(value, dict):

                value = (
                    value.get("accuracy")
                    or value.get("test_accuracy")
                    or value.get("score")
                )

            if value is not None:
                metrics[key] = percentage(value)

    # --------------------------------------------------------
    # Role metrics
    # --------------------------------------------------------

    if isinstance(role_metrics, dict):

        value = (
            role_metrics.get("accuracy")
            or role_metrics.get("test_accuracy")
        )

        if value is not None:
            metrics["logistic_regression"] = percentage(
                value
            )

    return metrics


def get_best_model(metrics):

    if not metrics:
        return "Not Available"

    best_key = max(
        metrics,
        key=metrics.get,
    )

    names = {
        "logistic_regression": "Logistic Regression",
        "random_forest": "Random Forest",
        "xgboost": "XGBoost",
    }

    return names.get(
        best_key,
        best_key,
    )


# ============================================================
# COHORT ANALYTICS
# ============================================================

def build_cohort_analytics(df):

    if df.empty:
        return {
            "total_jobs": 0,
            "unique_roles": 0,
            "unique_companies": 0,
            "top_roles": pd.DataFrame(),
            "skill_data": pd.DataFrame(),
        }

    role_column = extract_role_column(df)

    company_column = get_column(
        df,
        [
            "company_name",
            "company",
        ],
    )

    # --------------------------------------------------------
    # Roles
    # --------------------------------------------------------

    if role_column:

        roles = (
            df[role_column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        roles = roles[
            roles != ""
        ]

        role_counts = (
            roles
            .value_counts()
            .head(15)
            .reset_index()
        )

        role_counts.columns = [
            "Role",
            "Jobs",
        ]

        unique_roles = roles.nunique()

    else:

        role_counts = pd.DataFrame(
            columns=["Role", "Jobs"]
        )

        unique_roles = 0

    # --------------------------------------------------------
    # Companies
    # --------------------------------------------------------

    if company_column:

        companies = (
            df[company_column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        companies = companies[
            companies != ""
        ]

        unique_companies = companies.nunique()

    else:

        unique_companies = 0

    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    skill_columns = [
        column
        for column in df.columns
        if "skill" in str(column).lower()
    ]

    skill_records = []

    for column in skill_columns:

        values = (
            df[column]
            .dropna()
            .astype(str)
        )

        for value in values.head(10000):

            parts = re.split(
                r"[,;|]",
                value,
            )

            for part in parts:

                skill = part.strip()

                if (
                    skill
                    and len(skill) > 1
                    and len(skill) < 60
                ):
                    skill_records.append(
                        skill.lower()
                    )

    if skill_records:

        skill_counts = (
            pd.Series(skill_records)
            .value_counts()
            .head(15)
            .reset_index()
        )

        skill_counts.columns = [
            "Skill",
            "Count",
        ]

    else:

        skill_counts = pd.DataFrame(
            columns=["Skill", "Count"]
        )

    return {
        "total_jobs": len(df),
        "unique_roles": unique_roles,
        "unique_companies": unique_companies,
        "top_roles": role_counts,
        "skill_data": skill_counts,
    }


# ============================================================
# CAREER COMPARISON
# ============================================================

DEFAULT_CAREER_SKILLS = {

    "Data Scientist": [
        "python",
        "sql",
        "machine learning",
        "statistics",
        "pandas",
        "numpy",
        "scikit-learn",
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "tensorflow",
        "pytorch",
        "docker",
        "git",
        "sql",
    ],

    "Software Engineer": [
        "python",
        "java",
        "javascript",
        "git",
        "sql",
        "rest api",
        "docker",
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "statistics",
    ],

    "Product Manager": [
        "product management",
        "communication",
        "analytics",
        "roadmap",
        "leadership",
    ],

    "DevOps Engineer": [
        "linux",
        "docker",
        "kubernetes",
        "aws",
        "git",
        "ci/cd",
    ],

    "Business Analyst": [
        "sql",
        "excel",
        "requirements analysis",
        "communication",
        "business analysis",
    ],

    "AI Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp",
    ],
}


def compare_careers(
    career_one,
    career_two,
):

    skills_one = set(
        DEFAULT_CAREER_SKILLS.get(
            career_one,
            [],
        )
    )

    skills_two = set(
        DEFAULT_CAREER_SKILLS.get(
            career_two,
            [],
        )
    )

    common = sorted(
        skills_one.intersection(
            skills_two
        )
    )

    unique_one = sorted(
        skills_one.difference(
            skills_two
        )
    )

    unique_two = sorted(
        skills_two.difference(
            skills_one
        )
    )

    return {
        "career_one": career_one,
        "career_two": career_two,
        "skills_one": sorted(skills_one),
        "skills_two": sorted(skills_two),
        "common": common,
        "unique_one": unique_one,
        "unique_two": unique_two,
    }


# ============================================================
# PDF EXPORT
# ============================================================

def generate_pdf_report(
    metrics,
    cohort,
    comparison=None,
):

    if not REPORTLAB_AVAILABLE:
        return None

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CareerCastTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "CareerCastHeading",
        parent=styles["Heading2"],
        fontSize=15,
        spaceBefore=15,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "CareerCastBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8,
    )

    story = []

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "CareerCast",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Milestone 4 - Packaging, Testing & Finalization",
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Generated on: "
            f"{datetime.now().strftime('%d %B %Y, %H:%M')}",
            body_style,
        )
    )

    story.append(Spacer(1, 15))

    # --------------------------------------------------------
    # Model Metrics
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Model Performance",
            heading_style,
        )
    )

    model_table_data = [
        ["Model", "Accuracy"]
    ]

    for model, accuracy in metrics.items():

        model_name = {
            "logistic_regression":
                "Logistic Regression",
            "random_forest":
                "Random Forest",
            "xgboost":
                "XGBoost",
        }.get(
            model,
            model,
        )

        model_table_data.append(
            [
                model_name,
                f"{accuracy:.2f}%",
            ]
        )

    model_table = Table(
        model_table_data,
        colWidths=[250, 150],
    )

    model_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1e3a8a"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
            ]
        )
    )

    story.append(model_table)

    story.append(Spacer(1, 15))

    # --------------------------------------------------------
    # Cohort Analytics
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Cohort Analytics",
            heading_style,
        )
    )

    cohort_table_data = [
        ["Metric", "Value"],
        [
            "Total Job Records",
            str(cohort["total_jobs"]),
        ],
        [
            "Unique Career Roles",
            str(cohort["unique_roles"]),
        ],
        [
            "Unique Companies",
            str(cohort["unique_companies"]),
        ],
    ]

    cohort_table = Table(
        cohort_table_data,
        colWidths=[250, 150],
    )

    cohort_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1e3a8a"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
            ]
        )
    )

    story.append(cohort_table)

    story.append(Spacer(1, 15))

    # --------------------------------------------------------
    # Career Comparison
    # --------------------------------------------------------

    if comparison:

        story.append(
            Paragraph(
                "Career Comparison",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                f"Comparison: "
                f"{comparison['career_one']} vs "
                f"{comparison['career_two']}",
                body_style,
            )
        )

        comparison_table_data = [
            [
                comparison["career_one"],
                "Common Skills",
                comparison["career_two"],
            ]
        ]

        max_length = max(
            len(comparison["skills_one"]),
            len(comparison["skills_two"]),
            len(comparison["common"]),
        )

        for index in range(max_length):

            left = (
                comparison["skills_one"][index]
                if index < len(
                    comparison["skills_one"]
                )
                else ""
            )

            middle = (
                comparison["common"][index]
                if index < len(
                    comparison["common"]
                )
                else ""
            )

            right = (
                comparison["skills_two"][index]
                if index < len(
                    comparison["skills_two"]
                )
                else ""
            )

            comparison_table_data.append(
                [
                    left,
                    middle,
                    right,
                ]
            )

        comparison_table = Table(
            comparison_table_data,
            colWidths=[170, 150, 170],
        )

        comparison_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1e3a8a"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                ]
            )
        )

        story.append(
            comparison_table
        )

    # --------------------------------------------------------
    # Milestone 4 Status
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "Milestone 4 Finalization Status",
            heading_style,
        )
    )

    status_lines = [
        "Packaging: CareerCast package structure prepared.",
        "Testing: Integration and regression testing structure prepared.",
        "Streamlit UI: Cohort analytics and career comparison implemented.",
        "PDF Export: Report generation implemented.",
        "Documentation: API, dataset and model documentation prepared.",
        "Release: Project prepared for final packaging and public release.",
    ]

    for line in status_lines:

        story.append(
            Paragraph(
                "• " + line,
                body_style,
            )
        )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:30px;
            font-weight:800;
            margin-bottom:5px;
        ">
            CareerCast
        </div>

        <div style="
            color:#94a3b8;
            margin-bottom:25px;
        ">
            AI-Powered Career Intelligence Platform
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Milestone 4")

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Cohort Analytics",
            "Career Comparison",
            "PDF Export",
            "Finalization",
        ],
    )

    st.markdown("---")

    st.markdown(
        """
        <div class="small-text">
        Milestone 4 focuses on packaging, testing,
        analytics, comparison views, documentation,
        PDF export and final release preparation.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# LOAD DATA
# ============================================================

df = get_postings()

model_metrics = load_model_metrics()

cohort = build_cohort_analytics(df)

best_model = get_best_model(
    model_metrics
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            CareerCast — Milestone 4
        </div>

        <div class="hero-subtitle">
            Packaging, Testing & Finalization
        </div>

        <p style="
            margin-top:15px;
            color:#cbd5e1 !important;
        ">
            Final-stage project interface for cohort analytics,
            career comparison, PDF reporting, testing readiness,
            documentation and release preparation.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">Milestone 4 Overview</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        <p>
        Milestone 4 completes the CareerCast project by
        transforming the existing machine-learning system
        into a structured, tested and release-ready application.
        </p>

        <p>
        The milestone covers reusable Python packaging,
        API and CLI documentation, integration and regression
        testing, Streamlit analytics, career comparison,
        PDF export and final public-release documentation.
        </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Job Records
                </div>
                <div class="metric-value">
                    {cohort["total_jobs"]:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Career Roles
                </div>
                <div class="metric-value">
                    {cohort["unique_roles"]:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Companies
                </div>
                <div class="metric-value">
                    {cohort["unique_companies"]:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Best Model
                </div>
                <div class="metric-value"
                     style="font-size:22px;">
                    {best_model}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    # --------------------------------------------------------
    # Model Performance
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Model Performance</div>',
        unsafe_allow_html=True,
    )

    model_rows = []

    for key, value in model_metrics.items():

        name = {
            "logistic_regression":
                "Logistic Regression",
            "random_forest":
                "Random Forest",
            "xgboost":
                "XGBoost",
        }.get(
            key,
            key,
        )

        model_rows.append(
            {
                "Model": name,
                "Accuracy": round(
                    value,
                    2,
                ),
            }
        )

    if model_rows:

        model_df = pd.DataFrame(
            model_rows
        )

        st.dataframe(
            model_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "Model metrics are not available."
        )

    st.markdown(
        """
        <div class="info-box">

        <strong>Milestone 4 goal:</strong>

        Package the existing CareerCast ML system,
        validate it through automated tests, enhance
        analytics and reporting, and prepare the project
        for final release.

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# COHORT ANALYTICS
# ============================================================

elif page == "Cohort Analytics":

    st.markdown(
        '<div class="section-title">Cohort Analytics</div>',
        unsafe_allow_html=True,
    )

    if df.empty:

        st.warning(
            "postings.csv was not found. "
            "Cohort analytics cannot be generated."
        )

    else:

        st.markdown(
            """
            <div class="card">

            Cohort analytics summarizes the available
            career/job dataset and provides an overview
            of career-role distribution.

            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Jobs",
                f"{cohort['total_jobs']:,}",
            )

        with col2:
            st.metric(
                "Career Roles",
                f"{cohort['unique_roles']:,}",
            )

        with col3:
            st.metric(
                "Companies",
                f"{cohort['unique_companies']:,}",
            )

        # ----------------------------------------------------
        # Career Distribution
        # ----------------------------------------------------

        st.markdown(
            "### Career Distribution"
        )

        role_data = cohort[
            "top_roles"
        ]

        if not role_data.empty:

            st.bar_chart(
                role_data.set_index(
                    "Role"
                )["Jobs"]
            )

            st.dataframe(
                role_data,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Career-role information is not available."
            )

        # ----------------------------------------------------
        # Skill Distribution
        # ----------------------------------------------------

        st.markdown(
            "### Skill Distribution"
        )

        skill_data = cohort[
            "skill_data"
        ]

        if not skill_data.empty:

            st.bar_chart(
                skill_data.set_index(
                    "Skill"
                )["Count"]
            )

            st.dataframe(
                skill_data,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "Skill distribution could not be extracted "
                "from the available dataset columns."
            )


# ============================================================
# CAREER COMPARISON
# ============================================================

elif page == "Career Comparison":

    st.markdown(
        '<div class="section-title">Career Comparison</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        Compare two career paths based on their
        representative skill profiles. The comparison
        highlights common skills and skills that are
        more specific to each career.

        </div>
        """,
        unsafe_allow_html=True,
    )

    career_options = list(
        DEFAULT_CAREER_SKILLS.keys()
    )

    col1, col2 = st.columns(2)

    with col1:

        career_one = st.selectbox(
            "Select Career 1",
            career_options,
            index=0,
        )

    with col2:

        default_index = (
            career_options.index(
                "Machine Learning Engineer"
            )
            if "Machine Learning Engineer"
            in career_options
            else 1
        )

        career_two = st.selectbox(
            "Select Career 2",
            career_options,
            index=default_index,
        )

    if st.button(
        "Compare Careers",
        type="primary",
        use_container_width=True,
    ):

        comparison = compare_careers(
            career_one,
            career_two,
        )

        st.session_state[
            "career_comparison"
        ] = comparison

    comparison = st.session_state.get(
        "career_comparison"
    )

    if comparison:

        st.markdown("### Comparison Result")

        # ----------------------------------------------------
        # Common Skills
        # ----------------------------------------------------

        common = comparison[
            "common"
        ]

        st.markdown(
            f"""
            <div class="success-box">

            <strong>Common Skills:</strong><br>

            {
                ", ".join(common)
                if common
                else "No common skills found."
            }

            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # Career-specific skills
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"### {comparison['career_one']}"
            )

            for skill in comparison[
                "unique_one"
            ]:

                st.write(
                    f"• {skill}"
                )

        with col2:

            st.markdown(
                f"### {comparison['career_two']}"
            )

            for skill in comparison[
                "unique_two"
            ]:

                st.write(
                    f"• {skill}"
                )

        # ----------------------------------------------------
        # Skill table
        # ----------------------------------------------------

        st.markdown(
            "### Complete Skill Comparison"
        )

        rows = []

        max_len = max(
            len(
                comparison["skills_one"]
            ),
            len(
                comparison["skills_two"]
            ),
        )

        for index in range(
            max_len
        ):

            left = (
                comparison["skills_one"][index]
                if index <
                len(
                    comparison["skills_one"]
                )
                else ""
            )

            right = (
                comparison["skills_two"][index]
                if index <
                len(
                    comparison["skills_two"]
                )
                else ""
            )

            rows.append(
                {
                    comparison["career_one"]:
                        left,
                    comparison["career_two"]:
                        right,
                }
            )

        if rows:

            st.dataframe(
                pd.DataFrame(rows),
                use_container_width=True,
                hide_index=True,
            )


# ============================================================
# PDF EXPORT
# ============================================================

elif page == "PDF Export":

    st.markdown(
        '<div class="section-title">PDF Report Export</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        Generate a Milestone 4 project report containing
        model performance, cohort analytics, career
        comparison and finalization status.

        </div>
        """,
        unsafe_allow_html=True,
    )

    if not REPORTLAB_AVAILABLE:

        st.error(
            "ReportLab is not installed. "
            "Install it using: pip install reportlab"
        )

    else:

        comparison = st.session_state.get(
            "career_comparison"
        )

        pdf_bytes = generate_pdf_report(
            model_metrics,
            cohort,
            comparison,
        )

        if pdf_bytes:

            st.success(
                "PDF report is ready."
            )

            st.download_button(
                label="Download CareerCast Milestone 4 PDF",
                data=pdf_bytes,
                file_name=(
                    "CareerCast_Milestone4_Report.pdf"
                ),
                mime="application/pdf",
                use_container_width=True,
            )

        else:

            st.error(
                "Unable to generate the PDF report."
            )


# ============================================================
# FINALIZATION
# ============================================================

elif page == "Finalization":

    st.markdown(
        '<div class="section-title">Finalization & Release Readiness</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">

        Milestone 4 prepares CareerCast for final
        submission and public release.

        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Packaging
    # --------------------------------------------------------

    st.markdown(
        "### Packaging"
    )

    packaging_items = {

        "Python package directory":
            BASE_DIR / "careercast",

        "pyproject.toml":
            BASE_DIR / "pyproject.toml",

        "CLI module":
            BASE_DIR / "careercast" / "cli.py",

    }

    for name, path in packaging_items.items():

        if path.exists():

            st.success(
                f"{name}: Available"
            )

        else:

            st.warning(
                f"{name}: Pending"
            )

    # --------------------------------------------------------
    # Testing
    # --------------------------------------------------------

    st.markdown(
        "### Testing"
    )

    tests_dir = BASE_DIR / "tests"

    if tests_dir.exists():

        test_files = list(
            tests_dir.glob(
                "test_*.py"
            )
        )

        if test_files:

            st.success(
                f"Testing structure available — "
                f"{len(test_files)} test file(s)"
            )

        else:

            st.warning(
                "Tests folder exists but test files "
                "have not been created yet."
            )

    else:

        st.warning(
            "Tests folder has not been created yet."
        )

    # --------------------------------------------------------
    # Documentation
    # --------------------------------------------------------

    st.markdown(
        "### Documentation"
    )

    documentation_items = {

        "README":
            BASE_DIR / "README.md",

        "API Reference":
            BASE_DIR / "docs" / "api_reference.md",

        "Dataset Card":
            BASE_DIR / "docs" / "dataset_card.md",

        "Model Card":
            BASE_DIR / "docs" / "model_card.md",

        "License":
            BASE_DIR / "LICENSE",

    }

    documentation_count = 0

    for name, path in documentation_items.items():

        if path.exists():

            documentation_count += 1

            st.success(
                f"{name}: Available"
            )

        else:

            st.warning(
                f"{name}: Pending"
            )

    # --------------------------------------------------------
    # Final Release Status
    # --------------------------------------------------------

    st.markdown(
        "### Release Status"
    )

    total_documentation = len(
        documentation_items
    )

    documentation_percentage = (
        documentation_count
        / total_documentation
        * 100
        if total_documentation
        else 0
    )

    st.progress(
        int(
            documentation_percentage
        )
    )

    if documentation_percentage == 100:

        st.markdown(
            """
            <div class="success-box">

            <strong>
            CareerCast is documentation-ready for release.
            </strong>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            f"""
            <div class="warning-box">

            Documentation completion:
            <strong>
            {documentation_percentage:.0f}%
            </strong>

            Complete the remaining documentation
            before final release.

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        CareerCast — AI-Powered Career Intelligence Platform<br>

        Milestone 4: Packaging, Testing & Finalization

    </div>
    """,
    unsafe_allow_html=True,
)