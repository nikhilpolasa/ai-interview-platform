
from pydantic import BaseModel, Field

from app.schemas.resume import ResumeProfile
from app.schemas.interview import (
    InterviewBlueprint,
    Difficulty
)


class QuestionGenerationRequest(BaseModel):
    resume_profile: ResumeProfile

    blueprint: InterviewBlueprint

    section_index: int = Field(ge=0)

    previous_questions: list[str] = Field(
        default_factory=list
    )


class GeneratedQuestion(BaseModel):
    question: str = Field(min_length=10)

    topic: str

    section_name: str

    difficulty: Difficulty
