#Nuestra colección se llamará "movies"#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

#Importamos la biblioteca de MongoDB para Python
import pymongo
from pymongo import MongoClient

#Creamos una conexión con el servidor
client = MongoClient("mongodb://rafael:S7BNKu4WAj2z3ca6@nonstructureddatamanagementclass-shard-00-00-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-01-xa2lb.mongodb.net:27017,nonstructureddatamanagementclass-shard-00-02-xa2lb.mongodb.net:27017/twitter_db?ssl=true&replicaSet=NonStructuredDataManagementClass-shard-0&authSource=admin&retryWrites=true")

#Se conecta a una base de datos especificada. Si no existe, la crea
#Creamos la base de datos o nos conectamos a ella
db = client["vgcharacters"]

#Crea una nueva colección o recupera el contenido de una existente
#Si la colección se está creando, MongoDB no la va a crear hasta que se le inserte documentos
collection_characters = db["characters"]
collection_rooms = db["rooms"]
collection_items = db["items"]

character_link = {
  'name': 'Link',
  'character': {
    'health': 3,
    'strength': 1,
    'constitution': 1
  },
  'location': {
    'id': 'room-1',
    'description': "Un vestíbulo vacío. Se ven tres salidas: una al norte, una al este y una al oeste.",
    'exits': {
      'n': 'room-4',
      'e': 'room-2',
      'w': 'room-3'
    },
    'inventory': []
  },
  'rupees': 0,
  'keys': 0,
  'armor': {'name': 'basic-tunic'},
  'weapons': [
    {'name': 'wooden-sword', 'hand': 'left'},
    {'name': 'boomerang', 'hand': 'right'}
  ],
  'inventory': [
    {'qty': 1, 'name': 'bombs', 'bonus': 2},
    {'qty': 1, 'name': 'wooden-sword', 'bonus': 1},
    {'qty': 1, 'name': 'basic-tunic', 'bonus': 0},
    {'qty': 1, 'name': 'boomerang', 'bonus': 1}
  ]
}

room1 = {
  'id': 'room-1',
  'description': 'Un vestíbulo vacío. Se ven tres salidas: una al norte, una al este y una al oeste. La puerta norte se encuentra cerrada con llave',
  'exits':{
      'n': 'room-4',
      'e': 'room-2',
      'w': 'room-3'
  },
  'inventory': [],
  'playesr': []
}

room2 = {
  'id': 'room-2',
  'description': 'Al entrar ves un cofre dorado. Contiene una llave',
  'exits':{
      'w': 'room-1'
  },
  'inventory': [{'qty': 1, 'name': 'key'}],
  'players': []
}

room3 = {
  'id': 'room-3',
  'description': 'Al fondo, en una pila de rocas ves un objeto de madera. Es un arco!',
  'exits':{
      'e': 'room-1'
  },
  'inventory': [{'qty': 1, 'name': 'bow'}],
  'players': []
}

room4 = {
  'id': 'room-4',
  'description': 'Hay una vasija en la habitación. Tiene 10 rupias!\nVes una salida hacia el norte.',
  'exits':{
      'n': 'room-5',
      's': 'room-1'
  },
  'inventory': [{'qty': 10, 'name': 'rupee'}],
  'players': []
}

room5 = {
  'id': 'room-5',
  'description': 'Al entrar ves una figura enorme. Es un dragón!',
  'exits':{
      's': 'room-4'
  },
  'inventory': [{'qty': 1, 'name': 'triforce_piece'}],
  'players': []
}

boombs = {
  'name': 'bombs',
  'bonus': 2
}

bow = {
  'name': 'bow',
  'bonus': 2
}

boomerang = {
  'name': 'boomerang',
  'bonus': 1
}

key = {
  'name': 'key',
  'bonus': 0
}

rupee = {
  'name': 'rupee',
  'bonus': 0
}

#collection_characters.delete_many({})
#collection_items.delete_many({})
#collection_rooms.delete_many({})

#collection_rooms.insert_many([room1, room2, room3, room4, room5])
#collection_items.insert_many([boombs, bow, boomerang, key, rupee])
character_list = collection_characters.find()

def print_characters(character_list):
    for c in character_list:
        print(c["name"])
        print(str(c["character"]["health"]))
        print(c["location"]["id"])
        print()

def room1(character):    
    room = collection_rooms.find_one({"id": "room-1"})
    room["player"] = True
    character["location"] = room
    
    collection_rooms.update_one({"name": "room-1"}, {"$set":{"player": True}})
    
    print(room["description"])

    while True:
        print("Qué deseas hacer?")
        print("1) Ir a la sala norte")
        print("2) Ir a la sala este")
        print("3) Ir a la sala oeste")

        opt = input("Elige una opción: ")

        if int(opt) == 1: 
            room4(character)
            collection_rooms.update_one({"name": "room-1"}, {"$set": {"player": False}})
        elif int(opt) == 2: 
            room2(character)
            collection_rooms.update_one({"name": "room-1"}, {"$set": {"player": False}})
        elif int(opt) == 3: 
            room3(character)
            collection_rooms.update_one({"name": "room-1"}, {"$set": {"player": False}})

print("Bienvenido!\n")

print_characters(character_list)

print("Escriba el nombre del personaje con quien quiere continuar su partida o iniciar una nueva: ")

name = input("Nombre del personaje: ")

character = collection_characters.find_one({"name": name})

print()

if not character:
    character_link["name"] = name
    collection_characters.insert_one(character_link)
    room1(character_link)
else:
    room_loc = character["location"]["id"]

    if room_loc == 1:
        room1(character)
    elif room_loc == 2:
        room2(character)
    elif room_loc == 3:
        room3(character)
    elif room_loc == 4:
        room4(character)
    elif room_loc == 5:
        room5(character)

#mongodb+srv://rafael:S7BNKu4WAj2z3ca6@nonstructureddatamanagementclass-xa2lb.mongodb.net/admin