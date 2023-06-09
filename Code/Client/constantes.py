
# ===================================================== TAMAÑOS IMAGEN =====================================================
# TAMAÑOS IMAGEN ORIGINAL
WIDTH_IMG = 2592
HEIGHT_IMG = 1944

# TAMAÑO TARGET DE IMAGEN
PROPORCION = 8
TARGET_WIDTH_IMG = int(WIDTH_IMG / PROPORCION)
TARGET_HEIGHT_IMG = int(HEIGHT_IMG / PROPORCION)


# ===================================================== CLASES =====================================================
CLASSES = ['0_Hexapod'
            '1_NanoBug_Azul',
           '2_NanoBug_Negro',
           '3_NanoBug_Celeste',
           '4_NanoBug_Blanco',
           '5_NanoBug_GrisClaro',
           '6_NanoBug_GrisOscuro',
           '7_NanoBug_Naranja']

NUM_CUCAS = {'0_Hexapod': 0,
            '1_NanoBug_Azul': 1,
           '2_NanoBug_Negro': 4,
           '3_NanoBug_Celeste': 3,
           '4_NanoBug_Blanco': 5,
           '5_NanoBug_GrisClaro': 6,
           '6_NanoBug_GrisOscuro': 2,
           '7_NanoBug_Naranja': 7}

CLASS_NUMBER = len(CLASSES)

# ===================================================== PATHS =====================================================
# Definimos ruta del Dataset
DATASET_PATH = "../Dataset/"

# Definimos la ruta de la carpeta donde se guardarán las imágenes extraídas
IMAGE_DIR = DATASET_PATH + "imagenes/"

CSV_PATH = DATASET_PATH + "CSVs/"

CSV_HEXBUG_NANO = CSV_PATH + "HexBug_Nano.CSV"

CSV_TRAIN_HEXBUG_NANO = CSV_PATH + "HexBug_Nano_train.csv"
CSV_TEST_HEXBUG_NANO = CSV_PATH + "HexBug_Nano_test.csv"
CSV_VALIDATION_HEXBUG_NANO = CSV_PATH + "HexBug_Nano_validation.csv"


# ================================== NEURAL NETWORK  ==================================
BATCH_SIZE = 8