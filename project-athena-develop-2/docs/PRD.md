# Project Athena – PRD (Product Requirements Document)

| **Field**    | **Value**                            |
| ------------ | ------------------------------------ |
| **Product:** | AI-Powered Internal Hiring Assistant |
| **Version:** | 1.0                                  |
| **Date:**    | May 4, 2025                          |

> **Codename:** Project Athena  
> **One-liner:** An AI-powered internal tool that enhances hiring workflows through intelligent resume and candidate evaluation capabilities.

---

## Background & Motivation

The current recruiting process is largely manual, relying on referrals or reviewing resumes submitted through job boards like LinkedIn. As the company grows, this process lacks the structure, consistency, and scalability needed to support efficient hiring at scale. While tools like ChatGPT can offer ad-hoc assistance, they are not reusable, trackable, or integrated into any consistent workflow.

**Project Athena** addresses these gaps by offering an intelligent, internally owned hiring assistant that supports key parts of the hiring workflow. From job description creation to resume analysis and candidate ranking, the tool augments decision-making for recruiters and hiring managers.

---

## Minimum Viable Product (MVP)

Project Athena will focus on delivering three foundational features that streamline the resume evaluation and job matching process.

### 1. Job Description Generator

**Overview:**  
Generates customized, role-specific job descriptions based on minimal inputs, leveraging LLM capabilities.

**Functionality:**

- Input fields: job title and contextual role details (e.g., department, seniority, required skills, location preferences, tone).
- Outputs a formatted, editable job description with standardized sections (e.g., responsibilities, qualifications).
- Includes options to export or copy for internal or external use.

**Benefits:**

- Accelerates job description drafting.
- Promotes consistency across postings.
- Reduces workload for hiring managers.

---

### 2. Resume Evaluation & Ranking

**Overview:**  
Analyzes one or many resumes against a job description, providing a detailed match analysis for each and automatically ranking candidates by score.

**Functionality:**

- Inputs: one job description plus one or more resumes.
- Uses AI to evaluate each resume on factors such as skills, experience, and domain relevance.
- Generates for every resume:
  - A match score.
  - A concise explanatory analysis of contributing factors.
- Automatically sorts all evaluated resumes by their match scores to produce a ranked shortlist.

**Benefits:**

- Delivers in-depth fit insights for each candidate.
- Enables quick prioritization of top candidates by ranking.
- Reduces manual review time and increases objectivity with explainable scores.

---

## Technical Stack & Architecture

**Frontend:**

- **Streamlit** for building the interactive UI (file uploads, result display).

**Backend/API:**

- **FastAPI** for RESTful endpoints (job/resume ingestion, matching services).
- **Pydantic** for data validation and schema definitions.

**AI/ML & Data Processing:**

- **Google GenAI** for LLM access.

**Storage & Database:**

- **Supabase** as the primary database and file storage solution for resumes, job descriptions, and match results.

---

## Stretch Goals

- Resume Q&A chatbot interface.
- Admin panel + database management.
- Exportable match reports (PDF/CSV).
- Auto-tagging and talent pool categorization.
- Personalized candidate communication: auto-draft tailored emails for interview invitations, rejections, or follow-ups.
- Interviewer Briefing Pack: generate tailored interview questions and candidate summaries.

## Notes

- Not intended as a full ATS replacement; complements internal workflows.
- Designed for use by hiring managers, recruiters, and technical leads.
- Lightweight, low-cost, and fully owned in-house.
