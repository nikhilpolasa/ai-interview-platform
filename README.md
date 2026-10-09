# AI Interview Platform

**Resume-aware interviews. Adaptive questioning. Multimodal feedback.**

AI Interview Platform is an in-development **multimodal mock interview and interview-preparation system**. Its goal is to combine resume intelligence, role-aware technical interviewing, speech analytics, and computer-vision-derived behavioral signals into a single, actionable practice experience.

Instead of generating a fixed list of generic questions, the planned interview engine will use a candidate's resume, target role, and responses to plan topic coverage, ask contextual follow-ups, and explain areas for improvement.

> **Project status — active development:** The **PDF resume ingestion and structured resume-analysis pipeline** is working locally, alongside the initial **Node.js/Express + PostgreSQL/Prisma** backend foundation. **Adaptive interviewing, voice, computer vision, frontend, and deployment are not yet implemented.**

## What we're building

The platform has five connected goals:

| Capability | Purpose | Status |
| --- | --- | --- |
| **Resume intelligence** | Extract and structure skills, education, experience, projects, and other resume facts | **Implemented (initial version)** |
| **Adaptive interview engine** | Plan role-relevant interview sections, generate questions, evaluate answers, and select follow-ups | **Planned** |
| **Speech & communication analytics** | Analyze transcribed responses, speaking rate, pauses, filler words, and response latency | **Planned** |
| **Computer vision analytics** | Measure observable webcam-based signals such as estimated gaze direction, head pose, blinking, face presence, and posture/movement | **Planned** |
| **Interview experience & feedback** | Provide a browser interview room, history, and a useful post-interview improvement report | **Planned** |

The intended primary use case is **interview practice and self-improvement for students and job candidates**. Vision and audio signals are intended to describe *observable behavior*, not diagnose nervousness, confidence, honesty, or employability.

## How it works today

The working resume-intelligence pipeline is:

```mermaid
flowchart TD
    PDF[Resume PDF] --> Upload[FastAPI file-upload endpoint]
    Upload --> Extract[PyMuPDF text extraction]
    Extract --> Text[Resume text]
    Text --> Gemini[Google Gemini semantic extraction]
    Text --> Rules[Regex contact extraction]
    Gemini --> Schema[Schema-constrained JSON]
    Schema --> Validate[Pydantic validation]
    Rules --> Merge[Merge validated fields]
    Validate --> Merge
    Merge --> Profile[Structured candidate profile]
```

The profile can represent contact details, skills, education and grades, professional experience, projects, project technologies and engineering concepts, achievements, certifications, volunteer activities, and event participation.

**Important:** Resume extraction and resume analysis are currently exposed as **two separate API requests**. A combined end-to-end upload/process endpoint is not implemented yet. Extracted profiles are not yet persisted through the Node.js backend.

## Architecture

### Current implementation

The repository contains two independently runnable backend applications. **They are not yet wired together**; the FastAPI resume pipeline can be tested directly via its API documentation.

```mermaid
flowchart LR
    User[Developer / API client] --> AI[Python / FastAPI AI service]
    AI --> Parse[PyMuPDF + regex]
    AI --> LLM[Google Gemini]
    AI --> Pydantic[Pydantic schemas]

    Node[Node.js / Express platform backend] --> Prisma[Prisma ORM]
    Prisma --> DB[(PostgreSQL)]
```

- **Platform backend — Node.js, Express, TypeScript:** Initial application server, Prisma integration, relational data model, and database-backed health check.
- **AI service — Python, FastAPI:** PDF extraction, prompt-driven resume analysis, structured JSON output, deterministic contact extraction, and validation.
- **PostgreSQL:** Initial persistent schema for users, interviews, and questions.
- **Frontend:** Directory reserved for future development; no functional UI has been built yet.

### Target architecture (planned)

```mermaid
flowchart TB
    UI[Web interview room\nResume upload / mic / camera] --> API[Node.js / Express platform API]
    API --> DB[(PostgreSQL + Prisma)]
    API <-->|Internal APIs - planned| AI[FastAPI AI service]
    AI --> Gemini[Gemini / interview intelligence]
    AI --> Resume[Resume understanding]
    AI --> Speech[Speech processing / analytics]
    AI --> Vision[OpenCV + MediaPipe\ncomputer vision]
    API --> Report[Interview history and reports]
    UI -.->|Real-time media channel - design pending| Vision
    UI -.->|Audio channel - design pending| Speech
```

