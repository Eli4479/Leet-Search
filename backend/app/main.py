import logging

from app.routes import search_route
from app.scripts.populate_db import populate_db
from app.services.scrape_problems import scrape_problems
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="LeetCode Vector Search API", version="1.0")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    # Replace with frontend URLs in production
    allow_origins=["https://leet-search-sepia.vercel.app/search",
                   "https://leet-search-sepia.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint


@app.get("/")
def root():
    return {"message": "LeetCode Vector Search API is running 🚀"}


# Register routes
app.include_router(search_route.router, prefix="/api", tags=["Search"])

# run initial population of the database only once then only run scraping
# populate_db()
