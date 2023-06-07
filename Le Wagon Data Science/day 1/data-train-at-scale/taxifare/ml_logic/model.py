import numpy as np
import time

from colorama import Fore, Style
from typing import Tuple

# Timing the TF import
print(Fore.BLUE + "\nLoading TensorFlow..." + Style.RESET_ALL)
start = time.perf_counter()

from tensorflow import keras
from keras import Model, Sequential, layers, regularizers, optimizers
from keras.callbacks import EarlyStopping

end = time.perf_counter()
print(f"\n✅ TensorFlow loaded ({round(end - start, 2)}s)")



def initialize_model(input_shape: tuple) -> Model:
    model = Sequential()
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Dense(100, activation="relu", kernel_regularizer=regularizers.l1_l2(l1=0.005)))
    model.add(layers.BatchNormalization(momentum=0.9))
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(50, activation="relu"))
    model.add(layers.BatchNormalization(momentum=0.9))
    model.add(layers.Dropout(rate=0.1))
    model.add(layers.Dense(1, activation="linear"))

    print("✅ Model initialized")

    return model


def compile_model(model: Model, learning_rate=0.0005) -> Model:
    optimizer = optimizers.Adam(learning_rate=learning_rate)
    model.compile(loss="mean_squared_error", optimizer=optimizer, metrics=["mae"])

    print("✅ Model compiled")

    return model


def train_model(model: Model, X: np.ndarray, y: np.ndarray, batch_size=256,
                patience=2, validation_data=None, validation_split=0.3) -> Tuple[Model, dict]:
    es = EarlyStopping(monitor="val_loss", patience=patience, restore_best_weights=True, verbose=0)

    history = model.fit(X, y, batch_size=batch_size, epochs=100,
                        validation_data=validation_data, validation_split=validation_split,
                        callbacks=[es], verbose=1)

    print(f"✅ Model trained on {len(X)} rows with min val MAE: {round(np.min(history.history['val_mae']), 2)}")

    return model, history
