# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:34:10 2013

@author: Mat
"""
from PyQt4.QtGui import QApplication, QDialog
from PyQt4 import uic
from PyQt4.QtCore import *
import sys
from webcam_support import *

UiMaFenetre, Klass = uic.loadUiType('fenetre.ui')


class MaFenetre(QDialog, UiMaFenetre):
    def __init__(self, conteneur=None):
        if conteneur is None:
            conteneur = self
        QDialog.__init__(conteneur)
        self.timer = QTimer(self)
        self.setupUi(conteneur)
        self.pushButton.clicked.connect(self.start_chrono)
        self.pushButton_2.clicked.connect(self.reset)
        self.duree = 11.0  # la duree en sec
        self.lcdNumber.display(str(self.duree))
        self.intervale = 50/1000.0
        self.time = QTime()

        self.cameraDevice = CameraDevice(mirrored=True)
        self.cameraWidget = CameraWidget(self.cameraDevice)

        self.horizontalLayout.insertWidget(1, self.cameraWidget)
        self.cameraWidget.show()

    @pyqtSlot()
    def reset(self):
        if self.timer.isActive():
            self.timer.stop()

        self.lcdNumber.display(str(self.duree))
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.pushButton.setEnabled(True)
        # afficher le fond en blanc

        # on arrete l'enregistrement


    @pyqtSlot()
    def start_chrono(self):
        self.timer.timeout.connect(self.decompte)
        self.timer.start(self.intervale*1000.0)
        self.time.start()
        self.pushButton.setEnabled(False)
        self.cameraRecord = CameraDevice(record=True)
        

    def decompte(self):
        val = -(self.time.elapsed() - self.duree*1000)
        if(val >= 0):
            if val < 10*1000:
                self.lcdNumber.display('0'+str(val/1000.0)[:-1])
                # faire clignoter le fond en rouge
            else:
                self.lcdNumber.display(str(val/1000.0))
        else:
            self.lcdNumber.display('00.0')
            self.timer.stop()
            print("stopp")
            # on arrete l'enregistrement

            # afficher le fond en rouge


if __name__ == "__main__":
    a = QApplication(sys.argv)
    f = MaFenetre()
    f.show()
    r = a.exec_()
