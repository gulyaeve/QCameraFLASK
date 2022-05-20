from logging import log, INFO

from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap, QImage

from models import Camera


class UI_Window(QWidget):

    def __init__(self):
        super().__init__()
        # print('UI')
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)


        # Create a layout.
        layout = QVBoxLayout()

        # Add a button
        button_layout = QHBoxLayout()

        # btnCamera = QPushButton("Open camera")
        # btnCamera.clicked.connect(self.start)
        # button_layout.addWidget(btnCamera)

        self.cameras = []
        for i in QCameraInfo.availableCameras():
            self.cameras.append(i.description())

        camerasCombo = QComboBox()
        camerasCombo.addItems(self.cameras)
        camerasCombo.activated[str].connect(self.onCameraSelect)
        # camerasCombo.activated[str].connect(self.start)
        button_layout.addWidget(camerasCombo)

        layout.addLayout(button_layout)

        # btnCamera2 = QPushButton("Stream")
        # btnCamera2.clicked.connect(self.stream2)
        # button_layout.addWidget(btnCamera2)
        # layout.addLayout(button_layout)

        # Add a label
        self.label = QLabel()
        self.label.setFixedSize(640, 640)

        layout.addWidget(self.label)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("First GUI with QT")
        # self.setFixedSize(800, 800)
        self.cameraindx = 0
        self.camera = Camera(self.cameraindx)
        self.start()

    def selectedCamera(self):
        return self.cameraindx

    def start(self):
        if not self.camera.open():
            log(INFO, "Failed camera")
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

        self.timer.start(1000. / 24)

    def nextFrameSlot(self):
        frame = self.camera.read()
        # frame = self.camera.read_gray()
        if frame is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)

    def onCameraSelect(self, text):
        self.cameraindx = self.cameras.index(text)
        self.camera = Camera(self.cameraindx)
        self.start()
