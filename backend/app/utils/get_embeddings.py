from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

__all__ = ['get_embedding']


def get_embedding(text: str):
    return model.encode(text).tolist()


if __name__ == "__main__":
    sample_text = "choose k things from n things such that sum of A[i] * minimum of B[i] is maximized"
    embedding = get_embedding(sample_text)
    print(f"Embedding for the sample text: {embedding}")
