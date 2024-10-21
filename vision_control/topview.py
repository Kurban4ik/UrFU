import cv2
import urllib.request
import numpy as np
import torch
from ultralytics import YOLO
import logging
from go import Go

key_points = [
    (),
    (525, 258),
    (773, 245),
    (895, 275),
    (1010, 250),
    (1252, 457),
    (1258, 543),
    (1220, 836),
    (990, 852),
    (882, 820),
    (748, 851),
    (522, 840),
    (534, 661),
    (727, 389),
    (895, 388),
    (1058, 398),
    (723, 540),
    (1058, 540),
    (723, 708),
    (883, 723),
    (1050, 708),
    (1201, 551),
    (1249, 563),
    (570, 543),
    (522, 443)
]


class TopView:
    def __init__(self, go: Go):
        self.go = go
        logging.getLogger("ultralytics").setLevel(logging.ERROR)
        self.model = YOLO("best (6).pt")
        url = "rtsp://Admin:rtf123@192.168.2.250/251:554/1/1"
        self.cap = cv2.VideoCapture(url)
        if not self.cap.isOpened():
            print("Ошибка открытия видеофайла")
            self.cap.release()
            cv2.destroyAllWindows()
            exit()
        self.vec = [0, -1]  # вектор, в который смотрит робот
        self.me = [*(key_points[11])]  # изначальные координаты

    def set_position(self):
        # здесь будет код Егора
        self.me = [500, 500]
        return
    def go_to_point(self, point):
        self.go.slow()

if __name__ == '__main__':
    topview = TopView()
