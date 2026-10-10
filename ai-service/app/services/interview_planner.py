
from app.schemas.interview import (
    InterviewPlanRequest,
    InterviewBlueprint,
    InterviewSection,
)


def select_skills(skills: list[str], allowed: set[str]) -> list[str]:
    return [
        skill for skill in skills
        if skill.lower() in allowed
    ]


def create_interview_plan(
    request: InterviewPlanRequest
) -> InterviewBlueprint:

    profile = request.resume_profile
    role = request.target_role.lower()

    difficulty = (
        "hard"
        if request.experience_level in ("mid", "senior")
        else "medium"
    )

    programming = select_skills(
        profile.skills,
        {"c", "c++", "python", "java", "javascript", "typescript"}
    )

    if "frontend" in role or "front-end" in role:
        role_topics = ["HTML", "CSS", "JavaScript", "React", "Browser APIs"]
        data_topics = ["State management", "API integration"]

    elif "backend" in role or "back-end" in role:
        role_topics = ["HTTP", "REST APIs", "Node.js", "Express.js"]
        data_topics = ["SQL", "PostgreSQL", "Database design"]

    else:
        role_topics = ["Software engineering fundamentals", "API design"]
        data_topics = ["Databases", "Data modeling"]

    declared = {skill.lower() for skill in profile.skills}

    focus_skills = [
        topic for topic in role_topics + data_topics
        if topic.lower() in declared
    ]

    project_topics = [
        project.name for project in profile.projects[:2]
    ] or ["Technical project decisions"]

    sections = [
        InterviewSection(
            name="Programming Fundamentals",
            objective="Assess core programming knowledge.",
            topics=programming or ["Programming fundamentals"],
            question_count=2,
            difficulty=difficulty,
        ),
        InterviewSection(
            name="Role Fundamentals",
            objective="Assess technical knowledge required for the target role.",
            topics=role_topics,
            question_count=2,
            difficulty=difficulty,
        ),
        InterviewSection(
            name="Data and Persistence",
            objective="Assess understanding of data handling and persistence.",
            topics=data_topics,
            question_count=2,
            difficulty=difficulty,
        ),
        InterviewSection(
            name="Project Deep Dive",
            objective="Verify understanding of project design and engineering decisions.",
            topics=project_topics,
            question_count=2,
            difficulty=difficulty,
        ),
        InterviewSection(
            name="Behavioral and Collaboration",
            objective="Assess teamwork, ownership, and communication.",
            topics=["Teamwork", "Problem solving", "Ownership"],
            question_count=2,
            difficulty="easy",
        ),
    ]

    return InterviewBlueprint(
        target_role=request.target_role,
        experience_level=request.experience_level,
        overall_difficulty=difficulty,
        focus_skills=focus_skills,
        sections=sections,
        total_questions=sum(s.question_count for s in sections),
    )
