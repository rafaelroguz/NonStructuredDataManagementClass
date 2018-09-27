#Este script sirve para recuperar los tweets vía streaming. 
#Se ejecutó este script los días lunes, martes y miércoles durante distintas horas y distintos tiempos

#Importamos las bibliotecas necesarias
import tweepy
import pymongo
from pymongo import MongoClient

#Creamos una conexión con el servidor
client = MongoClient("mongodb://<USER><PASSWORD>@nonstructureddatamanagementclass-shard-00-00-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-01-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-02-xa2lb.mongodb.net:27017/twitter_db?ssl=true&replicaSet=NonStructuredDataManagementClass-shard-0&authSource=admin&retryWrites=true")
#client = MongoClient()

#Nuestra base de datos se llamará "mongo_test"
db_name = "twitter_db"

#Se conecta a una base de datos especificada. Si no existe, la crea
#Creamos la base de datos "mongo_test" o nos conectamos a ella
db = client[db_name]

#Recuperamos el nombre de todas las bases de datos en el servidor
db_list = client.list_database_names()

#Revisamos si la base de datos existe
if db_name in db_list:
    print("La base de datos \"" + db_name + "\" existe!")

#Nuestra colección se llamará "tweets"
#Una colección es un grupo de documentos almacenados en MongoDB
collection_name = "tweets"

#Crea una nueva colección o recupera el contenido de una existente
#Si la colección se está creando, MongoDB no la va a crear hasta que se le inserte documentos
tweets_collection = db[collection_name]

#Recuperamos el nombre de todas las colecciones
collection_list = db.list_collection_names()

#Revisamos si la colección existe. Si la colección creada no tiene elementos, MongoDB no la va a crear hasta insertar un documento
if collection_name in collection_list:
    print("La coleccion \"" + collection_name + "\" existe!\n")

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    #Para cada tweet recuperado, guardamos la fecha, nombre de usuario, conteo de retweets, idioma y contenido
    def on_status(self, status):
        tweet = {
            "user_name": status.user.screen_name,
            "date": status.created_at,
            "language": status.lang,
            "source": status.source,
            "rt_count": status.retweet_count,
            "reply_count": status.reply_count,
            "favorite_count": status.favorite_count,
            "retweeted": status.retweeted,
            "text": status.text
        }
        
        inserted = tweets_collection.insert_one(tweet)

        #Imprimimos los tweets para verificar que el stream sigue activo
        print(status.text + "\n")

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

#Establecemos que los tweets que queremos recibir
myStream.filter(track=['FelizLunes', 'FelizMartes', 'FelizMiercoles', 'FelizJueves'])