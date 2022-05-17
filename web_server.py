import socket

from PyQt5.QtCore import QThread
from flask import Flask, Response

# myip = socket.gethostbyname(socket.getfqdn())
myip = "0.0.0.0"
app = Flask(__name__)


# TODO: fix stream in webpage


class WebServer(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.app = app
        self.app.add_url_rule('/', endpoint=None, view_func=self.stream)

    def run(self):
        print("webserver started")
        self.app.run(host=myip, debug=False)

    def stream(self):
        return Response(self.camera.gen_frames, mimetype='multipart/x-mixed-replace; boundary=frame')



