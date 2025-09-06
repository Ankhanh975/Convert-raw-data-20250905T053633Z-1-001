"""
Quick Medical Image Classification Demo
Shows the technologies and provides training results
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

def load_and_preprocess_data(data_dir='Processed', img_size=(128, 128)):
    """Load images from healthy and tumour folders and preprocess them"""
    print("Loading and preprocessing data...")
    
    images = []
    labels = []
    
    # Load healthy images (label = 0)
    healthy_dir = os.path.join(data_dir, 'healthy')
    for root, dirs, files in os.walk(healthy_dir):
        for file in files:
            if file.lower().endswith('.png'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path).convert('L')  # Convert to grayscale
                    img = img.resize(img_size)
                    img_array = np.array(img)
                    images.append(img_array)
                    labels.append(0)  # 0 for healthy
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")
    
    # Load tumour images (label = 1)
    tumour_dir = os.path.join(data_dir, 'tumour')
    for root, dirs, files in os.walk(tumour_dir):
        for file in files:
            if file.lower().endswith('.png'):
                img_path = os.path.join(root, file)
                try:
                    img = Image.open(img_path).convert('L')  # Convert to grayscale
                    img = img.resize(img_size)
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

def create_simplified_model(img_size=(128, 128)):
    """Create a simplified CNN model for demonstration"""
    print("Creating simplified CNN model...")
    
    model = models.Sequential([
        # First Convolutional Block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*img_size, 1)),
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
        
        # Global Average Pooling
        layers.GlobalAveragePooling2D(),
        
        # Dense layers
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
    
    print("Model created successfully!")
    print(f"Total parameters: {model.count_params():,}")
    
    return model

def main():
    """Main function to demonstrate the classification pipeline"""
    print("Medical Image Classification - Technology Overview")
    print("=" * 60)
    
    # Load and preprocess data
    X, y = load_and_preprocess_data()
    
    # Create model
    model = create_simplified_model()
    
    # Print model summary
    print("\nModel Architecture:")
    model.summary()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nData Split:")
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model with fewer epochs for demo
    print("\nTraining model (5 epochs for demo)...")
    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=5,
        batch_size=32,
        verbose=1
    )
    
    # Evaluate model
    print("\nEvaluating model...")
    test_loss, test_accuracy, test_precision, test_recall = model.evaluate(X_test, y_test, verbose=0)
    
    print(f"\nTest Results:")
    print(f"Accuracy: {test_accuracy:.4f}")
    print(f"Precision: {test_precision:.4f}")
    print(f"Recall: {test_recall:.4f}")
    print(f"F1-Score: {2 * (test_precision * test_recall) / (test_precision + test_recall):.4f}")
    
    # Make predictions
    y_pred_proba = model.predict(X_test)
    y_pred = (y_pred_proba > 0.5).astype(int).flatten()
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Healthy', 'Tumour']))
    
    # Plot training history
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 3, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 3, 3)
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=['Healthy', 'Tumour'],
               yticklabels=['Healthy', 'Tumour'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    
    plt.tight_layout()
    plt.savefig('classification_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nClassification pipeline completed successfully!")

if __name__ == "__main__":
    main()
