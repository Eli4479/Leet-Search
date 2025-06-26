from app.database.supabase_client import supabase
from typing import List


def get_questions_by_similarity_range(query_embedding: List[float], page: int = 0, limit: int = 5):
    vector_str = "[" + ",".join(map(str, query_embedding)) + "]"
    query = f"""
        SELECT id, title, content
        FROM problems
        ORDER BY embedding <-> '{vector_str}'
        OFFSET {page * limit}
        LIMIT {limit}
    """
    result = supabase.rpc('exec_sql', {"sql": query}).execute()
    if result.data:
        return result.data
    else:
        raise Exception(f"Query failed: {result}")
