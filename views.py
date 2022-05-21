from logging import log, INFO

from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap, QImage

from models import Camera
from web_server import WebServer


class UI_Window(QWidget):

    def __init__(self):
        super().__init__()
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        # Create a layout.
        self.layout = QVBoxLayout()

        # Add a button
        self.button_layout = QHBoxLayout()

        self.cameras = []
        for i in QCameraInfo.availableCameras():
            self.cameras.append(i.description())

        self.camerasCombo = QComboBox()
        self.camerasCombo.addItems(self.cameras)
        self.camerasCombo.activated[str].connect(self.onCameraSelect)
        self.camerasCombo.activated[str].connect(self.start)
        self.button_layout.addWidget(self.camerasCombo)

        self.layout.addLayout(self.button_layout)

        self.streambutton = QPushButton("Начать трансляцию")
        self.streambutton.clicked.connect(self.startStream)
        self.layout.addWidget(self.streambutton)

        self.streamlink = QLabel()
        self.streamlink.setText('')
        self.streamlink.setOpenExternalLinks(True)
        self.layout.addWidget(self.streamlink)

        # Add a label
        self.cameraview = QLabel()
        self.layout.addWidget(self.cameraview)

        # Set the layout
        self.setLayout(self.layout)
        self.setWindowTitle("NotVLC -- BETA")
        # self.setFixedSize(800, 800)
        self.cameraindx = 0
        self.camera = Camera(self.cameraindx)
        self.cameraheight = int(self.camera.getheight())
        self.start()

    def selectedCamera(self):
        return self.cameraindx

    def start(self):
        if not self.camera.open():
            log(INFO, "Failed camera")
            msgBox = QMessageBox()
            msgBox.setText("Ошибка при открытии камеры.")
            msgBox.exec_()
            self.streambutton.setDisabled(True)
            return
        else:
            self.streambutton.setEnabled(True)

        self.timer.start(60)

    def nextFrameSlot(self):
        frame = self.camera.read()
        if frame is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.cameraview.setPixmap(pixmap)

    def onCameraSelect(self, text):
        self.cameraindx = self.cameras.index(text)
        self.camera = Camera(self.cameraindx)
        self.cameraheight = self.camera.getheight()
        self.cameraview.setFixedSize(640, int(self.cameraheight))
        self.start()

    def startStream(self):
        self.timer.stop()
        self.cameraview.clear()
        self.cameraview.setFixedSize(640, int(self.cameraheight))
        webserver = WebServer(self.camera)
        selectedcamera = self.cameras[self.cameraindx]
        streamadrr = webserver.getinfo()
        self.setWindowTitle(f"ИДЁТ ТРАНСЛЯЦИЯ {selectedcamera} по адресу: {streamadrr}")
        message = f'Идёт трансляция <i>{selectedcamera}</i> по адресу: <a href="{streamadrr}">{streamadrr}</a>'
        self.streamlink.setText(message)
        webserver.start()
        self.camerasCombo.setDisabled(True)
        self.streambutton.setDisabled(True)
