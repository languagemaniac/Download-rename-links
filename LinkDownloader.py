import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Name of the file where the URLs are
archivo_urls = "urls.txt"

# File download folder
directorio_descarga = "Downloads"

# Get the number of the last downloaded file
if not os.path.exists(directorio_descarga):
    os.makedirs(directorio_descarga)
files = os.listdir(directorio_descarga)
last_file_num = max([int(f.split(".")[0]) for f in files]) if files else 0

# Open the URL list textfile
with open(archivo_urls, "r", encoding="utf-8") as f:
    urls = f.read().splitlines()

# Ask the user for the number from which to continue downloading
continuar_desde = input("From what file number do you want to continue downloading? (0 to start from the beginning): ")
try:
    continuar_desde = int(continuar_desde)
    if continuar_desde < 0:
        continuar_desde = 0
except:
    continuar_desde = 0

# Download files in parallel
def descargar_archivo(url, nombre_archivo):
    ruta_archivo = os.path.join(directorio_descarga, nombre_archivo)

    # Download files
    print(f"Downloading {nombre_archivo}...")
    try:
        response = requests.get(url)
        with open(ruta_archivo, "wb") as f:
            f.write(response.content)
        print(f"{nombre_archivo} Downloaded.")
    except Exception as e:
        print(f"Error downloading {nombre_archivo}: {str(e)}")
        # Wait some time and try again
        time.sleep(60)
        try:
            response = requests.get(url)
            with open(ruta_archivo, "wb") as f:
                f.write(response.content)
            print(f"{nombre_archivo} Downloaded.")
        except Exception as e:
            print(f"Error when downloading {nombre_archivo}: {str(e)}")
            # Wait some more time and try again
            time.sleep(120)
    
with ThreadPoolExecutor() as executor:
    # Download files in parallel
    futures = []
    for i, url in enumerate(urls[continuar_desde:]):
        num_archivo = i + continuar_desde + 1
        nombre_archivo = f"{num_archivo}.mp3"
        futures.append(executor.submit(descargar_archivo, url, nombre_archivo))
        
    # Wait for all the downloads to finish
    for future in futures:
        future.result()
    
print("Download completed")

# Create list with the URLs that couldn't be downloaded and the reason for that
errores_descarga = []
for i, url in enumerate(urls[continuar_desde:]):
    num_archivo = i + continuar_desde + 1
    nombre_archivo = f"{num_archivo}.mp3"
    ruta_archivo = os.path.join(directorio_descarga, nombre_archivo)

    if not os.path.exists(ruta_archivo):
        errores_descarga.append((url, "File not downloaded"))
    elif os.path.getsize(ruta_archivo) == 0:
        errores_descarga.append((url, "Empty file"))

# Write error list in a text file
if errores_descarga:
    with open("errors.txt", "w", encoding="utf-8") as f:
        for url, mensaje in errores_descarga:
            f.write(f"{url}\t{mensaje}\n")
    print("Download errors have been recorded. Check the 'errors.txt' file for more information.")
