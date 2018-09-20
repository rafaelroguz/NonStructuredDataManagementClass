#Instrucciones:
#Si no tienes pip instalado, instálalo usando sudo apt-get install python3-pip
#Es necesario instalar la biblioteca de Redis para Python pip3 install redis
#Es recomendado instalar las herramientas de Redis sudo apt-get install redis-tools
#Si después de instalar Redis aún no puedes ejecutar el servidor, instálalo con sudo apt-get install redis-server
#Es necesario instalar la biblioteca de tweepy pip3 install tweepy
#El script se ejecuta usando Python 3 phyton3 tweeter.py

#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

import redis
import tweepy
import json

#Cremos una variable para manejar la conexión con Redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

#Datos de acceso a la api. Reemplazar con los propios apenas den autorización
consumer_key = 'y1i3Hhy3GUMOx9jvulw4Y8B1z'
consumer_secret = 'GG5DsFKTNPKz8PabBDY7a7sbm9gjVlYJqx3y3ifBAGpS5MGEL0'
access_token = '240873982-qDYkFUqP8WSjD4M0LtBRn9w0ixPMFmvWcuj3lBlg'
access_token_secret = 'ahVTnCMzhaCBZNyWzRd4agB0eiWB23O92cY1ft6ba6BQy'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Autenticación a la api
api = tweepy.API(auth)

#Recuperamos los 20 estados más recientes (tweets) del usuario autenticado o amigos
#que aparecen en el dashboard principal del usuario
public_tweets = api.home_timeline()

for tweet in public_tweets:
    #print("id: " + str(tweet.id_str))
    #print("date: " + str(tweet.created_at))
    #print("retweet count: " + str(tweet.retweet_count))
    #print("language: " + str(tweet.lang))
    #print("content: " + tweet.text + "\n")

    redis.hset("twiter_user:" + str(tweet.id_str), "date", str(tweet.created_at))
    redis.hset("twiter_user:" + str(tweet.id_str), "rtcount", str(tweet.retweet_count))
    redis.hset("twiter_user:" + str(tweet.id_str), "language", str(tweet.lang))
    redis.hset("twiter_user:" + str(tweet.id_str), "content", tweet.text)

for key in redis.keys(pattern="twiter_user:*"):
    id = key.split(b':')[1]
    
    print("id: " + id.decode("utf-8"))
    print("date: " + redis.hget(key, "date").decode("utf-8"))
    print("retweet count: " + redis.hget(key, "rtcount").decode("utf-8"))
    print("language: " + redis.hget(key, "language").decode("utf-8"))
    print("content: " + redis.hget(key, "content").decode("utf-8") + "\n")