# insert_problems.py

from app.database.supabase_client import supabase
from app.utils.load_data import load_data


def insert_questions(problems):
    for prob in problems:
        # Insert into Supabase
        supabase.table("problems").insert({
            "id": prob["id"],
            "title": prob["title"],
            "url": prob["url"],
            "paid_only": prob["paidOnly"],
            "tags": prob["tags"],
            "content": prob["content"],
            "original_content": prob["original_content"],
            "embedding": prob["embedding"]
        }).execute()

    print(f"✅ Inserted {len(problems)} problems into Supabase.")


if __name__ == "__main__":
    problems = load_data("data_with_embeddings.json")
    if problems is None:
        print("No data to insert.")
    else:
        insert_questions(problems)
        print("Data insertion completed.")
