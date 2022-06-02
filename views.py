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

        self.version = '0.1.1'

        self.isPasswordEntered = False
        # Add a button
        self.button_layout = QHBoxLayout()
        self.password_layout = QHBoxLayout()

        self.cameras = []
        for i in QCameraInfo.availableCameras():
            self.cameras.append(i.description())

        self.cam1label = QLabel('Камера 1: ')
        self.camerasCombo = QComboBox()
        self.camerasCombo.addItems(self.cameras)
        self.camerasCombo.activated[str].connect(self.onCameraSelect)
        self.camerasCombo.activated[str].connect(self.start)
        self.button_layout.addWidget(self.cam1label)
        self.button_layout.addWidget(self.camerasCombo)

        self.portlabel = QLabel("Порт: ")
        self.portEdit = QLineEdit()
        self.passwordlabel = QLabel("Пароль: ")
        self.password_layout.addWidget(self.portlabel)
        self.password_layout.addWidget(self.portEdit)
        self.password_layout.addWidget(self.passwordlabel)

        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.send = QPushButton('Ввести порт и пароль')
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

        self.button2_layout = QHBoxLayout()
        self.password2_layout = QHBoxLayout()
        self.cam2label = QLabel('Камера 2: ')
        self.cameras2Combo = QComboBox()
        self.cameras2Combo.addItems(self.cameras)
        self.cameras2Combo.activated[str].connect(self.onCameraSelect)
        # self.cameras2Combo.activated[str].connect(self.start)
        self.button2_layout.addWidget(self.cam2label)
        self.button2_layout.addWidget(self.cameras2Combo)

        self.port2label = QLabel("Порт: ")
        self.port2Edit = QLineEdit()
        self.password2label = QLabel("Пароль: ")
        self.password2_layout.addWidget(self.port2label)
        self.password2_layout.addWidget(self.port2Edit)
        self.password2_layout.addWidget(self.password2label)

        self.password2Edit = QLineEdit()
        self.password2Edit.setEchoMode(QLineEdit.Password)
        self.send2 = QPushButton('Ввести порт и пароль')
        # self.send2.clicked.connect(self.sendPassword)
        self.password2_layout.addWidget(self.password2Edit)
        self.password2_layout.addWidget(self.send2)

        self.layout.addLayout(self.button2_layout)
        self.layout.addLayout(self.password2_layout)

        self.stream2button = QPushButton("Начать трансляцию")
        # self.stream2button.clicked.connect(self.startStream)
        self.layout.addWidget(self.stream2button)
        self.stream2button.setDisabled(True)

        self.stream2link = QLabel()
        self.stream2link.setText('')
        self.stream2link.setOpenExternalLinks(True)
        self.layout.addWidget(self.stream2link)


        # Add a label
        self.cameraview = QLabel()
        self.layout.addWidget(self.cameraview)

        # Set the layout
        self.setLayout(self.layout)
        self.setWindowTitle("NotVLC -- BETA ver. " + self.version)
        self.setFixedSize(650, 640)
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
        # self.start()

    def startStream(self):
        self.timer.stop()
        self.cameraview.clear()
        self.cameraview.setFixedSize(640, int(self.cameraheight))
        self.password = self.sendPassword()
        webserver = WebServer(self.camera, int(self.port1), self.password)
        selectedcamera = self.cameras[self.cameraindx]
        streamadrr = webserver.getinfo()
        self.setWindowTitle(f"<<ИДЁТ ТРАНСЛЯЦИЯ>>")
        message = f'Идёт трансляция <i>{selectedcamera}</i> по адресу: <br />' \
                  f'<a href="{streamadrr}/admin:{self.password}">{streamadrr}/admin:{self.password}</a>'
        self.streamlink.setText(message)
        webserver.start()
        self.camerasCombo.setDisabled(True)
        self.streambutton.setDisabled(True)

    def sendPassword(self):
        self.passwordText = self.passwordEdit.text()
        self.port1 = self.portEdit.text()
        if self.passwordText != '' and self.port1.isdigit() and 1 < int(self.port1) < 65536:
            self.isPasswordEntered = True
            self.streambutton.setEnabled(True)
        else:
            self.isPasswordEntered = False
            self.streambutton.setDisabled(True)
        return self.passwordText

# TODO: add field to enter port