from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search_route
from app.services.scrape_problems import scrape_problems
import threading
import time
import logging

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

# Scraping thread setup
scrape_lock = threading.Lock()


def run_scraping():
    while True:
        if scrape_lock.acquire(blocking=False):
            try:
                logging.info("Starting problem scrape...")
                scrape_problems()
                logging.info("Scraping completed successfully.")
            except Exception as e:
                logging.exception("Error during scraping:")
            finally:
                scrape_lock.release()
        else:
            logging.warning(
                "Previous scraping still in progress. Skipping this run.")
        time.sleep(60*60*24*3)  # Run every 3 days


# Start the background scraping thread
threading.Thread(target=run_scraping, daemon=True).start()
