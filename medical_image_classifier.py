"""
Medical Image Classification using TensorFlow
Binary classification of healthy vs tumour tissue images
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

class MedicalImageClassifier:
    def __init__(self, data_dir='Processed', img_size=(128, 128)):
        self.data_dir = data_dir
        self.img_size = img_size
        self.model = None
        self.history = None
        
    def load_and_preprocess_data(self):
        """Load images from healthy and tumour folders and preprocess them"""
        print("Loading and preprocessing data...")
        
        images = []
        labels = []
        
        # Load healthy images (label = 0)
        healthy_dir = os.path.join(self.data_dir, 'healthy')
        for root, dirs, files in os.walk(healthy_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path).convert('L')  # Convert to grayscale
                        img = img.resize(self.img_size)
                        img_array = np.array(img)
                        images.append(img_array)
                        labels.append(0)  # 0 for healthy
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        
        # Load tumour images (label = 1)
        tumour_dir = os.path.join(self.data_dir, 'tumour')
        for root, dirs, files in os.walk(tumour_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    img_path = os.path.join(root, file)
                    try:
                        img = Image.open(img_path).convert('L')  # Convert to grayscale
                        img = img.resize(self.img_size)
                        img_array = np.array(img)
                        images.append(img_array)
                        labels.append(1)  # 1 for tumour
                    except Exception as e:
                        print(f"Error loading {img_path}: {e}")
        
        # Convert to numpy arrays
        X = np.array(images)
        y = np.array(labels)
        
        # Normalize pixel values to [0, 1]
        X = X.astype('float32') / 255.0
        
        # Add channel dimension for CNN (128, 128, 1)
        X = np.expand_dims(X, axis=-1)
        
        print(f"Loaded {len(X)} images")
        print(f"Healthy images: {np.sum(y == 0)}")
        print(f"Tumour images: {np.sum(y == 1)}")
        print(f"Image shape: {X.shape}")
        
        return X, y
    
    def create_model(self):
        """Create CNN model architecture"""
        print("Creating CNN model...")
        
        model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 1)),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Second Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Third Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Fourth Convolutional Block
            layers.Conv2D(256, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.25),
            
            # Global Average Pooling instead of Flatten
            layers.GlobalAveragePooling2D(),
            
            # Dense layers
            layers.Dense(512, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            # Output layer for binary classification
            layers.Dense(1, activation='sigmoid')
        ])
        
        # Compile model
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        self.model = model
        print("Model created successfully!")
        print(f"Total parameters: {model.count_params():,}")
        
        return model
    
    def train_model(self, X, y, validation_split=0.2, epochs=50, batch_size=32):
        """Train the model with data augmentation"""
        print("Training model...")
        
        # Split data into train and validation sets
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=validation_split, random_state=42, stratify=y
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Validation samples: {len(X_val)}")
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rotation_range=20,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            zoom_range=0.1,
            fill_mode='nearest'
        )
        
        # No augmentation for validation
        val_datagen = ImageDataGenerator()
        
        # Create data generators
        train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
        val_generator = val_datagen.flow(X_val, y_val, batch_size=batch_size)
        
        # Callbacks
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            callbacks.ModelCheckpoint(
                'best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
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
        
        # Make predictions
        y_pred_proba = self.model.predict(X_test)
        y_pred = (y_pred_proba > 0.5).astype(int).flatten()
        
        # Calculate metrics
        test_loss, test_accuracy, test_precision, test_recall = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"\nTest Results:")
        print(f"Accuracy: {test_accuracy:.4f}")
        print(f"Precision: {test_precision:.4f}")
        print(f"Recall: {test_recall:.4f}")
        print(f"F1-Score: {2 * (test_precision * test_recall) / (test_precision + test_recall):.4f}")
        
        # Classification report
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
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
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
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
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
        plt.savefig('sample_predictions.png', dpi=300, bbox_inches='tight')
        plt.show()

def main():
    """Main function to run the classification pipeline"""
    print("Medical Image Classification Pipeline")
    print("=" * 50)
    
    # Initialize classifier
    classifier = MedicalImageClassifier()
    
    # Load and preprocess data
    X, y = classifier.load_and_preprocess_data()
    
    # Create model
    model = classifier.create_model()
    
    # Print model summary
    print("\nModel Architecture:")
    model.summary()
    
    # Train model
    history = classifier.train_model(X, y, epochs=50, batch_size=32)
    
    # Split data for final evaluation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Evaluate model
    y_pred, y_pred_proba = classifier.evaluate_model(X_test, y_test)
    
    # Plot results
    classifier.plot_training_history()
    classifier.plot_confusion_matrix(y_test, y_pred)
    classifier.plot_sample_predictions(X_test, y_test, y_pred, y_pred_proba)
    
    # Save model
    classifier.model.save('medical_classifier_model.h5')
    print("\nModel saved as 'medical_classifier_model.h5'")
    
    print("\nClassification pipeline completed successfully!")

if __name__ == "__main__":
    main()
