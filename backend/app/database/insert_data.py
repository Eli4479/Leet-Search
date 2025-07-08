# insert_problems.py
import logging
from app.database.supabase_client import supabase


logging.basicConfig(level=logging.INFO)


def insert_questions(problems):
    for prob in problems:
        # Insert into Supabase
        supabase.table("problems_bge").upsert({
            "id": prob["id"],
            "title": prob["title"],
            "url": prob["url"],
            "paid_only": prob["paidOnly"],
            "content": prob.get("content", ""),
            "original_content": prob.get("original_content", ""),
            "embedding": prob.get("embedding", []),
            "id_num": int(prob["id"])
        }, on_conflict=["id"]).execute()
    logging.info(f"Inserted {len(problems)} problems into Supabase.")
