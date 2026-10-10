
from typing import Literal
from pydantic import BaseModel, Field

from app.schemas.resume import ResumeProfile


Difficulty = Literal["easy", "medium", "hard"]
ExperienceLevel = Literal[
    "student", "intern", "junior", "mid", "senior"
]


class InterviewPlanRequest(BaseModel):
    target_role: str = Field(min_length=3)
    experience_level: ExperienceLevel
    resume_profile: ResumeProfile


class InterviewSection(BaseModel):
    name: str
    objective: str
    topics: list[str]
    question_count: int = Field(ge=1, le=10)
    difficulty: Difficulty


class InterviewBlueprint(BaseModel):
    target_role: str
    experience_level: ExperienceLevel
    overall_difficulty: Difficulty
    focus_skills: list[str]
    sections: list[InterviewSection]
    total_questions: int = Field(ge=1, le=30)
