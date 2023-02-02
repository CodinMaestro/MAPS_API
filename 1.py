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
        self.nmap()
        self.size = 0.005

    def nmap(self):
        map_req = 'http://static-maps.yandex.ru/1.x/?ll=37.530883,55.702999&l=sat&spn=0.005,0.005'
        resp = requests.get(map_req)

        if not resp:
            print(f"Ай-ай-ай {resp.status_code}")
            sys.exit()

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
