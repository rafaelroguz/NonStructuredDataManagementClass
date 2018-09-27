#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

import pymongo
from pymongo import MongoClient
import dateutil.parser

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

print("La base de datos contiene " + str(tweets_collection.count()) + " tweets!\n")

#Recupar todos los documentos de la bd y los almacena en una variable
#CUIDADO: Este proceso puede recuperar una cantidad enorme de datos
def get_all_tweets():
    return tweets_collection.find()

#Imprime el contenido del tweet recuperado de MongoDB
def print_single_tweet(tweet) :
    print("\nuser_name: " + tweet["user_name"])
    print("date: " + str(tweet["date"]))
    print("language: " + tweet["language"])
    print("source: " + tweet["source"])
    print("rt_count: " + str(tweet["rt_count"]))
    print("reply_count: " + str(tweet["reply_count"]))
    print("favorite_count: " + str(tweet["favorite_count"]))
    print("retweeted: " + str(tweet["retweeted"]))
    print("text: " + tweet["text"])

#Imprimimos todos los tweets de un conjunto dado
def print_tweets(tweets):
    for tweet in tweets:
        print_single_tweet(tweet)

#Recupera los tweets de la db filtrándolos por nombre de usuario
def print_tweets_by_user(user_name):
    tweets = tweets_collection.find({"user_name": user_name})
    
    for tweet in tweets:
        print_single_tweet(tweet)

#Imprimimos todos los tweets que contengan en su texto la palabra clave señadala por el usuario
def print_tweets_by_keyword(keyword, tweets):
    for tweet in tweets:
        if keyword in tweet["text"]:
            print_single_tweet(tweet)

#Lista de todas las aplicaciones desde las que se realizaron los tweets con sus conteos
source_list = []

#Verifica si la aplicación ya se está contabilizando o es una nueva
def is_in_source(source):
    if len(source_list) == 0:
        return False

    for src in source_list:
        if source == src["source"]:
            return True
    
    return False

#Incrementamos el contador de tweets para una aplicación
def increment_source(source):
    idx = 0

    for src in source_list:
        if source == src["source"]:
            source_list[idx]["count"] = source_list[idx]["count"] + 1
            return True

        idx = idx + 1

    return False

#Añadimos una nueva aplicación a la lista de fuentes de tweets
def add_source(source):
    new_src = {
        "source": source,
        "count": 1
    }

    source_list.append(new_src)

#Imprime la aplicación de origen del tweet y número de tweets que se realizaron con dicha aplicación
def print_sources():
    print("\nNúmero de tweets por aplicación de origen: \n")

    for src in source_list:
        print("Aplicación: " + src["source"])
        print("Cantidad de tweets: " + str(src["count"]))

#Organiza las aplicaciones desde las que se realizaron los tweets, aumentando el contendo de tweet por aplicación o añadiendo nuevas aplicaciones al conteo
def print_tweets_by_app(tweets):
    for tweet in tweets:
        if not is_in_source(tweet["source"]):
            add_source(tweet["source"])
        else:
            increment_source(tweet["source"])

    print_sources()

#------------------------------------------------------------------------------------
#Ejecución normal del script

#Recuperamos todos los tweets
tweets = get_all_tweets()

#print_keyword_tweets("FelizLunes", tweets)
#print_keyword_tweets("FelizMartes", tweets)
#print_keyword_tweets("FelizMiercoles", tweets)

print("Bienvenido!\nSelecciona una opción:")
print("1) Listar todos los tweets")
print("2) Listar tweets por nombre de usuario")
print("3) Listar tweets por palabra clave")
print("4) Mostrar cantidad de tweets por aplicación usada")
print("5) Salir")

option = input("\nMi opcion: ")

if int(option) == 1:
    print_tweets(tweets)
    print()
elif int(option) == 2:
    user_name = input("Introduce el nombre de usuario a buscar: ")
    print_tweets_by_user(user_name)
    print()
elif int(option) == 3:
    keyword = input("Introduce una palabra clave: ")
    print_tweets_by_keyword(keyword, tweets)
    print()
elif int(option) == 4:
    print_tweets_by_app(tweets)
    print()
else:
    print("Goodbye!")