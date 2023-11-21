import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# leemos el dataset generado
datos = pd.read_csv('dataset.tsv', sep="\t")

numero_instancias_humanas = 0
numero_instancias_generado = 0
total_caracteres_humanos = 0
total_caracteres_generados = 0

# recorremos el dataset para obtener sus estadísticas (1º parte punto 4 de la actividad )
for i in range(len(datos)):
    texto = datos["text"][i]
    label = datos["label"][i]
    if label == 'humano':
        numero_instancias_humanas += 1
        total_caracteres_humanos += len(texto)
    else:
        numero_instancias_generado += 1
        total_caracteres_generados += len(texto)

longitud_media_humano = total_caracteres_humanos / numero_instancias_humanas
longitud_media_generado = total_caracteres_generados / numero_instancias_generado

# imprimos las estadísticas del dataset
print("Número de instancias en el dataset:", len(datos))
print("Número de instancias humanas:", numero_instancias_humanas)
print("Número de instancias generadass:", total_caracteres_generados)
print("Longitud media de textos humanos:", longitud_media_humano)
print("Longitud media de textos generados:", longitud_media_generado)

# Balanceamos los datos para que haya el mismo número de textos humanos que generados
# Para ello primero vemos cual es el número minimo de instancias entre las dos clases
numero_minimo_instancias = 0
if numero_instancias_humanas > total_caracteres_generados:
    numero_minimo_instancias = total_caracteres_generados
else:
    numero_minimo_instancias = numero_instancias_humanas

# realizamos el subsampleo agrupando por label
datos_balanceados = datos.groupby("label").sample(n=numero_minimo_instancias, random_state=777)

numero_instancias_humanas = (datos_balanceados["label"]=="humano").sum()
total_caracteres_generados = (datos_balanceados["label"]=="generado").sum()
print("numero instancias humanas después de balanceo: ", numero_instancias_humanas)
print("numero instancias ChatGPT después de balanceo: ", total_caracteres_generados)

# Asignamos un 80% de los datos a train y un 20% a test
train_df, test_df = train_test_split(datos_balanceados, test_size=0.2, random_state=42)
print("isntancias en train:", len(train_df["label"]))
print("instancias en test:", len(test_df["label"]))  
print("Instancias en train de humanos", (train_df["label"]=="humano").sum())
print("Instancias en train de generado", (train_df["label"]=="generado").sum())
print("Instancias en test de humanos", (test_df["label"]=="humano").sum())
print("Instancias en test de generado", (test_df["label"]=="generado").sum())



# data paths and config
max_instances_per_class = 5000
max_features = 20000 # maximum number of features extracted for our instances
id2label = {0: "human", 1: "machine"}

# vectorize data: extract features from our data (from text to numeric vectors)
vectorizer = TfidfVectorizer(max_features=max_features, stop_words="english", ngram_range=(1,1))
X_train = vectorizer.fit_transform(train_df["text"])
X_test = vectorizer.transform(test_df["text"])

# vectorize labels : from text to numeric vectors
le = LabelEncoder()
Y_train = le.fit_transform(train_df["label"])
Y_test = le.transform(test_df["label"])

# create model
model = LogisticRegression()

# train model
model.fit(X_train, Y_train)

# get test predictions
predictions = model.predict(X_test)

# evaluate predictions
target_names = [label for idx, label in id2label.items()]
print(classification_report(Y_test, predictions, target_names=target_names))

# classify your own text
custom_texts = ["I'm ChatGPT, your virtual assistant, and I'm generating texts"]
X_custom = vectorizer.transform(custom_texts)
preds = model.predict(X_custom)
print("Classification label:", target_names[preds[0]])