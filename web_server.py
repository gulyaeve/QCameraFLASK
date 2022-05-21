from logging import log, INFO

import socket
from PyQt5.QtCore import QThread
from flask import Flask, Response


class WebServer(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

        self.app = Flask(__name__)
        self.app.add_url_rule('/', endpoint=None, view_func=self.stream)

        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 8899

    def run(self):
        log(INFO, f"webserver started")
        self.app.run(host=self.ip, port=self.port)

    def getinfo(self):
        return f'http://{self.ip}:{self.port}'

    def stream(self):
        return Response(next(self.camera), mimetype='multipart/x-mixed-replace; boundary=frame')

