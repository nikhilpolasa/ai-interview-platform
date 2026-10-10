
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.interview import (
    InterviewPlanRequest,
    InterviewBlueprint,
)

from app.schemas.question import (
    QuestionGenerationRequest,
    GeneratedQuestion,
)

from app.services.interview_planner import create_interview_plan
from app.services.question_generator import generate_question


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)

logger = logging.getLogger(__name__)


@router.post("/plan", response_model=InterviewBlueprint)
def generate_interview_plan(request: InterviewPlanRequest):
    return create_interview_plan(request)


@router.post("/question", response_model=GeneratedQuestion)
def generate_interview_question(
    request: QuestionGenerationRequest
):
    try:
        return generate_question(request)

    except IndexError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("Question generation failed")

        raise HTTPException(
            status_code=502,
            detail="Unable to generate interview question",
        )
