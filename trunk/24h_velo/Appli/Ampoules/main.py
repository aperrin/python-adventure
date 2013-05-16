import sys
import random

from PyQt4 import QtCore
from PyQt4.QtCore import QObject, QUrl, pyqtSignal
from PyQt4.QtGui import QApplication
from PyQt4.QtDeclarative import QDeclarativeView,  QDeclarativeProperty, QDeclarativeItem

"""http://pyqt.sourceforge.net/Docs/PyQt4/qml.html
"""


class allume:
    def __init__(self, rootObject) :
        self.rootObject = rootObject
        self.a = 10
        self.l_children = self.rootObject.children()
        
    def allume(self) :
        self.a += random.randint(-1, 1)
        self.a = self.a % 100
        nb_allume = self.a//4
        
        for i in range(4) :
            i += 1
            _property = QDeclarativeProperty(
                        self.rootObject, "st_amp"+str(i))
            print self.a, nb_allume, "st_amp"+str(i)
            if i <= nb_allume :
                _property.write("./images/ampoule_allumee.png")
            else : 
                _property.write("./images/ampoule_eteinte.png")
                
    def allume2(self) :
        #print self.rootObject.st_amp1
        #self.rootObject.st_amp1 = "./images/ampoule_eteinte.png"
     
        _property = QDeclarativeProperty(
                        self.rootObject, "st_amp1")
        _property.write("./images/ampoule_eteinte.png")


app = QApplication(sys.argv)

# Create the QML user interface.
view = QDeclarativeView()
view.setSource(QUrl('ampoule.qml'))
view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
rootObject = view.rootObject()
allu = allume(rootObject)

_timer = QtCore.QTimer()
_timer.timeout.connect(allu.allume)
_timer.start(100)


view.showFullScreen()

app.exec_()
