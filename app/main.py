from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.config import settings
from app.services.openai_client import openai_client
from app.utils.logger import logger
from app.db import get_db
from app.services.similarity import similarity_service  # Import similarity service

from pathlib import Path
import os

# Define base directories using pathlib for better path management
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"  # Directory for static files
TEMPLATES_DIR = BASE_DIR / "templates"  # Directory for HTML templates
LOGS_DIR = BASE_DIR / "logs"  # Directory for log files

# Ensure the logs directory exists
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configure Loguru to write logs to the logs directory
logger.add(
    LOGS_DIR / "app.log", rotation="1 MB", retention="10 days", compression="zip"
)

# Initialize FastAPI app
app = FastAPI()

# Mount static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Initialize Jinja2 templates for rendering HTML files
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Load the expected token from environment variables
EXPECTED_TOKEN = os.getenv("API_TOKEN")


def get_token(request: Request):
    """
    Dependency function to verify the token provided in request headers.
    """
    token = request.headers.get("Authorization")
    if not token or token != f"Bearer {EXPECTED_TOKEN}":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# Route to serve favicon.ico for browsers
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Route to serve favicon.ico for browsers
    """
    return RedirectResponse(url="/static/favicon.ico")


# Root endpoint to serve the index.html template
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the main page of the application.
    """
    logger.info("Rendering the main form page.")
    current_year = datetime.now().year  # Pass current year to the template
    return templates.TemplateResponse(
        "index.html", {"request": request, "current_year": current_year}
    )


# POST endpoint to handle user questions
@app.post("/ask-question", response_class=JSONResponse)
async def ask_question(
    request: Request,
    token: bool = Depends(get_token),
    db: AsyncSession = Depends(get_db),
):
    """
    Process user questions, perform similarity search, and respond accordingly.
    Requires a valid authentication token.
    """
    try:
        data = await request.json()
    except Exception as e:
        logger.error(f"Invalid JSON payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON payload.")

    user_question = data.get("user_question", "").strip()

    if not user_question:
        logger.error("No question provided.")
        raise HTTPException(status_code=400, detail="No question provided.")

    logger.info(f"Received question: {user_question}")

    # Find the most similar question from the FAQ
    try:
        faq_entry, similarity_score = await similarity_service.find_most_similar(
            user_question, db
        )

        logger.info(f"Similarity score: {similarity_score}")
    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        raise HTTPException(
            status_code=500, detail="Internal Server Error during similarity search."
        )

    # Check similarity and decide response source
    if faq_entry is None or similarity_score < settings.SIMILARITY_THRESHOLD:
        # If no similar question found or similarity below threshold, forward to OpenAI API
        try:
            answer = openai_client.get_answer(user_question)
            response = {"source": "OpenAI", "matched_question": "N/A", "answer": answer}
            logger.info("Answer sourced from OpenAI API.")
        except Exception as e:
            logger.error(f"Error fetching answer from OpenAI: {e}")
            raise HTTPException(
                status_code=500,
                detail="Internal Server Error fetching answer from OpenAI.",
            )
    else:
        # Use the local FAQ answer
        response = {
            "source": "Local FAQ",
            "matched_question": faq_entry["question"],
            "answer": faq_entry["answer"],
        }
        logger.info("Answer sourced from local FAQ database.")

    return JSONResponse(response)


# Custom handler for 404 errors (page not found)
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException) -> HTMLResponse:
    """
    Handle 404 errors and display a custom error page.
    """
    logger.warning(f"404 error encountered: {request.url}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_code": 404,
            "error_message": "Page Not Found",
            "error_detail": "The requested page does not exist.",
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


# Custom handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions and display a custom error page.
    """
    logger.warning(
        f"HTTP error encountered: {exc.detail} (Status Code: {exc.status_code})"
    )
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_code": exc.status_code,
            "error_message": exc.detail,
            "error_detail": exc.detail,
        },
        status_code=exc.status_code,
    )


# Custom handler for all other exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handle general exceptions and display a custom error page.
    """
    logger.error(f"Unhandled exception: {exc}")
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "error_code": 500,
            "error_message": "Internal Server Error",
            "error_detail": "An unexpected error occurred.",
        },
        status_code=500,
    )
