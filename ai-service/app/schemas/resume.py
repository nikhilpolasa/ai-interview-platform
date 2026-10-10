from pydantic import BaseModel, Field


class Education(BaseModel):
    institution: str = Field(
        description="Exact educational institution stated in the resume."
    )

    degree: str | None = Field(
        description="Degree or qualification exactly as supported by the resume."
    )

    field_of_study: str | None = Field(
        description="Field, major, specialization, or academic stream if explicitly stated."
    )

    start_date: str | None = Field(
        description="Education start date exactly as stated."
    )

    end_date: str | None = Field(
        description="Education end date or Present if stated."
    )

    grade: str | None = Field(
        description="CGPA, GPA, percentage, grade, or academic score exactly as stated."
    )


class Experience(BaseModel):
    organization: str = Field(
        description="Exact organization or institution associated with this experience."
    )

    role: str | None = Field(
        description="Exact role or position stated in the resume."
    )

    start_date: str | None = Field(
        description="Experience start date if explicitly stated."
    )

    end_date: str | None = Field(
        description="Experience end date or Present if explicitly stated."
    )

    description: str | None = Field(
        description="Concise factual description based only on the resume."
    )


class Project(BaseModel):
    name: str = Field(
        description="Exact project name."
    )

    description: str | None = Field(
        description="Factual project description supported by the resume."
    )

    technologies: list[str] = Field(
        description="Actual programming languages, frameworks, libraries, databases, platforms, or developer tools explicitly associated with the project."
    )

    concepts: list[str] = Field(
        description="Architectural patterns, AI concepts, engineering approaches, or methodologies explicitly associated with the project, such as microservices or prompt engineering."
    )


class Activity(BaseModel):
    name: str = Field(
        description="Exact activity or volunteer role name."
    )

    organization: str | None = Field(
        description="Organization associated with the activity if explicitly stated."
    )

    date: str | None = Field(
        description="Date or year associated with the activity if explicitly stated."
    )

    description: str | None = Field(
        description="Concise factual description of the activity."
    )


class ResumeProfile(BaseModel):
    name: str | None = Field(
        description="Candidate's full name if explicitly present."
    )

    email: str | None = Field(
        description="Candidate email address if explicitly present."
    )

    phone: str | None = Field(
        description="Candidate phone number if explicitly present."
    )

    location: str | None = Field(
        description="Candidate location only if explicitly presented as their location."
    )

    summary: str | None = Field(
        description="Resume summary only if the resume explicitly contains one. Do not generate one."
    )

    skills: list[str] = Field(
        description="Every explicitly listed technical skill, tool, language, framework, database, or relevant coursework item."
    )

    education: list[Education] = Field(
        description="Every education entry explicitly present in the resume."
    )

    experience: list[Experience] = Field(
        description="Every work, internship, or explicitly labeled professional experience entry."
    )

    projects: list[Project] = Field(
        description="Every project explicitly present in the Projects section."
    )

    achievements: list[str] = Field(
        description="Every explicitly stated achievement or award."
    )

    certifications: list[str] = Field(
        description="Every explicitly stated certification."
    )

    links: list[str] = Field(
        description="Every explicitly stated professional or project URL."
    )

    volunteer_experience: list[Activity] = Field(
        description="Every item explicitly listed under volunteer or extracurricular experience."
    )

    participation: list[str] = Field(
        description="Hackathons, competitions, events, or programs where the candidate participated without claiming an award."
    )


class ResumeAnalyzeRequest(BaseModel):
    text: str = Field(min_length=50)