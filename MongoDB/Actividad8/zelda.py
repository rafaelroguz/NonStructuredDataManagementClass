#Equipo:
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

#Esquemas de los objetos
bombs = {
  'qty': 3,
  'name': 'bombs',
  'bonus': 1
}

bow = {
  'qty': 1,
  'name': 'bow',
  'bonus': 1
}

boomerang = {
  'qty': 1,
  'name': 'boomerang',
  'bonus': 1
}

key = {
  'qty': 1,
  'name': 'key',
  'bonus': 0
}

rupee = {
  'qty': 10,
  'name': 'rupee',
  'bonus': 0
}

wooden_sword = {
  'qty': 1,
  'name': 'wooden_sword',
  'bonus': 2
}

basic_tunic = {
  'qty': 1,
  'name': 'basic_tunic',
  'bonus': 1
}

triforce_piece = {
  'qty': 1,
  'name': 'triforce_piece',
  'bonus': 0
}

#Esquemas de las habitaciones
room1 = {
  'name': 'room-1',
  'description': 'Un vestíbulo vacío. Se ven tres salidas: una al norte, una al este y una al oeste. La puerta norte se encuentra cerrada con llave',
  'exits':{
      'n': 'room-4',
      'e': 'room-2',
      'w': 'room-3'
  },
  'inventory': [],
  'players': [],
  'open': True
}

room2 = {
  'name': 'room-2',
  'description': 'Al entrar ves un cofre dorado. La habitación no parece tener ninguna otra salida más que por donde entraste.',
  'exits':{
      'w': 'room-1'
  },
  'inventory': [key],
  'players': [],
  'open': True
}

room3 = {
  'name': 'room-3',
  'description': 'La habitación está en ruinas. Al fondo puedes ver una pila de rocas.\nNo parece haber una salida fuera de por donde entraste.',
  'exits':{
      'e': 'room-1'
  },
  'inventory': [bow],
  'players': [],
  'open': True
}

room4 = {
  'name': 'room-4',
  'description': 'La sala se encuentra adornada con crestas que no reconoces. Hay una vasija en la habitación.\nVes una enorme puerte hacia el norte. No encuentras más salidas a excepción de donde entraste',
  'exits':{
      'n': 'room-5',
      's': 'room-1'
  },
  'inventory': [rupee],
  'players': [],
  'open': True
}

room5 = {
  'name': 'room-5',
  'description': 'Al entrar ves una figura enorme. Es un dragón!',
  'exits':{
      's': 'room-4'
  },
  'inventory': [triforce_piece],
  'players': [],
  'open': False
}

#Esquema del personaje
character_link = {
  'name': 'Link',
  'character': {
    'health': 3,
    'strength': 1,
    'constitution': 1
  },
  'location': {
    'name': 'room-1',
    'description': "Un vestíbulo vacío. Se ven tres salidas: una al norte, una al este y una al oeste.",
    'exits': {
      'n': 'room-4',
      'e': 'room-2',
      'w': 'room-3'
    },
    'inventory': [],
    'players': []
  },
  'rupees': 0,
  'keys': 0,
  'armor': {'name': 'basic-tunic'},
  'weapons': [
    {'name': 'wooden-sword', 'hand': 'left'}
  ],
  'inventory': [bombs, boomerang, basic_tunic, wooden_sword]
}

#collection_characters.delete_many({})
#collection_items.delete_many({})
#collection_rooms.delete_many({})

#collection_rooms.insert_many([room1, room2, room3, room4, room5])
#collection_items.insert_many([bombs, bow, boomerang, key, rupee])

#Recuperamos la lista de personajes disponibles
character_list = collection_characters.find()

#Muestra la información de los personajes en el menú principal
def print_characters(character_list):
  for c in character_list:
    print("Jugador: " + c["name"])
    print("Vidas: " + str(c["character"]["health"]))
    print("Sala: " + c["location"]["name"])
    print()

