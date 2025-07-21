from typing import List
# Adjust the import path as needed
from app.database.supabase_client import supabase


def get_questions_by_similarity_range(query_embedding: List[float], page: int
                                      = 0, limit: int = 5):
    vector_str = "[" + ",".join(map(str, query_embedding)) + "]"
    query = f"""
        SELECT
            id,
            title,
            url,
            content,
            original_content,
            paid_only,
            difficulty,
            topictags,
            LEAST(
                GREATEST(
                    ROUND(
                        ((1 - (embedding <=> '{vector_str}')) * 100)::numeric,
                        2
                    ),
                    0
                ),
                100
            ) AS match_percentage
        FROM problems_bge
        ORDER BY embedding <=> '{vector_str}'
        OFFSET {page * limit}
        LIMIT {limit}
    """
    result = supabase.rpc('exec_sql', {"sql": query}).execute()
    if result.data:
        return result.data
    else:
        raise Exception(f"Query failed: {result}")