The diagram is a **design target, not a claim of implemented service-to-service APIs, real-time streaming, or independent scaling**. The final media transport and the split between browser-side and server-side CV processing will be chosen during implementation.

## Computer vision and multimodal analytics (planned)

Computer vision is a **core planned subsystem**, not an afterthought. The intended stack includes **OpenCV** for video/frame processing and **MediaPipe** for facial and pose landmarks.

The planned analysis includes:

- **Face presence:** whether a face is detected in sampled frames.
- **Head pose:** approximate head orientation over time.
- **Gaze direction:** a calibrated estimate of eye/gaze direction, not a definitive measure of interpersonal eye contact.
- **Blink-related metrics:** observable blink frequency or duration, when camera conditions support estimation.
- **Pose and movement:** head/upper-body landmark movement and posture changes.
- **Per-response timelines:** contextualize measurable signals alongside speech and technical-answer feedback.

Speech analytics may include transcription, speaking rate, filler words, pauses, silence duration, and response latency. These features require explicit consent, careful handling of recordings, accessibility considerations, and evaluation under varying camera/microphone conditions.

**We will not equate blink rate, gaze, posture, or other visual cues with a candidate's confidence, nervousness, truthfulness, or competence.** Such claims are not reliable enough for automated judgments. Technical-answer evaluation and observable delivery metrics will be kept conceptually separate.

## Technical stack

| Layer | Technology | Status |
| --- | --- | --- |
| Platform API | Node.js, Express 5, TypeScript | Initial foundation implemented |
| Data layer | PostgreSQL, Prisma ORM, Prisma migrations | Initial schema/migration implemented |
| AI API | Python, FastAPI, Uvicorn | Implemented |
| Resume files | FastAPI `UploadFile`, `python-multipart`, PyMuPDF | Implemented for PDFs |
| LLM integration | Google Gemini via `google-genai` | Implemented for resume analysis |
| Validation/config | Pydantic, `pydantic-settings`, environment variables | Implemented |
| Rule-based extraction | Python regular expressions | Implemented for email and professional links |
| Frontend | React/Next.js-based interview UI | Planned |
| Vision | OpenCV, MediaPipe | Planned |
| Voice | Microphone capture, transcription, speech-feature extraction | Planned |
| Real-time transport | WebSockets or an appropriate media-streaming solution | Under design |
| Deployment/testing | Containers, CI/CD, automated tests, hosting | Planned |

## Existing API endpoints

### FastAPI AI service

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Basic AI-service health check |
| `POST` | `/resume/extract` | Accept a PDF and return its extracted text, filename, page count, and character count |
| `POST` | `/resume/analyze` | Analyze resume text and return a validated structured candidate profile |

Interactive API documentation: **http://127.0.0.1:8000/docs** when the AI service is running locally.

### Node.js platform backend

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Backend health check, including a Prisma database query |

**Currently confirmed: 4 method-and-service endpoints across the 2 backends.** No interview creation, answer submission, scoring, or authentication API is implemented yet.

## Database foundation

The initial Prisma schema defines **3 models**:

```mermaid
 erDiagram
    User ||--o{ Interview : owns
    Interview ||--o{ Question : contains
```

- **`User`** — identity fields, unique email, and related interviews.
- **`Interview`** — associated user, job title, resume text, status, and related questions.
- **`Question`** — interview association, question text, and optional answer, feedback, and score fields.

The schema and initial migration exist; **the full interview persistence workflow is not yet implemented**. The models will evolve as interview state and result requirements are finalized.

## Project structure

The following illustrates the working modules and intended repository layout, omitting generated dependencies:

```text
ai-interview-platform/
├── backend/
│   ├── prisma/
│   │   ├── schema.prisma
│   │   └── migrations/
│   ├── src/
│   │   ├── index.ts
│   │   └── lib/prisma.ts
│   ├── package.json
│   └── tsconfig.json
├── ai-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/resume.py
│   │   ├── core/config.py
│   │   ├── schemas/resume.py
│   │   └── services/
│   │       ├── resume_analyzer.py
│   │       └── contact_extractor.py
│   └── .env                    # local only; do NOT commit
├── frontend/                   # planned, currently empty
└── README.md
```

## Running locally

### Prerequisites

- Node.js and npm
- Python and pip
- A running PostgreSQL database for the Node backend
- A Gemini API key for AI resume analysis

