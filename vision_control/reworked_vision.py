import cv2
import urllib.request
import numpy as np
import torch
from ultralytics import YOLO
import logging


class NewView:
    def __init__(self):
        logging.getLogger("ultralytics").setLevel(logging.ERROR)
        self.model = YOLO("best (6).pt")
        self.url = 'http://192.168.2.35:8080/?action=stream'
        self.stream = urllib.request.urlopen(self.url)
        self.bts = bytes()

    def view(self):
        while True:
            self.bts += self.stream.read(1024)
            a = self.bts.find(b'\xff\xd8')
            b = self.bts.find(b'\xff\xd9')
            if a == -1 or b == -1:
                continue
            jpg = self.bts[a:b + 2]
            self.bts = self.bts[b + 2:]
            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            predict = self.model.predict(frame, conf=0.7)
            frame = predict[0].plot()
            cv2.imshow('Live Stream', frame)
            key = cv2.waitKey(1)
            if key & 0xff == ord('q'):
                return -1
            obj = self.find_obj(0, predict)
            try:
                with open('costyl', 'w') as f:
                    if type(obj) != list:
                        # x, y, X, Y = obj.tolist()
                        # print((x + X) / 2)
                        # print((y + Y) / 2)
                        f.write(' '.join(list(map(str, obj.tolist()))) + '\n')
                    else:
                        f.write('-1')
            except Exception as e:
                pass

    def define_class(self, cls_id, xyxys, classes):
        mask = classes == cls_id
        return xyxys[mask][0] if torch.any(mask) else [-1]

    def find_obj(self, cls_id, results):
        boxes = results[0].boxes
        classif = boxes.cls
        xyxys = boxes.xyxy
        return self.define_class(cls_id, xyxys, classif)


if __name__ == '__main__':
    vied = NewView()
    vied.view()
