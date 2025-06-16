from fastapi import FastAPI  # noqa: I001, INP001
from backend.email_generator.router import router as email_generator_router

app = FastAPI(
    title="Email Generator Service",
    description="API endpoints for generating candidate emails.",
    version="1.0.0"
)

app.include_router(email_generator_router, prefix="/api/email-generator")
