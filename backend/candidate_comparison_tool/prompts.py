def build_comparison_prompt(job_description: str, resumes: list[str]) -> str:
    """Build a prompt for Gemini to compare multiple resumes to a single job description.

    This prompt will instruct Gemini to score each resume,
    then produce a structured JSON output including a final comparison summary.
    """
    resumes_section = "\n\n".join(
        [f"Resume {i + 1}:\n{resume}" for i, resume in enumerate(resumes)]
    )

    return f"""
You are an advanced Candidate Comparison Engine for an Applicant Tracking System (ATS).

## Instructions:
1. Compare each resume **individually** against the **same job description**.
2. Extract key qualifications for each:
   - Minimum years of experience
   - Tools & technologies
   - Domain knowledge
   - Degrees/certifications
3. Score **each resume**:
   - Skills Match (30)
   - Experience Relevance (20)
   - Keyword Match (15)
   - Projects (15)
   - Education (10)
   - Formatting (5)
   - Additional Value (5)

4. After scoring **each resume**, generate a **final comparison summary**:
   - Who is the strongest fit and why.
   - Key strengths & weaknesses for each candidate.

Return your output strictly in **valid JSON** with this structure:

{{
  "candidates": [
    {{
      "name": "Resume 1",
      "ATS Match Score": 85,
      "Verdict": "Strong fit",
      "Skills Match": 25,
      "Experience Relevance": 15
    }},
    {{
      "name": "Resume 2",
      "ATS Match Score": 78
    }}
  ],
  "comparison_summary": "Who is the best fit and why."
}}

## Job Description:
{job_description}

## Resumes:
{resumes_section}
"""
