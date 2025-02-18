import os, threading, atexit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QMessageBox, QMenuBar, QAction
from PyQt5.QtGui import QIcon
from dialog import *
from exercice import *
from soundManager import *
from server import *
import sys
from pydub import AudioSegment
from config import activities


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.initialized = False
        self.setupUi()
        self.initialize()

    def initialize(self):
        #démarrage pyo
        self.soundManager = SoundManager(self)

        if not self.soundManager.working:
            QMessageBox.critical(None, "Error", "Veuillez allumer la carte son puis l'ampli, et relancer l'application.")
            return 
        self.initialized = True

        # démarrage du serveur
        self.thread = Server(self.widget, self.soundManager, self)

        # initialisation de la bibliothèque
        self.updateBiblio()


    def setupUi(self):

        self.selection = 0
        self.selectionne = 0

        self.sounds1 = []
        self.sounds2 = []

        self.setGeometry(40, 40, 800, 600)
        self.setWindowTitle("Salle d'immersion sonore")
        self.setStyleSheet("background-color: rgb(255, 255, 255);color: rgb(0, 0, 0)")

        #PARTIE GAUCHE
        #titres
        self.titreSonsAmbiants = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titreSonsAmbiants.setFont(font)
        self.titreSonsAmbiants.setStyleSheet("background-color: rgb(125, 190, 255); padding:5px;")
        self.titreSonsAmbiants.setFrameShape(QtWidgets.QFrame.Box)
        self.titreSonsAmbiants.setAlignment(QtCore.Qt.AlignCenter)
        self.titreSonsAmbiants.setText("Sons ambiants")

        self.titreSonsPonctuels = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.titreSonsPonctuels.setFont(font)
        self.titreSonsPonctuels.setStyleSheet("background-color: rgb(255, 205, 99); padding:5px;")
        self.titreSonsPonctuels.setFrameShape(QtWidgets.QFrame.Box)
        self.titreSonsPonctuels.setAlignment(QtCore.Qt.AlignCenter)
        self.titreSonsPonctuels.setText("Sons ponctuels")

        #listes
        self.listeSonsAmbiants = QtWidgets.QListWidget()
        self.listeSonsAmbiants.setStyleSheet("background-color: rgb(199, 227, 255);")
        self.listeSonsAmbiants.setFrameShape(QtWidgets.QFrame.Box)
        self.listeSonsAmbiants.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listeSonsAmbiants.itemDoubleClicked.connect(self.handleDoubleClick)

        self.listeSonsPonctuels = QtWidgets.QListWidget()
        self.listeSonsPonctuels.setStyleSheet("background-color: rgb(255, 237, 199);")
        self.listeSonsPonctuels.setFrameShape(QtWidgets.QFrame.Box)
        self.listeSonsPonctuels.setFrameShadow(QtWidgets.QFrame.Plain)
        self.listeSonsPonctuels.itemDoubleClicked.connect(self.handleDoubleClick)

        #boutons d'ajout
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)

        self.addAmbiant = QtWidgets.QPushButton()
        self.addAmbiant.setStyleSheet("background-color: rgb(199, 227, 255); margin: 0 5px; padding: 5px 0;")
        self.addAmbiant.setIcon(icon)
        self.addAmbiant.clicked.connect(self.addFile)

        self.addPonctuel = QtWidgets.QPushButton()
        self.addPonctuel.setStyleSheet("background-color: rgb(255, 237, 199); margin: 0 5px; padding: 5px 0;")
        self.addPonctuel.setIcon(icon)
        self.addPonctuel.clicked.connect(self.addFile)

        #layout
        self.layoutGauche = QVBoxLayout()

        self.layoutGauche.addWidget(self.titreSonsAmbiants)
        self.layoutGauche.addWidget(self.listeSonsAmbiants)
        self.layoutGauche.addWidget(self.addAmbiant)
        self.layoutGauche.addWidget(self.titreSonsPonctuels)
        self.layoutGauche.addWidget(self.listeSonsPonctuels)
        self.layoutGauche.addWidget(self.addPonctuel)

        #PARTIE DROITE
        #exercices
        self.fidev = Exercice(0, "Type cercle")
        self.fidev.getWidget().clicked.connect(self.clicked)

        self.marcheParallele = Exercice(1, "Marche parallèle")
        self.marcheParallele.getWidget().clicked.connect(self.clicked)

        self.carrefour = Exercice(2, "Carrefour")
        self.carrefour.getWidget().clicked.connect(self.clicked)

        self.test = QtWidgets.QPushButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/type3.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.test.setIcon(icon)
        self.test.setIconSize(QtCore.QSize(200, 200))
        self.test.setFlat(True)
        self.test.clicked.connect(self.clicked)
        self.test.setStyleSheet("border: 5px solid white;")

        for button in [self.fidev, self.marcheParallele, self.carrefour] :
            button.getWidget().setStyleSheet("border: 5px solid white;")

        #verifications de connexion
        self.connexion = QtWidgets.QLabel()
        self.connexion.setAlignment(QtCore.Qt.AlignCenter)
        self.connexion.setText("En attente de connexion")

        #valider
        self.btnValider = QtWidgets.QPushButton()
        self.btnValider.setStyleSheet("background-color: rgb(224, 224, 224);")
        self.btnValider.setText("Valider >")
        self.btnValider.clicked.connect(self.valider)

        #layout
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout.addWidget(self.fidev.getWidget(), 0, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.fidev.getLabel(), 1, 0)
        self.gridLayout.addWidget(self.marcheParallele.getWidget(), 0, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.marcheParallele.getLabel(), 1, 1)
        self.gridLayout.addWidget(self.carrefour.getWidget(), 2, 0, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.carrefour.getLabel(), 3, 0)
        self.gridLayout.addWidget(self.test, 2, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout.addWidget(self.connexion, 3, 1)
        self.gridLayout.addWidget(self.btnValider, 4, 0, 1, 2)

        #PARTIE GAUCHE + DROITE
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.layoutGauche)
        self.layout.addLayout(self.gridLayout)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        #MENU
        self.menuBar = self.menuBar()
        self.menuHelp = self.menuBar.addMenu("Aide")
        self.action = QAction(QIcon('help.png'), "Aide", self)
        self.menuHelp.addAction(self.action)
        self.action.triggered.connect(self.help)

        self.menuBiblio = self.menuBar.addMenu("Bibliothèque")
        self.action3 = QAction(QIcon('test.png'), "Mise à jour", self)
        self.menuBiblio.addAction(self.action3)
        self.action3.triggered.connect(self.updateBiblio)

        QtCore.QMetaObject.connectSlotsByName(self)



    def clicked(self):
        for button in [self.fidev.getWidget(), self.marcheParallele.getWidget(), self.carrefour.getWidget(), self.test] :
            button.setStyleSheet("border: 5px solid white;")
        btn = self.sender()
        btn.setStyleSheet("border: 5px solid red;")
        self.soundManager.clear()
        self.selection = btn

    def handleDoubleClick(self, item):
        deleteFrom = self.sender()
        deleteFrom.takeItem(deleteFrom.row(item))

    def addFile(self):
        filenames, filter = QtWidgets.QFileDialog.getOpenFileNames(parent=self, caption='Sélectionner les sons', directory=config["library_dir"], filter='*.wav')
        for filename in filenames :
            if filename: 
                file = os.path.splitext(os.path.basename(filename))[0]
                self.sounds1.append(os.path.splitext(os.path.basename(filename))[0]) 
                self.sounds2.append([os.path.splitext(filename)[0].replace(os.path.splitext(os.path.basename(filename))[0], ''), os.path.splitext(os.path.basename(filename))[1]]) 
                if self.sender() == self.addAmbiant:
                    addTo = self.listeSonsAmbiants
                elif self.sender() == self.addPonctuel:
                    addTo = self.listeSonsPonctuels
                item = QtWidgets.QListWidgetItem()
                item.setText(file)
                addTo.addItem(item)

    def valider(self):
        #validation
        if self.btnValider.text() == "Valider >" :
            #vérifications avant validation
            if self.selection not in [self.fidev.getWidget(), self.marcheParallele.getWidget(), self.carrefour.getWidget(), self.test] :
                QMessageBox.about(self.widget, "Erreur", "Veuillez sélectionner un type d'exercice avant de valider.")
            else :
                self.envoyer()
                self.btnValider.setText("< Changer d'exercice")
                for button in [self.fidev.getWidget(), self.marcheParallele.getWidget(), self.carrefour.getWidget(), self.test] :
                    if button != self.selection :
                        button.setStyleSheet("border: 5px solid grey;")
        else : #changement d'activité
            for button in [self.fidev.getWidget(), self.marcheParallele.getWidget(), self.carrefour.getWidget(), self.test] :
                button.setStyleSheet("border: 5px solid white;")
                self.btnValider.setText("Valider >")
            self.selection = 0
            self.envoi("stop")

    def envoyer(self):
        if (self.selection == self.fidev.getWidget()) :
            self.selectionne = activities.fidev
        elif (self.selection == self.marcheParallele.getWidget()) :
            self.selectionne = activities.marche_parallele
        elif (self.selection == self.carrefour.getWidget()) :
            self.selectionne = activities.carrefour
        elif (self.selection == self.test) :
            self.selectionne = activities.test

        if self.selectionne != activities.test:
            #envoi à la tablette
            message = "<communication_tablette>"
            
            if self.selectionne == activities.fidev:
                message = message + "<groupe numbers=\"0\" />"
                message = message + "<individuels numbers=\"12345678\" />"

            elif self.selectionne == activities.marche_parallele:
                message = message + "<groupe numbers=\"1\" />"
                message = message + "<individuels numbers=\"26\" />"

            elif self.selectionne == activities.carrefour:
                message = message + "<groupe numbers=\"2\" />"
                message = message + "<individuels numbers=\"\" />"

            for son in range(self.listeSonsAmbiants.count()):
                message = message + "<sonAmbiant titre=\"" + self.listeSonsAmbiants.item(son).text() + "\" />"
            for son in range(self.listeSonsPonctuels.count()):
                message = message + "<sonPonctuel titre=\"" + self.listeSonsPonctuels.item(son).text() + "\" />"

            message = message + "</communication_tablette>\n"
            print(message)

            self.thread.sending(message.encode())

            self.soundManager.creaEnceinte(self.selectionne)
            self.soundManager.creaTrajectoire(self.selectionne)
            self.soundManager.creaSource(self.selectionne)
            self.soundManager.start(self.sounds1, self.sounds2)
        else :
            self.soundManager.creaEnceinte(0)
            self.soundManager.creaTrajectoire(0)
            self.soundManager.creaSource(0)
            self.soundManager.start(self.sounds1, self.sounds2)
            self.soundManager.testerEnceintes()


    def envoi(self, data):
        liste = str(data) + "\n"
        self.thread.sending(liste.encode())

    def setConnexion(self):
        self.connexion.setText("Tablette connectée")

    def setDeconnexion(self):
        self.connexion.setText("En attente de connexion")
    
    def help(self):
        QMessageBox.about(self.widget, "Aide", "Pour ajouter des sons ambiants, cliquer sur le bouton \"+\" correspondant. Pour supprimer un son de la liste, double cliquer dessus. Pour sélectionner un type d'exercice, cliquer dessus.")

    def updateBiblio(self):

        # on va convertir tous les fichiers mp3 vers wav (et supprimer les mp3)
        print("Mise à jour de la bibliothèque")
        self.conversion_wav(config["library_dir"])

    def conversion_wav(self, path):
        # si le répertoire n'existe pas, on le créée
        if not os.path.exists(path):
            os.mkdir(path)

        files = os.listdir(path)
        for name in files:
            np = path + "\\" + name
            if os.path.isdir(np):
                print("Parcours du répertoire", np)
                self.conversion_wav(np)
            else:
                if np.lower().endswith("mp3"):
                    wav = np.split('.')[0] + ".wav"
                    if not os.path.isfile(wav) or os.path.getmtime(wav) < os.path.getmtime(np):
                        print("Conversion du fichier", np)
                        sound = AudioSegment.from_mp3(np)
                        sound.export(wav, format="wav")
                

if __name__ == "__main__":
    def OnExitApp():
            app.exec_()

    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    if ui.initialized:
        ui.show()
        atexit.register(OnExitApp)
