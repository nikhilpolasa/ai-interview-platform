from fastapi import FastAPI

from app.api.resume import router as resume_router
from app.api.interview import router as interview_router

app = FastAPI(
    title="AI Interview Service",
    version="0.1.0"
)


app.include_router(resume_router)

app.include_router(interview_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "ai-service"
    }