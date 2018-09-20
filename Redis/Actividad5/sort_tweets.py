#Este script te permite recuperar los tweets almacenados en Redis previamente
#Los tweets almacenados usan el tema "Viva México"
#Para organizar los tweets y mostrarlos en pantalla se accede a Redis usando hashmaps
#El script te permite escribir una palabra clave y recuperar los tweets que contienen dicha palabra
#También permite escribir un nombre de usuario, anteponiendo el "@" y recuperar los tweets de dicho usuario

#Importamos las bibliotecas necesarias
import redis
import tweepy

#Cremos una variable para manejar la conexión con Redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

print("Bienvenido!")

palabra = input("Introduce una palabra clave (eje: pozole) o un nombre de usuario (eje: @tim_cook) para ordenar los tweets:")

print("")

def sortTweets(palabra):
    #Contador para ver cuántos tweets mencionaron la palabra
    numeroOcurrencias = 0

    #Si la palabra que escribió el usuario tiene un "@" quiere decir que quiere ver los tweets donde se menciona a un usuario específico (ejemplo: @tim_cook)
    #sino, quiere decir que sólo busca una palabra dentro de tweet (ejemplo: pozole)
    if ("@" in palabra):
        #Iteramos entre las llaves almacenadas en Redis, buscando las que tienen como llave el prefijo "twiterA5_user:"
        for key in redis.keys(pattern="twiterA5_user:*"):
            #Recuperamos los nombres de usuario para ver si se encuentra el que se busca
            #Me regresa una lista de usuarios cuando sólo debería regresarme un nombre. Código es idéntico al siguiente bloque if
            #Es un error por corregir
            user_names = redis.hget(key, "username").decode("utf-8")
            palabra = palabra.replace("@", "")

            #Verifica si el usuario se encuentra en los tweets que se almacenaron, es decir, si realizó algún tweet
            if (palabra in user_names):
                #Incrementamos el contador de número de tweets del usuario
                numeroOcurrencias = numeroOcurrencias + 1

                #Recuperamos los datos del tweet de Redis
                id_key = (key.split(b':')[1]).decode("utf-8")
                user_name = redis.hget(key, "username").decode("utf-8")
                date = redis.hget(key, "date").decode("utf-8")
                rt_count = redis.hget(key, "rtcount").decode("utf-8")
                language = redis.hget(key, "language").decode("utf-8")
                content = redis.hget(key, "content").decode("utf-8")

                #Imprimimos los datos del tweet
                print("id: " + id_key)
                print("user_name: " + user_name)
                print("date: " + date)
                print("retweet count: " + rt_count)
                print("language: " + language)
                print("content: " + content + "\n")

        if (numeroOcurrencias == 0):
            #No se encontró el usuario deseado
            print("No se encontraron tweets para @" + palabra + "\n")
        else:
            #Se imprime el número de tweets que el usuario realizó
            print("Se encontraron " + str(numeroOcurrencias) + " tweets para @" + palabra + "\n")
    else:
        #Iteramos entre las llaves almacenadas en Redis, buscando las que tienen como llave el prefijo "twiterA5_user:"
        for key in redis.keys(pattern="twiterA5_user:*"):
            #Recuperamos el contenido del tweet
            content = redis.hget(key, "content").decode("utf-8")

            #Validamos si el tweet contiene la palabra mencionada
            if (palabra in content):
                #Incrementamos el contador de número de tweets que mencionan la palabra
                numeroOcurrencias = numeroOcurrencias + 1

                #Recuperamos los datos del tweet de Redis
                id_key = (key.split(b':')[1]).decode("utf-8")
                user_name = redis.hget(key, "username").decode("utf-8")
                date = redis.hget(key, "date").decode("utf-8")
                rt_count = redis.hget(key, "rtcount").decode("utf-8")
                language = redis.hget(key, "language").decode("utf-8")

                #Imprimimos los datos del tweet
                print("id: " + id_key)
                print("user_name: " + user_name)
                print("date: " + date)
                print("retweet count: " + rt_count)
                print("language: " + language)
                print("content: " + content + "\n")

        if (numeroOcurrencias == 0):
            #No se encontró la palabra en los tweets
            print("No se encontro la palabra \"" + palabra + "\" dentro de los tweets almacenados!\n")
        else:    
            #Imprimimos cuántas veces se mencionó la palabra
            print("La palabra \"" + palabra + "\" fue mencionada " + str(numeroOcurrencias) + " veces!\n")
    
sortTweets(palabra)