"""
Histogram Image Classification using TensorFlow
Binary classification of healthy vs tumour histogram images
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

class HistogramImageClassifier:
    def __init__(self, data_dir='Processed_histograms', img_size=(128, 128)):
        self.data_dir = data_dir
        self.img_size = img_size
        self.model = None
        self.history = None
        
    def load_and_preprocess_data(self, test_size=0.2, val_size=0.2):
        """Load images, preprocess, and split into train/val/test sets"""
        print("Loading and preprocessing data...")
        images = []
        labels = []
        healthy_dir = os.path.join(self.data_dir, 'healthy')
        for root, dirs, files in os.walk(healthy_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path).convert('L')
                        img = img.resize(self.img_size)
                        img_array = np.array(img)
                        images.append(img_array)
                        labels.append(0)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        tumour_dir = os.path.join(self.data_dir, 'tumour')
        for root, dirs, files in os.walk(tumour_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path).convert('L')
                        img = img.resize(self.img_size)
                        img_array = np.array(img)
                        images.append(img_array)
                        labels.append(1)
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        X = np.array(images).astype('float32') / 255.0
        y = np.array(labels)
        X = np.expand_dims(X, axis=-1)
        # Split into train+val and test
        X_trainval, X_test, y_trainval, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        # Split train+val into train and val
        val_relative = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_trainval, y_trainval, test_size=val_relative, random_state=42, stratify=y_trainval
        )
        # Print class balance
        print(f"Train samples: {len(X_train)}, Healthy: {np.sum(y_train==0)}, Tumour: {np.sum(y_train==1)}")
        print(f"Val samples: {len(X_val)}, Healthy: {np.sum(y_val==0)}, Tumour: {np.sum(y_val==1)}")
        print(f"Test samples: {len(X_test)}, Healthy: {np.sum(y_test==0)}, Tumour: {np.sum(y_test==1)}")
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def create_model(self):
        """Create a very simple CNN model with minimal parameters"""
        print("Creating minimal-parameter CNN model...")
        model = models.Sequential([
            layers.Conv2D(8, (3, 3), activation='relu', input_shape=(*self.img_size, 1)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(8, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Flatten(),
            layers.Dense(8, activation='relu'),
            layers.Dense(1, activation='sigmoid')
        ])
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        self.model = model
        return model
    
    def train_model(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
        """Train the model with minimal augmentation"""
        print("Training model...")
        # Minimal augmentation
        train_datagen = ImageDataGenerator()
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
                'best_hist_model.h5', monitor='val_accuracy', save_best_only=True, verbose=1
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
        """Evaluate model performance"""
        print("Evaluating model...")
        y_pred_proba = self.model.predict(X_test)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        test_loss, test_accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"\nTest Results:")
        print(f"Accuracy: {test_accuracy:.4f}")
        print(f"Loss: {test_loss:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Healthy', 'Tumour']))
        return y_pred, y_pred_proba
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("No training history available!")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Training Accuracy')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        axes[0, 0].set_title('Model Accuracy')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Training Loss')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[0, 1].set_title('Model Loss')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Precision
        axes[1, 0].plot(self.history.history['precision'], label='Training Precision')
        axes[1, 0].plot(self.history.history['val_precision'], label='Validation Precision')
        axes[1, 0].set_title('Model Precision')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Precision')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Recall
        axes[1, 1].plot(self.history.history['recall'], label='Training Recall')
        axes[1, 1].plot(self.history.history['val_recall'], label='Validation Recall')
        axes[1, 1].set_title('Model Recall')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Recall')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig('hist_training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_confusion_matrix(self, y_true, y_pred):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Healthy', 'Tumour'],
                   yticklabels=['Healthy', 'Tumour'])
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.savefig('hist_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_sample_predictions(self, X_test, y_test, y_pred, y_pred_proba, num_samples=8):
        """Plot sample predictions"""
        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.ravel()
        
        # Get random samples
        indices = np.random.choice(len(X_test), num_samples, replace=False)
        
        for i, idx in enumerate(indices):
            img = X_test[idx].squeeze()
            true_label = 'Healthy' if y_test[idx] == 0 else 'Tumour'
            pred_label = 'Healthy' if y_pred[idx] == 0 else 'Tumour'
            confidence = y_pred_proba[idx][0] if y_pred[idx] == 1 else 1 - y_pred_proba[idx][0]
            
            axes[i].imshow(img, cmap='gray')
            axes[i].set_title(f'True: {true_label}\nPred: {pred_label}\nConf: {confidence:.3f}')
            axes[i].axis('off')
            
            # Color code based on correctness
            if y_test[idx] == y_pred[idx]:
                axes[i].add_patch(plt.Rectangle((0, 0), 127, 127, fill=False, edgecolor='green', lw=3))
            else:
                axes[i].add_patch(plt.Rectangle((0, 0), 127, 127, fill=False, edgecolor='red', lw=3))
        
        plt.tight_layout()
        plt.savefig('hist_sample_predictions.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    print("Histogram Image Classification Pipeline")
    print("=" * 50)
    classifier = HistogramImageClassifier(data_dir='Processed_histograms')
    # Load and preprocess data (splits into train/val/test)
    X_train, X_val, X_test, y_train, y_val, y_test = classifier.load_and_preprocess_data()
    model = classifier.create_model()
    print("\nModel Architecture:")
    model.summary()
    # Train model
    history = classifier.train_model(X_train, y_train, X_val, y_val, epochs=50, batch_size=32)
    # Evaluate model
    y_pred, y_pred_proba = classifier.evaluate_model(X_test, y_test)
    # Plot results
    classifier.plot_training_history()
    classifier.plot_confusion_matrix(y_test, y_pred)
    classifier.plot_sample_predictions(X_test, y_test, y_pred, y_pred_proba)
    classifier.model.save('histogram_classifier_model.h5')
    print("\nModel saved as 'histogram_classifier_model.h5'")
    print("\nHistogram classification pipeline completed successfully!")

if __name__ == "__main__":
    main()
