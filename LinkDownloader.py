import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

# Name of the file where the URLs are
url_file = "urls.txt"

# File download folder
download_folder = "Downloads"

# Get the number of the last downloaded file
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
files = os.listdir(download_folder)
last_file_num = max([int(f.split(".")[0]) for f in files]) if files else 0

# Open the URL list textfile
with open(url_file, "r", encoding="utf-8") as f:
    urls = f.read().splitlines()

# Ask the user for the number from which to continue downloading
continue_from = input("From what file number do you want to continue downloading? (0 to start from the beginning): ")
try:
    continue_from = int(continue_from)
    if continue_from < 0:
        continue_from = 0
except:
    continue_from = 0

# Download files in parallel
def download_file(url, file_name):
    file_path = os.path.join(download_folder, file_name)

    # Download files
    print(f"Downloading {file_name}...")
    try:
        response = requests.get(url)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"{file_name} Downloaded.")
    except Exception as e:
        print(f"Error downloading {file_name}: {str(e)}")
        # Wait some time and try again
        time.sleep(60)
        try:
            response = requests.get(url)
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"{file_name} Downloaded.")
        except Exception as e:
            print(f"Error when downloading {file_name}: {str(e)}")
            # Wait some more time and try again
            time.sleep(120)
    
with ThreadPoolExecutor() as executor:
    # Download files in parallel
    futures = []
    for i, url in enumerate(urls[continue_from:]):
        file_num = i + continue_from + 1
        file_name = f"{file_num}.mp3"
        futures.append(executor.submit(download_file, url, file_name))
        
    # Wait for all the downloads to finish
    for future in futures:
        future.result()
    
print("Download completed")

# Create list with the URLs that couldn't be downloaded and the reason for that
download_errors = []
for i, url in enumerate(urls[continue_from:]):
    file_num = i + continue_from + 1
    file_name = f"{file_num}.mp3"
    file_path = os.path.join(download_folder, file_name)

    if not os.path.exists(file_path):
        download_errors.append((url, "File not downloaded"))
    elif os.path.getsize(file_path) == 0:
        download_errors.append((url, "Empty file"))

# Write error list in a text file
if download_errors:
    with open("errors.txt", "w", encoding="utf-8") as f:
        for url, message in download_errors:
            f.write(f"{url}\t{message}\n")
    print("Download errors have been recorded. Check the 'errors.txt' file for more information.")
