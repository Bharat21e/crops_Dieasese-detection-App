import os
import json
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ReduceLROnPlateau,
    ModelCheckpoint,
    Callback
)

# ============================================================
# 1. TensorFlow Information
# ============================================================

print("TensorFlow version:", tf.__version__)
print("CPU:", tf.config.list_physical_devices("CPU"))

# ============================================================
# 2. Paths
# ============================================================

BASE_DIR = r"C:\Users\BHARAT\OneDrive\ドキュメント\vscode coding\8 th sem project 2\crops de\my-app"

DATASET_PATH = os.path.join(
    BASE_DIR,
    "wheatleaf_disease",
    "dataset"
)

# Your existing BEST model
MODEL_PATH = os.path.join(
    BASE_DIR,
    "crop_leaf_model.h5"
)

# New proper resume checkpoint
RESUME_MODEL_PATH = os.path.join(
    BASE_DIR,
    "crop_leaf_resume.keras"
)

# Save class names
CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "class_names.json"
)

# Save last completed epoch
EPOCH_FILE = os.path.join(
    BASE_DIR,
    "last_epoch.txt"
)

# ============================================================
# 3. Parameters
# ============================================================

IMG_HEIGHT = 150
IMG_WIDTH = 150
BATCH_SIZE = 32

# Total desired epochs
EPOCHS = 30

# Your existing model was saved at Epoch 9
START_EPOCH = 9

# ============================================================
# 4. Check Dataset
# ============================================================

if not os.path.exists(DATASET_PATH):

    raise FileNotFoundError(
        f"Dataset not found:\n{DATASET_PATH}"
    )

if not os.path.exists(MODEL_PATH):

    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )

print("\n================================")
print("PATH INFORMATION")
print("================================")

print("Dataset:")
print(DATASET_PATH)

print("\nExisting model:")
print(MODEL_PATH)

print("\nResume model:")
print(RESUME_MODEL_PATH)

# ============================================================
# 5. Data Augmentation
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


val_datagen = ImageDataGenerator(

    rescale=1.0 / 255,

    validation_split=0.20
)

# ============================================================
# 6. Training Generator
# ============================================================

train_generator = train_datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(
        IMG_HEIGHT,
        IMG_WIDTH
    ),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training",

    shuffle=True,

    seed=42
)

# ============================================================
# 7. Validation Generator
# ============================================================

val_generator = val_datagen.flow_from_directory(

    DATASET_PATH,

    target_size=(
        IMG_HEIGHT,
        IMG_WIDTH
    ),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation",

    shuffle=False,

    seed=42
)

# ============================================================
# 8. Class Information
# ============================================================

print("\n================================")
print("CLASS INFORMATION")
print("================================")

print(train_generator.class_indices)

NUM_CLASSES = train_generator.num_classes

print("\nNumber of classes:", NUM_CLASSES)

# Make sure Non_Leaf exists
if "Non_Leaf" not in train_generator.class_indices:

    raise ValueError(
        "\nNon_Leaf class was not found.\n"
        "Create:\n"
        f"{DATASET_PATH}\\Non_Leaf"
    )

# ============================================================
# 9. Save Class Names
# ============================================================

class_names = [
    name
    for name, index in sorted(
        train_generator.class_indices.items(),
        key=lambda x: x[1]
    )
]

with open(
    CLASS_NAMES_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        class_names,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nClass names saved:")
print(CLASS_NAMES_PATH)

# ============================================================
# 10. Load Existing Best Model
# ============================================================

print("\n================================")
print("LOADING EXISTING MODEL")
print("================================")

print(
    "\nLoading best model from Epoch 9..."
)

model = load_model(
    MODEL_PATH
)

print("\nModel loaded successfully.")

# ============================================================
# 11. Check Model Output
# ============================================================

model_output_classes = model.output_shape[-1]

print(
    "\nModel output classes:",
    model_output_classes
)

print(
    "Dataset classes:",
    NUM_CLASSES
)

if model_output_classes != NUM_CLASSES:

    raise ValueError(
        f"\nERROR:\n"
        f"Model has {model_output_classes} classes, "
        f"but dataset has {NUM_CLASSES} classes."
    )

# ============================================================
# 12. Recompile Model
# ============================================================

# We are continuing from the saved BEST model.
#
# Use a smaller learning rate than the original 0.001
# because the model is already trained.

model.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0002
    ),

    loss="categorical_crossentropy",

    metrics=[
        "accuracy"
    ]
)

