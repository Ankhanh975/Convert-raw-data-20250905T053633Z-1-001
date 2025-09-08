"""
2-Class Image Classification on Processed_1858_divided using TensorFlow
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from PIL import Image
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

class DividedImageClassifier:
    def __init__(self, data_dir='Processed_1858_filtered_divided', img_size=(32, 32)):
        self.data_dir = data_dir
        self.img_size = img_size
        self.model = None
        self.history = None
        
    def load_and_preprocess_data(self):
        print("Loading and preprocessing data...")
        images = []
        labels = []
        # Healthy
        healthy_dir = os.path.join(self.data_dir, 'healthy')
        for root, dirs, files in os.walk(healthy_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path).convert('L')
                        img = img.resize(self.img_size)
                        img_array = np.array(img)
                        # Add all 4 rotations: 0°, 90°, 180°, 270°
                        rotations = [
                            img_array,
                            np.rot90(img_array, k=1),
                            np.rot90(img_array, k=2),
                            np.rot90(img_array, k=3)
                        ]
                        images.extend(rotations)
                        labels.extend([0] * 4)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        # Tumour
        tumour_dir = os.path.join(self.data_dir, 'tumour')
        for root, dirs, files in os.walk(tumour_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path).convert('L')
                        img = img.resize(self.img_size)
                        img_array = np.array(img)
                        # Add all 4 rotations: 0°, 90°, 180°, 270°
                        rotations = [
                            img_array,
                            np.rot90(img_array, k=1),
                            np.rot90(img_array, k=2),
                            np.rot90(img_array, k=3)
                        ]
                        images.extend(rotations)
                        labels.extend([1] * 4)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        X = np.array(images)
        y = np.array(labels)
        X = X.astype('float32') / 255.0
        X = np.expand_dims(X, axis=-1)
        print(f"Loaded {len(X)} images (after 4-way rotation augmentation)")
        print(f"Healthy images: {np.sum(y == 0)}")
        print(f"Tumour images: {np.sum(y == 1)}")
        print(f"Image shape: {X.shape}")
        return X, y
    
    def create_model(self):
        print("Creating 2-layer fully connected model...")
        model = models.Sequential([
            layers.Flatten(input_shape=(*self.img_size, 1)),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=[
                'accuracy',
                tf.keras.metrics.Precision(name='precision', thresholds=0.5),
                tf.keras.metrics.Recall(name='recall', thresholds=0.5)
            ]
        )
        self.model = model
        print("Model created successfully!")
        print(f"Total parameters: {model.count_params():,}")
        return model
    
    def train_model(self, X, y, validation_split=0.2, epochs=50, batch_size=32):
        print("Training model...")
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42, stratify=y
        )
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            zoom_range=0.1,
            fill_mode='nearest'
        )
        val_datagen = ImageDataGenerator()
        train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
        val_generator = val_datagen.flow(X_val, y_val, batch_size=batch_size)
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_loss', patience=10, restore_best_weights=True, verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.5, patience=5, min_lr=1e-7, verbose=1
            ),
            callbacks.ModelCheckpoint(
                'best_divided_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1
            )
        ]
        self.history = self.model.fit(
            train_generator,
            steps_per_epoch=len(X_train) // batch_size,
            epochs=epochs,
            validation_data=val_generator,
            validation_steps=len(X_val) // batch_size,
            callbacks=callbacks_list,
            verbose=1
        )
        return self.history
    
    def evaluate_model(self, X_test, y_test):
        print("Evaluating model...")
        y_pred_proba = self.model.predict(X_test)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        test_loss, test_accuracy, test_precision, test_recall = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\nTest Results:")
        print(f"Accuracy: {test_accuracy:.4f}")
        print(f"Precision: {test_precision:.4f}")
        print(f"Recall: {test_recall:.4f}")
        print(f"F1-Score: {2 * (test_precision * test_recall) / (test_precision + test_recall):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Healthy', 'Tumour']))
        return y_pred, y_pred_proba
    
    def plot_training_history(self):
        if self.history is None:
            print("No training history available!")
            return
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes[0, 0].plot(self.history.history['accuracy'], label='Training Accuracy')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        axes[0, 1].plot(self.history.history['loss'], label='Training Loss')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        axes[1, 0].plot(self.history.history['precision'], label='Training Precision')
        axes[1, 0].plot(self.history.history['val_precision'], label='Validation Precision')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        axes[1, 1].plot(self.history.history['recall'], label='Training Recall')
        axes[1, 1].plot(self.history.history['val_recall'], label='Validation Recall')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        plt.tight_layout()
        plt.savefig('divided_training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred):
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Healthy', 'Tumour'],
                   yticklabels=['Healthy', 'Tumour'])
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.savefig('divided_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_sample_predictions(self, X_test, y_test, y_pred, y_pred_proba, num_samples=8):
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.ravel()
        indices = np.random.choice(len(X_test), num_samples, replace=False)
        for i, idx in enumerate(indices):
            img = X_test[idx].squeeze()
            true_label = 'Healthy' if y_test[idx] == 0 else 'Tumour'
            pred_label = 'Healthy' if y_pred[idx] == 0 else 'Tumour'
            confidence = y_pred_proba[idx][0] if y_pred[idx] == 1 else 1 - y_pred_proba[idx][0]
            axes[i].imshow(img, cmap='gray')
            axes[i].set_title(f'True: {true_label}\nPred: {pred_label}\nConf: {confidence:.3f}')
            axes[i].axis('off')
            if y_test[idx] == y_pred[idx]:
                axes[i].add_patch(plt.Rectangle((0, 0), 31, 31, fill=False, edgecolor='green', lw=3))
            else:
                axes[i].add_patch(plt.Rectangle((0, 0), 31, 31, fill=False, edgecolor='red', lw=3))
        plt.tight_layout()
        plt.savefig('divided_sample_predictions.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    print("Divided Image Classification Pipeline")
    print("=" * 50)
    classifier = DividedImageClassifier(data_dir='Processed_1858_filtered_divided')
    X, y = classifier.load_and_preprocess_data()
    model = classifier.create_model()
    print("\nModel Architecture:")
    model.summary()
    history = classifier.train_model(X, y, epochs=50, batch_size=32)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    y_pred, y_pred_proba = classifier.evaluate_model(X_test, y_test)
    classifier.plot_training_history()
    classifier.plot_confusion_matrix(y_test, y_pred)
    classifier.plot_sample_predictions(X_test, y_test, y_pred, y_pred_proba)
    classifier.model.save('divided_classifier_model.h5')
    print("\nModel saved as 'divided_classifier_model.h5'")
    print("\nClassification pipeline completed successfully!")

if __name__ == "__main__":
    main()
