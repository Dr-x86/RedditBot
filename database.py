import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_DB = os.getenv("SUPABASE_DB")
supabase: Client = create_client(SUPABASE_DB, SUPABASE_KEY)

def verificar(url,db):
    response = supabase.table(f'{db}').select('id').eq('url', url).execute()
    return True if response.data else False
    
def agregar(url,db):
    insert_response = supabase.table(f'{db}').insert({'url': url}).execute()
    return True if insert_response.data else False    

def verificar_videos(urls: list) -> set:
    used = supabase.table('set_videos').select('url').in_('url', urls).execute()
    usados = set([v['url'] for v in used.data])
    return usados