#Habitación 1. Sirve como un hub para las demás habitaciones
def room1(player):    
  #Actualizamos la ubicación del jugador localmente
  player["location"] = collection_rooms.find_one({"name": "room-1"})
  #Actualizamos la ubicación del jugador en la bd 
  collection_characters.update_one({"name": player["name"]}, {"$set": {"location": player["location"]}})
  #Añadimos al jugador a la lista de jugadores del cuarto
  collection_rooms.update_one({"name": "room-1"}, {"$push": {"players": player}})
  
  print()
  #Mostramos la descripción del cuarto la cuál nos muestra qué acciones podemos realizar
  print(player["location"]["description"])

  #El jugador tiene que introducir una de las opciones o no podrá avanzar
  while True:
    print("Qué deseas hacer?\n")
    print("1) Ir a la sala norte")
    print("2) Ir a la sala este")
    print("3) Ir a la sala oeste")

    #Recuperamos la opción que el usuario introdujo
    opcion = input("\nElige una opción: ")

    #Probamos que la opción introducida por el usuario sea numérica
    try:
      #De acuerdo a la opción que el jugador seleccione será la habitación a la cual se mueva
      if int(opcion) == 1: 
        #Como el jugador se movió de la habitación, lo removemos de la lista de jugadores dentro de esa sala
        collection_rooms.update_one({"name": "room-1"}, {"$pull": {"players": {"name": player["name"]}}})
        #Ejecutamos el código de la habitación a la cuál el jugador se movió
        room4(player)
      elif int(opcion) == 2: 
        collection_rooms.update_one({"name": "room-1"}, {"$pull": {"players": {"name": player["name"]}}})
        room2(player)
      elif int(opcion) == 3: 
        collection_rooms.update_one({"name": "room-1"}, {"$pull": {"players": {"name": player["name"]}}})
        room3(player)
      else:
        print("\nEsa no es una opción válida!\n")
    except ValueError:
      print("\nEsa no es una opción válida!\n")

#Habitación 2. El jugador encuentra la llave para abrir la habitación 5
def room2(player):          
  #Actualizamos la ubicación del jugador localmente
  player["location"] = collection_rooms.find_one({"name": "room-2"})
  #Actualizamos la ubicación del jugador en la bd 
  collection_characters.update_one({"name": player["name"]}, {"$set": {"location": player["location"]}})
  #Añadimos al jugador a la lista de jugadores del cuarto
  collection_rooms.update_one({"name": "room-2"}, {"$push": {"players": player}})
  
  print()
  #Mostramos la descripción del cuarto la cuál nos muestra qué acciones podemos realizar
  print(player["location"]["description"])

  #El jugador tiene que introducir una de las opciones o no podrá avanzar
  while True:
    print("Qué deseas hacer?\n")
    print("1) Abrir el cofre")
    print("2) Regresar a la sala anterior")

    #Recuperamos la opción que el usuario introdujo
    opcion = input("\nElige una opción: ")

    #Probamos que la opción introducida por el usuario sea numérica
    try:
      #El usuario decide revisar el cofre y encuentra una llave
      if int(opcion) == 1: 
        print("\nTe acercas al cofre y lo abres.")

        #Recuperamos el inventario de la habitación
        room_inventory = collection_rooms.find_one({"name": "room-2"}, {"inventory": 1})
        
        #Si la habitación tiene inventario es que la llave aún no ha sido tomada
        #NOTA: preguntar por un query donde en vez de obtener una lista de inventary, obtenga sólo si "key" se encuentra o no
        if room_inventory["inventory"]:
          print("Encontraste una llave!\n")

          #Incrementamos el número de llaves que el usuario lleva consigo
          player["keys"] = int(player["keys"]) + 1
          #Removemos la llave del inventario
          player["location"]["inventory"] = []
          
          #Actualizamos el valor de las llaves que el usuario lleva en la db
          collection_characters.update_one({"name": player["name"]}, {"$set": {"keys": player["keys"]}})
          #Removemos la llave que se tomó del inventario del cuarto
          collection_rooms.update({"name": "room-2"}, {"$pull": {"inventory": {"name": "key"}}})

          #No es óptimo, pero lo que se quiere hacer es actualizar el valor de "location" del jugador en el arreglo de jugadores del cuarto
          #NOTA: preguntar cómo escribir una query para actualizar sólo el valor de location del jugador en la lista de jugadores del cuarto       
          collection_rooms.update_one({"name": "room-2"}, {"$pull": {"players": {"name": player["name"]}}})
          collection_rooms.update_one({"name": "room-2"}, {"$push": {"players": player}})
        else:
          print("El cofre está vacío\n")
      elif int(opcion) == 2: 
        #Como el jugador se movió de la habitación, lo removemos de la lista de jugadores dentro de esa sala
        collection_rooms.update_one({"name": "room-2"}, {"$pull": {"players": {"name": player["name"]}}})
        #Ejecutamos el código de la habitación a la cuál el jugador se movió
        room1(player)
    except ValueError:
      print("\nEsa no es una opción válida!\n")

