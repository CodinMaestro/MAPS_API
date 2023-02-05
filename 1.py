import sys
import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
import requests
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.s = 0.005
        self.get.clicked.connect(self.get_c)
        self.new_2.clicked.connect(self.new_r)
        self.comboBox.currentIndexChanged.connect(self.new_view)
        self.view = 'map'
        self.X = 0.004
        self.nx = 1
        self.ny = 1
    def new_view(self):
        if self.comboBox.currentText() == 'схема':
            self.view = 'map'
        elif self.comboBox.currentText() == 'спутник':
            self.view = 'sat'
        else:
            self.view = 'sat,skl'
        self.nmap()

    def get_c(self):
        self.x2 = self.x.text()
        self.y2 = self.y.text()
        if self.y2 == '' and self.x2 == '':
            self.x2 = 37.530883
            self.y2 = 55.702999
        self.x.setReadOnly(True)
        self.y.setReadOnly(True)
        self.nmap()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            if float(self.x2) - self.s > -172.912563:
                self.x2 = float(self.x2) - self.s
                self.nmap()
        if event.key() == Qt.Key_PageUp:
            if self.s / 2 > 0.000:
                self.s /= 2
                self.nmap()
        if event.key() == Qt.Key_PageDown:
            if self.s * 2 < 79.995:
                self.s *= 2
                self.nmap()
        if event.key() == Qt.Key_W:
            if float(self.y2) + self.s < 85.053838:
                self.y2 = float(self.y2) + self.s
                self.nmap()
        if event.key() == Qt.Key_S:
            if float(self.y2) - self.s > -84.992840:
                self.y2 = float(self.y2) - self.s
                self.nmap()
        if event.key() == Qt.Key_D:
            if float(self.x2) + self.s < 172.011028:
                self.x2 = float(self.x2) + self.s
                self.nmap()

    def new_r(self):
        self.x.setReadOnly(False)
        self.y.setReadOnly(False)
        self.im_map.clear()

    def nmap(self, x1=0, y1=0):
        try:
            x = str(float(self.x2) + x1)
            y = str(float(self.y2) + y1)
            s = self.s
            map_req = f'http://static-maps.yandex.ru/1.x/?ll={x},{y}&l={self.view}&spn={s},{s}'
            resp = requests.get(map_req)
            if not resp:
                self.im_map.setText('По таким координатам невозможно открыть карту')
            else:
                map_file = 'map.png'
                with open(map_file, 'wb') as file:
                    file.write(resp.content)
                self.pixmap = QPixmap(map_file)
                self.im_map.setPixmap(self.pixmap)
                os.remove(map_file)
        except Exception:
            self.im_map.setText('По таким координатам невозможно открыть карту')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
