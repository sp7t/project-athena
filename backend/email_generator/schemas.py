from pydantic import BaseModel


class CandidateInfo(BaseModel):
    """Schema representing candidate information."""

    name: str
    email: str
    skills: list[str]
    experience: str
    title: str


class EmailRequest(BaseModel):
    """Schema representing an email request with candidate and decision details."""

    candidate: CandidateInfo
    verdict: str
    rejection_reason: str | None = None
    notes: str | None = None
