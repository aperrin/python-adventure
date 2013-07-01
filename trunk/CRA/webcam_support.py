# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ce script temporaire est sauvegardé ici:
C:\Users\Mat\.spyder2\.temp.py
"""

from cv2 import cv
import cv2
import Image

from PyQt4 import QtCore
from PyQt4 import QtGui

import time


class OpenCVQImage(QtGui.QImage):
    def __init__(self, opencvBgrImg):
        depth, nChannels = opencvBgrImg.depth, opencvBgrImg.nChannels
        if depth != cv.IPL_DEPTH_8U or nChannels != 3:
            raise ValueError("the input image must be 8-bit, 3-channel")
        w, h = cv.GetSize(opencvBgrImg)
        opencvRgbImg = cv.CreateImage((w, h), depth, nChannels)
        # it's assumed the image is in BGR format
        cv.CvtColor(opencvBgrImg, opencvRgbImg, cv.CV_BGR2RGB)
        self._imgData = opencvRgbImg.tostring()
        super(OpenCVQImage, self).__init__(self._imgData, w, h,
                                           QtGui.QImage.Format_RGB888)


class CameraDevice(QtCore.QObject):

    _DEFAULT_FPS = 20.0


    newFrame = QtCore.pyqtSignal(cv.iplimage)

    def __init__(self, cameraId=0, mirrored=False, parent=None, 
                 record=False, timer = None, name = 'out.avi'):
        super(CameraDevice, self).__init__(parent)

        self.mirrored = mirrored

        self._cameraDevice = cv.CaptureFromCAM(cameraId)
        cv.SetCaptureProperty(self._cameraDevice, cv.CV_CAP_PROP_FPS, self._DEFAULT_FPS)
        
        
        self._timer = timer
        print self._timer

        """
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(1000/self._DEFAULT_FPS)#self.fps)
        """
        self.paused = False
        self.record = record
        self.name = name
            
    def setRecord(self, record) :
        self.record = record
        self.time = time.clock()
        if record :
            self.create_writer(fps=self._DEFAULT_FPS, fname=self.name)


    @QtCore.pyqtSlot()
    def _queryFrame(self):
        frame = cv.QueryFrame(self._cameraDevice)
        if self.mirrored:
            mirroredFrame = cv.CreateImage(cv.GetSize(frame), frame.depth,
                                           frame.nChannels)
            cv.Flip(frame, mirroredFrame, 1)
            frame = mirroredFrame
        if self.record :
            print 1.0/(time.clock() - self.time)
            self.time = time.clock()
            cv.WriteFrame(self.writer, frame)
        self.newFrame.emit(frame)
       
    @property   
    def paused(self):
        print 'paused'        
        return not self._timer.isActive()

    @paused.setter
    def paused(self, p):
        if p:
            self._timer.stop()
        else:
            if not self._timer.isActive():
                self._timer.start()

    @property
    def frameSize(self):
        w = cv.GetCaptureProperty(self._cameraDevice,
                                  cv.CV_CAP_PROP_FRAME_WIDTH)
        h = cv.GetCaptureProperty(self._cameraDevice,
                                  cv.CV_CAP_PROP_FRAME_HEIGHT)
        return int(w), int(h)

    @property
    def fps(self):
        fps = int(cv.GetCaptureProperty(self._cameraDevice, cv.CV_CAP_PROP_FPS))
        if not fps > 0:
            fps = self._DEFAULT_FPS

        return fps

    def create_writer(self, fps, fname) :
        w, h = self.frameSize
        print fps
        fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
        self.writer = cv.CreateVideoWriter(fname, fourcc, self._DEFAULT_FPS/2, (w, h), 1)        

#    def record(self):
#        self.createWriter(fps=24, fname='out.avi')
#        self.capture = True
#        print self.capture
#        cap = cv.QueryFrame(self._cameraDevice)
        
        
class CameraWidget(QtGui.QWidget):

    newFrame = QtCore.pyqtSignal(cv.iplimage)

    def __init__(self, cameraDevice, parent=None):
        super(CameraWidget, self).__init__(parent)

        self._frame = None

        self._cameraDevice = cameraDevice
        self._cameraDevice.newFrame.connect(self._onNewFrame)

        w, h = self._cameraDevice.frameSize
        self.setMinimumSize(w, h)
        self.setMaximumSize(w, h)

    @QtCore.pyqtSlot(cv.iplimage)
    def _onNewFrame(self, frame):
        self._frame = cv.CloneImage(frame)
        self.newFrame.emit(self._frame)
        self.update()

    def changeEvent(self, e):
        if e.type() == QtCore.QEvent.EnabledChange:
            if self.isEnabled():
                self._cameraDevice.newFrame.connect(self._onNewFrame)
            else:
                self._cameraDevice.newFrame.disconnect(self._onNewFrame)

    def paintEvent(self, e):
        if self._frame is None:
            return
        painter = QtGui.QPainter(self)
        painter.drawImage(QtCore.QPoint(0, 0), OpenCVQImage(self._frame))


def _main():
    @QtCore.pyqtSlot(cv.iplimage)
    def onNewFrame(frame):
        cv.CvtColor(frame, frame, cv.CV_RGB2BGR)
        msg = "processed frame"
        font = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 1.0, 1.0)
        tsize, baseline = cv.GetTextSize(msg, font)
        w, h = cv.GetSize(frame)
        tpt = (w - tsize[0]) / 2, (h - tsize[1]) / 2
        cv.PutText(frame, msg, tpt, font, cv.RGB(255, 0, 0))

    import sys

    app = QtGui.QApplication(sys.argv)

    cameraDevice = CameraDevice(mirrored=True)

#    cameraWidget1 = CameraWidget(cameraDevice)
#    cameraWidget1.newFrame.connect(onNewFrame)
#    cameraWidget1.show()

    cameraWidget2 = CameraWidget(cameraDevice)
    cameraWidget2.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    _main()
