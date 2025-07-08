from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any
from app.models.problem_model import Problem
from app.controllers.search_controller import handle_search

router = APIRouter()


@router.post("/search")
def search_problems(
    body: Dict[str, Any] = Body(...),
    page: int = Query(0, ge=0),
    limit: int = 5
):
    query_text = body.get("query", "").strip()
    if not query_text:
        raise HTTPException(
            status_code=400, detail="Missing or empty 'query' in request body")

    try:
        problems = handle_search(query_text, limit, page)
        return problems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
