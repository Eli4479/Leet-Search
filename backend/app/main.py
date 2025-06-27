from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search_route  # import your router

app = FastAPI(title="LeetCode Vector Search API", version="1.0")

# Allow all CORS for testing; tighten for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint


@app.get("/")
def root():
    return {"message": "LeetCode Vector Search API is running 🚀"}


# Include the search router
app.include_router(search_route.router, prefix="/api", tags=["Search"])
