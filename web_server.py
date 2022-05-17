import socket

from flask import Flask, Response

# myip =
# app = Flask(__name__)

# TODO: Make method in WebServer class, make QThread for server
@app.route("/")
def stream():
    return Response(camera, mimetype='multipart/x-mixed-replace; boundary=frame')

class WebServer(Flask):
    def __init__(self, camera=None):
        super().__init__()
        self.host = socket.gethostbyname(socket.getfqdn())
        self.camera = camera




if __name__ == '__main__':
    webserver = WebServer.run(debug=False)
    # app.run(host=myip, debug=False)
