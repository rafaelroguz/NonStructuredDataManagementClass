#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

#Instalamos paquetes necesarios antes de instalar twitteR
#install.packages(c("devtools", "rjson", "bit64", "httr"))

#Importamos los paquetes necesarios
library(devtools)

#Instalamos twitteR
#install_github("geoffjentry/twitteR")

#Importamos twitteR
library(twitteR)

#Son las llaves de acceso a la api de twitter
access_key = "0zLVRnLCdP0JuUxjsMlB5P6id"
access_secret = "UEOvI6l0QFgaWxIzee3LJMOt5C59M5YhL9yh40dOq0ZGBXs85n"
access_token = "940271662959906816-CEzHkOji1IYR1Z1VZeXdSYDrNetgRVT"
access_token_secret = "wXev8vS56LhX06adGOgDX8HFTrAcjhwSztQGBGlzQePVA"

#Autorizamos acceso a la api
setup_twitter_oauth(access_key, access_secret, access_token, access_token_secret)

#Recuperamos tweets con el hashtag "bigdata"
bigdata = searchTwitter("#bigdata", n=1500)

#Nos devuelte el tipo del objeto, en este caso "list"
class(bigdata)

#Nos devuelve los primeros objetos de la lista
head(bigdata)

#Accedemos al cuarto elemento en la lista
bigdata[[4]]

#Devuelve la longitud de la lista
length(bigdata)

#Convertimos la lista a un data frame
bigdata.df = do.call(rbind, lapply(bigdata, as.data.frame))

#Guardamos los datos en un archivo .csv
write.csv(bigdata.df, "/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/Actividad10/bigdata.csv")

#Antes de instalar el siguiente paquete es necesario instalar estos paquetes en la terminal de Linux:
#sudo apt install libpoppler-cpp-dev
#sudo apt install libxml2-dev

#Instalamos el paquete para manejar matrices de tipo Document-term 
#install.packages("tm", dependencies=TRUE)

#Importamos la bibliteca para usar matrices Document-term
library("tm")

#Sapply recorre la matriz para recuperar el texto de los tweets y crea una lista de objetos
bigdata_list = sapply(bigdata, function(x) x$getText())

#Convierte la lista de tweets en un corpus, el cual es una abstracción de R para representar una colección de documentos
bigdata_corpus = Corpus(VectorSource(bigdata_list))

#Convierte las palabras a minúsculas
bigdata_corpus = tm_map(bigdata_corpus, tolower)

#Remueve los signos de puntuación
bigdata_corpus = tm_map(bigdata_corpus, removePunctuation)

#Remueve las stopwords ("a", "are", "that", etc)
bigdata_corpus = tm_map(bigdata_corpus,function(x)removeWords(x,stopwords()))

#Instalamos el paquete para crear una WordCloud
#install.packages("wordcloud")

#Importamos la biblioteca para generar una nube de palabras
library("wordcloud")

#Generamos la nube de palabras usando la lista de tweets
wordcloud(bigdata_corpus)

#Generamos una matriz de Document-term
bigdata.tdm = TermDocumentMatrix(bigdata_corpus)

#Muestra información básica de la matriz
#NOTA: R deja de funcionar al ejecutar esta línea de código
bigdata.tdm

#Muestra los términos más frecuentemente usados en la matrix
#findFreqTerms(bigdata.tdm, lowfreq=10)

#Muesta información sobre la asociación de la palabra "people" en términos de qué tan frecuente ocurre una co-ocurrencia
findAssocs(bigdata.tdm, 'people', 0.50)

#Removemos términos esparsos en el documento. Esto son aquellos que ocurren muy pocas veces
bigdata2.tdm = removeSparseTerms(bigdata.tdm, sparse=0.92)

#Convertimos la matriz a dataframe
#NOTA: Error al ejecutar la línea de código
#Error in as.data.frame.default(bigdata2.tdm) : 
#  cannot coerce class ‘c("TermDocumentMatrix", "simple_triplet_matrix")’ to a data.frame
bigdata2.df = as.data.frame(bigdata2.tdm)

#Se escalan los datos
bigdata2.df.scale = scale(bigdata2.df)

#Se crea una matriz de distancia
bigdata.dist = dist(bigdata2.df.scale, method = "euclidean")

bigdata.fit = hclust(bigdata.dist, method="ward")

#Se grafica el resultado
plot(bigdata.fit, main="Cluster - Big Data")

groups = cutree(bigdata.fit, k=5)
rect.hclust(bigdata.fit, k=5, border="blue")