import pandas as pd
from sklearn.model_selection import train_test_split # para crear la división estratificada

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator

from constantes import *

'''
Preprocesar las imágenes para que tengan un tamaño fijo y normalizarlas.

Dividir el conjunto de datos en entrenamiento, validación y prueba.

Definir la arquitectura de la red neuronal, por ejemplo, una red convolucional.

Compilar la red neuronal, seleccionando una función de pérdida, un optimizador y una métrica para evaluar el desempeño de la red.

Entrenar la red neuronal en los datos de entrenamiento, utilizando la función de pérdida y el optimizador seleccionados, y evaluando el desempeño en los datos de validación.

Ajustar los hiperparámetros de la red neuronal, como el número de capas, el tamaño del kernel, el tamaño del lote, etc.

Evaluar el desempeño de la red neuronal en los datos de prueba.

Guardar la red neuronal entrenada para su uso futuro.
'''