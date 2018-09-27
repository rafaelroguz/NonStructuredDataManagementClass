import pymongo
from pymongo import MongoClient

#Creamos una conexión con el servidor
#client = MongoClient("mongodb://rafael:S7BNKu4WAj2z3ca6@nonstructureddatamanagementclass-shard-00-00-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-01-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-02-xa2lb.mongodb.net:27017/twitter_db?ssl=true&replicaSet=NonStructuredDataManagementClass-shard-0&authSource=admin&retryWrites=true")
client = MongoClient()

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

print("La base de datos contiene " + str(tweets_collection.count()) + " tweets!\n")

#Imprime el contenido del tweet recuperado de MongoDB
def print_tweet(tweet) :
    print("\nuser_name: " + tweet["user_name"])
    print("date: " + str(tweet["date"]))
    print("language: " + tweet["language"])
    print("source: " + tweet["source"])
    print("rt_count: " + str(tweet["rt_count"]))
    print("reply_count: " + str(tweet["reply_count"]))
    print("favorite_count: " + str(tweet["favorite_count"]))
    print("retweeted: " + str(tweet["retweeted"]))
    print("text: " + tweet["text"])

#Recupar todos los documentos de la bd y los almacena en una variable
#CUIDADO: Este proceso puede recuperar una cantidad enorme de datos
def get_all_tweets():
    return tweets_collection.find()

#Imprimimos todos los tweets de la bd
def print_all_tweets(tweets):
    for tweet in tweets:
        print_tweet(tweet)

def posting_devices():
    tweets = get_all_tweets()
    language_count = {
        "lang": "es",
        "count": 0
    }

    #for tweet in tweets:
        #if device.language in language_count:

print_all_tweets(get_all_tweets())