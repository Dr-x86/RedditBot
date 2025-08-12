from supabase import create_client, Client
from config import SUPABASE_DB, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_DB, SUPABASE_KEY)

def verificar(url: str , db: str) -> bool:
    response = supabase.table(db).select('id').eq('url', url).execute()
    return True if response.data else False
    
def agregar(bot: dict, db: str) -> bool:
    try:
        insert_response = supabase.table(db).insert(bot).execute()
        return bool(insert_response.data)
    except Exception as e:
        print(f"Error al insertar en la tabla '{db}': {e}")
        return False


def verificar_videos(urls: list) -> set:
    used = supabase.table('set_videos').select('url').in_('url', urls).execute()
    usados = set([v['url'] for v in used.data])
    return usados