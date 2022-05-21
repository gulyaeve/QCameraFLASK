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

        self.btnCamera2 = QPushButton("Stream")
        self.btnCamera2.clicked.connect(self.startStream)
        self.layout.addWidget(self.btnCamera2)

        self.label1 = QLabel()
        self.label1.setText('')
        self.label1.setOpenExternalLinks(True)
        self.layout.addWidget(self.label1)

        # Add a label
        self.label = QLabel()
        self.label.setFixedSize(640, 640)

        self.layout.addWidget(self.label)

        # Set the layout
        self.setLayout(self.layout)
        self.setWindowTitle("NotVLC")
        # self.setFixedSize(800, 800)
        self.cameraindx = 0
        self.camera = Camera(self.cameraindx)
        self.start()

    def selectedCamera(self):
        return self.cameraindx

    def start(self):
        if not self.camera.open():
            log(INFO, "Failed camera")
            self.msgBox = QMessageBox()
            self.msgBox.setText("Failed to open camera.")
            self.msgBox.exec_()
            self.btnCamera2.setDisabled(True)
            return
        else:
            self.btnCamera2.setEnabled(True)

        self.timer.start(60)

    def nextFrameSlot(self):
        frame = self.camera.read()
        if frame is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)

    def onCameraSelect(self, text):
        self.cameraindx = self.cameras.index(text)
        self.camera = Camera(self.cameraindx)
        self.start()

    def startStream(self):
        self.webserver = WebServer(self.camera)
        self.label1.setText(f'<a href="{self.webserver.getinfo()}">{self.webserver.getinfo()}</a>')
        self.webserver.start()
        self.camerasCombo.setDisabled(True)
        self.btnCamera2.setDisabled(True)
