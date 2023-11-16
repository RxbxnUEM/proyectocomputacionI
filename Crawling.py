import requests
import json

links = []

# A partir del código obtenido en Serper obtenemos la información de varias páginas
def crawl_url(url):

    for page_number in range(1, 6):
            payload = json.dumps({
            "q": "site:sharegpt.com",
            "page": page_number,
            "num": 100
            })
            headers = {
            'X-API-KEY': '75e47a41b5e58073ba89845c02fdd6cb1a3cbc94',
            'Content-Type': 'application/json'
            }
        
            response = requests.request("POST", url, headers=headers, data=payload)

            # Accedemos a organic dentro del json
            paginas = response.json()["organic"]

            # Recorremos los elementos del json y agregamos las url a la lista links
            for pagina in paginas:
                if "ShareGPT conversation" in pagina["title"]:
                    enlace = pagina["link"]
                    links.append(enlace)

    return links