from fastapi import APIRouter, HTTPException, Query, Body
from typing import Dict, Any
from app.controllers.search_controller import handle_search

router = APIRouter()


@router.post("/search")
def search_problems(
    body: Dict[str, Any] = Body(...),
):
    query_text = body.get("query", "").strip()
    if not query_text:
        raise HTTPException(
            status_code=400, detail="Missing or empty 'query' in request body")
    try:
        problems = handle_search(query_text)
        return problems
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
