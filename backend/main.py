from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger

from backend.email_generator.router import router as email_generator_router
from backend.exceptions import APIException
from backend.job_descriptions.router import router as job_descriptions_router

# Add routers to the main API router
router = APIRouter()
router.include_router(email_generator_router)
router.include_router(job_descriptions_router)

# Initialize FastAPI app
app = FastAPI(
    title="Project Athena",
    description="API endpoints for job description generation and resume evaluations.",
)


# Custom exception handler for APIException
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:  # noqa: ARG001
    """Handle custom API exceptions with structured error responses."""
    logger.error("API Exception: {}", str(exc))

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:  # noqa: ARG001
    """Handle unexpected exceptions with generic error responses."""
    logger.error("Unexpected error: {}", str(exc))

    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred"},
    )


# Register all routers with /api prefix
app.include_router(router, prefix="/api")
