from app.database.supabase_client import supabase


def get_last_fetched_question(type):
    result = (
        supabase
        .from_("problems_bge")
        .select("id_num")
        .eq("paid_only", type)
        .order("id_num", desc=True)
        .limit(1)
        .execute()
    )
    if result.data:
        return result.data[0]
    else:
        return None
