from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import *

class GroupeListe(QListWidget):

    def __init__(self, parent, root, identifiant):
        super(GroupeListe, self).__init__( parent)
    
        self.id = identifiant
        self.root = root
        self.liste = []
        
        self.setDragDropMode(QtWidgets.QAbstractItemView.DropOnly)
        self.setFlow(QtWidgets.QListView.LeftToRight)
        item = QtWidgets.QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)
        item.setText("+")
        self.addItem(item)
            
    def dropEvent(self, e):
        if e.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
            data = e.mimeData()
            source_item = QtGui.QStandardItemModel()
            source_item.dropMimeData(data, QtCore.Qt.CopyAction, 0,0, QtCore.QModelIndex())
            print(source_item.item(0, 0).text()) 

        #suppression du +
        items = self.findItems("+", QtCore.Qt.MatchExactly)
        for item in items :
            self.takeItem(self.row(item))

        #ajout du nouvel item
        self.addItem(source_item.item(0, 0).text())

        self.liste.append(source_item.item(0, 0).text())

        #ajout du +
        item = QtWidgets.QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)
        item.setText("+")
        self.addItem(item)

        #mise en gris du numéro de l'enceinte
        self.root.hide(source_item.item(0, 0).text())

    def getListe(self):
        listeEnceintes = ""
        for enceinte in self.liste :
            listeEnceintes = listeEnceintes + enceinte
        return listeEnceintes
