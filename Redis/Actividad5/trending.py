#Este script sirve para recuperar los tweets vía streaming. 
#Se ejecutó este script por al menos 36 horas

#Importamos las bibliotecas necesarias
import redis
import tweepy

#Cremos una variable para manejar la conexión con Redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    #Para cada tweet recuperado, guardamos la fecha, nombre de usuario, conteo de retweets, idioma y contenido
    def on_status(self, status):
        redis.hset("twiterA5_user:" + str(status.id_str), "date", str(status.created_at))
        redis.hset("twiterA5_user:" + str(status.id_str), "username", str(status.user.screen_name))
        redis.hset("twiterA5_user:" + str(status.id_str), "rtcount", str(status.retweet_count))
        redis.hset("twiterA5_user:" + str(status.id_str), "language", str(status.lang))
        redis.hset("twiterA5_user:" + str(status.id_str), "content", status.text)
        
        #Imprimimos los tweets para verificar que el stream sigue activo
        print(status.text)

#Datos de acceso a la api. Reemplazar con los propios apenas den autorización
consumer_key = 'y1i3Hhy3GUMOx9jvulw4Y8B1z'
consumer_secret = 'GG5DsFKTNPKz8PabBDY7a7sbm9gjVlYJqx3y3ifBAGpS5MGEL0'
access_token = '240873982-qDYkFUqP8WSjD4M0LtBRn9w0ixPMFmvWcuj3lBlg'
access_token_secret = 'ahVTnCMzhaCBZNyWzRd4agB0eiWB23O92cY1ft6ba6BQy'

#Se realiza la validación con la api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Autenticación a la api
api = tweepy.API(auth)

#Iniciamos un nuevo stream de tweets
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#Establecemos que los tweets que queremos recibir sean los que tengan el tema "Viva México"
myStream.filter(track=['Viva México'])