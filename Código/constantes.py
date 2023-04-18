
# ===================================================== TAMAÑOS IMAGEN =====================================================
# TAMAÑOS IMAGEN ORIGINAL
WIDTH_IMG = 2592
HEIGHT_IMG = 1944

# TAMAÑO TARGET DE IMAGEN
PROPORCION = 8
TARGET_WIDTH_IMG = int(WIDTH_IMG / PROPORCION)
TARGET_HEIGHT_IMG = int(HEIGHT_IMG / PROPORCION)


# ===================================================== CLASES =====================================================
CLASSES = ['1_NanoBug_Azul',
           '2_NanoBug_Negro',
           '3_NanoBug_Celeste',
           '4_NanoBug_Blanco',
           '5_NanoBug_GrisClaro',
           '6_NanoBug_GrisOscuro',
           '7_NanoBug_Naranja']


# ===================================================== PATHS =====================================================
# Definimos ruta del Dataset
DATASET_PATH = "../Dataset/"

# Definimos la ruta de la carpeta donde se guardarán las imágenes extraídas
IMAGE_DIR = DATASET_PATH + "/imagenes/"