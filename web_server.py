from logging import log, INFO

from PyQt5.QtCore import QThread, QObject
from flask import Flask, Response


class WebServer(QObject):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

        # print(self.thread().)
        # self.moveToThread()


    def run(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/', endpoint=None, view_func=self.stream)
        log(INFO, f"webserver started")
        self.app.run(host="0.0.0.0")
    #     log(INFO, f"webserver started")
    #     self.app.run(host="0.0.0.0")

    # def stopstream(self):
    #     log(INFO, "webserver closed")
    #     del self
        # self.setTerminationEnabled(True)
        # self.currentThread().terminate()

    def stream(self):
        return Response(next(self.camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    #
    # def stopstream(self):
    #
    #     log(INFO, "webserver closed")





