from PIL import Image, ImageDraw
import datetime

# Create a new image (width x height)
img = Image.new('RGB', (300, 100), color='white')
draw = ImageDraw.Draw(img)

# Draw 4 sweets as red circles
for i in range(4):
    draw.ellipse((20 + i*60, 30, 60 + i*60, 70), fill=(255, 100, 100))

# Name the file using current timestamp or question type
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"sweets_{timestamp}.png"

# Save the image
img.save(filename)

print(f"Image saved as {filename}")
