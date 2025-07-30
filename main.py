import requests
import random
from apis import reddit_post
from apis import waifu_datos
from database import agregar

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
    contenido = bot.buscar_contenido()
    
    if contenido:
        print(f">> Bot: [{bot.tema}] encontro contenido")
        post = bot.publicar(contenido).json()
        
        if post and 'id' in post:
            print(f">> Bot: [{bot.tema}] publico contenido")
            
            if [x for x in ['(oc)','my','by me','mine','[oc]','i made','i did','i make'] if x in contenido.get('title').lower()]: # Honor a quien honor merece
                print(f">> Bot: [{bot.tema}] comento ")
                bot.comentar(post['id'],f"Credits: {contenido.get('author')}")
            else:
                print(f">> Bot: [{bot.tema}] comento ")
                bot.comentar(post['id'],f"Suggested by: {contenido.get('author')}")
            
            agregar(contenido.get('url'),'set_redditbot') # Una mierda que te digo
            print(f">> Bot: [{bot.tema}] registró la url")
            
        else:
            print(f">> Bot: [{bot.tema}] no pudo publicar \n>> Notificando... \n>> Detalles: {post}")
            notify.Me(f">> Bot: [{bot.tema}] no pudo publicar \n>> Notificando... \n>> Detalles: {post}")
    else:
        print(f">> Bot no pudo encontrar contenido \n>> Notificando... \n>> Detalles: {contenido}")
        notify.Me(f">> Bot no pudo encontrar contenido \n>> Notificando... \n>> Detalles: {contenido}")


if __name__ == "__main__":
    print("Inicio del script")
    
    """Args: page_id: str | access_token: str  | subreddits: list | tema: str"""
    bot_cut = Bot("715085511692670", TOKEN_FB1, ["wholesomememes","memes"],"Perfectly Cut Screams")
    instancia_ejecucion(bot_cut)
    
    print("Fin del script")
    