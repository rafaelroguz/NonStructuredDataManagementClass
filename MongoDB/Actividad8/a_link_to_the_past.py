#Nuestra colección se llamará "movies"#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

#Importamos la biblioteca de MongoDB para Python
import pymongo
from pymongo import MongoClient

#Creamos una conexión con el servidor
client = MongoClient()

#Nuestra base de datos se llamará "mongo_test"
db_name = "vgcharacters"

#Se conecta a una base de datos especificada. Si no existe, la crea
#Creamos la base de datos o nos conectamos a ella
db = client[db_name]

#Recuperamos el nombre de todas las bases de datos en el servidor
db_list = client.list_database_names()

#Revisamos si la base de datos existe
if db_name in db_list:
    print("La base de datos \"" + db_name + "\" existe!")

#Nombramos nuestra colección
#Una colección es un grupo de documentos almacenados en MongoDB
collection_name = "characters"

#Crea una nueva colección o recupera el contenido de una existente
#Si la colección se está creando, MongoDB no la va a crear hasta que se le inserte documentos
collection = db[collection_name]

#Recuperamos el nombre de todas las colecciones
collection_list = db.list_collection_names()

#Revisamos si la colección existe. Si la colección creada no tiene elementos, MongoDB no la va a crear
if collection_name in collection_list:
    print("La coleccion \"" + collection_name + "\" existe!\n")

collection.delete_many({})

character_link = {
    'name': 'Link',
    'location': {
        'id': 'room-1',
        'description': 'Sala 1'
    }
}

collection.insert_one(character_link)
