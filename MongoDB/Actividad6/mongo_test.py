#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

#Importamos la biblioteca de MongoDB para Python
import pymongo
from pymongo import MongoClient

#Imprimimos los datos de la película
def print_in_screen(json_data):
    print()
    print(json_data["name"])
    print(json_data["director"])
    print(json_data["year"])
    print(json_data["country"])
    print(str(json_data["running_time"]) + " minutes")
    
    for genre in json_data["genres"]:
        print(genre, end="  ", flush=True)
    
    print("\n_____________________________________________________")
    
    for comment in json_data["comments"]:
        print("user: " + comment["user_name"])
        print("score: " + str(comment["score"]))
        print("opinion: " + comment["comment"])
        print()

#Creamos una conexión con el servidor
client = MongoClient()

#Nuestra base de datos se llamará "mongo_test"
db_name = "mongo_test"

#Se conecta a una base de datos especificada. Si no existe, la crea
#Creamos la base de datos "mongo_test" o nos conectamos a ella
db = client[db_name]

#Recuperamos el nombre de todas las bases de datos en el servidor
db_list = client.list_database_names()

#Revisamos si la base de datos existe
if db_name in db_list:
    print("La base de datos existe!")

#Nuestra colección se llamará "movies"
#Una colección es un grupo de documentos almacenados en MongoDB
collection_name = "movies"

#Crea una nueva colección o recupera el contenido de una existente
#Si la colección se está creando, MongoDB no la va a crear hasta que se le inserte documentos
movies = db[collection_name]

#Recuperamos el nombre de todas las colecciones
movie_list = db.list_collection_names()

#Revisamos si la colección existe. Si la colección creada no tiene elementos, MongoDB no la va a crear
if collection_name in movie_list:
    print("La coleccion existe!")

#Limpiamos la base de datos para evitar tener inserciones repetidas
movies.delete_many({})

#Ejemplo del contenido de una sola película a insertar
movie = {
    "name": "Pulp Fiction",
    "director": "Quentin Tarantino",
    "year": 1994,
    "country": "United States",
    "running_time": 154,
    "genres": ["Thriller", "Comedy", "Crime"],
    "comments": [
        {
            "user_name": "rafael91",
            "score": 100,
            "comment": "This is the best movie ever! I loved it!"
        },
        {
            "user_name": "rodri_go",
            "score": 75,
            "comment": "Meh, I've seen better."
        },
        {
            "user_name": "dani_dani",
            "score": 99,
            "comment": "The neddle part was so sick!"
        }
    ]
}

#Insertamos la película
inserted = movies.insert_one(movie)

#Verificamos si se añadió correctamente
print(inserted)

many_movies = [
    {
    "name": "Kill Bill",
    "director": "Quentin Tarantino",
    "year": 2003,
    "country": "United States",
    "running_time": 111,
    "genres": ["Thriller", "Action", "Crime"],
    "comments": [
        {
            "user_name": "rafael91",
            "score": 99,
            "comment": "This is the second best movie ever! I loved it!"
        },
        {
            "user_name": "panchi_to",
            "score": 80,
            "comment": "Really good"
        },
        {
            "user_name": "dani_dani",
            "score": 90,
            "comment": "Cool"
        }
    ]
    },
    {
    "name": "The Hateful Eight",
    "director": "Quentin Tarantino",
    "year": 2016,
    "country": "United States",
    "running_time": 187,
    "genres": ["Thriller", "Drama", "Crime", "Western"],
    "comments": [
        {
            "user_name": "rafael91",
            "score": 90,
            "comment": "La octava de Tarantino!"
        },
        {
            "user_name": "mario_jump",
            "score": 70,
            "comment": "Esperaba mas"
        }
    ]
    },
    {
    "name": "Inglorious Basterds",
    "director": "Quentin Tarantino",
    "year": 2009,
    "country": "United States",
    "running_time": 153,
    "genres": ["Adventure", "Drama", "War"],
    "comments": [
        {
            "user_name": "rafael91",
            "score": 100,
            "comment": "MAAARGHERETIIIII"
        },
        {
            "user_name": "waltz",
            "score": 99,
            "comment": "Ese momento cuando estás comiendo y te acuerdas de la Shoshana esa"
        },
        {
            "user_name": "bear_jew",
            "score": 100,
            "comment": "jackpot!"
        }
    ]
    }
]

#Insertamos varias películas al mismo tiempo
inserted_many = movies.insert_many(many_movies)

#Comprobamos la inserción con los ids
print(inserted_many.inserted_ids)

#Recuperamos la información de sólo una película
def search_movie():
    movie_search = input("Qué película quieres buscar?")
    
    #Realizamos la búsqueda de la película deseada
    find_movie = movies.find_one({"name": movie_search})
    
    print_in_screen(find_movie)

while True:
    print("Bienvenido! Seleccione una opción:")
    print("1) Buscar una película·")
    print("2) Listar todas las películas")
    print("3) Salir")

    option = input()

    if (int(option) == 1):
        search_movie()
    elif (int(option) == 2):
       #Recuperamos todos los documentos de la base de datos
        for mve in movies.find():
            print_in_screen(mve)     
    else:
        break