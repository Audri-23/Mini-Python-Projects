from rembg import remove
from PIL import Image

input_path = "./remove.jpg"
output_path = "./removed.png"

inp = Image.open(input_path)
output = remove(inp)
output.save(output_path)