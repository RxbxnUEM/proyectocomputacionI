import pandas as pd

# leemos el dataset generado
datos = pd.read_csv('dataset.tsv', sep="\t")

isntancias_humanas = 0
instancias_generado = 0
longitud_total_humano = 0
longitud_total_generado = 0

# recorremos el dataset para obtener sus estadísticas (1º parte punto 4 de la actividad )
for i in range(len(datos)):
    texto = datos["text"][i]
    label = datos["label"][i]

    if label == 'humano':
        isntancias_humanas += 1
        longitud_total_humano += len(texto)
    else:
        instancias_generado += 1
        longitud_total_generado += len(texto)

longitud_media_humano = longitud_total_humano / isntancias_humanas
longitud_media_generado = longitud_total_generado / instancias_generado

print("Número de instancias en el dataset: ", len(datos))
print("Número de instancias humanas:", isntancias_humanas)
print("Número de instancias generadass:", instancias_generado)
print("Longitud media de textos humanos:", longitud_media_humano)
print("Longitud media de textos generados:", longitud_media_generado)
