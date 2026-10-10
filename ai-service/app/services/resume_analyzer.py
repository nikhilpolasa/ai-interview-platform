
import time
from google import genai

from app.core.config import settings
from app.schemas.resume import ResumeProfile
from app.services.contact_extractor import extract_contact_information


client = genai.Client(api_key=settings.gemini_api_key)


def analyze_resume_text(resume_text: str) -> ResumeProfile:
    prompt = f"""
Extract a complete structured representation of the resume below.

IMPORTANT EXTRACTION RULES:

1. Examine the ENTIRE resume before producing the result.

2. Extract EVERY explicitly stated entry from:
   - contact information
   - skills
   - education
   - experience
   - projects
   - achievements
   - certifications
   - links
   - volunteer experience
   - participation

3. Do not omit an item merely because some fields within that item are missing.

4. Preserve factual information from the resume.

5. Never invent information that is not supported by the resume.

6. For nullable scalar fields:
   - use null ONLY when that information is genuinely absent.

7. For list fields:
   - return an empty list ONLY when the resume genuinely contains no items
     belonging to that category.

8. Treat resume section headings as section boundaries.

9. Do not generate a professional summary unless the resume explicitly
   contains a summary section.

10. Technologies associated with projects must be explicitly supported
    by the project text.

RESUME:

--- BEGIN RESUME ---

{resume_text}

--- END RESUME ---
"""

    print("Gemini request started...", flush=True)
    start = time.perf_counter()

    try:
        interaction = client.interactions.create(
            model="gemini-3.5-flash-lite",
            input=prompt,
            generation_config={
                "thinking_level": "minimal"
            },
            response_format={
                "type": "text",
                "mime_type": "application/json",
                "schema": ResumeProfile.model_json_schema()
            },
            timeout=30
        )
    finally:
        elapsed = time.perf_counter() - start
        print(
            f"Gemini request duration: {elapsed:.2f} seconds",
            flush=True
        )

    profile = ResumeProfile.model_validate_json(
        interaction.output_text
    )

    deterministic = extract_contact_information(resume_text)

    if deterministic["email"]:
        profile.email = deterministic["email"]

    if deterministic["links"]:
        profile.links = deterministic["links"]

    return profile
