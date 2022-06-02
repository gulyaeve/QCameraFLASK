from logging import log, INFO

import socket
from PyQt5.QtCore import QThread
from flask import Flask, Response


class WebServer(QThread):
    def __init__(self, camera, port, password):
        super().__init__()
        self.camera = camera
        self.password = password


        self.app = Flask(__name__)
        self.app.add_url_rule(f'/admin:{self.password}', endpoint=None, view_func=self.stream)

        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        self.port = port

    def run(self):
        log(INFO, f"webserver started at http://{self.ip}:{self.port}")
        self.app.run(host=self.ip, port=self.port)

    def getinfo(self):
        return f'http://{self.ip}:{self.port}'

    def stream(self):
        return Response(next(self.camera), mimetype='multipart/x-mixed-replace; boundary=frame')
