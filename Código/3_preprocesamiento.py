import pandas as pd
import cv2
import numpy as np
import os

from sklearn.model_selection import train_test_split # para crear la división estratificada

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

from constantes import *

'''
Preprocesar las imágenes para que tengan un tamaño fijo y normalizarlas.

Definir la arquitectura de la red neuronal, por ejemplo, una red convolucional.

Compilar la red neuronal, seleccionando una función de pérdida, un optimizador y una métrica para evaluar el desempeño de la red.

Entrenar la red neuronal en los datos de entrenamiento, utilizando la función de pérdida y el optimizador seleccionados, y evaluando el desempeño en los datos de validación.

Ajustar los hiperparámetros de la red neuronal, como el número de capas, el tamaño del kernel, el tamaño del lote, etc.

Evaluar el desempeño de la red neuronal en los datos de prueba.

Guardar la red neuronal entrenada para su uso futuro.
'''

# Definimos la ruta del directorio donde se encuentran las imágenes
IMAGE_DIR = "../Dataset/imagenes/"

# Definimos la ruta donde se guardarán las imágenes preprocesadas
PREPROCESSED_DIR = "../Dataset/preprocessed_images/"

# Creamos el directorio si no existe
if not os.path.exists(PREPROCESSED_DIR):
    os.makedirs(PREPROCESSED_DIR)

# Definimos la función para preprocesar las imágenes
def preprocess_image(image_path):
    # Cargamos la imagen
    image = cv2.imread(image_path)
    # Convertimos la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Aplicamos un filtro gaussiano para suavizar la imagen y reducir el ruido
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Aplicamos la técnica de umbralización adaptativa para binarizar la imagen
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # Cambiamos el tamaño de la imagen a 128x128 píxeles
    resized = cv2.resize(thresh, (128, 128), interpolation=cv2.INTER_AREA)
    # Devolvemos la imagen preprocesada
    return resized

# Cargamos el CSV de train
train_df = pd.read_csv(CSV_TRAIN_HEXBUG_NANO)

# Preprocesamos las imágenes de train y las guardamos en el directorio correspondiente
for index, row in train_df.iterrows():
    image_path = os.path.join(IMAGE_DIR, row['filename'])
    preprocessed_image = preprocess_image(image_path)
    preprocessed_image_path = os.path.join(PREPROCESSED_DIR, row['filename'])
    cv2.imwrite(preprocessed_image_path, preprocessed_image)

# Cargamos el CSV de test
test_df = pd.read_csv(CSV_TEST_HEXBUG_NANO)

# Preprocesamos las imágenes de test y las guardamos en el directorio correspondiente
for index, row in test_df.iterrows():
    image_path = os.path.join(IMAGE_DIR, row['filename'])
    preprocessed_image = preprocess_image(image_path)
    preprocessed_image_path = os.path.join(PREPROCESSED_DIR, row['filename'])
    cv2.imwrite(preprocessed_image_path, preprocessed_image)

# Cargamos el CSV de validation
val_df = pd.read_csv(CSV_VALIDATION_HEXBUG_NANO)

# Preprocesamos las imágenes de validation y las guardamos en el directorio correspondiente
for index, row in val_df.iterrows():
    image_path = os.path.join(IMAGE_DIR, row['filename'])
    preprocessed_image = preprocess_image(image_path)
    preprocessed_image_path = os.path.join(PREPROCESSED_DIR, row['filename'])
    cv2.imwrite(preprocessed_image_path, preprocessed_image)
