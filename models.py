from logging import log, INFO

import cv2
import imutils as imutils
from PyQt5 import QtTest

class Camera:

    def __init__(self, camera):
        self.vc = cv2.VideoCapture(camera, cv2.CAP_ANY)

    def open(self):
        return self.vc.isOpened()

    def read(self, negative=False):
        if self.open():
            ret, frame = self.vc.read()
            frame = imutils.resize(frame, width=640)
            if frame is not None:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                if negative:
                    frame = cv2.bitwise_not(frame)
                return frame

    def getheight(self):
        if self.open():
            ret, frame = self.vc.read()
            frame = imutils.resize(frame, width=640)
            frame_height = frame.shape[0]
            log(INFO, f"Frame height {frame_height}")
            return frame_height

    def __next__(self):
        if self.open():
            while True:
                QtTest.QTest.qWait(100)
                ret, frame = self.vc.read()
                frame = imutils.resize(frame, width=640)
                if ret:
                    ret, buffer = cv2.imencode(".jpg", frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# TODO: add timer to delay fps