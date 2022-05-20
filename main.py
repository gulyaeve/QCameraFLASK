import logging

from PyQt5.QtWidgets import QApplication

from views import UI_Window
from models import Camera
from web_server import WebServer

logging.basicConfig(handlers=(logging.FileHandler('logs/log.txt'), logging.StreamHandler()),
                    format=u'%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)-15s %(message)s',
                    level=logging.INFO,
                    )

if __name__ == '__main__':
    app = QApplication([])
    start_window = UI_Window()
    # selectedCamera = start_window.selectedCamera()
    # camera = Camera(selectedCamera)
    # webserver = WebServer(camera)
    # webserver.start()
    start_window.show()
    app.exit(app.exec_())

