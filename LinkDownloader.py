import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Nombre del archivo que contiene las urls a descargar
archivo_urls = "urls.txt"

# Directorio de descarga de los archivos
directorio_descarga = "descargas"

# Obtener el número del último archivo descargado
if not os.path.exists(directorio_descarga):
    os.makedirs(directorio_descarga)
files = os.listdir(directorio_descarga)
last_file_num = max([int(f.split(".")[0]) for f in files]) if files else 0

# Abrir el archivo de urls
with open(archivo_urls, "r", encoding="utf-8") as f:
    urls = f.read().splitlines()

# Pedir al usuario el número a partir del cual se debe continuar descargando
continuar_desde = input("¿A partir de qué número de archivo desea continuar descargando? (0 para comenzar desde el principio): ")
try:
    continuar_desde = int(continuar_desde)
    if continuar_desde < 0:
        continuar_desde = 0
except:
    continuar_desde = 0

# Descargar archivos en paralelo
def descargar_archivo(url, nombre_archivo):
    ruta_archivo = os.path.join(directorio_descarga, nombre_archivo)

    # Descargar archivo
    print(f"Descargando {nombre_archivo}...")
    try:
        response = requests.get(url)
        with open(ruta_archivo, "wb") as f:
            f.write(response.content)
        print(f"Descarga de {nombre_archivo} completa.")
    except Exception as e:
        print(f"Error al descargar {nombre_archivo}: {str(e)}")
        # Esperar un tiempo y volver a intentar
        time.sleep(60)
        try:
            response = requests.get(url)
            with open(ruta_archivo, "wb") as f:
                f.write(response.content)
            print(f"Descarga de {nombre_archivo} completa.")
        except Exception as e:
            print(f"Error al descargar {nombre_archivo}: {str(e)}")
            # Esperar un tiempo adicional y volver a intentar
            time.sleep(120)
    
with ThreadPoolExecutor() as executor:
    # Descargar archivos en paralelo
    futures = []
    for i, url in enumerate(urls[continuar_desde:]):
        num_archivo = i + continuar_desde + 1
        nombre_archivo = f"{num_archivo}.mp3"
        futures.append(executor.submit(descargar_archivo, url, nombre_archivo))
        
    # Esperar a que se completen todas las descargas
    for future in futures:
        future.result()
    
print("Descarga completa.")

# Crear lista de URLs que no se pudieron descargar y motivo
errores_descarga = []
for i, url in enumerate(urls[continuar_desde:]):
    num_archivo = i + continuar_desde + 1
    nombre_archivo = f"{num_archivo}.mp3"
    ruta_archivo = os.path.join(directorio_descarga, nombre_archivo)

    if not os.path.exists(ruta_archivo):
        errores_descarga.append((url, "Archivo no descargado"))
    elif os.path.getsize(ruta_archivo) == 0:
        errores_descarga.append((url, "Archivo vacío"))

# Escribir lista de errores en archivo de texto
if errores_descarga:
    with open("errores.txt", "w") as f:
        for url, mensaje in errores_descarga:
            f.write(f"{url}\t{mensaje}\n")
    print("Se han registrado errores de descarga. Verifique el archivo 'errores.txt' para más información.")
