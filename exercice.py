from PyQt5 import QtCore, QtGui, QtWidgets

class Exercice():

	def __init__(self, identifiant, text):
		self.id = identifiant
		self.text = text

		self.icone = "images/type" + str(self.id) + ".png"

		self.button = QtWidgets.QPushButton()
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(self.icone), QtGui.QIcon.Normal, QtGui.QIcon.On)
		self.button.setIcon(icon)
		self.button.setIconSize(QtCore.QSize(200, 200))
		self.button.setFlat(True)

		self.label = QtWidgets.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.label.setText(self.text)

	def getWidget(self):
		return self.button

	def getLabel(self):
		return self.label

	def getID(self):
		return self.id