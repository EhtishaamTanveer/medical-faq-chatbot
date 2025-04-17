# src/main.py (updated)
import logging
import sys
import os

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.endpoints import router as api_router
from src.config import settings
from src.utils.gradio_app import create_gradio_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Medical FAQ Chatbot",
    description="A chatbot that answers medical questions based on symptoms, reports, and medications",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Return the home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Create and mount Gradio app
gradio_app = create_gradio_app()
app = gr.mount_gradio_app(app, gradio_app, path="/chat")

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run("src.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)