"""
CareerCast Skill Gap Analysis Module

This module analyzes:

- Skills available in the resume
- Required skills for a career
- Matched skills
- Missing skills
- Skill alignment percentage
- Learning recommendations
"""


# ============================================================
# ROLE REQUIRED SKILLS
# ============================================================

ROLE_REQUIRED_SKILLS = {

    "Software Engineer": [

        "python",
        "java",
        "javascript",
        "sql",
        "git",
        "html",
        "css"
    ],

    "Data Scientist": [

        "python",
        "pandas",
        "numpy",
        "machine learning",
        "statistics",
        "scikit-learn",
        "sql"
    ],

    "Machine Learning Engineer": [

        "python",
        "machine learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "numpy",
        "pandas"
    ],

    "Data Analyst": [

        "python",
        "sql",
        "excel",
        "pandas",
        "statistics",
        "data analysis",
        "power bi"
    ],

    "AI Engineer": [

        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "nlp"
    ]
}


# ============================================================
# LEARNING RESOURCES
# ============================================================

LEARNING_RESOURCES = {

    "python": {
        "resource": "Python Programming Fundamentals",
        "type": "Course",
        "duration": "6 Weeks",
        "level": "Beginner"
    },

    "java": {
        "resource": "Java Programming Fundamentals",
        "type": "Course",
        "duration": "6 Weeks",
        "level": "Beginner"
    },

    "javascript": {
        "resource": "JavaScript Fundamentals",
        "type": "Course",
        "duration": "4 Weeks",
        "level": "Beginner"
    },

    "sql": {
        "resource": "SQL for Data Analysis",
        "type": "Course",
        "duration": "4 Weeks",
        "level": "Beginner"
    },

    "git": {
        "resource": "Git and GitHub",
        "type": "Course",
        "duration": "2 Weeks",
        "level": "Beginner"
    },

    "html": {
        "resource": "HTML Fundamentals",
        "type": "Course",
        "duration": "2 Weeks",
        "level": "Beginner"
    },

    "css": {
        "resource": "CSS Fundamentals",
        "type": "Course",
        "duration": "3 Weeks",
        "level": "Beginner"
    },

    "pandas": {
        "resource": "Pandas for Data Analysis",
        "type": "Course",
        "duration": "3 Weeks",
        "level": "Intermediate"
    },

    "numpy": {
        "resource": "NumPy Fundamentals",
        "type": "Course",
        "duration": "3 Weeks",
        "level": "Intermediate"
    },

    "machine learning": {
        "resource": "Machine Learning Fundamentals",
        "type": "Course",
        "duration": "8 Weeks",
        "level": "Intermediate"
    },

    "deep learning": {
        "resource": "Deep Learning Fundamentals",
        "type": "Course",
        "duration": "8 Weeks",
        "level": "Advanced"
    },

    "tensorflow": {
        "resource": "TensorFlow Deep Learning",
        "type": "Course",
        "duration": "6 Weeks",
        "level": "Intermediate"
    },

    "pytorch": {
        "resource": "PyTorch Deep Learning",
        "type": "Course",
        "duration": "6 Weeks",
        "level": "Intermediate"
    },

    "scikit-learn": {
        "resource": "Scikit-learn Machine Learning",
        "type": "Course",
        "duration": "4 Weeks",
        "level": "Intermediate"
    },

    "statistics": {
        "resource": "Statistics for Data Science",
        "type": "Course",
        "duration": "5 Weeks",
        "level": "Beginner"
    },

    "excel": {
        "resource": "Excel for Data Analysis",
        "type": "Course",
        "duration": "3 Weeks",
        "level": "Beginner"
    },

    "data analysis": {
        "resource": "Data Analysis Fundamentals",
        "type": "Course",
        "duration": "5 Weeks",
        "level": "Beginner"
    },

    "power bi": {
        "resource": "Power BI Data Visualization",
        "type": "Course",
        "duration": "4 Weeks",
        "level": "Intermediate"
    },

    "nlp": {
        "resource": "Natural Language Processing",
        "type": "Course",
        "duration": "6 Weeks",
        "level": "Intermediate"
    }
}


# ============================================================
# GET REQUIRED SKILLS
# ============================================================

def get_required_skills(role):

    """
    Get the required skills for a career role.
    """

    return ROLE_REQUIRED_SKILLS.get(
        role,
        []
    )


# ============================================================
# NORMALIZE SKILLS
# ============================================================

