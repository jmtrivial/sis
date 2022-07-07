from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from groupeListe import *

class Groupe():

    def __init__(self, dialog, root, identifiant):
        self.id = identifiant
        self.dialog = dialog
        self.root = root

        self.groupe = QtWidgets.QLabel()
        self.groupe.setText("Groupe "+str(self.id))
        self.groupeListe = GroupeListe(self.dialog, self.root, self.id)

        if self.id > 1 : 
            self.boutonSuppr = QtWidgets.QPushButton()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("images/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.boutonSuppr.setIcon(icon)
            self.boutonSuppr.setObjectName("groupeDelete"+str(self.id))

    def getLabel(self):
        return self.groupe

    def getListe(self):
        return self.groupeListe

    def getDelete(self):
        return self.boutonSuppr

    def setVisibility(self, state):
        if state == True :
            self.groupe.setVisible(True)
            self.groupeListe.setVisible(True)
            self.boutonSuppr.setVisible(True)
        else :
            self.groupe.setVisible(False)
            self.groupeListe.setVisible(False)
            self.boutonSuppr.setVisible(False)