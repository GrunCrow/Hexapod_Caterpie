import pandas as pd
import os

from constantes import *

# Definimos ruta del Dataset
DATASET_PATH = "../Dataset/"

# Creamos una lista con los nombres de los archivos CSV
csv_files = [os.path.join(DATASET_PATH, "CSVs", c + ".csv") for c in CLASSES]

# Creamos una lista vacía para almacenar los DataFrames de cada archivo CSV
dfs = []

# Leemos cada archivo CSV y lo agregamos a la lista de DataFrames
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    dfs.append(df)

# Concatenamos los DataFrames en un solo DataFrame
merged_df = pd.concat(dfs)

# Guardamos el DataFrame combinado en un archivo CSV
merged_df.to_csv(os.path.join(DATASET_PATH, "CSVs", "HexBug_Nano.csv"), index=False)
