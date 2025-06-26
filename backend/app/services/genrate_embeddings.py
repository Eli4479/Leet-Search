from app.utils.load_data import load_data
from app.utils.get_embeddings import get_embedding
from app.utils.save_data import save_problems


if __name__ == "__main__":
    data = load_data("data.json")
    if data is None:
        print("Error: No data loaded from data.json.")
    else:
        for problem in data:
            embedding = get_embedding(problem.get('content', ''))
            problem['embedding'] = embedding
        save_problems(data, "data_with_embeddings.json")
        print("Embeddings generated and saved successfully.")
