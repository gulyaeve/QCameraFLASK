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
        self.layout = QHBoxLayout()

        self.CameraLayout = [QVBoxLayout(), QVBoxLayout()]

        self.version = '0.1.1'

        self.isPasswordEntered = [False, False]
        # Add a button
        self.button_layout = [QHBoxLayout(), QHBoxLayout()]
        self.password_layout = [QHBoxLayout(), QHBoxLayout()]

        self.cameras = []
        for i in QCameraInfo.availableCameras():
            self.cameras.append(i.description())

        self.index = 0
        self.camlabel = [QLabel('Камера 1: '), QLabel('Камера 2: ')]
        self.camerasCombo = [QComboBox(), QComboBox()]
        for i in range(2):
            self.camerasCombo[i].addItems(self.cameras)
            #    self.camerasCombo[i].activated[str].connect(self.start)
        self.camerasCombo[0].activated[str].connect(self.onCamera0Select)
        self.camerasCombo[1].activated[str].connect(self.onCamera1Select)

        for i in range(2):
            self.button_layout[i].addWidget(self.camlabel[i])
            self.button_layout[i].addWidget(self.camerasCombo[i])

        self.portlabel = QLabel("Порт: ")
        self.portEdit = [QLineEdit(), QLineEdit()]
        self.passwordlabel = QLabel("Пароль: ")

        for i in range(2):
            self.password_layout[i].addWidget(self.portlabel)
            self.password_layout[i].addWidget(self.portEdit[i])
            self.password_layout[i].addWidget(self.passwordlabel)

        self.passwordEdit = [QLineEdit(), QLineEdit()]
        for i in range(2):
            self.passwordEdit[i].setEchoMode(QLineEdit.Password)
        self.send = [QPushButton('Ввести порт и пароль'), QPushButton('Ввести порт и пароль')]
        self.send[0].clicked.connect(self.sendPassword0)
        self.send[1].clicked.connect(self.sendPassword1)

        for i in range(2):
            self.password_layout[i].addWidget(self.passwordEdit[i])
            self.password_layout[i].addWidget(self.send[i])

            self.CameraLayout[i].addLayout(self.button_layout[i])
            self.CameraLayout[i].addLayout(self.password_layout[i])

        self.streambutton = [QPushButton("Начать трансляцию"), QPushButton("Начать трансляцию")]
        self.streambutton[0].clicked.connect(self.startStream0)
        self.streambutton[1].clicked.connect(self.startStream1)
        for i in range(2):
            self.CameraLayout[i].addWidget(self.streambutton[i])
            self.streambutton[i].setDisabled(True)

        self.streamlink = [QLabel(), QLabel()]
        for i in range(2):
            self.streamlink[i].setText('')
            self.streamlink[i].setOpenExternalLinks(True)
            self.CameraLayout[i].addWidget(self.streamlink[i])


        # Add a label
        self.cameraview = [QLabel(), QLabel()]
        for i in range(2):
            self.CameraLayout[i].addWidget(self.cameraview[i])
            # Set the layout
            self.layout.addLayout(self.CameraLayout[i])

        self.setLayout(self.layout)
        self.setWindowTitle("NotVLC -- BETA ver. " + self.version)
        # self.setFixedSize(650, 640)
        self.cameraindx = [0, 1]

    def selectedCamera(self):
        return self.cameraindx[self.index]

    def start(self):
        if not self.camera.open():
            log(INFO, f"Failed camera {self.cameras[self.selectedCamera()]}")
            msgBox = QMessageBox()
            msgBox.setText("Ошибка при открытии камеры.")
            msgBox.exec_()
            self.streambutton[self.index].setDisabled(True)
            return
        else:
            if self.isPasswordEntered:
                self.streambutton[self.index].setEnabled(True)

        self.timer.start(60)

    def nextFrameSlot(self):
        frame = self.camera.read()
        if frame is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.cameraview[self.index].setPixmap(pixmap)

    def onCameraSelect(self, text):
        self.cameraindx[self.index] = self.cameras.index(text)
        if self.cameraindx[0] == self.cameraindx[1]:
            print("Нельзя вести трансляцию с одной камеры в двух потоках")
            return
        self.camera = Camera(self.cameraindx[self.index])
        self.cameraheight = self.camera.getheight()
        if self.cameraheight is not None:
            self.cameraview[self.index].setFixedSize(640, int(self.cameraheight))
        self.start()

    def onCamera0Select(self, text):
        self.index = 0
        self.onCameraSelect(text)

    def onCamera1Select(self, text):
        self.index = 1
        self.onCameraSelect(text)

    def startStream(self):
        self.timer.stop()
        self.cameraview[self.index].clear()
        self.cameraview[self.index].setFixedSize(640, int(self.cameraheight))
        self.password = self.sendPassword()
        webserver = WebServer(self.camera, int(self.port1), self.password)
        selectedcamera = self.cameras[self.cameraindx[self.index]]
        streamadrr = webserver.getinfo()
        self.setWindowTitle(f"<<ИДЁТ ТРАНСЛЯЦИЯ>>")
        message = f'Идёт трансляция <i>{selectedcamera}</i> по адресу: <br />' \
                  f'<a href="{streamadrr}/admin:{self.password}">{streamadrr}/admin:{self.password}</a>'
        self.streamlink[self.index].setText(message)
        webserver.start()
        self.camerasCombo[self.index].setDisabled(True)
        self.streambutton[self.index].setDisabled(True)

    def startStream0(self):
        self.index = 0
        self.startStream(self)

    def startStream1(self):
        self.index = 1
        self.startStream(self)

    def sendPassword(self):
        self.passwordText = self.passwordEdit[self.index].text()
        self.port1 = self.portEdit[self.index].text()
        if self.passwordText != '' and self.port1.isdigit() and 1 < int(self.port1) < 65536:
            self.isPasswordEntered[self.index] = True
            self.streambutton[self.index].setEnabled(True)
        else:
            self.isPasswordEntered[self.index] = False
            self.streambutton[self.index].setDisabled(True)

        return self.passwordText

    def sendPassword0(self):
        self.index = 0
        self.sendPassword(self)

    def sendPassword1(self):
        self.index = 1
        self.sendPassword(self)
# TODO: add field to enter port