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
print("Número de instancias generadas:", numero_instancias_generado)
print("Longitud media en carácteres de las instancias humanas:", longitud_media_humano)
print("Longitud media en carácteres de las instancias generadas:", longitud_media_generado)

# Balanceamos los datos para que haya el mismo número de textos humanos que generados
# Para ello primero vemos cual es el número minimo de instancias entre las dos clases
numero_minimo_instancias = 0
if numero_instancias_humanas > total_caracteres_generados:
    numero_minimo_instancias = total_caracteres_generados
else:
    numero_minimo_instancias = numero_instancias_humanas

# realizamos el subsampleo agrupando por label
datos_balanceados = datos.groupby("label").sample(n=numero_minimo_instancias, random_state=777)

# Asignamos un 80% de los datos a train y un 20% a test
train_df, test_df = train_test_split(datos_balanceados, test_size=0.2, random_state=42)

# Imprimimos estadísticas de train y de test
print("Número instancias en el training:", len(train_df["label"]))
print("Número instancias en el test:", len(test_df["label"]))  
print("Número instancias humanas en el training", (train_df["label"]=="humano").sum())
print("Número instancias generadas en el training", (train_df["label"]=="generado").sum())
print("Número instancias humanas en el test", (test_df["label"]=="humano").sum())
print("Número instancias generadas en el test", (test_df["label"]=="generado").sum())

# Datos de configuración para el entrenamiento modelo
max_instances_per_class = 5000
max_features = 20000 # Número máximo de características extraídas para nuestras instancias


# Vectorizar datos: extraer características de nuestros datos (desde texto hasta vectores numéricos)
vectorizer = TfidfVectorizer(max_features=max_features, stop_words="english", ngram_range=(1,1))
X_train = vectorizer.fit_transform(train_df["text"])
X_test = vectorizer.transform(test_df["text"])

# Vectorizar etiquetas: de texto a vectores numéricos
le = LabelEncoder()
Y_train = le.fit_transform(train_df["label"])
Y_test = le.transform(test_df["label"])

# Crear modelo 
model = LogisticRegression()

# train modelo
model.fit(X_train, Y_train)

# obtener predicciones de test
predictions = model.predict(X_test)

# Evaluar predicciones
print(classification_report(Y_test, predictions, target_names=le.classes_))

# Clasifica el texto introducido en custom_text
custom_texts = ["In the context of data science, machine learning, and data analysis, many algorithms make use of random numbers for initializing parameters, performing random data splits, among other tasks. Setting the random seed ensures that, even though the process uses random numbers, the results obtained are consistent and reproducible across different code runs."]
X_custom = vectorizer.transform(custom_texts)
preds = model.predict(X_custom)
print("Classification label:", le.classes_[preds[0]])