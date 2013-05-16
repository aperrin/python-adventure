# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:34:10 2013

@author: Mat
"""
import sys
import os
os.system("pyuic4 fenetre.ui > intGra.py")

from PyQt4.QtGui import QApplication, QDialog
from PyQt4 import uic
from PyQt4.QtCore import *

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
        self.duree = 10.0  # la duree en sec
        self.lcdNumber.display(str(self.duree))
        self.intervale = 50/1000.0
        self.time = QTime()
        self._timer = QtCore.QTimer(self)

        self.cameraDevice = CameraDevice(mirrored=True, timer = self._timer)
        self.cameraWidget = CameraWidget(self.cameraDevice)
        self.cameraRecord = CameraDevice(mirrored=True, record=False, 
                                         timer = self._timer)

        self._timer.timeout.connect(self.cameraDevice._queryFrame)
        self._timer.timeout.connect(self.cameraRecord._queryFrame)
        
        self.lineEdit.cursorPositionChanged.connect(self.clearScore)
        self.lineEdit_2.cursorPositionChanged.connect(self.clearScore)
        self.pushButton_score.clicked.connect(self.addScoreToDict)

        self.score = score()
        
        self.horizontalLayout.insertWidget(1, self.cameraWidget)
        self.cameraWidget.show()
        self.load_teams()
        self.tour = -1
        
    def addScoreToDict(self):
        l_team = (self.comboBox.currentText(), self.comboBox_2.currentText())
        l_score = (self.lineEdit.text(), self.lineEdit_2.text())
        self.score.add_match(self.spinBox.value(), l_team, l_score)
        print self.score.results
        self.addScoreToWidget()
        
    def addScoreToWidget(self):
        #self.treeWidget.addTopLevelItem("plop")
        tour = self.spinBox.value()
        if tour!=self.tour:
            newTour = QtGui.QTreeWidgetItem(self.treeWidget)
            newTour.setText(0, "Tour "+str(tour))
            tour = self.spinBox.value()
            self.tour = tour 
        
        scores = QtGui.QTreeWidgetItem()
        scores.setText(0,"{} - {}".format(self.lineEdit.text(), 
                       self.lineEdit_2.text()))
        
        teams = QtGui.QTreeWidgetItem()
        teams.setText(0,"{} - {}".format(self.comboBox.currentText(), 
                      self.comboBox_2.currentText()))
        
        self.treeWidget.topLevelItem(tour-1).addChild(teams)
        self.treeWidget.topLevelItem(tour-1).child(self.score.nb_match-1)\
                                            .addChild(scores)
        
#        teams.addChild(scores)
#        
#        self.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("Dialog", ",lm", None, QtGui.QApplication.UnicodeUTF8))
#        self.treeWidget.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("Dialog", "l,m", None, QtGui.QApplication.UnicodeUTF8))
#        self.treeWidget.topLevelItem(0).child(0).child(0).setText(0, QtGui.QApplication.translate("Dialog", ",ml", None, QtGui.QApplication.UnicodeUTF8))
#        self.treeWidget.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("Dialog", "nkln!", None, QtGui.QApplication.UnicodeUTF8))
#        self.treeWidget.topLevelItem(0).child(1).child(0).setText(0, QtGui.QApplication.translate("Dialog", "kln,l!", None, QtGui.QApplication.UnicodeUTF8))
# 
#        
#        self.treeWidget.setHeaderLabel("plop")
#        self.treeWidget.insertTopLevelItem(2, tours)  
        
        
        
    def checkScore(self,newString):
        if not str(newString).isdigit():
            print newString
        
    def clearScore(self):
        if "Score" in str(self.sender().text()):
           self.sender().clear()
           self.sender().setInputMask('9999')
        

    def load_teams(self):
        f_name = "./team_names.txt"
        with open(f_name, "r") as f:
            lines = f.readlines()
        lines = map(lambda x: x.strip(), lines)
        self.comboBox.clear()
        self.comboBox.addItems(lines)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(lines)


    @pyqtSlot()
    def reset(self):
        if self.timer.isActive():
            self.timer.stop()

        self.lcdNumber.display(str(self.duree))
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.pushButton.setEnabled(True)
        # afficher le fond en blanc

        # on arrete l'enregistrement
        self.stopRecord()

    def stopRecord(self) :
        self.cameraRecord.setRecord(False)

    def create_record_name(self) :
        name = "{0}_vs_{1}_match_1".format(self.comboBox.currentText(), 
                                                self.comboBox_2.currentText())
        #print 'name_video : {0}'.format(name_video)     
        l_avi = [i for i in os.listdir('.') if '.avi' in i]
        l_avi = map(lambda x: x.split('.avi')[0], l_avi)
        print l_avi
        while name in l_avi :
            num = int(name[-1]) + 1
            name = name[:-1] + str(num)
        return name + '.avi'

    @pyqtSlot()
    def start_chrono(self):
        self.timer.timeout.connect(self.decompte)
        self.timer.start(self.intervale*1000.0)
        self.time.start()
        self.pushButton.setEnabled(False)
        name_video = self.create_record_name()
        print 'name_video : {0}'.format(name_video)        
        self.cameraRecord.name = name_video
        self.cameraRecord.setRecord(True)

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
            self.stopRecord()
            # on ajoute les deux équipes à la feuille de match            
            self.addMatch()
            

            # afficher le fond en rouge
            
    def addMatch(self) :
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("Score Equipe A")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("Score Equipe B")
        pass        

class score :
    
    def __init__(self):
        self.results = {}    
        self.nb_match = 0
        self.tour = 0
    
    def get_score(self, tour):
        pass
    
    def add_match(self, tour, l_team, l_score):
        if tour == self.tour:
            self.nb_match += 1
        else :
            self.nb_match = 1
            self.tour = tour
        teamA, teamB = l_team
        scoreA, scoreB = l_score
        self.results.setdefault(tour, {})
        self.results[tour].setdefault(self.nb_match, {})
        
        print 'ajout', self.nb_match
        print self.results
        
        self.results[tour][self.nb_match].setdefault(teamA, scoreA)
        self.results[tour][self.nb_match].setdefault(teamB, scoreB)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    f = MaFenetre()
    f.show()
    r = a.exec_()
