"""
CareerCast Parser Tests

Tests for:
- Skill extraction
- Education extraction
- TXT resume parsing
- Complete resume text parsing
"""

import io

from careercast.parser import (
    extract_skills,
    extract_education,
    parse_resume_text,
    extract_txt,
)


# ============================================================
# SAMPLE RESUME
# ============================================================

SAMPLE_RESUME = """
Sabiha Shaik

Software Engineer

Skills:
Python, Java, SQL, Machine Learning, Flask, Git

Education:
Bachelor of Technology in Computer Science

Experience:
Developed machine learning applications using Python.
Built web applications using Flask.
"""


# ============================================================
# TEST SKILL EXTRACTION
# ============================================================

def test_extract_skills():
    """
    Test that skills are correctly extracted
    from resume text.
    """

    skills = extract_skills(
        SAMPLE_RESUME
    )

    assert isinstance(
        skills,
        list
    )

    assert len(skills) > 0

    skills_lower = [
        str(skill).lower()
        for skill in skills
    ]

    assert "python" in skills_lower


# ============================================================
# TEST EDUCATION EXTRACTION
# ============================================================

def test_extract_education():
    """
    Test education extraction from resume text.
    """

    education = extract_education(
        SAMPLE_RESUME
    )

    assert isinstance(
        education,
        list
    )

    assert len(education) > 0


# ============================================================
# TEST RESUME TEXT PARSING
# ============================================================

def test_parse_resume_text():
    """
    Test complete resume text parsing.
    """

    result = parse_resume_text(
        SAMPLE_RESUME
    )

    assert isinstance(
        result,
        dict
    )

    assert "skills" in result

    assert "education" in result

    assert "text_length" in result

    assert isinstance(
        result["skills"],
        list
    )

    assert isinstance(
        result["education"],
        list
    )

    assert isinstance(
        result["text_length"],
        int
    )


# ============================================================
# TEST EMPTY TEXT
# ============================================================

def test_empty_resume_text():
    """
    Test parser behavior with empty input.
    """

    result = parse_resume_text(
        ""
    )

    assert isinstance(
        result,
        dict
    )


# ============================================================
# TEST TXT FILE EXTRACTION
# ============================================================

def test_extract_txt():
    """
    Test TXT file extraction using an
    in-memory file object.
    """

    content = (
        "Python Developer\n"
        "Skills: Python, SQL, Flask\n"
        "Education: Bachelor of Technology"
    )

    file_object = io.BytesIO(
        content.encode("utf-8")
    )

    file_object.name = "resume.txt"

    text = extract_txt(
        file_object
    )

    assert isinstance(
        text,
        str
    )

    assert "Python" in text

    assert "SQL" in text


# ============================================================
# TEST SKILL EXTRACTION WITH EMPTY INPUT
# ============================================================

def test_extract_skills_empty():
    """
    Test skill extraction with empty text.
    """

    skills = extract_skills(
        ""
    )

    assert isinstance(
        skills,
        list
    )


# ============================================================
# TEST EDUCATION EXTRACTION WITH EMPTY INPUT
# ============================================================

def test_extract_education_empty():
    """
    Test education extraction with empty text.
    """

    education = extract_education(
        ""
    )

    assert isinstance(
        education,
        list
    )


# ============================================================
# TEST PARSER OUTPUT STRUCTURE
# ============================================================

def test_parser_output_structure():
    """
    Verify that the parser returns the
    fields actually provided by parser.py.
    """

    result = parse_resume_text(
        SAMPLE_RESUME
    )

    expected_fields = [
        "skills",
        "education",
        "text_length"
    ]

    for field in expected_fields:

        assert field in result

    assert isinstance(
        result["skills"],
        list
    )

    assert isinstance(
        result["education"],
        list
    )

    assert isinstance(
        result["text_length"],
        int
    )

    assert result["text_length"] > 0


# ============================================================
# TEST CASE INSENSITIVITY
# ============================================================

def test_skill_extraction_case_insensitive():
    """
    Verify that skill extraction works
    regardless of capitalization.
    """

    text = """
    PYTHON
    python
    Python
    SQL
    """

    skills = extract_skills(
        text
    )

    skills_lower = [
        str(skill).lower()
        for skill in skills
    ]

    assert "python" in skills_lower

    assert "sql" in skills_lower


# ============================================================
# TEST EDUCATION KEYWORD
# ============================================================

def test_education_keyword_detection():
    """
    Verify that common education information
    is detected.
    """

    text = """
    Education:
    Bachelor of Technology in Computer Science
    """

    education = extract_education(
        text
    )

    assert len(education) > 0


# ============================================================
# TEST MODULE IMPORT
# ============================================================

def test_parser_module_import():
    """
    Verify that the CareerCast parser module
    can be imported successfully.
    """

    import careercast.parser

    assert careercast.parser is not None