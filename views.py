from logging import log, INFO

from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QLineEdit
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

        self.isPasswordEntered = False
        # Add a button
        self.button_layout = QHBoxLayout()
        self.password_layout = QHBoxLayout()

        self.cameras = []
        for i in QCameraInfo.availableCameras():
            self.cameras.append(i.description())

        self.camerasCombo = QComboBox()
        self.camerasCombo.addItems(self.cameras)
        self.camerasCombo.activated[str].connect(self.onCameraSelect)
        self.camerasCombo.activated[str].connect(self.start)
        self.button_layout.addWidget(self.camerasCombo)

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.send = QPushButton('Ввести пароль')
        self.send.clicked.connect(self.sendPassword)
        self.password_layout.addWidget(self.passwordEdit)
        self.password_layout.addWidget(self.send)

        self.layout.addLayout(self.button_layout)
        self.layout.addLayout(self.password_layout)

        self.streambutton = QPushButton("Начать трансляцию")
        self.streambutton.clicked.connect(self.startStream)
        self.layout.addWidget(self.streambutton)
        self.streambutton.setDisabled(True)

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
        self.cameraheight = 480
        self.start()

    def selectedCamera(self):
        return self.cameraindx

    def start(self):
        if not self.camera.open():
            log(INFO, f"Failed camera {self.cameras[self.selectedCamera()]}")
            msgBox = QMessageBox()
            msgBox.setText("Ошибка при открытии камеры.")
            msgBox.exec_()
            self.streambutton.setDisabled(True)
            return
        else:
            if self.isPasswordEntered:
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
        if self.cameraheight is not None:
            self.cameraview.setFixedSize(640, int(self.cameraheight))
        self.start()

    def startStream(self):
        self.timer.stop()
        self.cameraview.clear()
        self.cameraview.setFixedSize(640, int(self.cameraheight))
        self.password = self.sendPassword()
        webserver = WebServer(self.camera, self.password)
        selectedcamera = self.cameras[self.cameraindx]
        streamadrr = webserver.getinfo()
        self.setWindowTitle(f"ИДЁТ ТРАНСЛЯЦИЯ {selectedcamera} по адресу: {streamadrr}")
        message = f'Идёт трансляция <i>{selectedcamera}</i> по адресу: ' \
                  f'<a href="{streamadrr}/admin:{self.password}">{streamadrr}/admin:{self.password}</a>'
        self.streamlink.setText(message)
        webserver.start()
        self.camerasCombo.setDisabled(True)
        self.streambutton.setDisabled(True)

    def sendPassword(self):
        self.passwordText = self.passwordEdit.text()
        if self.passwordText != '':
            self.isPasswordEntered = True
            self.streambutton.setEnabled(True)
        else:
            self.isPasswordEntered = False
            self.streambutton.setDisabled(True)
        return self.passwordText