import cv2
import numpy as np
from lib import StrokeBuilder


def image2stroke(img):
    return StrokeBuilder().from_image_m(img)


def file2stroke(filename):
    return StrokeBuilder().from_image_m(cv2.imread(filename))


if __name__ == '__main__':
    stroke = file2stroke("test.jpg")
    print(stroke)
    from matplotlib import pyplot as plt

    plt.ion()
    for i in stroke:
        data = list(zip(*i))
        plt.plot(np.array(data[0]) * 1, np.array(data[1]) * -1)
        plt.pause(0.001)
    plt.pause(1000)
