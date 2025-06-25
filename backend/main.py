from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

from backend.candidate_comparison_tool.router import (
    router as candidate_comparison_router,
)
from backend.exceptions import APIException
from backend.job_descriptions.router import router as job_descriptions_router

router = APIRouter()
router.include_router(job_descriptions_router)
router.include_router(candidate_comparison_router)

app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation, resume scoring, and candidate comparisons.",
)


@app.exception_handler(APIException)
async def api_exception_handler(exc: APIException) -> JSONResponse:
    """Handle custom API exceptions with structured error responses."""
    logger.error("API Exception: {}", str(exc))
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions with generic error responses."""
    logger.error("Unexpected error: {}", str(exc))
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"},
    )


app.include_router(router, prefix="/api")
