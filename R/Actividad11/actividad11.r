#Equipo:
#Daniel Fernando Baas Colonia
#Rodrigo Castilla López
#Luis Gerardo Castillo Pinkus
#Rafael Rodríguez Guzmán

#Instalamos paquetes necesarios
#install.packages("tm")
#install.packages("reshape")
#install.packages("SnowballC")
#install.packages("RColorBrewer")
#install.packages("wordcloud")
#install.packages("ggplot2")

#Importamos los paquetes
require(tm)
require(reshape)
require(SnowballC)
require(RColorBrewer)
require(wordcloud)
require(ggplot2)

#Crea una función para cargar archivos a R
https_function <- function(url, ...) {
    require(RCurl)
    
    #Carga y evalua cada script .r
    sapply(c(url, ...), function(u) {
        eval(parse(text = getURL(u, followlocation = TRUE, cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl"))), envir = .GlobalEnv)
    })
}

#Asigna un puntaje a cada palabra de acuerdo al sentimiento que expresa. Se basa en un rango de -1 a 1
score.sentiment = function(sentences, pos.words, neg.words, .progress='none')
{
	require(plyr)
	require(stringr)

	scores = laply(sentences, function(sentence, pos.words, neg.words) {
    
		word.list = str_split(sentence, '\\s+')
		words = unlist(word.list)
    
		pos.matches = match(words, pos.words)
		neg.matches = match(words, neg.words)
	
		pos.matches = !is.na(pos.matches)
		neg.matches = !is.na(neg.matches)

		score = sum(pos.matches) - sum(neg.matches)

		return(score)
	}, pos.words, neg.words, .progress=.progress )

	scores.df = data.frame(score=scores, text=sentences)
	return(scores.df)
}

#Cargamos el diccionario con palabras positivas de uso general
pos <- scan(file.path("/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/R/Actividad11/files", "positive-words.txt"), what = "character", comment.char = ';')

#Cargamos el diccionario con palabras positivas de términos financieros
pos_finance <- scan(file.path("/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/R/Actividad11/files", "LoughranMcDonald_pos.csv"), what = "character", comment.char = ';')

#Combinamos los diccionarios de palabras positivas en un solo
pos_all <- c(pos, pos_finance)

#Cargamos el diccionario de palabras negativas de uso general
neg <- scan(file.path("/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/R/Actividad11/files", "negative-words.txt"), what = "character", comment.char = ';')

#Cargamos el diccionar de palabras negativas de términos financieros
neg_finance <- scan(file.path("/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/R/Actividad11/files", "LoughranMcDonald_neg.csv"), what = "character", comment.char = ';')

#Combinamos los diccionarios de palabras negativas en uno solo
neg_all <- c(neg, neg_finance)

#Leemos el Beige Book completo
bb <-read.csv("/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/R/Actividad11/files/beigebook_summary.csv")

#Muestra el nombre de las columnas en el dataframe
colnames(bb)

#Muestra una matriz que indica datos faltantes en los meses de los años contenidos en el dataframe
#cast(bb, year ~ month, length)

#Crea un objeto que almacena los datos faltantes de bb
bad <- is.na(bb)

#Muestra los elementos faltantes. Podemos usar !bad[bb] para retornar todos los elementos que si se encuentran
bb[bad]

#Limpiamos los datos de signos de puntuación
bb$text<- gsub('[[:punct:]]', ' ', bb$text)

#Limpiamos los datos de caracteres sin salida, como backspace o tabs
bb$text<- gsub('[[:cntrl:]]', ' ', bb$text)

#Limpiamos los datos de caracteres numéricos rodeados por espacios
bb$text<- gsub('\\d+', ' ', bb$text)

#Damos formato al frame y limpiamos los datos, mostrando el texto y la fecha
bb.text <- as.data.frame(bb$text)
bb.text$year<- bb$year
bb.text$Date <- as.Date( paste(bb$year, bb$month, bb$day, sep = "-") , format ="%Y-%m-%d" )
bb.text$Date <- strptime(as.character(bb.text$Date), "%Y-%m-%d")
colnames(bb.text) <- c("text", "year", "date")
colnames(bb.text)

#Combinamos dos cadenas y las asignamos al objeto
example_docs<- c("this is an useful example", "augmented by another useful example")
#Muestra el contenido del objeto
example_docs
#Muestra el tipo de dato del objeto
class(example_docs)

#Creamos un corpus
example_corpus<- Corpus(VectorSource(example_docs))
#Mostramos el corpus
example_corpus

#Creamos el corpus a trabajar
bb_corpus<- Corpus(VectorSource(bb.text))

#Vemos qué transformaciones se le han aplicado
getTransformations()

#Warning message:
#In tm_map.SimpleCorpus(bb_corpus, tolower) : transformation drops documents
#Convierte las cadenas a minúsculas
bb_corpus<- tm_map(bb_corpus, tolower)

#Vemos el contenido del corpus
#Show Object Exception: No such file o directory
View(inspect(bb_corpus))

#Warning message:
#In tm_map.SimpleCorpus(bb_corpus, stemDocument) : transformation drops documents
bb.text_stm<- tm_map(bb_corpus, stemDocument)

#Stopwords stopwords
stnd.stopwords<- stopwords("SMART")
head(stnd.stopwords)
length(stnd.stopwords)

#Añadimos stopwords específicas para el tema y las combinamos con las estándar
bb.stopwords<- c(stnd.stopwords, "district", "districts",
"reported", "noted", "city", "cited",
"activity", "contacts",
"chicago", "dallas", "kansas", "san", "richmond", "francisco",
"cleveland", "atlanta", "sales", "boston", "york", "philadelphia",
"minneapolis", "louis",
"services","year", "levels", " louis")

length(bb.stopwords)

#Limpiamos palabras que carecen de poder discriminatorio
#bb.tf será usado como punto de control para la creación de nuestra matriz term-document
bb.tf <- list(weighting = weightTf, stopwords = bb.stopwords,
removePunctuation = TRUE,
tolower = TRUE,
minWordLength = 4,
removeNumbers = TRUE)

#Creamos una matrix term-document
bb_tdm<- TermDocumentMatrix(bb_corpus, control = bb.tf)

dim(bb_tdm)
bb_tdm
class(bb_tdm)

#Obtenemos todos los términos
Terms(bb_tdm)

#Elimina stopwords por su uso repetido
bb.frequent<- sort(rowSums(as.matrix(bb_tdm)), decreasing = TRUE)

#Suma de todos los términos
sum(bb.frequent)

bb.frequent[1:30]

#Mira a los términos con frecuencia mínima
findFreqTerms(bb_tdm, lowfreq = 60)

#Añadimos más palabras positivas
pos.words<- c(pos_all, "spend", "buy", "earn", "hike", "increase",
"increases",
"development", "expansion", "raise", "surge", "add",
"added", "advanced", "advances",
"boom", "boosted", "boosting",
"waxed", "upbeat", "surge")

#Añadimos más palabras negativas
neg.words = c(neg_all, "earn", "shortfall", "weak", "fell",
"decreases", "decreases",
"decreased", "contraction", "cutback",
"cuts", "drop", "shrinkage", "reduction",
"abated", "cautious",
"caution", "damped", "waned", "undermine", "unfavorable",
"soft",
"softening", "soften", "softer", "sluggish", "slowed", "slowdown",
"slower",
"recession")

#True si la palabra ya se encuentra en el diccionario, false de lo contrario
any(pos.words == "strong")
any(pos.words == "increases")

#Encuentra asociaciones con relaciones mayores a 0.5
findAssocs(bb_tdm, "demand", 0.5)
findAssocs(bb_tdm, "increased", 0.5)
findAssocs(bb_tdm, "growth", 0.5)

#Remueve términos esparsos de la matriz con un valor de .95
bb.95 <- removeSparseTerms(bb_tdm, .95)

#Ordenando y contando la suma de las filas
bb.rsums <- sort(rowSums(as.matrix(bb.95)), decreasing=TRUE)

#Creamos un data frame con las palabras y sus frecuencias
bbdf.rsums <- data.frame(word=names(bb.rsums), freq=bb.rsums)

#Mostramos los nombres de las columnas
colnames(bbdf.rsums)

#Crea una imagen png
png(filename="/home/rafael/Dropbox/LIS/7mo semestre/Manejo de Datos no Estructurados/Actividades/R/Actividad11/img1.png")

#Crea una nube de palabras
#Warning messages:
#1: In wordcloud(bbdf.rsums$word, bbdf.rsums$freq, scale = c(7, 0.2),  :
#  wday could not be fit on page. It will not be plotted.
#2: In wordcloud(bbdf.rsums$word, bbdf.rsums$freq, scale = c(7, 0.2),  :
#  yday could not be fit on page. It will not be plotted.
bb_wordcloud <- wordcloud(bbdf.rsums$word, bbdf.rsums$freq, scale=c(7,.2), min.freq=4, max.words=200, random.order=FALSE, colors=palette)

#Termina la imagen y guarda la imagen
dev.off()

b.keeps <- bb.text[,c("date", "year")]

#Ejecuta el análsis de sentimientos con score.sentiment usando las palabras positivas y negativas
bb.score<- score.sentiment(bb.text$text, pos.words, neg.words, .progress = 'text')
bb.sentiment <- cbind(bb.keeps, bb.score)
colnames(bb.sentiment)

#Cálculo de la media
bb.sentiment$mean <- mean(bb.sentiment$score)
#Cálculo de la suma
bb.sum <- bb.sentiment$score
bb.sentiment$centered <- bb.sum - bb.sentiment$mean
bb.sentiment$pos[bb.sentiment$centered>0] <- 1
bb.sentiment$neg[bb.sentiment$centered<0] <- 1

#Error in as.POSIXlt.numeric(value) : 'origin' must be supplied
bb.sentiment[is.na(bb.sentiment)] <- 0

sum(bb.sentiment$pos)

#Crea un histograma
bb.hist <- hist(bb.sentiment$score, main="Sentiment Histogram", xlab="Score", ylab="Frequency")
bb.hist <- hist(bb.sentiment$centered, main="Sentiment Histogram", xlab="Score", ylab="Frequency")

#Crea una gráfica boxplot
bb.boxplot<- ggplot(bb.sentiment, aes(x = bb.sentiment$year, y = bb.sentiment$centered, group = bb.text$year)) + 
geom_boxplot(aes(fill = bb.sentiment$year), outlier.colour = "black", outlier.shape = 16, outlier.size = 2)

#Añade etiquetas a la gráfica
#No se generó la gráfica
bb.boxplot<- bb.boxplot + xlab("Year") + ylab("Sentiment(Centered)") + ggtitle("Economic Sentiment - Beige Book (2011-2013)")

rect2001 <- data.frame (xmin=2001, xmax=2002, ymin=-Inf, ymax=Inf)
rect2007 <- data.frame (xmin=2007, xmax=2009, ymin=-Inf, ymax=Inf)

bb.boxplot <- ggplot(bb.sentiment, aes(x=bb.sentiment$year, y=bb.sentiment$centered, group=bb.sentiment$year))
bb.boxplot <- bb.boxplot + geom_boxplot(outlier.colour = "black", outlier.shape = 16, outlier.size = 2)
bb.boxplot <- bb.boxplot + geom_rect(data=rect2001, aes(xmin=xmin, xmax=xmax, ymin=-Inf, ymax=+Inf), fill='pink', alpha=0.2, inherit.aes = FALSE)
bb.boxplot <- bb.boxplot + geom_rect(data=rect2007, aes(xmin=xmin, xmax=xmax, ymin=-Inf, ymax=+Inf), fill='pink', alpha=0.2, inherit.aes = FALSE)
bb.boxplot <- bb.boxplot + xlab("Date") + ylab("Sentiment(Centered)") + ggtitle("Economic Sentiment - Beige Book (1996-2010)")
bb.boxplot