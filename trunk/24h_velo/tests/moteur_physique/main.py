import moteur_physique
import sys
import time

from PyQt4.QtCore import QTimer, QObject, QUrl, pyqtSignal
from PyQt4.QtGui import QApplication
from PyQt4.QtDeclarative import QDeclarativeView

# This class will emit the current date and time as a signal when
# requested.
class Pos(QObject):

    pos = pyqtSignal(str)

    def emit_position(self, x, y):
        self.pos.emit(x, y)

def position():
	gx, gy, dt = -9.81, 0, 0.01
	screen_size = 800, 640	
	p = moteur_physique.point(screen_size, dt, gx, gy)

	print 'computing positions'
	pos_x, pos_y = p.get_positions()
	return pos_x, pos_y

	

app = QApplication(sys.argv)
pos = Pos()

# Create the QML user interface.
view = QDeclarativeView()
view.setSource(QUrl('follow_mouse.qml'))
view.setResizeMode(QDeclarativeView.SizeRootObjectToView)

root = view.rootObject()
mouse = root.findChild(QObject, "plop")
time = QTimer()

p_x, p_y = position()
for x, y in zip(p_x, p_y) :
	# Provide the current date and time when requested by the user interface.
	root.positionRequired.connect(pos.emit_position)

	# Update the user interface with the current date and time.
	pos.pos.connect(root.updatePosition)

view.show()
app.exec_()

