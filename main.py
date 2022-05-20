import logging

from PyQt5.QtCore import QObject, QThread
from PyQt5.QtWidgets import QApplication

from Controller import Controller
# from views import UI_Window
# from models import Camera
# from web_server import WebServer
# from models import Camera
from views import UI_Window

logging.basicConfig(handlers=(logging.FileHandler('logs/log.txt'), logging.StreamHandler()),
                    format=u'%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)-15s %(message)s',
                    level=logging.INFO,
                    )
controller = Controller()

if __name__ == '__main__':
    app = QApplication([])

    start_window = UI_Window()
    start_window.show()

    # controller.runwindow()
    # camera = Camera(0)
    # controller.runserver(camera)

    app.exit(app.exec_())
    # start_window.show()


