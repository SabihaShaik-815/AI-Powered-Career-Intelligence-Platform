from typing import List

from pydantic import BaseModel, Field


# ============================================================
# PREDICTION REQUEST
# ============================================================

class PredictRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        description="Resume or candidate text"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of career predictions"
    )


# ============================================================
# RECOMMENDATION REQUEST
# ============================================================

class RecommendationRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        description="Resume or candidate text"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of recommendations"
    )


# ============================================================
# SKILL GAP REQUEST
# ============================================================

class SkillGapRequest(BaseModel):
    role: str = Field(
        ...,
        description="Target career role"
    )

    skills: List[str] = Field(
        ...,
        description="Candidate skills"
    )


# ============================================================
# REPORT REQUEST
# ============================================================

class ReportRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=10,
        description="Resume or candidate text"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Number of recommendations in report"
    )