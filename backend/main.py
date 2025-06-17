import os

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from backend.candidate_comparisons.router import router as candidate_comparisons_router
from backend.exceptions import APIException
from backend.job_descriptions.router import router as job_descriptions_router
from backend.resume_evaluations.router import router as resume_evaluations_router

# Only log APIException.debug_context when explicitly enabled
LOG_API_DEBUG_CONTEXT = os.getenv("LOG_API_DEBUG_CONTEXT", "").lower() in {
    "1",
    "true",
    "yes",
}

router = APIRouter()
router.include_router(job_descriptions_router)
router.include_router(resume_evaluations_router)
router.include_router(candidate_comparisons_router)

app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation, resume scoring, and candidate comparisons.",
)


@app.exception_handler(APIException)
async def api_exception_handler(_request: Request, exc: APIException) -> JSONResponse:
    # Avoid leaking PII/debug_context via __str__
    logger.error("API Exception: {}", exc.detail)
    if LOG_API_DEBUG_CONTEXT and getattr(exc, "debug_context", None):
        logger.debug("APIException debug_context: {}", exc.debug_context)
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    # Log traceback without exposing details to clients
    logger.opt(exception=exc).error("Unexpected error")
    return JSONResponse(
        status_code=500, content={"error": "An unexpected error occurred"}
    )


app.include_router(router, prefix="/api")
