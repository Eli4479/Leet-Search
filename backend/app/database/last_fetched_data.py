from app.database.supabase_client import supabase


def get_last_fetched_question():
    result = (
        supabase
        .from_("problems")
        .select("id_num")
        .order("id_num", desc=True)
        .limit(1)
        .execute()
    )
    if result.data:
        return result.data[0]
    else:
        return None
