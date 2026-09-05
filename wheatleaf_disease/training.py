import os
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    GlobalAveragePooling2D,
    Dense,
    Dropout,
    BatchNormalization
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint
)

# ============================================================
# 1. TensorFlow Information
# ============================================================

print("TensorFlow version:", tf.__version__)
print("CPU:", tf.config.list_physical_devices("CPU"))

# ============================================================
# 2. Parameters
# ============================================================

DATASET_PATH = r"C:/Users/BHARAT/OneDrive/ドキュメント/vscode coding/8 th sem project 2/crops de/my-app/wheatleaf_disease/dataset"

IMG_HEIGHT = 150
IMG_WIDTH = 150
BATCH_SIZE = 32
EPOCHS = 30

MODEL_PATH = "crop_leaf_model.h5"

# ============================================================
# 3. Data Augmentation
# ============================================================

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,

    rotation_range=25,
    width_shift_range=0.15,
    height_shift_range=0.15,

    zoom_range=0.20,
    shear_range=0.15,

    horizontal_flip=True,
    vertical_flip=False,

    brightness_range=[0.8, 1.2],

    validation_split=0.20
)

# Validation data should NOT have heavy augmentation
val_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.20
)

# ============================================================
# 4. Training Generator
# ============================================================

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,

    target_size=(IMG_HEIGHT, IMG_WIDTH),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training",

    shuffle=True,

    seed=42
)

# ============================================================
# 5. Validation Generator
# ============================================================

val_generator = val_datagen.flow_from_directory(
    DATASET_PATH,

    target_size=(IMG_HEIGHT, IMG_WIDTH),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation",

    shuffle=False,

    seed=42
)

# ============================================================
# 6. Class Information
# ============================================================

print("\n================================")
print("CLASS INFORMATION")
print("================================")

print("Classes:")
print(train_generator.class_indices)

NUM_CLASSES = train_generator.num_classes

print("\nNumber of classes:", NUM_CLASSES)

# Make sure Non_Leaf exists
if "Non_Leaf" not in train_generator.class_indices:
    print("\nWARNING:")
    print("Non_Leaf class was not found!")
    print("Create this folder inside dataset:")
    print("dataset/Non_Leaf/")

# ============================================================
# 7. CNN Model
# ============================================================

model = Sequential([

    # -------------------------
    # Block 1
    # -------------------------

    Conv2D(
        32,
        (3, 3),
        activation="relu",
        padding="same",
        input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)
    ),

    BatchNormalization(),

    Conv2D(
        32,
        (3, 3),
        activation="relu",
        padding="same"
    ),

    MaxPooling2D(pool_size=(2, 2)),

    Dropout(0.20),

    # -------------------------
    # Block 2
    # -------------------------

    Conv2D(
        64,
        (3, 3),
        activation="relu",
        padding="same"
    ),

    BatchNormalization(),

    Conv2D(
        64,
        (3, 3),
        activation="relu",
        padding="same"
    ),

    MaxPooling2D(pool_size=(2, 2)),

    Dropout(0.25),

    # -------------------------
    # Block 3
    # -------------------------

    Conv2D(
        128,
        (3, 3),
        activation="relu",
        padding="same"
    ),

    BatchNormalization(),

    Conv2D(
        128,
        (3, 3),
        activation="relu",
        padding="same"
    ),

    MaxPooling2D(pool_size=(2, 2)),

    Dropout(0.30),

    # -------------------------
    # Block 4
    # -------------------------

    Conv2D(
        256,
        (3, 3),
        activation="relu",
        padding="same"
    ),

    BatchNormalization(),

    MaxPooling2D(pool_size=(2, 2)),

    Dropout(0.35),

    # -------------------------
    # Classification
    # -------------------------

    GlobalAveragePooling2D(),

    Dense(
        256,
        activation="relu"
    ),

    BatchNormalization(),

    Dropout(0.50),

    Dense(
        NUM_CLASSES,
        activation="softmax"
    )
])

# ============================================================
# 8. Compile
# ============================================================

model.compile(

    optimizer=Adam(
        learning_rate=0.001
    ),

    loss="categorical_crossentropy",

    metrics=[
        "accuracy"
    ]
)

# ============================================================
# 9. Model Summary
# ============================================================

model.summary()

# ============================================================
# 10. Callbacks
# ============================================================

early_stopping = EarlyStopping(

    monitor="val_loss",

    patience=5,

    restore_best_weights=True,

    verbose=1
)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=2,

    min_lr=0.00001,

    verbose=1
)

checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1
)

# ============================================================
# 11. Train Model
# ============================================================

print("\n================================")
print("STARTING TRAINING")
print("================================")

history = model.fit(

    train_generator,

    epochs=EPOCHS,

    validation_data=val_generator,

    callbacks=[
        early_stopping,
        reduce_lr,
        checkpoint
    ]
)

# ============================================================
# 12. Save Final Model
# ============================================================

model.save(MODEL_PATH)

print("\n================================")
print("MODEL SAVED")
print("================================")

print(
    "Model saved at:",
    os.path.abspath(MODEL_PATH)
)

# ============================================================
# 13. Evaluation
# ============================================================

print("\n================================")
print("EVALUATING MODEL")
print("================================")

results = model.evaluate(
    val_generator,
    verbose=1
)

print("\nValidation Loss:", results[0])
print("Validation Accuracy:", results[1])

# ============================================================
# 14. Plot Accuracy
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy",
    marker="o"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy",
    marker="o"
)

plt.title("Training vs Validation Accuracy")

plt.xlabel("Epoch")

plt.ylabel("Accuracy")

plt.legend()

plt.grid(True)

plt.show()

# ============================================================
# 15. Plot Loss
# ============================================================

plt.figure(figsize=(8, 5))

plt.plot(
    history.history["loss"],
    label="Training Loss",
    marker="o"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss",
    marker="o"
)

plt.title("Training vs Validation Loss")

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.legend()

plt.grid(True)

plt.show()








# ```python
# import os
# import json
# import tensorflow as tf
# import matplotlib.pyplot as plt

# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras.layers import (
#     Conv2D,
#     MaxPooling2D,
#     GlobalAveragePooling2D,
#     Dense,
#     Dropout,
#     BatchNormalization
# )
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import (
#     EarlyStopping,
#     ReduceLROnPlateau,
#     ModelCheckpoint,
#     Callback
# )

# # ============================================================
# # 1. TensorFlow Information
# # ============================================================

# print("TensorFlow version:", tf.__version__)
# print("CPU:", tf.config.list_physical_devices("CPU"))

# # ============================================================
# # 2. Parameters
# # ============================================================

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# DATASET_PATH = r"C:/Users/BHARAT/OneDrive/ドキュメント/vscode coding/8 th sem project 2/crops de/my-app/wheatleaf_disease/dataset"

# IMG_HEIGHT = 150
# IMG_WIDTH = 150
# BATCH_SIZE = 32

# # Total training epochs
# EPOCHS = 30

# # ============================================================
# # Model / Resume Files
# # ============================================================

# MODEL_PATH = os.path.join(
#     BASE_DIR,
#     "crop_leaf_model.h5"
# )

# RESUME_MODEL_PATH = os.path.join(
#     BASE_DIR,
#     "crop_leaf_resume.keras"
# )

# EPOCH_FILE = os.path.join(
#     BASE_DIR,
#     "last_epoch.txt"
# )

# CLASS_NAMES_PATH = os.path.join(
#     BASE_DIR,
#     "class_names.json"
# )

# # ============================================================
# # 3. Data Augmentation
# # ============================================================

# train_datagen = ImageDataGenerator(
#     rescale=1.0 / 255,

#     rotation_range=25,

#     width_shift_range=0.15,

#     height_shift_range=0.15,

#     zoom_range=0.20,

#     shear_range=0.15,

#     horizontal_flip=True,

#     vertical_flip=False,

#     brightness_range=[0.8, 1.2],

#     validation_split=0.20
# )

# # ============================================================
# # Validation Data
# # No heavy augmentation
# # ============================================================

# val_datagen = ImageDataGenerator(
#     rescale=1.0 / 255,

#     validation_split=0.20
# )

# # ============================================================
# # 4. Training Generator
# # ============================================================

# train_generator = train_datagen.flow_from_directory(

#     DATASET_PATH,

#     target_size=(IMG_HEIGHT, IMG_WIDTH),

#     batch_size=BATCH_SIZE,

#     class_mode="categorical",

#     subset="training",

#     shuffle=True,

#     seed=42
# )

# # ============================================================
# # 5. Validation Generator
# # ============================================================

# val_generator = val_datagen.flow_from_directory(

#     DATASET_PATH,

#     target_size=(IMG_HEIGHT, IMG_WIDTH),

#     batch_size=BATCH_SIZE,

#     class_mode="categorical",

#     subset="validation",

#     shuffle=False,

#     seed=42
# )

# # ============================================================
# # 6. Class Information
# # ============================================================

# print("\n================================")
# print("CLASS INFORMATION")
# print("================================")

# print("\nClasses:")
# print(train_generator.class_indices)

# NUM_CLASSES = train_generator.num_classes

# print("\nNumber of classes:", NUM_CLASSES)

# # ============================================================
# # Check Non_Leaf
# # ============================================================

# if "Non_Leaf" not in train_generator.class_indices:

#     print("\nWARNING:")
#     print("Non_Leaf class was not found!")

#     print("Create this folder:")
#     print(
#         os.path.join(
#             DATASET_PATH,
#             "Non_Leaf"
#         )
#     )

# else:

#     print(
#         "\nNon_Leaf class index:",
#         train_generator.class_indices["Non_Leaf"]
#     )

# # ============================================================
# # 7. Save Class Names
# # ============================================================

# class_names = list(train_generator.class_indices.keys())

# with open(CLASS_NAMES_PATH, "w") as f:

#     json.dump(
#         class_names,
#         f,
#         indent=4
#     )

# print(
#     "\nClass names saved:",
#     CLASS_NAMES_PATH
# )

# # ============================================================
# # 8. Resume Training Check
# # ============================================================

# initial_epoch = 0

# if (
#     os.path.exists(RESUME_MODEL_PATH)
#     and os.path.exists(EPOCH_FILE)
# ):

#     print("\n================================")
#     print("RESUME TRAINING")
#     print("================================")

#     with open(EPOCH_FILE, "r") as f:

#         initial_epoch = int(
#             f.read().strip()
#         )

#     print(
#         "Last completed epoch:",
#         initial_epoch
#     )

#     print(
#         "Next epoch:",
#         initial_epoch + 1
#     )

#     print(
#         "\nLoading resume model..."
#     )

#     model = load_model(
#         RESUME_MODEL_PATH
#     )

#     print(
#         "Resume model loaded successfully."
#     )

# else:

#     # ========================================================
#     # 9. Create New CNN Model
#     # ========================================================

#     print("\n================================")
#     print("CREATING NEW CNN MODEL")
#     print("================================")

#     model = Sequential([

#         # -------------------------
#         # Block 1
#         # -------------------------

#         Conv2D(
#             32,
#             (3, 3),
#             activation="relu",
#             padding="same",
#             input_shape=(
#                 IMG_HEIGHT,
#                 IMG_WIDTH,
#                 3
#             )
#         ),

#         BatchNormalization(),

#         Conv2D(
#             32,
#             (3, 3),
#             activation="relu",
#             padding="same"
#         ),

#         MaxPooling2D(
#             pool_size=(2, 2)
#         ),

#         Dropout(0.20),

#         # -------------------------
#         # Block 2
#         # -------------------------

#         Conv2D(
#             64,
#             (3, 3),
#             activation="relu",
#             padding="same"
#         ),

#         BatchNormalization(),

#         Conv2D(
#             64,
#             (3, 3),
#             activation="relu",
#             padding="same"
#         ),

#         MaxPooling2D(
#             pool_size=(2, 2)
#         ),

#         Dropout(0.25),

#         # -------------------------
#         # Block 3
#         # -------------------------

#         Conv2D(
#             128,
#             (3, 3),
#             activation="relu",
#             padding="same"
#         ),

#         BatchNormalization(),

#         Conv2D(
#             128,
#             (3, 3),
#             activation="relu",
#             padding="same"
#         ),

#         MaxPooling2D(
#             pool_size=(2, 2)
#         ),

#         Dropout(0.30),

#         # -------------------------
#         # Block 4
#         # -------------------------

#         Conv2D(
#             256,
#             (3, 3),
#             activation="relu",
#             padding="same"
#         ),

#         BatchNormalization(),

#         MaxPooling2D(
#             pool_size=(2, 2)
#         ),

#         Dropout(0.35),

#         # -------------------------
#         # Classification
#         # -------------------------

#         GlobalAveragePooling2D(),

#         Dense(
#             256,
#             activation="relu"
#         ),

#         BatchNormalization(),

#         Dropout(0.50),

#         Dense(
#             NUM_CLASSES,
#             activation="softmax"
#         )
#     ])

#     # ========================================================
#     # Compile New Model
#     # ========================================================

#     model.compile(

#         optimizer=Adam(
#             learning_rate=0.001
#         ),

#         loss="categorical_crossentropy",

#         metrics=[
#             "accuracy"
#         ]
#     )

# # ============================================================
# # 10. Model Summary
# # ============================================================

# model.summary()

# # ============================================================
# # 11. Epoch Saver
# # ============================================================

# class EpochSaver(Callback):

#     def on_epoch_end(
#         self,
#         epoch,
#         logs=None
#     ):

#         completed_epoch = epoch + 1

#         print(
#             f"\nEpoch {completed_epoch}: "
#             f"saving resume model..."
#         )

#         # Save complete training state
#         self.model.save(
#             RESUME_MODEL_PATH
#         )

#         # Save epoch number
#         with open(
#             EPOCH_FILE,
#             "w"
#         ) as f:

#             f.write(
#                 str(completed_epoch)
#             )

#         print(
#             f"Completed epoch saved: "
#             f"{completed_epoch}"
#         )

# # ============================================================
# # 12. Callbacks
# # ============================================================

# early_stopping = EarlyStopping(

#     monitor="val_loss",

#     patience=5,

#     restore_best_weights=True,

#     verbose=1
# )

# reduce_lr = ReduceLROnPlateau(

#     monitor="val_loss",

#     factor=0.5,

#     patience=2,

#     min_lr=0.00001,

#     verbose=1
# )

# # ============================================================
# # Best Model Checkpoint
# # ============================================================

# checkpoint = ModelCheckpoint(

#     MODEL_PATH,

#     monitor="val_accuracy",

#     save_best_only=True,

#     verbose=1
# )

# # ============================================================
# # 13. Start Training
# # ============================================================

# print("\n================================")
# print("STARTING TRAINING")
# print("================================")

# print(
#     "Starting from epoch:",
#     initial_epoch + 1
# )

# print(
#     "Training until epoch:",
#     EPOCHS
# )

# # ============================================================
# # If already completed 30 epochs
# # ============================================================

# if initial_epoch >= EPOCHS:

#     print(
#         "\nTraining is already complete."
#     )

# else:

#     history = model.fit(

#         train_generator,

#         initial_epoch=initial_epoch,

#         epochs=EPOCHS,

#         validation_data=val_generator,

#         callbacks=[

#             early_stopping,

#             reduce_lr,

#             checkpoint,

#             EpochSaver()
#         ]
#     )

#     # ========================================================
#     # 14. Save Final Resume Model
#     # ========================================================

#     model.save(
#         RESUME_MODEL_PATH
#     )

#     print(
#         "\nResume model saved:"
#     )

#     print(
#         RESUME_MODEL_PATH
#     )

#     # ========================================================
#     # 15. Save Final Model
#     # ========================================================

#     model.save(
#         MODEL_PATH
#     )

#     print("\n================================")
#     print("MODEL SAVED")
#     print("================================")

#     print(
#         "Best/Final model:",
#         MODEL_PATH
#     )

#     # ========================================================
#     # 16. Evaluation
#     # ========================================================

#     print("\n================================")
#     print("EVALUATING MODEL")
#     print("================================")

#     results = model.evaluate(

#         val_generator,

#         verbose=1
#     )

#     print(
#         "\nValidation Loss:",
#         results[0]
#     )

#     print(
#         "Validation Accuracy:",
#         results[1]
#     )

#     # ========================================================
#     # 17. Plot Accuracy
#     # ========================================================

#     plt.figure(
#         figsize=(8, 5)
#     )

#     plt.plot(

#         history.history["accuracy"],

#         label="Training Accuracy",

#         marker="o"
#     )

#     plt.plot(

#         history.history["val_accuracy"],

#         label="Validation Accuracy",

#         marker="o"
#     )

#     plt.title(
#         "Training vs Validation Accuracy"
#     )

#     plt.xlabel(
#         "Epoch"
#     )

#     plt.ylabel(
#         "Accuracy"
#     )

#     plt.legend()

#     plt.grid(True)

#     plt.show()

#     # ========================================================
#     # 18. Plot Loss
#     # ========================================================

#     plt.figure(
#         figsize=(8, 5)
#     )

#     plt.plot(

#         history.history["loss"],

#         label="Training Loss",

#         marker="o"
#     )

#     plt.plot(

#         history.history["val_loss"],

#         label="Validation Loss",

#         marker="o"
#     )

#     plt.title(
#         "Training vs Validation Loss"
#     )

#     plt.xlabel(
#         "Epoch"
#     )

#     plt.ylabel(
#         "Loss"
#     )

#     plt.legend()

#     plt.grid(True)

#     plt.show()
# ```
