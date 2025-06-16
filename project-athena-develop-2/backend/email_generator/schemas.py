from pydantic import BaseModel  # noqa: INP001


class CandidateInfo(BaseModel):  # noqa: D101
    name: str
    email: str
    skills: list[str]
    experience: str
    title: str


class EmailRequest(BaseModel):  # noqa: D101
    candidate: CandidateInfo
    verdict: str
    rejection_reason: str | None = None
    notes: str | None = None
