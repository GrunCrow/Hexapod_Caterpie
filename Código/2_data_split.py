import pandas as pd
from sklearn.model_selection import train_test_split # para crear la división estratificada

from constantes import *

'''
Cargar el CSV con las imágenes y etiquetas.
'''

# Cargamos el CSV con las etiquetas
df = pd.read_csv(CSV_HEXBUG_NANO)

# Dividimos los datos en entrenamiento y prueba (80-20%)
train, test = train_test_split(df, test_size=0.1, random_state=42, stratify=df['class'])

# Dividimos los datos de entrenamiento en entrenamiento y validación (75-25%)
train, val = train_test_split(train, test_size=0.1, random_state=42, stratify=train['class'])

# Guardamos los conjuntos de datos en CSVs separados
train.to_csv(CSV_TRAIN_HEXBUG_NANO, index=False)
test.to_csv(CSV_TEST_HEXBUG_NANO, index=False)
val.to_csv(CSV_VALIDATION_HEXBUG_NANO, index=False)

'''# Generador de imágenes de entrenamiento y validación con aumento de datos
train_datagen = ImageDataGenerator(rescale=1./255,
                                   rotation_range=40,
                                   width_shift_range=0.2,
                                   height_shift_range=0.2,
                                   shear_range=0.2,
                                   zoom_range=0.2,
                                   horizontal_flip=True,
                                   fill_mode='nearest')
val_datagen = ImageDataGenerator(rescale=1./255)

# Carga de las imágenes de entrenamiento y validación
train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=(224, 224),
                                                    batch_size=32,
                                                    class_mode='categorical')
                                                    
val_generator = val_datagen.flow_from_directory(val_dir,
                                                target_size=(224, 224),
                                                batch_size=32,
                                                class_mode='categorical')

# Definir la arquitectura de la red neuronal
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(224, 224, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(256, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# Compilar el modelo
model.compile(optimizer=Adam(lr=0.0001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Entrenar el modelo
model.fit_generator(train_generator,
                    steps_per_epoch=train_generator.samples//train_generator.batch_size,
                    epochs=30,
                    validation_data=val_generator,
                    validation_steps=val_generator.samples//val_generator.batch_size)

# Evaluar el modelo con el conjunto de prueba
test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory(test_dir,
                                                  target_size=(224, 224),
                                                  batch_size=32,
                                                  class_mode='categorical')
test_loss, test_acc = model.evaluate_generator(test_generator, steps=test_generator.samples//test_generator.batch_size)
print('Test accuracy:', test_acc)'''
