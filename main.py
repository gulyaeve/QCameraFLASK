
from PyQt5.QtWidgets import QApplication

from views import UI_Window
from models import Camera
from web_server import WebServer

if __name__ == '__main__':

    camera = Camera(0)

    webserver = WebServer(camera)
    webserver.start()

    app = QApplication([])
    start_window = UI_Window(camera)
    start_window.show()
    app.exit(app.exec_())
