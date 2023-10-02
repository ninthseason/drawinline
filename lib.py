from collections import deque

import cv2
import numpy as np


class StrokeBuilder:
    def __init__(self):
        self.stroke = []
        self.tmp = []

    def commit(self):
        if len(self.tmp) != 0:
            self.stroke.append(self.tmp)
            self.tmp = []

    def add(self, point):
        self.tmp.append(point)

    def build(self):
        return self.stroke

    def from_image(self, img, preprocess=True, resize=None):
        if preprocess:
            if resize is not None:
                img = cv2.resize(img, resize)
            img_bin = image_linearize(img)
            img_bin = image_linearize(img_bin, size=(2, 2), is_gray=True)
        else:
            img_bin = img
        # cv2.imwrite("result.jpg", img_bin)
        # exit()
        area_to_scan = []
        for x in range(img_bin.shape[0]):
            for y in range(img_bin.shape[1]):
                if img_bin[x][y] == 0:
                    img_bin[x][y] = 255
                    self.add([y, x])
                    area_to_scan = area8(x, y, img_bin.shape)

                while len(area_to_scan) != 0:
                    ix, iy = area_to_scan.pop(0)
                    if img_bin[ix][iy] == 0:
                        img_bin[ix][iy] = 255
                        self.add([iy, ix])
                        for jx, jy in area_to_scan:
                            if img_bin[jx][jy] == 0:
                                img_bin[jx][jy] = 255
                        area_to_scan = area8(ix, iy, img_bin.shape)
                self.commit()
        return self.build()

    def from_image_df(self, img, preprocess=True, resize=None):
        if preprocess:
            if resize is not None:
                img = cv2.resize(img, resize)
            img_bin = image_linearize(img)
            img_bin = image_linearize(img_bin, size=(2, 2), is_gray=True)
        else:
            img_bin = img
        # cv2.imwrite("result.jpg", img_bin)
        # exit()
        area_to_scan = deque()
        for x in range(img_bin.shape[0]):
            for y in range(img_bin.shape[1]):
                if img_bin[x][y] == 0:
                    img_bin[x][y] = 255
                    self.add([y, x])
                    [area_to_scan.appendleft(i) for i in area8(x, y, img_bin.shape)]

                while len(area_to_scan) != 0:
                    ix, iy = area_to_scan.popleft()
                    if img_bin[ix][iy] == 0:
                        img_bin[ix][iy] = 255
                        self.add([iy, ix])
                        [area_to_scan.appendleft(i) for i in area8(ix, iy, img_bin.shape)]
                self.commit()
        return self.build()


def image_linearize(img, size=(3, 3), is_gray=False):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if not is_gray else img
    img_invert = 255 - img_gray

    shape = cv2.MORPH_RECT
    kernel = cv2.getStructuringElement(shape, size)

    min_image = cv2.erode(img_invert, kernel)

    linear_reduction = img_gray + min_image
    threshold = 230
    img_bin = np.where(linear_reduction > threshold, 255, 0).astype("uint8")
    return img_bin


def area8(px, py, im_shape):
    area = [(px - 1, py - 1), (px, py - 1), (px + 1, py - 1),
            (px - 1, py), (px + 1, py),
            (px - 1, py + 1), (px, py + 1), (px + 1, py + 1)]
    i = 0
    while i < len(area):
        p = area[i]
        if p[0] < 0 or p[0] >= im_shape[0] or p[1] < 0 or p[1] >= im_shape[1]:
            area.pop(i)
            i -= 1
        i += 1
    return area
