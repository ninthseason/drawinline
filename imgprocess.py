import cv2
import numpy as np
from lib import StrokeBuilder


def image2stroke(img):
    return StrokeBuilder().from_image(img)


def file2stroke(filename, resize=None):
    return StrokeBuilder().from_image(cv2.imread(filename), resize=resize)


if __name__ == '__main__':
    stroke = file2stroke("test.jpg", resize=(700, 700))
    print(stroke)
    from matplotlib import pyplot as plt

    plt.ion()
    for i in stroke:
        data = list(zip(*i))
        plt.plot(np.array(data[0]) * 1, np.array(data[1]) * -1)
        plt.pause(0.001)
    plt.pause(1000)