#Habitación 3. El jugador encuentra un arco.
def room3(player):          
  #Actualizamos la ubicación del jugador localmente
  player["location"] = collection_rooms.find_one({"name": "room-3"})
  #Actualizamos la ubicación del jugador en la bd 
  collection_characters.update_one({"name": player["name"]}, {"$set": {"location": player["location"]}})
  #Añadimos al jugador a la lista de jugadores del cuarto
  collection_rooms.update_one({"name": "room-3"}, {"$push": {"players": player}})
  
  print()
  #Mostramos la descripción del cuarto la cuál nos muestra qué acciones podemos realizar
  print(player["location"]["description"])

  #El jugador tiene que introducir una de las opciones o no podrá avanzar
  while True:
    print("Qué deseas hacer?\n")
    print("1) Investigar la pila de rocas")
    print("2) Regresar a la sala anterior")

    #Recuperamos la opción que el usuario introdujo
    opcion = input("\nElige una opción: ")

    #Probamos que la opción introducida por el usuario sea numérica
    try:
      #El usuario decide revisar la pila de rocas y encuentra el arco y algunas flechas
      if int(opcion) == 1: 
        print("\nTe acercas a la pila de rocas.")

        #Recuperamos el inventario de la habitación
        room_inventory = collection_rooms.find_one({"name": "room-3"}, {"inventory": 1})
        
        #Si la habitación tiene inventario es que la llave aún no ha sido tomada
        #NOTA: preguntar por un query donde en vez de obtener una lista de inventary, obtenga sólo si "key" se encuentra o no
        if room_inventory["inventory"]:
          print("¡Moviendo el escombro encuentras un arco y algunas flechas!\n")

          #Añadimos el arco a las armas del personaje
          player["inventory"].append(bow)
          player["weapons"].append({'name': 'bow', 'hand': 'none'})

          #Removemos el arco del inventario de la sala en el registro del personaje
          player["location"]["inventory"] = []
          
          #Actualizamos los objetos del jugador
          collection_characters.update_one({"name": player["name"]}, {"$set": {"weapons": player["weapons"]}})
          collection_characters.update_one({"name": player["name"]}, {"$set": {"inventory": player["inventory"]}})
          
          #Removemos la llave que se tomó del inventario del cuarto
          collection_rooms.update({"name": "room-3"}, {"$pull": {"inventory": {"name": "bow"}}})

          #No es óptimo, pero lo que se quiere hacer es actualizar el valor de "location" del jugador en el arreglo de jugadores del cuarto
          #NOTA: preguntar cómo escribir una query para actualizar sólo el valor de location del jugador en la lista de jugadores del cuarto       
          collection_rooms.update_one({"name": "room-3"}, {"$pull": {"players": {"name": player["name"]}}})
          collection_rooms.update_one({"name": "room-3"}, {"$push": {"players": player}})
        else:
          print("Al acercarte ves que los escombros ya han sido removidos. No encuentras nada.\n")
      elif int(opcion) == 2: 
        #Como el jugador se movió de la habitación, lo removemos de la lista de jugadores dentro de esa sala
        collection_rooms.update_one({"name": "room-3"}, {"$pull": {"players": {"name": player["name"]}}})
        #Ejecutamos el código de la habitación a la cuál el jugador se movió
        room1(player)
    except ValueError:
      print("\nEsa no es una opción válida!\n")

