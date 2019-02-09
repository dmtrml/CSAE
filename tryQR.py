from pyzbar.pyzbar import decode
from PIL import Image


im = Image.open("2.jpg")

x = decode(im)
print(x)