# supabase_client.py

from dotenv import load_dotenv
import os

from supabase import create_client

load_dotenv()
# replace with your actual project URL
SUPABASE_URL = os.environ.get(
    "SUPABASE_URL", "https://your-project.supabase.co")
# use your Supabase service role key (not anon key)
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "your-service-role-key")

if not SUPABASE_URL or SUPABASE_URL == "https://your-project.supabase.co":
    raise ValueError("SUPABASE_URL environment variable is not set correctly.")
if not SUPABASE_KEY or SUPABASE_KEY == "your-service-role-key":
    raise ValueError("SUPABASE_KEY environment variable is not set correctly.")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
