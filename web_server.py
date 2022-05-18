from PyQt5.QtCore import QThread
from flask import Flask, Response


class WebServer(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.app = Flask(__name__)
        self.app.add_url_rule('/', endpoint=None, view_func=self.stream)

    def run(self):
        print("webserver started")
        self.app.run(host="0.0.0.0", debug=False)

    def stream(self):
        return Response(next(self.camera), mimetype='multipart/x-mixed-replace; boundary=frame')
