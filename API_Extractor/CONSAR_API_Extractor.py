import requests # this for API requests
import pandas as pd # This to handle the data
import json # to handle JSON files
from io import BytesIO, StringIO # For reading XLSX and CSV files
import os

# URL of the API 
api_url = "https://datos.gob.mx/busca/api/3/action/package_search?fq=organization:consar"

# Get a dataset list 
response = requests.get(api_url)
if response.status_code != 200:
    print(f"Error: No se pudo obtener los datos (Código {response.status_code})")
    exit()

# Convert the response into JSON format
data = response.json()

# Check that the format is correct
if "result" not in data or "results" not in data["result"]:
    print("Error: La respuesta de la API no contiene datos válidos.")
    exit()

# Extract the dataset list
datasets = data["result"]["results"]

# Directory on where to keep the download files
download_dir = "datos_consar"
os.makedirs(download_dir, exist_ok=True)

# Iterate over the datasets and extract the files
for dataset in datasets:
    print(f"\n Dataset: {dataset['title']}")

    for resource in dataset.get("resources", []):
        file_url = resource.get("url", "")
        file_format = resource.get("format", "").lower()
        file_name = resource.get("name", "").replace(" ", "_")  # Limpiar nombre

        if not file_url:
            continue

        print(f"Downloading {file_name} ({file_format})...")

        # Download the file
        file_response = requests.get(file_url)
        if file_response.status_code != 200:
            print(f"Error wile downloading {file_url}")
            continue

        # Saving it according to the file type
        if "csv" in file_format:
            df = pd.read_csv(StringIO(file_response.text))
            df.to_csv(os.path.join(download_dir, f"{file_name}.csv"), index=False)
            print(f"Saved as {file_name}.csv")
            print(df.head())

        elif "json" in file_format:
            json_data = file_response.json()
            with open(os.path.join(download_dir, f"{file_name}.json"), "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            print(f"Saved as {file_name}.json")

        elif "xlsx" in file_format or "excel" in file_format:
            df = pd.read_excel(BytesIO(file_response.content), engine="openpyxl")
            df.to_excel(os.path.join(download_dir, f"{file_name}.xlsx"), index=False)
            print(f"Saved as {file_name}.xlsx")
            print(df.head())

        else:
            print(f"Not supported file: {file_format}")

print("\n Extraction completed")
