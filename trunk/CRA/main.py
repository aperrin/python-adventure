# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 22:34:10 2013

@author: Mat
"""
import sys
import os
#os.system("pyuic4 fenetre.ui > intGra.py")

import json

from PyQt4.QtGui import QApplication, QDialog, QMessageBox
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
        self.pushButton_3.clicked.connect(self.load_scores)
        self.pushButton_4.clicked.connect(self.deleteMatch)        
        
        self.score = score()
        
        self.horizontalLayout.insertWidget(1, self.cameraWidget)
        self.cameraWidget.show()
        self.load_teams()
        self.tour = -1
        
    def deleteMatch(self):
        ''' pour supprimer un match s'il a ete ajoute par erreur :
            supprime la ligne selectionnee s'il s'agit d'un match ;
            ne fait rien sinon (si on a selectionne la ligne "tour x")
            
            Supprime egalement l'entree correspondante du dictionnaire et
            reenregistre dans le fichier json
        '''
        curItem = self.treeWidget.currentItem()
        parent = curItem.parent()
        if parent :
            parent.removeChild(curItem)
            curMatch = str(curItem.text(0)).split()[0]
            curTour = str(parent.text(0)).split()[-1]
            del self.score.results[curTour][curMatch]
            self.score.save_matchs()
        
        #index = 0
        #self.treeWidget.takeTopLevelItem(index)     
        
    def addScoreToDict(self):
        ''' lorsqu'on clic sur valider score, ajoute le match en cours au
        tableau des scores (2eme onglet) et au dictionnaire qui est enregistre 
        en json, sauf si les deux equipes sont les
        memes, auquel cas il affiche une box pour prevenir de les changer
        '''
        if self.comboBox.currentText() == self.comboBox_2.currentText():
            QMessageBox.information(None, "Attention", 
                    "Une equipe ne peut pas jouer un match contre elle-meme ! \
                    \n Veuillez changer au moins une equipe pour pouvoir enregistrer le match.")
        elif self.lineEdit.text() == "" or self.lineEdit_2.text() == "" :
            QMessageBox.information(None, "Attention", 
                    "Veuillez entrer le score de chacune des equipes.")
        else:
            l_team = (self.comboBox.currentText(), self.comboBox_2.currentText())
            l_score = (self.lineEdit.text(), self.lineEdit_2.text())
            self.score.add_match(self.spinBox.value(), l_team, l_score)
            self.addScoreToWidget()
            # on reinitialise les champs de texte ou entrer les scores            
            self.addMatch()
            
        
    def addScoreToWidget(self):
        '''ajouter graphiquement le score du match en cours 
        au tableau des scores
        '''
        tour = self.spinBox.value()
        if tour!=self.tour:
            if not self.treeWidget.topLevelItem(tour-1):
                newTour = QtGui.QTreeWidgetItem(self.treeWidget)
                newTour.setText(0, "Tour "+str(tour))
            self.tour = tour 
        
        teams = QtGui.QTreeWidgetItem()
        teams.setText(0,"{} : {} - {}".format(self.score.nb_match,
                      self.comboBox.currentText(), 
                      self.comboBox_2.currentText()))
        teams.setText(1,"{} - {}".format(self.lineEdit.text(), 
                       self.lineEdit_2.text()))
                       
        self.treeWidget.topLevelItem(tour-1).addChild(teams)
        
    def _decode_dict(self, data):
        '''Lorsqu'on load un fichier json, les chaines de caractère sont en 
        unicode. Cette méthode permet de passer toutes les chaines des 
        dictionnaires en ascii, pour que ce soit 
        utilisable par la suite
        '''
        res = {}
        for key, value in data.iteritems():
            if isinstance(key, unicode):
               key = key.encode('utf-8')
            if isinstance(value, unicode):
               value = value.encode('utf-8')
            elif isinstance(value, list):
               value = self._decode_list(value)
            elif isinstance(value, dict):
               value = self._decode_dict(value)
            res[key] = value
        return res


    
    def load_scores(self):
        '''si le programme a été fermé et qu'on le rouvre pendant la coupe,
        charger les scores des matchs qui ont déjà eu lieu avant dans le 
        tableau des scores
        '''
        f_name = "./resultats.json"
        with open(f_name, "r") as f:
            obj = json.load(f)
            obj = self._decode_dict(obj)
            self.score.results = obj
#        print self.score.results.keys()
#        print self.score.results
        map(self.createTreeWidIt, self.score.results.keys())
        #print "nb match charges"+ str(self.score.nb_match)
        
    def createTreeWidIt(self, tour):
        '''Quand on load un fichier de scores, on commence par effacer tout
        ce qu'il y a actuellement, puis on cree les item pour chaque match
        '''
        self.treeWidget.clear()
        newTour = QtGui.QTreeWidgetItem(self.treeWidget)
        newTour.setText(0, "Tour "+str(tour))
        matchs = sorted(self.score.results[tour].keys())
        #print matchs
        for m in matchs:
            teamA, teamB = self.score.results[tour][m].keys()
            scoreA = self.score.results[tour][m][teamA]
            scoreB = self.score.results[tour][m][teamB]
            
            teams = QtGui.QTreeWidgetItem()
            teams.setText(0,"{} : {} - {}".format(m, teamA, teamB))
            teams.setText(1,"{} - {}".format(scoreA, scoreB))
            self.treeWidget.topLevelItem(int(tour)-1).addChild(teams)
            if int(m)>self.score.nb_match:
                self.score.nb_match = int(m)
                
    def clearScore(self):
        ''' Efface l'inscription 'score equipe A' pour pouvoir entrer le score
        '''
        if "Score" in str(self.sender().text()):
           self.sender().clear()
           self.sender().setValidator(QtGui.QIntValidator())

    def load_teams(self):
        ''' Charger les noms des equipes participantes (contenues dans
        team_names.txt)
        '''
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
        
        # on reinitialise les champs de texte ou entrer les scores            
        self.addMatch()
            
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

            # afficher le fond en rouge
            
    def addMatch(self) :
        self.lineEdit.setValidator(QtGui.QRegExpValidator())
        self.lineEdit.setText("Score Equipe A")
        self.lineEdit_2.setValidator(QtGui.QRegExpValidator())
        self.lineEdit_2.setText("Score Equipe B")

class score :
    
    def __init__(self):
        self.results = {}    
        self.nb_match = 0
        self.tour = 0
    
    def save_matchs(self):
        f_name = "./resultats.json"
        with open(f_name, "w") as f:
            json.dump(self.results,f, sort_keys=True, 
                      indent=4)
    
    def add_match(self, tour, l_team, l_score):
#        if tour == self.tour:
        self.nb_match += 1
#        else :
#            self.nb_match = 1
#            self.tour = tour
        teamA, teamB = l_team
        scoreA, scoreB = l_score
        self.results.setdefault(str(tour), {})
        self.results[str(tour)].setdefault(str(self.nb_match), {})
        
        print 'ajout', self.nb_match
        
        self.results[str(tour)][str(self.nb_match)].setdefault(str(teamA), str(scoreA))
        self.results[str(tour)][str(self.nb_match)].setdefault(str(teamB), str(scoreB))
        
#        print "score enregistre : " 
#        print(self.results)
#        print("____________________________")
#        
        self.save_matchs()
                      



if __name__ == "__main__":
    a = QApplication(sys.argv)
    f = MaFenetre()
    f.show()
    r = a.exec_()
