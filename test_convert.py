from PIL import Image
import numpy as np

# Convert try.tiff to try.png
with Image.open('try.tiff') as img:
    print(f"Original mode: {img.mode}")
    print(f"Original size: {img.size}")
    print(f"Original format: {img.format}")
    
    # Convert floating point mode to uint8 for PNG
    if img.mode == 'F':
        # Convert to numpy array, normalize to 0-255, then back to PIL
        img_array = np.array(img)
        img_array = ((img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255).astype(np.uint8)
        img = Image.fromarray(img_array, mode='L')
        print(f"Converted mode to: {img.mode}")
    
    # Save as PNG
    img.save('try.png', 'PNG')
    print("Converted to try.png")
