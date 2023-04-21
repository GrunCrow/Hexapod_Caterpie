import cv2
import os
import pandas as pd

from constantes import *

# Creamos una lista con las clases disponibles
# CLASSES = ['1_NanoBug_Azul', '2_NanoBug_Negro', '3_NanoBug_Celeste', '4_NanoBug_Blanco', '5_NanoBug_GrisClaro', '6_NanoBug_GrisOscuro', '7_NanoBug_Naranja']

# Definimos NanoBug a procesar
NANOBUG_NAME = CLASSES[6]

# Definimos la ruta del vídeo
VIDEO_NAME = "naranja.mp4"
VIDEO_PATH = DATASET_PATH + NANOBUG_NAME + "/" + VIDEO_NAME

# Definimos el nombre del archivo CSV donde se guardarán las etiquetas
CSV_PATH = DATASET_PATH + "/CSVs/" + NANOBUG_NAME + ".csv"

# Creamos la carpeta de imágenes si no existe
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Leemos el vídeo
cap = cv2.VideoCapture(VIDEO_PATH)

# Definimos el nombre del archivo
file_name = NANOBUG_NAME

# Inicializamos el contador de imágenes
count = 0

# Creamos una lista para almacenar las etiquetas
labels = []

# Leemos el vídeo cuadro por cuadro
while cap.isOpened():
    # Leemos el cuadro
    ret, frame = cap.read()

    # Si no hay más cuadros, salimos del bucle
    if not ret:
        break

    # Redimensionamos el cuadro para que sea más rápido el proceso de grabado de la imagen
    frame = cv2.resize(frame, (TARGET_WIDTH_IMG, TARGET_HEIGHT_IMG))

    # Dibujamos el cuadro con el nombre del archivo y el número de cuadro
    # cv2.putText(frame, "{}_{}".format(file_name, count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Guardamos la imagen y añadimos la etiqueta a la lista de etiquetas
    '''image_name = "{}_{}.jpg".format(file_name, count)
    cv2.imwrite(os.path.join(IMAGE_DIR, image_name), frame)
    labels.append({"path": os.path.join(IMAGE_DIR, image_name), "class": CLASSES[int(input("Introduce el número de clase (1-7): ")) - 1]})'''
    # Etiqueta automáticamente las cucarachas
    label = NANOBUG_NAME
    # Añade la imagen y la etiqueta a la lista de etiquetas
    image_name = "{}_{}.jpg".format(file_name, count)
    cv2.imwrite(os.path.join(IMAGE_DIR, image_name), frame)
    labels.append({"path": os.path.join(IMAGE_DIR, image_name), "class": label})


    # Incrementamos el contador de imágenes
    count += 1

    # Mostramos el cuadro
    cv2.imshow("Video", frame)

    # Esperamos la pulsación de una tecla
    key = cv2.waitKey(1)

    # Si se pulsa la tecla "q", salimos del bucle
    if key == ord('q'):
        break

# Creamos un DataFrame con las etiquetas
df_labels = pd.DataFrame(labels)

# Guardamos el DataFrame en un archivo CSV
df_labels.to_csv(CSV_PATH, index=False)