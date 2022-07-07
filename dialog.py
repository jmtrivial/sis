import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent
from PyQt5.QtWidgets import QDialog
from groupe import *


class Dialog(QDialog):

    def __init__(self, main):
        super().__init__(parent=None)
        self.main = main
        self.setupUi(self)
        self.show()

    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setWindowTitle("Placement libre")
        self.Dialog.resize(420, 328)

        #explications
        self.explications = QtWidgets.QLabel()
        self.explications.setText("Glisser et déposer les numéros d'enceintes dans les groupes. \nDouble cliquer sur un numéro pour le supprimer d'un groupe")


        #numéros d'enceintes
        self.listeEnceintes = QtWidgets.QListWidget()
        font = QtGui.QFont()
        font.setPointSize(36)
        self.listeEnceintes.setFont(font)
        self.listeEnceintes.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listeEnceintes.setDragEnabled(True)
        self.listeEnceintes.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.listeEnceintes.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.listeEnceintes.setFlow(QtWidgets.QListView.LeftToRight)

        enceintes = ["1", "2", "3", "4", "5", "6", "7", "8"]

        for enceinte in enceintes :
            self.listeEnceintes.addItem(enceinte)

        #groupes
        self.groupe1 = Groupe(self.Dialog, self, 1)
        self.groupe1.getListe().itemDoubleClicked.connect(self.handleDoubleClick)

        self.groupe2 = Groupe(self.Dialog, self, 2)
        self.groupe2.getListe().itemDoubleClicked.connect(self.handleDoubleClick)
        self.groupe2.setVisibility(False)
        self.groupe2.getDelete().clicked.connect(self.deleteGroup)

        self.groupe3 = Groupe(self.Dialog, self, 3)
        self.groupe3.getListe().itemDoubleClicked.connect(self.handleDoubleClick)
        self.groupe3.setVisibility(False)
        self.groupe3.getDelete().clicked.connect(self.deleteGroup)

        self.nombreGroupe = 1

        #ajouter un groupe
        self.addGroup = QtWidgets.QPushButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.addGroup.setIcon(icon)
        self.addGroup.clicked.connect(self.addingGroup)

        self.lAddGroup = QtWidgets.QLabel()
        self.lAddGroup.setText("Ajouter un groupe")

        #boutons ok et cancel
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)

        self.buttonBox.accepted.connect(self.Dialog.accept)
        self.buttonBox.rejected.connect(self.Dialog.reject)

        #layout
        self.layout = QtWidgets.QGridLayout()

        self.layout.addWidget(self.explications, 0, 0, 1, 3)
        self.layout.addWidget(self.listeEnceintes, 1, 0, 1, 3)
        self.layout.addWidget(self.groupe1.getLabel(), 2, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.groupe1.getListe(), 2, 1)
        self.layout.addWidget(self.groupe2.getLabel(), 3, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.groupe2.getListe(), 3, 1)
        self.layout.addWidget(self.groupe2.getDelete(), 3, 2, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.groupe3.getLabel(), 4, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.groupe3.getListe(), 4, 1)
        self.layout.addWidget(self.groupe3.getDelete(), 4, 2, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.addGroup, 5, 0, QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.lAddGroup, 5, 1, QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.buttonBox, 6, 1, 1, 2, QtCore.Qt.AlignRight)

        self.Dialog.setLayout(self.layout)

        QtCore.QMetaObject.connectSlotsByName(self.Dialog)     

    def handleDoubleClick(self, item):
        print(item.text())
        for groupe in [self.groupe1, self.groupe2, self.groupe3] :
            groupe.getListe().takeItem(groupe.getListe().row(item))
        self.unhide(item.text())

    def addingGroup(self):
        if self.nombreGroupe == 1 :
            self.groupe2.setVisibility(True)
            self.nombreGroupe = 2
        elif self.nombreGroupe == 2 :
            self.groupe3.setVisibility(True)
            self.groupe2.getDelete().setVisible(False)
            self.nombreGroupe = 3
            self.addGroup.setVisible(False)
            self.lAddGroup.setVisible(False)

    def deleteGroup(self):
        if self.nombreGroupe == 3 :
            self.suppr = self.groupe3
            self.groupe2.getDelete().setVisible(True)
            self.addGroup.setVisible(True)
            self.lAddGroup.setVisible(True)
        elif self.nombreGroupe == 2 :
            self.suppr = self.groupe2
        self.nombreGroupe -= 1

        self.suppr.setVisibility(False)

        all_items = self.suppr.getListe().findItems('', QtCore.Qt.MatchRegularExpression)
        for item in all_items:
            if item.text() != "+" :
                self.unhide(item.text())
                self.suppr.getListe().takeItem(self.suppr.getListe().row(item))

    def hide(self, position) :
        items = self.listeEnceintes.findItems(str(position),Qt.MatchExactly)
        for item in items:
            item.setFlags(Qt.NoItemFlags)

    def unhide(self, position) :
        items = self.listeEnceintes.findItems(str(position),Qt.MatchExactly)
        for item in items:
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsDragEnabled)

    def accept(self):
        print("envoi : selection numero 3")
        for groupe in [self.groupe1, self.groupe2, self.groupe3]:
            print(groupe.getListe().getListe())
        self.main.envoyer(3)
        self.done(1)

    def reject(self):
        self.done(0)



