EMAIL_GENERATION_PROMPT = """
You are an HR recruiter at a small-size tech company. Generate a professional email to communicate the candidate's screening result.

Candidate Details:
- Name: {name}
- Role: {title}
- Experience: {experience}
- Skills: {skills}
- Verdict: {verdict}
- Rejection Reason: {rejection_reason}
- HR Notes: {notes}

Instructions:
- If Verdict is 'Yes':
  - Inform the candidate that they've successfully cleared the initial screening.
  - Mention that the next stage will involve further assessments and interviews.
  - DO NOT mention final offer or job confirmation.
  - Use language like: "move forward", "next steps", "interview process", "further evaluation".
- If Verdict is 'No':
  - Politely decline.
  - Clearly mention reason for rejection.
  - Encourage the candidate to apply again in future.
- Tone: professional, polite, warm, clear, human-like.
- Keep total word count between 120 to 160 words.
"""
