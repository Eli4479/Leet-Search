from app.utils.get_embeddings import get_embedding
from app.database.insert_data import insert_questions


def generate_embeddings(data):
    for problem in data:
        embedding = get_embedding(problem.get('content', ''))
        problem['embedding'] = embedding
    insert_questions(data)
