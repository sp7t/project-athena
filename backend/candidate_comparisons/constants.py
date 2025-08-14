from string import Template

CANDIDATE_COMPARISON_PROMPT = Template("""
You are an advanced Candidate Comparison Engine for an ATS.

## Instructions:
1. Return ONLY a valid JSON array (no prose). Each element MUST be exactly:
{
  "name": "Candidate 1",
  "score": {
    "Skills_Match": 30,
    "Experience_Relevance": 20,
    "Keyword_Match": 15,
    "Projects": 15,
    "Education": 10,
    "Formatting": 5,
    "Additional_Value": 5
  }
}
- All score values MUST be integers in [0, 100].
- The sum of all score components for each candidate MUST equal 100.
- Do NOT include extra keys, comments, or trailing commas.

## Job Description:
$job_description

## Resumes:
Use ONLY the attached PDF files. Score each resume independently and output
one array element per resume in the same order as the files are provided.
""")
