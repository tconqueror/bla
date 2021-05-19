import numpy as np
from PIL import Image
import sys


def convert_image(image_name, size):
    img = Image.open(image_name).resize((size, size), 1)
    img = img.convert('L')
    image_array = np.array(img.getdata(), dtype=np.byte)
    image_array.tofile(".\\buffer.buf")
    img.save(".\\Grayscale.png")
    print(img)
    return image_array

def restore_image(path, size):
    #arr = Image.fromarray()
    data = np.fromfile(path, dtype = np.byte)
    data = np.reshape(data, (size,size))
    print(data)
    arr = Image.fromarray(data, mode = "L")
    arr.resize(size = (size,size))
    arr.save(".\\extract.png")
    return arr

def main():
    if (sys.argv[1] == "--extract"):
        c = convert_image(sys.argv[2], 100) #path
        print(c)
        print('Convert to buffer.buf')
    if (sys.argv[1] == "--restore"):
        c = restore_image(sys.argv[2], 100) #path to extracted buffer
        print(c)
        print('Restore to image')
if __name__ == "__main__":
    main()


# pip install pillow numpy
# --extract path_to_watermark_image
# --restore path_to_buffer