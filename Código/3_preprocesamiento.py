import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from sklearn.model_selection import train_test_split
from keras import layers
from keras.layers import *
from keras.optimizers import *


import matplotlib.pyplot as plt

from constantes import *

# Cargar los datos
train = pd.read_csv(CSV_PATH + "HexBug_Nano_train.csv")
val = pd.read_csv(CSV_PATH + "HexBug_Nano_validation.csv")
test = pd.read_csv(CSV_PATH + "HexBug_Nano_test.csv")

# Creamos un generador de imágenes para el preprocesamiento
datagen_train = ImageDataGenerator(
    rescale=1. / 255,
    zoom_range=0.1,
    rotation_range=20,
    horizontal_flip=True,
    brightness_range=(0.8, 1),
    shear_range=0.1
)

datagen_basic = ImageDataGenerator(
    rescale=1. / 255)

# Cargamos las imágenes de entrenamiento con el generador de imágenes y aplicamos el preprocesamiento
train_generator = datagen_train.flow_from_dataframe(
    dataframe=train,
    x_col="path",
    y_col="class",
    color_mode='rgb',
    target_size=(TARGET_HEIGHT_IMG, TARGET_WIDTH_IMG),
    batch_size=BATCH_SIZE,
    shuffle=True,
    class_mode='categorical')

# Cargamos las imágenes de validación con el generador de imágenes y aplicamos el preprocesamiento
val_generator = datagen_basic.flow_from_dataframe(
    dataframe=val,
    x_col="path",
    y_col="class",
    color_mode='rgb',
    target_size=(TARGET_HEIGHT_IMG, TARGET_WIDTH_IMG),
    batch_size=BATCH_SIZE,
    class_mode='categorical')

# Cargamos las imágenes de test con el generador de imágenes y aplicamos el preprocesamiento
test_generator = datagen_basic.flow_from_dataframe(
    dataframe=test,
    x_col="path",
    y_col="class",
    color_mode='rgb',
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


# sample_images, sample_labels = next(iter(train_images))
'''sample_images = train_df["Image Path"]
sample_labels = train_df['Label']'''

ROWS = int(BATCH_SIZE/4)
COLS = 4

plt.figure(figsize=(2*2*COLS, 2*ROWS))
for n in range(BATCH_SIZE):
    ax = plt.subplot(ROWS, 2*COLS, 2*n+1)
    '''image = (sample_images[n] * STD + MEAN).numpy()
    image = (image - image.min()) / (
        image.max() - image.min()
    )  # convert to [0, 1] for avoiding matplotlib warning
    plt.imshow(image)'''
    sample_image, sample_label = next(train_generator)
    n_label = np.where(sample_label[0] == 1.)
    # si se muestra one hot encoding se muestra en negativo, si se muestra una string sale en rgb
    n_label = n_label[0][0]
    label = CLASSES[n_label]
    plt.title(label)
    plt.imshow(sample_image[0])

    plt.axis("off")
plt.tight_layout()
plt.show()


# Reference:
# https://www.kaggle.com/ashusma/training-rfcx-tensorflow-tpu-effnet-b2

class WarmUpCosine(tf.keras.optimizers.schedules.LearningRateSchedule):
    def __init__(
        self, learning_rate_base, total_steps, warmup_learning_rate, warmup_steps
    ):
        super(WarmUpCosine, self).__init__()

        self.learning_rate_base = learning_rate_base
        self.total_steps = total_steps
        self.warmup_learning_rate = warmup_learning_rate
        self.warmup_steps = warmup_steps
        self.pi = tf.constant(np.pi)

    def __call__(self, step):
        if self.total_steps < self.warmup_steps:
            raise ValueError("Total_steps must be larger or equal to warmup_steps.")
        learning_rate = (
            0.5
            * self.learning_rate_base
            * (
                1
                + tf.cos(
                    self.pi
                    * (tf.cast(step, tf.float32) - self.warmup_steps)
                    / float(self.total_steps - self.warmup_steps)
                )
            )
        )

        if self.warmup_steps > 0:
            if self.learning_rate_base < self.warmup_learning_rate:
                raise ValueError(
                    "Learning_rate_base must be larger or equal to "
                    "warmup_learning_rate."
                )
            slope = (
                self.learning_rate_base - self.warmup_learning_rate
            ) / self.warmup_steps
            warmup_rate = slope * tf.cast(step, tf.float32) + self.warmup_learning_rate
            learning_rate = tf.where(
                step < self.warmup_steps, warmup_rate, learning_rate
            )
        return tf.where(
            step > self.total_steps, 0.0, learning_rate, name="learning_rate"
        )

EPOCHS = 5
WARMUP_STEPS = 10
INIT_LR = 0.03
WAMRUP_LR = 0.006

TOTAL_STEPS = int((len(train_generator.filenames) / BATCH_SIZE) * EPOCHS)

scheduled_lrs = WarmUpCosine(
    learning_rate_base=INIT_LR,
    total_steps=TOTAL_STEPS,
    warmup_learning_rate=WAMRUP_LR,
    warmup_steps=WARMUP_STEPS,
)

lrs = [scheduled_lrs(step) for step in range(TOTAL_STEPS)]
plt.figure(figsize=(10, 6))
plt.plot(lrs)
plt.xlabel("Step", fontsize=14)
plt.ylabel("LR", fontsize=14)
plt.show()

optimizer = keras.optimizers.SGD(scheduled_lrs)

'''
class_mode: One of "categorical", "binary", "sparse", "input", or None. Default: "categorical". Determines the type of label arrays that are returned: - "categorical" will be 2D one-hot encoded labels, - "binary" will be 1D binary labels, "sparse" will be 1D integer labels, - "input" will be images identical to input images (mainly used to work with autoencoders). - If None, no labels are returned (the generator will only yield batches of image data, which is useful to use with model.predict_generator()). Please note that in case of class_mode None, the data still needs to reside in a subdirectory of directory for it to work correctly.

So you should use categorical_crossentropy as loss function if you choose categorical for class_mode, and sparse_categorical_crossentropy if you choose sparse
'''
loss = keras.losses.CategoricalCrossentropy()


model = tf.keras.models.Sequential()
model.add(Conv2D(BATCH_SIZE, kernel_size=5,
                 padding='same',
                 activation='relu',
                 input_shape=(TARGET_HEIGHT_IMG, TARGET_WIDTH_IMG, 3)))
model.add(MaxPool2D(padding='same'))
model.add(Conv2D(64, kernel_size=5,
                 padding='same',
                 activation='relu'))
model.add(MaxPool2D(padding='same'))
model.add(Conv2D(128, kernel_size=3,
                 padding='same',
                 activation='relu'))
model.add(MaxPool2D(padding='same'))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(CLASS_NUMBER))


