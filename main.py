from graph import build_graph, segment_graph
from random import random
from PIL import Image, ImageFilter
import numpy as np
import cv2


def preprocess_image(image):
    load = cv2.imread(image, 0)
    greyscale = cv2.equalizeHist(load)
    greyscale = cv2.Canny(greyscale, 50, 75)
    _, greyscale = cv2.threshold(greyscale, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return greyscale


# Get intensity difference between two pixels.
def diff(img, x1, y1, x2, y2):
    _out = np.sum((img[x1, y1] - img[x2, y2]) ** 2)
    return np.sqrt(_out)


# Threshold function controlling the degree of how much the internal difference of two regions should be lower than the
# difference between the regions to conclude there is an evidence for a boundary.
def threshold(size, const):
    return const * 1.0 / size


# Generate the image with each component (segment) re-colored with a randomly chosen color.
def generate_image(forest, width, height):
    def random_color(): return int(random() * 255), int(random() * 255), int(random() * 255)
    colors = [random_color() for _ in range(width * height)]
    img = Image.new('RGB', (width, height))
    im = img.load()
    for y in range(height):
        for x in range(width):
            comp = forest.find(y * width + x)
            im[x, y] = colors[comp]
    return img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)


def get_segmented_image(sigma, k, min_comp_size, input_file, output_file):
    image = Image.fromarray(input_file)
    image.save("greyscale.jpg")
    # Image width and height (size[0], size[1]).
    size = image.size
    # Gaussian blur using PIL, parameter is sigma.
    smooth = image.filter(ImageFilter.GaussianBlur(sigma))
    # Convert an image into an array of data containing each pixel's RGB value like a 3x3 matrix.
    smooth = np.array(smooth)
    graph = build_graph(smooth, size[1], size[0], diff)
    forest = segment_graph(graph, size[0] * size[1], k, min_comp_size, threshold)
    image = generate_image(forest, size[1], size[0])
    image.save(output_file)


if __name__ == '__main__':
    sigma_value = 0.8
    k_value = 1000
    min_comp = 10
    input_image = "input.jpg"
    output_image = "output.jpg"
    img = preprocess_image(input_image)
    get_segmented_image(sigma_value, k_value, min_comp, img, output_image)