#Habitación 4. Presala al jefe. Es necesario tener la llave para abrir la siguiente puerta
def room4(player):          
  #Actualizamos la ubicación del jugador localmente
  player["location"] = collection_rooms.find_one({"name": "room-4"})
  #Actualizamos la ubicación del jugador en la bd 
  collection_characters.update_one({"name": player["name"]}, {"$set": {"location": player["location"]}})
  #Añadimos al jugador a la lista de jugadores del cuarto
  collection_rooms.update_one({"name": "room-4"}, {"$push": {"players": player}})
  
  print()
  #Mostramos la descripción del cuarto la cuál nos muestra qué acciones podemos realizar
  print(player["location"]["description"])

  #El jugador tiene que introducir una de las opciones o no podrá avanzar
  while True:
    print("Qué deseas hacer?\n")
    print("1) Revisar la vasija")
    print("2) Entrar a la puerta norte")
    print("3) Regresar a la sala anterior")

    #Recuperamos la opción que el usuario introdujo
    opcion = input("\nElige una opción: ")

    #Probamos que la opción introducida por el usuario sea numérica
    try:
      #El usuario decide revisar el cofre y encuentra una llave
      if int(opcion) == 1: 
        print("\nTe acercas a la vasija y la revisas.")

        #Recuperamos el inventario de la habitación
        room_inventory = collection_rooms.find_one({"name": "room-4"}, {"inventory": 1})
        
        #Si la habitación tiene inventario es que la llave aún no ha sido tomada
        #NOTA: preguntar por un query donde en vez de obtener una lista de inventary, obtenga sólo si "key" se encuentra o no
        if room_inventory["inventory"]:
          print("¡Encontraste 10 rupias!\n")

          #Incrementamos el número de rupias
          player["rupees"] = int(player["rupees"]) + 10
          #Removemos las rupias del inventario del cuarto
          player["location"]["inventory"] = []
          
          #Actualizamos el valor de las rupias del personaje en la db
          collection_characters.update_one({"name": player["name"]}, {"$set": {"rupees": player["rupees"]}})
          #Removemos las rupias del inventario del cuarto
          collection_rooms.update({"name": "room-4"}, {"$pull": {"inventory": {"name": "rupee"}}})

          #No es óptimo, pero lo que se quiere hacer es actualizar el valor de "location" del jugador en el arreglo de jugadores del cuarto
          #NOTA: preguntar cómo escribir una query para actualizar sólo el valor de location del jugador en la lista de jugadores del cuarto       
          collection_rooms.update_one({"name": "room-4"}, {"$pull": {"players": {"name": player["name"]}}})
          collection_rooms.update_one({"name": "room-4"}, {"$push": {"players": player}})
        else:
          print("La vasija está vacía\n")
      elif int(opcion) == 2:
        print("Te acercas a la puerta norte. Es una gran puerta, adornada con detalles de oro y alguna especie de advertencia.\nSabes que hay peligro del otro lado")
        
        boss_room = collection_rooms.find_one({"name": "room-5"}, {"open": 1})
        
        if boss_room["open"] == True:
          print("Al examinar de cerca la puerta ves que esta ya ha sido abierta. Entras a la siguiente sala.")
          
          #Como el jugador se movió de la habitación, lo removemos de la lista de jugadores dentro de esa sala
          collection_rooms.update_one({"name": "room-4"}, {"$pull": {"players": {"name": player["name"]}}})
          #Ejecutamos el código de la habitación a la cuál el jugador se movió
          room5(player)
        else:
          print("Al examinar de cerca la puerta ves que esta se encuentra cerrada con llave.")
          
          #Revisamos el inventario del jugador para ver si tiene la llave
          if player["keys"] > 0:
            print("Tomas la llave que encontraste previamente. ¡Encaja en la ranura!")

            player["keys"] = player["keys"] - 1

            #Actualizamos los valores del personaje en la db
            collection_characters.update_one({"name": player["name"]}, {"$set": {"keys": player["keys"]}})
            
            #Actualizamos los valores del cuarto en la db
            collection_rooms.update_one({"name": "room-5"}, {"$set": {"open": True}})
      elif int(opcion) == 3: 
        #Como el jugador se movió de la habitación, lo removemos de la lista de jugadores dentro de esa sala
        collection_rooms.update_one({"name": "room-4"}, {"$pull": {"players": {"name": player["name"]}}})
        #Ejecutamos el código de la habitación a la cuál el jugador se movió
        room1(player)
    except ValueError:
      print("\nEsa no es una opción válida!\n")

