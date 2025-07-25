from app.utils.get_embeddings import get_embedding
from app.database.find_k_nearest import get_questions_by_similarity_range
from app.utils.simplify_statement import simplify_question


def handle_search(question):
    """
    Handles the search logic by querying the database for similar problems
    based on the provided embedding.

    Args:
        embedding (List[float]): The embedding vector to search for.
        limit (int): The maximum number of results to return.
        page (int): The page number for pagination.

    Returns:
        List[Problem]: A list of Problem objects matching the search criteria.
    """
    # Get the embedding for the problem description
    simplified_text = simplify_question(str(question))
    problem_embedding = get_embedding(simplified_text)
    # Query the database for similar problems
    similar_problems = get_questions_by_similarity_range(
        query_embedding=problem_embedding
    )
    if not similar_problems:
        raise Exception("No similar problems found")
    return similar_problems
