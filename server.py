import re
import socket, threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from config import config
import time

class Server():

    def __init__(self, qwidget, mixer, activity):
        self.mixer = mixer
        self.activity = activity
        self.qwidget = qwidget
        self.serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect
        HOST = config["server_host"]
        PORT = config["server_port"]
        self.client = 0

        self.serverSock.bind((HOST, PORT))   

        thread_listener = threading.Thread(target = self.listen)
        thread_listener.daemon = True
        thread_listener.start()

    def listen(self):
        while True :
            self.serverSock.listen(5)
            self.client, address = self.serverSock.accept()
            self.activity.setConnexion()
            thread_server = threading.Thread(target = self.server)
            thread_server.daemon = True
            thread_server.start()
            break

    def server(self):
        while True:
            response = ""
            if self.client != 0 :
                try :
                    response = self.client.recv(1024).decode('utf-8')
                except :
                    print("déconnexion")
                    self.activity.setDeconnexion()
                    self.listen()
                    break
            #response=input("message ? ")
            if response != "":
                self.mixer.receive(response)

    def sending(self, data):
        print(data)
        try :
            self.client.send(data)
        except:
            QMessageBox.about(self.qwidget, "Erreur", "L'application tablette n'est pas connectée. Veuillez lancer l'application tablette avant de valider la sélection.")