#Habitación 5. El jugador se encuentra de cara contra el jefe
def room5(player):          
  #Actualizamos la ubicación del jugador localmente
  player["location"] = collection_rooms.find_one({"name": "room-5"})
  #Actualizamos la ubicación del jugador en la bd 
  collection_characters.update_one({"name": player["name"]}, {"$set": {"location": player["location"]}})
  #Añadimos al jugador a la lista de jugadores del cuarto
  collection_rooms.update_one({"name": "room-5"}, {"$push": {"players": player}})
  
  print()
  #Mostramos la descripción del cuarto la cuál nos muestra qué acciones podemos realizar
  print(player["location"]["description"])

  #El jugador tiene que introducir una de las opciones o no podrá avanzar
  while True:
    print("Qué deseas hacer?\n")
    print("1) Atacar al dragón")
    print("2) Regresar a la sala anterior")

    #Recuperamos la opción que el usuario introdujo
    opcion = input("\nElige una opción: ")

    #Probamos que la opción introducida por el usuario sea numérica
    try:
      #El usuario decide enfrentar al jefe
      if int(opcion) == 1: 
        print("Lanzas un swing al aire con tu espada. Haces daño al dragón")

      elif int(opcion) == 2: 
        #Como el jugador se movió de la habitación, lo removemos de la lista de jugadores dentro de esa sala
        collection_rooms.update_one({"name": "room-5"}, {"$pull": {"players": {"name": player["name"]}}})
        #Ejecutamos el código de la habitación a la cuál el jugador se movió
        room4(player)
    except ValueError:
      print("\nEsa no es una opción válida!\n")

print("Bienvenido!\nEstos son los personajes disponibles:")

#Mostramos la lista de personajes jugables disponibles
print_characters(character_list)

print("Escriba el nombre del personaje con quien quiere continuar su partida o iniciar una nueva: ")

#Recuperamos el nombre del personaje con el cual el jugador quiere jugar
name = input("Nombre del personaje: ")

#Buscamos al personaje en la bd
player = collection_characters.find_one({"name": name})

#Si el personaje no existe en la bd, se crea uno nuevo
if not player:
  #Se nombra el personaje nuevo de acuerdo al introducido previamente
  character_link["name"] = name
  #Se añade el personaje a la bd
  collection_characters.insert_one(character_link)
  #Movemos al personaje a la sala 1, ejecutando el código de dicha sala
  room1(character_link)
#Si el personaje ya existe, se usa el obtenido de la bd
else:
  #Se obtiene el nombre de la sala en la que el personaje se encuentra
  player_location = player["location"]["name"]

  #Se mueve el personaje a la sala correspondiente, ejecutándo el código de dicha sala
  if player_location == "room-1":
      room1(player)
  elif player_location == "room-2":
      room2(player)
  elif player_location == "room-3":
      room3(player)
  elif player_location == "room-4":
      room4(player)
  elif player_location == "room-5":
      room5(player)

#mongodb+srv://rafael:S7BNKu4WAj2z3ca6@nonstructureddatamanagementclass-xa2lb.mongodb.net/admin