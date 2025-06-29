from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en")


def get_embedding(text: str):
    prompt = f"Represent this sentence for search: {text}"
    return model.encode(prompt, normalize_embeddings=True).tolist()
