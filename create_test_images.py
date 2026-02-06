from PIL import Image
import os

# Create directories
os.makedirs('media/products', exist_ok=True)
os.makedirs('media/categories', exist_ok=True)

# Create a simple test image
img = Image.new('RGB', (200, 200), color='blue')
img.save('media/products/test.jpg')

img2 = Image.new('RGB', (200, 200), color='red')
img2.save('media/categories/test.jpg')

print("Test images created successfully!")
