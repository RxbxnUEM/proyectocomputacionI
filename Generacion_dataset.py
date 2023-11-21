# Script en el que se ejecuta el crwaling, scraping, limpieza de los datos y generación del dataset

from Crawling import crawl_url
from bs4 import BeautifulSoup
import requests
from langdetect import detect, LangDetectException
import pandas as pd

# url que vamos a pasar al crwaler
url = "https://google.serper.dev/search"

# LLamada al crwaler para obtener la lista de links (punto 1 de la actividad)
links = []
links = crawl_url(url) 
print("Número de enlaces:", len(links))

# Variables auxiliares donde guardamos los datos originales obtenidos de las páginas web
datos_humanos_originales = []
datos_IA_originales = []

# Obtención de los textos existentes en las urls (punto 2 de la actividad)
for link in links:
    resultado = requests.get(link)

    # Recuperamos el HTML de la web
    contenido = resultado.text
        
    # Parseamos el HTML con beautifulsoup
    soup = BeautifulSoup(contenido, 'html.parser')

    # Buscamos los textos escritos por humanos
    textos_humanos = soup.find_all('p', class_='pb-2 whitespace-prewrap')
    # Reemplazamos los saltos de línea y las tabulaciones por espacios en blanco
    for texto in textos_humanos:
        instancia = texto.get_text().replace('\n', ' ').replace('\t', ' ')
        datos_humanos_originales.append(instancia)

    # Buscamos los textos escritos por IA
    textos_IA = soup.find_all('div', class_="utils_response__b5jEi")
    # Extraemos todo el texto que forme parte de los siguientes tipos de campos: ["p", "h1", "h2", "h3", "b", "p", "a"]
    # esto es necesario porque ChatGPT puede formatear sus respuestas utilizando código en html
    for texto in textos_IA:
        parrafos = texto.find_all(["p", "h1", "h2", "h3", "b", "a"])
        # Concatenamos los string obtenidos para conseguir la respuesta completa de ChatGPT
        # y reemplazamos los saltos de línea y las tabulaciones por espacios en blanco
        instancia = ""
        for parrafo in parrafos:
            instancia += parrafo.get_text().replace('\n', ' ').replace('\t', ' ') + " "
        datos_IA_originales.append(instancia)  

# Almacenamos en esta variable todos los datos originales indicando en la etiqueta si lo escribió un humano o si fue generado
datos_extraidos = {"text":[], "label":[]} 
for dato in datos_humanos_originales:
     datos_extraidos["text"].append(dato)
     datos_extraidos["label"].append("humano")
for dato in datos_IA_originales:
     datos_extraidos["text"].append(dato)
     datos_extraidos["label"].append("generado")

# Creamos un DataFrame con los datos extraidos
df_datos_extraidos = pd.DataFrame(datos_extraidos)

# Guardamos los datos extraidos en un archivo con formato tsv
df_datos_extraidos.to_csv('datos_extraidos.tsv', sep='\t', index=False)


# Comienzamos con el punto 3 de la actividad, Limpieza y almacenamiento del dataset

# Eliminamos duplicados de las listas utilizando la función set
datos_humanos_sin_duplicados = list(set(datos_humanos_originales))
datos_IA_sin_duplicados = list(set(datos_IA_originales))

# Eliminamos los textos de menos de 20 caracteres
datos_humanos_grandes = []
datos_IA_grandes = []
for texto in datos_humanos_sin_duplicados:
     if len(texto) > 19:
          datos_humanos_grandes.append(texto)
for texto in datos_IA_sin_duplicados:
     if len(texto) > 19:
          datos_IA_grandes.append(texto)

# Eliminamos los textos que no son en inglés
datos_humanos = []
datos_IA = []
for texto in datos_humanos_grandes:
    try:
        if detect(texto) == "en":
            datos_humanos.append(texto)
    except LangDetectException as e:
        # Si falla la deteción de idioma imprimos un mesaje de error
        print(f"Error al detectar el idioma: {e}")
for texto in datos_IA_grandes:
    try:
        if detect(texto) == "en":
            datos_IA.append(texto)
    except LangDetectException as e:
        # Si falla la deteción de idioma imprimos un mesaje de error
        print(f"Error al detectar el idioma: {e}")


# Almacenamos en esta variable todos los datos indicando en la etiqueta si lo escribió un humano o si fue generado
datos = {"text":[], "label":[]} 
for dato in datos_humanos:
     datos["text"].append(dato)
     datos["label"].append("humano")
for dato in datos_IA:
     datos["text"].append(dato)
     datos["label"].append("generado")

# Imprimimos estadísticas del dataset
print("Instancias totales del dataset: ", len(datos_humanos) + len(datos_IA))
print("Instancias humanas ", len(datos_humanos))
print("Instancias IA ", len(datos_IA))

# Creamos un DataFrame con los datos
df = pd.DataFrame(datos)

# Guardamos el dataset en un archivo con formato tsv
df.to_csv('dataset.tsv', sep='\t', index=False)
