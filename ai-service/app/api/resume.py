import logging

import pymupdf
from fastapi import APIRouter, HTTPException, UploadFile

from app.schemas.resume import ResumeAnalyzeRequest, ResumeProfile
from app.services.resume_analyzer import analyze_resume_text


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

logger = logging.getLogger(__name__)


@router.post("/extract")
async def extract_resume(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    contents = await file.read()

    try:
        document = pymupdf.open(stream=contents)

        text = ""

        for page in document:
            text += page.get_text() + "\n"

        page_count = len(document)
        document.close()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the PDF"
        )

    return {
        "filename": file.filename,
        "pages": page_count,
        "characters": len(text),
        "text": text.strip()
    }


@router.post(
    "/analyze",
    response_model=ResumeProfile
)
def analyze_resume(request: ResumeAnalyzeRequest):
    try:
        return analyze_resume_text(request.text)

    except Exception:
        logger.exception("Resume analysis failed")

        raise HTTPException(
            status_code=502,
            detail="Unable to analyze resume"
        )