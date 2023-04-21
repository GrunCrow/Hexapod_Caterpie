import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from sklearn.model_selection import train_test_split

from constantes import *


# Cargar los datos
train = pd.read_csv(CSV_PATH + "HexBug_Nano_train.csv")
val = pd.read_csv(CSV_PATH + "HexBug_Nano_val.csv")
test = pd.read_csv(CSV_PATH + "HexBug_Nano_test.csv")

# Creamos un generador de imágenes para el preprocesamiento
datagen = ImageDataGenerator(rescale=1./255)

# Cargamos las imágenes de entrenamiento con el generador de imágenes y aplicamos el preprocesamiento
train_generator = datagen.flow_from_dataframe(
        dataframe=train,
        x_col="filename",
        y_col="class",
        target_size=(TARGET_HEIGHT_IMG, TARGET_WIDTH_IMG),
        batch_size=BATCH_SIZE,
        class_mode='categorical')

# Cargamos las imágenes de validación con el generador de imágenes y aplicamos el preprocesamiento
val_generator = datagen.flow_from_dataframe(
        dataframe=val,
        x_col="filename",
        y_col="class",
        target_size=(TARGET_HEIGHT_IMG, TARGET_WIDTH_IMG),
        batch_size=BATCH_SIZE,
        class_mode='categorical')

# Cargamos las imágenes de test con el generador de imágenes y aplicamos el preprocesamiento
test_generator = datagen.flow_from_dataframe(
        dataframe=test,
        x_col="filename",
        y_col="class",
        target_size=(TARGET_HEIGHT_IMG, TARGET_WIDTH_IMG),
        batch_size=BATCH_SIZE,
        class_mode='categorical')

# Obtenemos el número de clases
num_classes = len(CLASSES)

# Imprimimos información de las imágenes cargadas
print("Número de imágenes de entrenamiento:", len(train_generator.filenames))
print("Número de imágenes de validación:", len(val_generator.filenames))
print("Número de imágenes de test:", len(test_generator.filenames))
print("Número de clases:", num_classes)
