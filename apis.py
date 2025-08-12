import requests
import random
from typing import List
from database import verificar_videos, verificar

"""Una coleccion de apis, con las funciones necesarias para asegurar obtener urls nuevas"""

def reddit_post(subs: List[str], max_intentos=550) -> dict: # Regresa data nueva
    """Esta funcion recibe una lista de subreddits.
    Regresa un diccionario con datos si se encuentra algo nuevo, None si no encontró nada"""
    
    intentos = 0
    while intentos < max_intentos:
        subreddit = random.choice(subs)
        url = f"https://meme-api.com/gimme/{subreddit}"
        print(f"Subreddit elegido: {subreddit}")
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()
            struct = respuesta.json()
            if not struct:
                intentos += 1
                continue
            
            if not verificar(struct.get('url'), db='set_redditbot'): # Verifica si es nueva
                break
            
        except requests.exceptions.RequestException as e:
            print(f"[REDDIT-API] - ERROR REQUESTS: {e} \n[RESPUESTA-API]: {respuesta.json().get('message')}")
            
        except Exception as e:
            print(f"[REDDIT-API] - ERROR EXCEPCION GENERAL: {e}\n[RESPUESTA-API]: {respuesta.json().get('message')}")
        
        intentos+=1
    
    if intentos == max_intentos or not struct: # Significa que no encontró nada
        print("[API] - Reddit. Error grave, no se consiguio una url nueva de la API ... ")
        return None
        
    data = {
        'url': struct.get('url'),
        'author': struct.get('author'),
        'title': struct.get('title'),
        'text': struct.get('text')
    }
    
    return data

def reddit_videos(subs: List[str], max_intentos=550) -> set: # Regresa data nueva
    """Recibe una lista de subreddits a revisar, regresa un set de url, titulo. None si no encuentra nada"""
    
    random.shuffle(subs)  # Aleatoriza el orden
    headers = {"User-agent": "Mozilla/5.0"}

    for subreddit in subs:
        url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=100"
        print(f"Subreddit elegido: {subreddit}")
        try:
            res = requests.get(url, headers=headers, timeout=5)
            res.raise_for_status()
            posts = res.json()["data"]["children"]

        except (ConnectionError, Timeout) as e:
            print(f"[VIDEOS] - ERROR EN CONECCION: {e}")

        except ValueError:
            print("[VIDEOS] - ERROR AL DECODIFICAR JSON.")

        except Exception as e:
            print(f"[VIDEOS] - ERROR INESPERADO: {e}")

        videos = [p['data'] for p in posts if p['data'].get('is_video')]
        print("[VIDEOS] - Videos encontrados: ",len(videos))

        urls = ["https://reddit.com" + v['permalink'] for v in videos]
        usados = verificar_videos(urls)

        nuevos_videos = [v for v in videos if "https://reddit.com" + v['permalink'] not in usados]
        print("[VIDEOS] - Nuevos videos: ", len(nuevos_videos))

        if nuevos_videos:
            selected = random.choice(nuevos_videos)
            video_url = "https://reddit.com" + selected['permalink']
            title = selected['title']
            print(f"\n NUEVO VIDEO ENCONTRADO ")
            print(f"Titulo: {title}\nURL: {video_url}\n")
            return (title, video_url)
            
    print("[VIDEOS] - ERROR: NO SE ENCONTRARON VIDEOS") # Si llega hasta aqui, no se encontraron nuevos videos.
    return (None, None)