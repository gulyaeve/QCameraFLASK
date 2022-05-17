import socket

from PyQt5.QtCore import QThread
from flask import Flask, Response

myip = socket.gethostbyname(socket.getfqdn())
app = Flask(__name__)


# TODO: Make method in WebServer class, make QThread for server


class WebServer(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.app = app

    def run(self):
        print("webserver started")
        self.app.run(host=myip, debug=False)

    @app.route("/")
    def stream(self):
        return Response(self.camera.gen_frames, mimetype='multipart/x-mixed-replace; boundary=frame')

