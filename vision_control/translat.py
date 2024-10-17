import asyncio
import time

import cv2
import urllib.request
import numpy as np
from ultralytics import YOLO
import logging

from movement_control.catch import make_a_move_to_ball, come_at_distance, rotate_to_pix, make_a_move_to_cube
from movement_control.move_commands import up, catch, straight_servo, prepare_to_catch

catch_methods = {0: make_a_move_to_ball, 7: make_a_move_to_cube}


def define_class(cls_id, xyxys, classes):
    result = -1
    if len(classes):
        for i in range(len(classes)):
            if classes[i] == cls_id:
                result = xyxys[i]
    return result

logging.getLogger("ultralytics").setLevel(logging.ERROR)
model = YOLO("best (2).pt")
url = 'http://192.168.1.1:8080/?action=stream'
stream = urllib.request.urlopen(url)

bytes = bytes()

def find_obj(cls_id, results):
    boxes = results[0].boxes
    classif = boxes.cls.to(int).tolist()
    t = define_class(cls_id, boxes.xyxy, classif)
    return t

async def do():
    global bytes
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]

        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        predict = model.predict(frame, conf=0.8)
        frame = predict[0].plot()
        cv2.imshow('Live Stream', frame)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):
            return -1
        return -1, 0
        obj = find_obj(0, predict)
        if type(obj) != int and len(obj):
            return obj.tolist(), 0


async def react(dots, cls_id):
    if dots == -1 or dots == 12:
        return
    res = catch_methods[cls_id](*dots)
    if res[0] == 'catch':
        come_at_distance(3)
        prepare_to_catch()
        straight_servo()
        catch()
        up()
    elif res[0] == 'rotate':
        rotate_to_pix(*res[1:])
    elif res[0] == 'come':
        come_at_distance(res[1])
    time.sleep(0.4)
async def main():
    while True:
        task_do = asyncio.create_task(do())
        task_react = asyncio.create_task(react(-1, -1))

        done, pending = await asyncio.wait({task_do, task_react}, return_when=asyncio.FIRST_COMPLETED)

        for task in done:
            if task == task_do:
                result_do = task.result()
                if result_do:
                    await react(*result_do)  # Вызов react() с результатом do()
            elif task == task_react:
                result_react = task.result()
                if result_react:
                    pass

asyncio.run(main())
cv2.destroyAllWindows()