The instructions below are oriented toward **Windows PowerShell**, the environment used during development.

### 1. Run the FastAPI AI service

```powershell
cd ai-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi "uvicorn[standard]" python-multipart pymupdf pydantic-settings google-genai
```

Create `ai-service/.env`:

```dotenv
GEMINI_API_KEY=replace_with_your_own_key
```

Start the server:

```powershell
uvicorn app.main:app --reload --port 8000
```

Open **http://127.0.0.1:8000/docs** to test `/resume/extract` and `/resume/analyze` separately. The first endpoint accepts the resume PDF; the second accepts the extracted text in a JSON body with a `text` field.

### 2. Run the Node.js backend

Open a second terminal from the repository root:

```powershell
cd backend
npm install
```

Ensure `backend/.env` contains a valid local PostgreSQL connection URL, for example:

```dotenv
DATABASE_URL="postgresql://USER:PASSWORD@localhost:5432/DATABASE_NAME?schema=public"
```

Replace the placeholders with credentials for a database you created. Then:

```powershell
npx prisma generate
npx prisma migrate deploy
npm run dev
```

The Node API's listen port depends on the configuration in `backend/src/index.ts`; check that file rather than assuming it uses port 8000.

> These are local development instructions. The application has **not yet been deployed** or tested as an integrated end-to-end interview experience.

## Key engineering decisions

**Separate platform and AI responsibilities.** Node/Express provides a natural home for application data and interview lifecycle management, while Python/FastAPI supports PDF processing and the planned AI/CV ecosystem. This split is useful only if the benefits outweigh the operational cost of multiple services; integration is still in progress.

**Use structured LLM outputs.** Pydantic models supply a JSON Schema for resume extraction; returned model data is validated before the application consumes it. Structure alone does not guarantee factual accuracy, so output must also be evaluated against the source resume.

**Combine LLM and deterministic parsing.** Gemini handles semantically varied content such as projects and experience; regex handles predictable patterns such as emails and LinkedIn/GitHub URLs.

**Represent different experience types separately.** Professional experience, volunteering, awards, and participation have distinct fields. This avoids later interview questions being grounded in a misleading candidate profile.

**Measure observables, not inferred emotions.** Planned multimodal analytics will report features with context and limitations instead of unreliable confidence/nervousness scores.

## Current limitations

- Only **PDF** resumes are supported; scanned/image-only documents are not yet handled with OCR.
- File type is initially checked using the uploaded MIME type; stronger file signatures, size limits, and abuse protections are future work.
- Resume extraction quality is validated manually; no benchmark, automated test suite, or formal accuracy claim exists yet.
- Some Gemini analysis requests have exhibited **unacceptably high latency** during development. Timeout policies and model selection still need to be validated.
- The AI service and Node service have not yet been integrated.
- No functional frontend, authentication, interview engine, recording, CV inference, or deployment is available yet.

## Development roadmap

- [x] Initialize Node.js/Express/TypeScript backend
- [x] Design initial PostgreSQL/Prisma schema and migration
- [x] Create FastAPI service with health endpoint
- [x] Implement PDF resume upload and text extraction
- [x] Implement Gemini + Pydantic structured resume parsing
- [x] Add deterministic extraction for email and professional links
- [ ] Stabilize LLM latency, error handling, and automated parser tests
- [ ] Build role-aware interview blueprint/planner
- [ ] Generate resume- and role-aware technical questions
- [ ] Evaluate candidate answers with explicit rubrics
- [ ] Implement adaptive follow-ups and interview state transitions
- [ ] Connect Node.js and FastAPI; persist interview sessions
- [ ] Build the frontend interview room, dashboard, and reports
- [ ] Implement consent-based audio transcription and delivery analytics
- [ ] Implement OpenCV/MediaPipe landmark and vision-feature processing
- [ ] Add structured multimodal feedback with uncertainty/limitations
- [ ] Add authentication, privacy controls, and data-retention policies
- [ ] Add unit/integration tests, containers, CI/CD, and deployment

## Development philosophy

This project is being developed **incrementally and with technical depth**. The aim is a useful interview-preparation product whose components can be explained, tested, and defended—not a collection of technologies added solely to a tech-stack list.

**Current milestone:** structured resume intelligence. **Next milestone:** a tested, role-aware interview planner and question-generation pipeline, once the resume-analysis latency is under control.
