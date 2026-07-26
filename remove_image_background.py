from rembg import remove
from PIL import Image

input_path = "./remove.jpg"     #name of the image file to remove background
output_path = "./removed.png"   #New image will be saved with this name

inp = Image.open(input_path)
output = remove(inp)
output.save(output_path)