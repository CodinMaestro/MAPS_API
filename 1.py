import sys
import PyQt5
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.s = 0.005
        self.get.clicked.connect(self.nmap)
        self.X = 0.004
        self.nx = 1
        self.ny = 1

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            if self.s - self.X > 0.000:
                self.s -= self.X
                self.nmap()
        if event.key() == Qt.Key_PageDown:
            if self.s + self.X < 79.995:
                self.s += self.X
                self.nmap()

    def nmap(self):
        x = self.x.text()
        y = self.y.text()
        x = str(x)
        y = str(y)
        s = self.s
        if y == '' or x == '':
            x = '37.530883'
            y = '55.702999'
        map_req = f'http://static-maps.yandex.ru/1.x/?ll={x},{y}&l=map&spn={s},{s}'
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
