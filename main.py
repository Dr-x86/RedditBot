import requests
import random
from apis import reddit_post
from apis import waifu_datos
from database import agregar
import notify

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN_FB1 = os.getenv("TOKEN_FB1")


class Bot():
    def __init__(self, page_id: str, access_token: str, subreddits: list, tema: str)-> None:
        self.subs = subreddits
        self.tema = tema
        self.page_id = page_id
        self.access_token = access_token
    
    def _subir_facebook(self, url: str, data: dict = None, files: dict = None)-> None:
        """ Esta funcion se encarga de hacer el post.
        y manejar las excepciones desde aqui mismo """
        
        try:
            respuesta = requests.post(url,data=data,files=files)
            respuesta.raise_for_status()
        
        except Exception as e:
            print(f"[POSTEAR] - Error: {e}\nResponse: {respuesta.json()}")
        
        return respuesta
    
    def publicar(self, post: dict) -> dict:
        url = f"https://graph.facebook.com/v23.0/{self.page_id}/photos"
        data = {
            'caption': post.get('title'),
            'access_token': self.access_token,
            'url': post.get('url')
        }
        return self._subir_facebook(url, data)
    
    def buscar_contenido(self) -> dict:
        """Esta funcion obtiene los datos nuevos de la API"""
        return reddit_post(self.subs)
    
    def comentar(self, post_id: str, mensaje: str) -> None:
        """Se explica sola la funcion -.-"""
        
        url = f'https://graph.facebook.com/v23.0/{post_id}/comments'
        params = {
            'message': mensaje,
            'access_token': self.access_token
        }

        self._subir_facebook(url,params)
    
    def buscar_waifu(self) -> dict:
        return waifu_datos() # Esta funcion no requiere de parametros
    
    def buscar_video(self) -> set:
        return reddit_videos(self.subs)    


def instancia_ejecucion(bot: Bot) -> None:
    """ 
    No hay valores de retorno, hay un unico parametro el Bot instanciado
    
    Un flujo tipico del funcionamiento del bot 
    Desde aqui puedes acceder a:
        Datos del contenido que se publica,
        Respuesta de la API de meta,
        Notificar de posibles errores.
    """    
    try:
        contenido = bot.buscar_contenido()
    
        if not contenido:
            raise ValueError("No se encontró contenido")
    
        print(f">> Bot: [{bot.tema}] encontró contenido")
    
        post = bot.publicar(contenido).json()
        if not post or 'id' not in post:
            raise RuntimeError(f"Publicación fallida: {post}")
    
        print(f">> Bot: [{bot.tema}] publicó contenido")
    
        title_lower = contenido.get('title', '').lower()
        mensaje = (
            f"Credits: {contenido.get('author')}" if any(
                x in title_lower for x in ['(oc)', 'my', 'by me', 'mine', '[oc]', 'i made', 'i did', 'i make']
            ) else f"Suggested by: {contenido.get('author')}"
        )
    
        bot.comentar(post['id'], mensaje)
        print(f">> Bot: [{bot.tema}] comentó")
    
        agregar(contenido.get('url'), 'set_redditbot')
        print(f">> Bot: [{bot.tema}] registró la URL")
    
    except ValueError as ve:
        print(f">> Bot: [{bot.tema}] no encontró contenido: {ve}")
        notify.Me(f">> Bot no encontró contenido: {ve}")
    
    except RuntimeError as re:
        print(f">> Bot: [{bot.tema}] no pudo publicar: {re}")
        notify.Me(f">> Bot: [{bot.tema}] no pudo publicar: {re}")
    
    except Exception as e:
        print(f">> Error inesperado: {e}")
        notify.Me(f">> Error inesperado: {e}")

    


if __name__ == "__main__":
    print("Inicio del script")
    
    """Args: page_id: str | access_token: str  | subreddits: list | tema: str"""
    bot_cut = Bot("715085511692670", TOKEN_FB1, ["wholesomememes","memes","crappyoffbrands"],"Perfectly Cut Screams")
    instancia_ejecucion(bot_cut)
    
    print("Fin del script")
    