def normalize_skills(skills):

    """
    Convert all skills to lowercase and
    remove duplicates.
    """

    if not skills:
        return set()

    return {

        str(skill).strip().lower()

        for skill in skills

        if str(skill).strip()
    }


# ============================================================
# CALCULATE SKILL GAP
# ============================================================

def calculate_skill_gap(
    role,
    user_skills
):

    """
    Compare user skills with required skills.
    """

    required_skills = get_required_skills(
        role
    )

    user_skills_lower = normalize_skills(
        user_skills
    )

    matched_skills = []

    missing_skills = []


    for skill in required_skills:

        if skill.lower() in user_skills_lower:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    # ========================================================
    # SKILL ALIGNMENT
    # ========================================================

    if required_skills:

        alignment = (

            len(matched_skills)
            /
            len(required_skills)

        ) * 100

    else:

        alignment = 0


    return {

        "role":
            role,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "total_required":
            len(required_skills),

        "total_matched":
            len(matched_skills),

        "total_missing":
            len(missing_skills),

        "alignment":
            round(alignment, 2)
    }


# ============================================================
# GET LEARNING RESOURCE
# ============================================================

def get_learning_resource(skill):

    """
    Get learning resources for a missing skill.
    """

    skill_lower = skill.lower()


    return LEARNING_RESOURCES.get(

        skill_lower,

        {

            "resource":
                f"Learn {skill.title()}",

            "type":
                "Course",

            "duration":
                "4 Weeks",

            "level":
                "Intermediate"
        }
    )


# ============================================================
# BUILD LEARNING PATH
# ============================================================

def build_learning_path(
    missing_skills
):

    """
    Create a learning path for missing skills.
    """

    learning_path = []


    for index, skill in enumerate(
        missing_skills,
        start=1
    ):

        resource = get_learning_resource(
            skill
        )


        learning_path.append({

            "step":
                index,

            "skill":
                skill.title(),

            "resource":
                resource["resource"],

            "type":
                resource["type"],

            "duration":
                resource["duration"],

            "level":
                resource["level"]
        })


    return learning_path


# ============================================================
# COMPLETE SKILL GAP ANALYSIS
# ============================================================

def analyze_skill_gap(
    role,
    user_skills
):

    """
    Perform complete skill gap analysis.
    """

    skill_gap = calculate_skill_gap(

        role,

        user_skills
    )


    learning_path = build_learning_path(

        skill_gap["missing_skills"]
    )


    result = {

        "success":
            True,

        "role":
            skill_gap["role"],

        "required_skills":
            skill_gap["required_skills"],

        "matched_skills":
            skill_gap["matched_skills"],

        "missing_skills":
            skill_gap["missing_skills"],

        "total_required":
            skill_gap["total_required"],

        "total_matched":
            skill_gap["total_matched"],

        "total_missing":
            skill_gap["total_missing"],

        "alignment":
            skill_gap["alignment"],

        "learning_path":
            learning_path
    }


    return result


# ============================================================
# SKILL GAP SUMMARY
# ============================================================

def get_skill_gap_summary(
    role,
    user_skills
):

    """
    Generate a simple summary of the skill gap.
    """

    result = analyze_skill_gap(

        role,

        user_skills
    )


    alignment = result["alignment"]


    if alignment >= 80:

        status = "Excellent Skill Match"

    elif alignment >= 60:

        status = "Good Skill Match"

    elif alignment >= 40:

        status = "Moderate Skill Match"

    else:

        status = "Needs Improvement"


    return {

        "role":
            role,

        "status":
            status,

        "alignment":
            alignment,

        "matched":
            result["total_matched"],

        "missing":
            result["total_missing"]
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    sample_skills = [

        "python",

        "java",

        "html",

        "css",

        "sql"
    ]


    result = analyze_skill_gap(

        "Software Engineer",

        sample_skills
    )


    print("\n========== SKILL GAP ANALYSIS ==========\n")

    print(
        "Career Role:",
        result["role"]
    )

    print(
        "Required Skills:",
        result["required_skills"]
    )

    print(
        "Matched Skills:",
        result["matched_skills"]
    )

    print(
        "Missing Skills:",
        result["missing_skills"]
    )

    print(
        "Skill Alignment:",
        result["alignment"],
        "%"
    )

    print("\nLearning Path:\n")

    for item in result["learning_path"]:

        print(

            f"{item['step']}. "

            f"{item['skill']} → "

            f"{item['resource']}"
        )