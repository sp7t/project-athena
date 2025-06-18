def build_prompt(resume_text: str, job_description: str) -> str:
    """Build a prompt for Gemini model using resume and job description."""
    return f"""
You are an advanced Applicant Tracking System (ATS) designed to evaluate a resume against a job description (JD).

### Instructions:
1. Analyze the resume and the job description to extract key qualifications:
   - Minimum years of experience
   - Required tools/technologies
   - Domain knowledge
   - Required degrees or certifications
2. Evaluate the resume strictly against the job description requirements.
3. Score the resume using the following breakdown (total 100 points):
   - Skills Match (30)
   - Experience Relevance (20)
   - Keyword Match (15)
   - Projects (15)
   - Education (10)
   - Formatting (5)
   - Additional Value (5)

Please return your output strictly in valid JSON format exactly like this:

{{
  "Estimated Experience": "4.2 years",
  "ATS Match Score": 85,
  "Verdict": "Suitable",
  "Summary Feedback": "Strong match on technical skills and experience.",
  "Skills Match": 25,
  "Experience Relevance": 15,
  "Keyword Match": 10,
  "Projects": 12,
  "Education": 8,
  "Formatting": 4,
  "Additional Value": 3,
  "Detailed Feedback": {{
      "Skills Match": "Your full paragraph feedback for skills match.",
      "Experience Relevance": "Your full paragraph feedback for experience relevance.",
      "Keyword Match": "Your full paragraph feedback for keyword match.",
      "Projects": "Your full paragraph feedback for projects.",
      "Education": "Your full paragraph feedback for education.",
      "Formatting": "Your full paragraph feedback for formatting.",
      "Additional Value": "Your full paragraph feedback for additional value."
  }}
}}

Now score this resume:

Resume:
{resume_text}

Job Description:
{job_description}
"""
