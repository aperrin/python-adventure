import sys
import random
import serial
import threading
import time

from PyQt4 import QtCore
from PyQt4.QtCore import QObject, QUrl, pyqtSignal
from PyQt4.QtGui import QApplication
from PyQt4.QtDeclarative import QDeclarativeView,  QDeclarativeProperty, QDeclarativeItem

"""http://pyqt.sourceforge.net/Docs/PyQt4/qml.html
"""

class serial_data(threading.Thread):
    def __init__(self, port, baud, timeout, len_moyenne):
        threading.Thread.__init__(self)  
        self.ser = serial.Serial(port, baud, timeout = timeout)
    
        self.res_moyenne = 1000
        self.len_moyenne = len_moyenne
        self.l_values = []     
        self.time_max = 60
        self.threshold = 4e-2 # anti-rebond
        self.alive = threading.Event()
        self.alive.set()
        self.max = 5 # empirique
        
    def init_l_values(self):
        old_time = time.clock()
        while len(self.l_values) < self.len_moyenne:
            data = self.ser.readline()
            if data :
                _time = time.clock()
                self.l_values.append(_time - old_time)        

    def calc_moy(self):
        self.init_l_values()
        time_now = time.clock()
        old_time = time.clock()
        while (time.clock() - time_now) < self.time_max:
            data = self.ser.readline()
            if data :
                _time = time.clock()
                if (_time - old_time) > self.threshold :
                    self.l_values = self.l_values[1:]
                    self.l_values.append(_time - old_time)
                    self.res_moyenne = sum(self.l_values)/len(self.l_values)
                old_time = _time
            else :
                self.res_moyenne = 1000
        
    def get_data(self):
        return self.res_moyenne

    def run(self):
        self.calc_moy()

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

class allume_ampoule:
    def __init__(self, rootObject, ser):
         self.rootObject = rootObject
         self.nb_ampoule = 24
         self.l_ampoule = range(1, self.nb_ampoule+1)
         random.shuffle(self.l_ampoule)
         self.ser = ser

    def get_nb_allume(self) :
        dt = self.ser.get_data()
        dt = 1.0/dt # vitesse : plus c'est grand, plus ca va vite
        print 'dt', dt      
        nb = int(dt*24.0/9)
        if nb > 24 :
            nb = 24
        return nb
                
        
    def allume(self) :
        nb_allume = self.get_nb_allume()
        print nb_allume
        for i in range(nb_allume):
            n_ampoule = self.l_ampoule[i]
            _property = QDeclarativeProperty(
                        self.rootObject, "st_amp"+str(n_ampoule))
            _property.write("./images/ampoule_allumee.png")
        
        for i in range(nb_allume, self.nb_ampoule):
            n_ampoule = self.l_ampoule[i]
            _property = QDeclarativeProperty(
                        self.rootObject, "st_amp"+str(n_ampoule))
            _property.write("./images/ampoule_eteinte.png")            

import serial
app = QApplication(sys.argv)

# Create the QML user interface.
view = QDeclarativeView()
view.setSource(QUrl('24.qml'))
view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
rootObject = view.rootObject()
ser = serial_data('COM1', 9600, 1, len_moyenne = 5)
ser.start()
allu = allume_ampoule(rootObject, ser)
_timer = QtCore.QTimer()

_timer.timeout.connect(allu.allume)
_timer.start(100)


view.showFullScreen()

app.exec_()
