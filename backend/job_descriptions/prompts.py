# This module contains the prompt templates for generating job descriptions.
# Main job description template
JOB_DESCRIPTION_TEMPLATE = """
Generate a detailed and professional job description for a **{job_title}** role at a U.S.-based tech company. Use a tone that is clear, structured, and appealing to experienced professionals.

---

**Guardrails:**
- Do not invent company-specific details. Assume the company is a mid-to-large U.S. tech firm.
- Reject or return a polite error if the input values (job title, custom note, or key skills) appear nonsensical or unrelated to a real job description.
- Only generate content if the job title sounds like a legitimate role (e.g., “Software Engineer,” “Data Analyst”). If it's a placeholder or fake (e.g., “asdf”, “blah”), do not proceed.
- Keep the tone professional, informative, and concise—avoid overly casual or buzzword-heavy language.
- Follow the section structure exactly as provided.
- Use bullet points for clarity, and avoid repetition.
- Do not include salary information unless explicitly specified.
- If the {custom_note} includes terms such as “undergrad student”, “opt student”, “cpt student”, or “f1 student” (not case-sensitive), include relevant notes.
- Don't include work authorization or visa sponsorship details unless explicitly requested.

---

1. **About the Job**
   - Start with a 2–3 sentence overview of the role, including the team or department context.
   - Then include this custom note: "{custom_note}"
   - Highlight key responsibilities, tools, or impact areas in 3–5 bullet points.
   - Each bullet point should be 1–2 sentences long to provide clear, descriptive context.
   - Use professional language with specifics where applicable.
   - Avoid generic phrases like "work on exciting projects" or "be part of a dynamic team." Instead, focus on tangible responsibilities and technologies used.
   - If experience level is specified, tailor the description to that level (e.g., 1 yr, 7 yr).

2. **Required Skills**
   - List 10–12 specific technical and soft skills related to **{key_focus}**.
   - Include tools, technologies, methodologies, and relevant interpersonal skills.
   - Each bullet point should explain why the skill is important or how it's applied in the role.
""".strip()  # noqa: RUF001

# Optional benefits section
JOB_BENEFITS_SECTION = """
3. **Featured Benefits**
   - Include the following benefits as bullet points:
{benefits}
""".strip()

# Final safety guardrail message
PROMPT_SUFFIX = """
Only generate a job description if the inputs are appropriate. If the input appears irrelevant, respond with:
"**Error:** The job title or provided information does not appear to be valid for generating a professional job description."
""".strip()

# OpenAI-style simple prompt (e.g., used in fallback models)
OPENAI_JOB_DESCRIPTION_PROMPT = (
    "Create a detailed and engaging job description for the following role: {title}\n"
    "Details: {details}\n"
    "Write the job description in markdown format. No backticks or code fences.\n"
    "Do not include any other text in your response. Only return the job description."
)