# ============================================================
# 13. Model Summary
# ============================================================

model.summary()

# ============================================================
# 14. Callbacks
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

# ------------------------------------------------------------
# Best model
# ------------------------------------------------------------

best_checkpoint = ModelCheckpoint(

    MODEL_PATH,

    monitor="val_accuracy",

    save_best_only=True,

    verbose=1
)

# ------------------------------------------------------------
# Resume checkpoint
# ------------------------------------------------------------

resume_checkpoint = ModelCheckpoint(

    RESUME_MODEL_PATH,

    save_best_only=False,

    verbose=1
)

# ============================================================
# 15. Epoch Saver
# ============================================================

class EpochSaver(Callback):

    def on_epoch_end(
        self,
        epoch,
        logs=None
    ):

        completed_epoch = epoch + 1

        with open(
            EPOCH_FILE,
            "w"
        ) as f:

            f.write(
                str(completed_epoch)
            )

        print(
            f"\nCompleted epoch saved: {completed_epoch}"
        )


epoch_saver = EpochSaver()

# ============================================================
# 16. Training
# ============================================================

print("\n================================")
print("CONTINUING TRAINING")
print("================================")

print(
    "\nExisting best model:"
)

print(
    "Epoch 9"
)

print(
    "Validation Accuracy: 92.64%"
)

print(
    "\nStarting training from Epoch 10..."
)

print(
    "Training will continue until Epoch 30."
)

# ============================================================
# 17. Train
# ============================================================

try:

    history = model.fit(

        train_generator,

        initial_epoch=START_EPOCH,

        epochs=EPOCHS,

        validation_data=val_generator,

        callbacks=[

            early_stopping,

            reduce_lr,

            best_checkpoint,

            resume_checkpoint,

            epoch_saver

        ]

    )

except KeyboardInterrupt:

    print("\n")
    print("================================")
    print("TRAINING STOPPED")
    print("================================")

    print(
        "\nTraining was stopped by Ctrl+C."
    )

    print(
        "The latest completed epoch was saved."
    )

    print(
        "\nResume checkpoint:"
    )

    print(
        RESUME_MODEL_PATH
    )

# ============================================================
# 18. Evaluation
# ============================================================

print("\n================================")
print("FINAL EVALUATION")
print("================================")

# Load BEST model again
# This guarantees evaluation uses the best
# validation-accuracy model.

best_model = load_model(
    MODEL_PATH
)

results = best_model.evaluate(

    val_generator,

    verbose=1
)

print(
    "\nBest Model Validation Loss:",
    results[0]
)

print(
    "Best Model Validation Accuracy:",
    results[1]
)

# ============================================================
# 19. Save Class Names Again
# ============================================================

with open(
    CLASS_NAMES_PATH,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        class_names,
        f,
        indent=4,
        ensure_ascii=False
    )

# ============================================================
# 20. Training Graph
# ============================================================

if "history" in locals():

    plt.figure(
        figsize=(8, 5)
    )

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

    plt.title(
        "Training vs Validation Accuracy"
    )

    plt.xlabel("Epoch")

    plt.ylabel("Accuracy")

    plt.legend()

    plt.grid(True)

    plt.show()

    # ========================================================
    # Loss Graph
    # ========================================================

    plt.figure(
        figsize=(8, 5)
    )

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

    plt.title(
        "Training vs Validation Loss"
    )

    plt.xlabel("Epoch")

    plt.ylabel("Loss")

    plt.legend()

    plt.grid(True)

    plt.show()

# ============================================================
# 21. Done
# ============================================================

print("\n================================")
print("TRAINING PROCESS FINISHED")
print("================================")

print(
    "\nBest model:"
)

print(
    MODEL_PATH
)

print(
    "\nResume checkpoint:"
)

print(
    RESUME_MODEL_PATH
)

print(
    "\nClass names:"
)

print(
    CLASS_NAMES_PATH
)