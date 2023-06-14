import xml.etree.ElementTree as ET
from pyo import *
from enceinte import *
from source  import *
from trajectoire import *
from math import sqrt
import time
import os
from config import config, activities

class SoundManager():

    def __init__(self, main):
        self.main = main
        self.message = ""
        self.type = self.enceinte = self.son = self.volume = self.state  = self.actuTime = self.lastTime= "0"
        self.source1 = self.source2 = self.source3 = self.source4 = self.source5 = self.source6 = self.source7 = self.source8 = self.sourceTraj1 = self.sourceTraj2 = self.sourceAmbiance = None
        self.sourcesMobiles = self.trajectoires = self.automatiques = []
        self.a = 6 / (20*log10(2))
        self.distanceEnceintesFictives = config["virtual_speaker_distance"]
        self.volumeGlobal = config["global_volume"]
        self.sourcesActives = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        # démarrage du serveur de son pyo
        self.s = Server(nchnls=12)
        self.s.setInputDevice(config["input_device"])
        self.s.setOutputDevice(config["output_device"]) 
        self.s.boot()
        self.s.deactivateMidi()
        self.s.start()

        # démarrage du mixer pyo
        self.mm = Mixer(outs=12, chnls=1, time=.025)
        self.mm.out()

        self.folder_path = config["folder_path"]

        self.volumeTotal = [0, 0, 0, 0, 0, 0, 0, 0]
        self.nombreSourcesActives = 0

        self.create_geometric_configurations()

    # chaque activité a ses propres configurations géométriques
    def create_geometric_configurations(self):
        
        self.position = {}
        
        self.position[activities.fidev] = [
            [2, 3],
            [2+sqrt(2)/2, 2+sqrt(2)/2],
            [3, 2],
            [2+sqrt(2)/2, 2-sqrt(2)/2],
            [2, 1],
            [2-sqrt(2)/2, 2-sqrt(2)/2],
            [1, 2],
            [2-sqrt(2)/2, 2+sqrt(2)/2]]

        self.position[activities.marche_parallele] = [
            [7, 0],
            [1, 1],
            [13, 0],
            [15, 0],
            [11, 0],
            [3, 3],
            [9, 0],
            [5, 0]]

        self.position[activities.carrefour] =[
            [4, 4],
            [6, 6],
            [4, 2],
            [6, 0],
            [2, 2],
            [0, 0],
            [2, 4],
            [0, 6]]

    def clear(self):
        self.mm.clear()

    # on démarre l'activité avec les sons d'ambiance (sounds1) et les sons ponctuels (sounds2)
    def start(self, sounds1, sounds2):
        self.sounds1 = sounds1
        self.sounds2 = sounds2
        # on utilise un thread séparé pour lancer l'activité
        thread_server = threading.Thread(target = self.boucle)
        thread_server.daemon = True
        thread_server.start()

    # boucle principale d'activité
    def boucle(self):
        while True :
            if self.message != "" : #si on a reçu une instruction, on la gère
                self.gestionMessage()
                self.message = ""

            if len(self.sourcesMobiles) != 0 : #s'il existe des sources, on les met à jour
                self.gestionSources()
            time.sleep(0.05)

    def creaEnceinte(self, selection):
        self.selection = selection

        # TODO REFACTORING: utiliser des tableaux pour enceinteX
        self.enceinte1 = Enceinte(1, self.position[self.selection][0][0], self.position[self.selection][0][1])
        self.enceinte2 = Enceinte(2, self.position[self.selection][1][0], self.position[self.selection][1][1])
        self.enceinte3 = Enceinte(3, self.position[self.selection][2][0], self.position[self.selection][2][1])
        self.enceinte4 = Enceinte(4, self.position[self.selection][3][0], self.position[self.selection][3][1])
        self.enceinte5 = Enceinte(5, self.position[self.selection][4][0], self.position[self.selection][4][1])
        self.enceinte6 = Enceinte(6, self.position[self.selection][5][0], self.position[self.selection][5][1])
        self.enceinte7 = Enceinte(7, self.position[self.selection][6][0], self.position[self.selection][6][1])
        self.enceinte8 = Enceinte(8, self.position[self.selection][7][0], self.position[self.selection][7][1])
        self.enceinte9 = Enceinte(9, 0, 0)
        self.enceinte10 = Enceinte(10, 0, 0)
        self.enceinte11 = Enceinte(11, 0, 0)
        self.enceinte12 = Enceinte(12, 0, 0)

        self.enceintes = [self.enceinte1, self.enceinte2, self.enceinte3, self.enceinte4, self.enceinte5, self.enceinte6, self.enceinte7, self.enceinte8]

    def creaTrajectoire(self, selection):
        self.selection = selection
        if self.selection == activities.marche_parallele:
            trajectoire1 = Trajectoire(1, [self.enceinte8, self.enceinte1, self.enceinte7, self.enceinte5, self.enceinte3, self.enceinte4])
            trajectoire2 = Trajectoire(2, [self.enceinte4, self.enceinte3, self.enceinte5, self.enceinte7, self.enceinte1, self.enceinte8])
            self.trajectoires = [trajectoire1, trajectoire2]
        if self.selection == activities.carrefour:
            trajectoire1 = Trajectoire(1, [self.enceinte8, self.enceinte7, self.enceinte5, self.enceinte6])
            trajectoire2 = Trajectoire(2, [self.enceinte8, self.enceinte7, self.enceinte3, self.enceinte4])
            trajectoire3 = Trajectoire(3, [self.enceinte8, self.enceinte7, self.enceinte1, self.enceinte2])
            trajectoire4 = Trajectoire(4, [self.enceinte2, self.enceinte1, self.enceinte7, self.enceinte8])
            trajectoire5 = Trajectoire(5, [self.enceinte2, self.enceinte1, self.enceinte5, self.enceinte6])
            trajectoire6 = Trajectoire(6, [self.enceinte2, self.enceinte1, self.enceinte3, self.enceinte4])
            trajectoire7 = Trajectoire(7, [self.enceinte4, self.enceinte3, self.enceinte1, self.enceinte2])
            trajectoire8 = Trajectoire(8, [self.enceinte4, self.enceinte3, self.enceinte7, self.enceinte8])
            trajectoire9 = Trajectoire(9, [self.enceinte4, self.enceinte3, self.enceinte5, self.enceinte6])
            trajectoire10 = Trajectoire(10, [self.enceinte6, self.enceinte5, self.enceinte3, self.enceinte4])
            trajectoire11 = Trajectoire(11, [self.enceinte6, self.enceinte5, self.enceinte1, self.enceinte2])
            trajectoire12 = Trajectoire(12, [self.enceinte6, self.enceinte5, self.enceinte7, self.enceinte8])
            self.trajectoires = [trajectoire1, trajectoire2, trajectoire3, trajectoire4, trajectoire5, trajectoire6, trajectoire7, trajectoire8, trajectoire9, trajectoire10, trajectoire11, trajectoire12]
        self.automatiques = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def creaSource(self, selection):
        self.selection = selection
        # TODO REFACTORING: utiliser des tableaux pour sourceX
        
        # on initialise les sources
        self.source1 = self.source2 = self.source3 = self.source4 = self.source5 = self.source6 = self.source7 = self.source8 = self.sourceTraj1 = self.sourceTraj2 = self.sourceAmbiance = None
        if self.selection == activities.fidev:
            self.source1 = Source(self.mm, [self.enceinte1], 0, 0)
            self.source2 = Source(self.mm, [self.enceinte2], 0, 0)
            self.source3 = Source(self.mm, [self.enceinte3], 0, 0)
            self.source4 = Source(self.mm, [self.enceinte4], 0, 0)
            self.source5 = Source(self.mm, [self.enceinte5], 0, 0)
            self.source6 = Source(self.mm, [self.enceinte6], 0, 0)
            self.source7 = Source(self.mm, [self.enceinte7], 0, 0)
            self.source8 = Source(self.mm, [self.enceinte8], 0, 0)
        elif self.selection == activities.marche_parallele:
            self.source2 = Source(self.mm, [self.enceinte2], 0, 0)
            self.source6 = Source(self.mm, [self.enceinte6], 0, 0)

        self.sourceAmbiance = Source(self.mm, Trajectoire(0, [self.enceinte9, self.enceinte10, self.enceinte11, self.enceinte12]), 0, 0)
        self.sources = [self.source1, self.source2, self.source3, self.source4, self.source5, self.source6, self.source7, self.source8]

    def setState(self):
        if self.type == "solo" or self.type == "ambiant":
            if self.state == "on":
                self.source.setState(True)
            else :
                self.source.setState(False)

    def setVolume(self):
        if self.type == "solo":
            self.source.setVolume(self.volume)
            # sons solo en 2 à 10
            self.mm.setAmp(self.enceinte, self.enceinte + 1, self.volume)
        elif self.type == "ambiant":
            self.source.setVolume(self.volume)
            # sons NUAGES en 0 et 1
            for i in range(0, 2) :
                self.mm.setAmp(self.enceinte, i, self.volume)
        else :
            self.volumeGlobal = self.volume

    def setSon(self):
        if self.type == "solo" or self.type == "ambiant" :
            if self.son != "clear":
                if isinstance(self.source.getPlayer(), bool):
                    self.source.setPlayer(self.son)
                    if self.source.getState() == True:
                        self.source.getPlayer().play()
                    else:
                        self.source.getPlayer().stop()
                    self.mm.delInput(self.enceinte)
                    self.mm.addInput(self.enceinte, self.source.getPlayer())
                    if self.type == "solo" :
                        # une source solo ne joue que dans une enceinte
                        # sons solo en 2 à 10
                        self.mm.setAmp(self.enceinte, self.enceinte + 1, self.source.getVolume())
                    elif self.type == "ambiant":
                        # sons NUAGES en 0 et 1
                        for i in range(0, 2) : #TODO NUAGES: on doit aussi changer ici si on veut passer les nuages en 0 et 1
                            self.mm.setAmp(self.enceinte, i, self.source.getVolume())
                else :
                    self.source.setPath(self.son)
            else:
                self.mm.delInput(self.enceinte)
                self.source.setPlayer(False)
        
    def setTrajectoire(self, numero, delay):
        self.sourcesMobiles.append(Source(self.mm, self.trajectoires[numero - 1], time.time() + (delay/100), -self.distanceEnceintesFictives, 1+(random.randint(-50, 50))/100))
        # TODO SON UNIQUE: le son est fixé ici
        self.sourcesMobiles[-1].setPlayer(self.folder_path + "/data/30km_h.wav")
        self.mm.addInput(self.sourcesMobiles[-1], self.sourcesMobiles[-1].getPlayer())
        self.sourcesActives[numero-1] += 1

    def automatique(self):
        if self.enceinte == 1:
            self.automatiques[int(self.trajectoire)-1] = 1
            self.setTrajectoire(int(self.trajectoire), 0)
        else :
            self.automatiques[int(self.trajectoire)-1] = 0

    def receive(self, data):
        self.message = data

    # Informations reçues depuis la tablette. 
    # Forme du message (attention, importance de l'ordre des balises filles):
    # <communication_appli><type style="P1"/><enceinte numero="P2"/><P3 value="P4" /></communication_appli>
    # Avec valeurs possibles:
    # - P1: 
    #    - "solo": enceinte spatialisée
    #    - "ambiant": enceinte d'ambiance
    #    - "groupe": pour les trajectoires (avec P3 "trajectoire", "automatique")
    # - P2: 0 (pour diffuser sur les nuages = ambiance), 1 à 8 (pour les enceintes spatialisées). 
    #       Attention: paramètre aussi utilisé en 0 ou 1 pour piloter l'automatique (voir plus bas).
    #       Remarque: il serait plus intuitif de considérer ce paramètre comme celui correspondant aux sources (ponctuelles).
    # - P3: 
    #    - "volume": régle le volume d'une enceinte (solo, ambiant), ou le volume global (groupe). P4 de 0 à 100
    #    - "state": éteint ou allume un son. P4 = on ou off
    #    - "son": choisi un fichier son. P4 = nom du fichier à jouer (TODO: incertitude sur le format exact), ou un entier (entre 1 et 8) pour le test, ou "clear"
    #    - "trajectoire": lance un véhicule suivant une trajectoire pré-établie. P4: numéro de la trajectoire
    #    - "automatique": lance (si P2=1) ou arrête (si P2=0) une trajectoire automatique (ie qui sera rejouée en boucle). P4: numéro de la trajectoire.
    #    - "stop": réduit le volume à zéro (fonctionnement pas intuitif, car l'interface suggère un stop, mais c'est un mute...).
    #
    # Remarque: on peut regarder la fonction testerEnceintes() qui utilise 3 messages pour diffuser chacun des sons "1", "2", "3"...
    # 
    # Remarque: P3 = "demande" n'est pas fonctionnel, la tablette n'envoyant jamais ce message.
    #   Cependant, si python émettait un "demande" (quand un son s'arrête par exemple), cela permettrait d'envoyer
    #   à l'application android des informations pour mettre à jour l'affichage :
    #     - nombre de véhicule mobile par trajectoire avec "sourcesActives"
    #     - nombre de sources actives avec "nombreSourcesActives"
    #     - volume de chacune des enceinte avec "volumeTotal" (à vérifier cependant, calcul éparpillé)
    def gestionMessage(self):
        try :
            root = ET.fromstring(self.message)
            
            for child in root:
                if child.tag == "type":
                    self.type = child.attrib.get('style')
    
                elif child.tag == "enceinte":
                    if int(child.attrib.get('numero')) == 0 and self.type == "ambiant" :
                        self.enceinte = 0
                        self.source = self.sourceAmbiance
                    else :
                        self.enceinte = int(child.attrib.get('numero'))
                        if self.type == "solo":
                            self.source = self.sources[int(child.attrib.get('numero')) - 1]
    
                elif child.tag == "volume":
                    self.volume = (float(child.attrib.get('value'))/100)/2
                    self.setVolume()
    
                elif child.tag == "state":
                    self.state = child.attrib.get('value')
                    self.setState()
    
                elif child.tag == "son":
                    if child.attrib.get('titre') == "clear" :
                        self.son = child.attrib.get('titre')
                    elif child.attrib.get('titre') in {"1", "2", "3", "4", "5", "6", "7", "8"} :
                        self.son = self.folder_path + "/data/" + child.attrib.get('titre') + ".wav"
                    else :
                        self.son = self.sounds2[self.sounds1.index(child.attrib.get('titre'))][0]+child.attrib.get('titre')+self.sounds2[self.sounds1.index(child.attrib.get('titre'))][1]
                    self.setSon()
    
                elif child.tag == "trajectoire":
                    self.setTrajectoire(int(child.attrib.get('value')), 0)
                
                elif child.tag == "automatique":
                    self.trajectoire = child.attrib.get('value')
                    self.automatique()
                    
                elif child.tag == "demande":
                    for i in range(0,8) :
                        self.volumeTotal[i] = int(round(self.volumeTotal[i],1) * 10)

                    self.main.envoi(self.sourcesActives+[self.nombreSourcesActives]+self.volumeTotal)

                elif child.tag == "stop":
                    self.volumeGlobal = 0
              
        except Exception as e : print(e)

    def gestionSources(self) :
        self.volumeTotal = [0, 0, 0, 0, 0, 0, 0, 0]
        self.nombreSourcesActives = 0
        for source in self.sourcesMobiles : #pour chaque source existante
            self.volumesSource = [0, 0, 0, 0, 0, 0, 0, 0]
            enceintestraj = source.getTrajectoire().getEnceintes()
            if source.getTimestamp() < time.time() :
                #je calcule le temps écoulé depuis la dernière fois, et je met à jour le dernier timestamp de la source
                timestamp = time.time()
                temps = timestamp - source.getTimestamp()
                source.setTimestamp(timestamp)

                #avec la vitesse, j'en déduit la distance parcourue (en m/s)
                distance = 2 * temps

                #je calcule la position actuelle, et je met à jour la dernière position de la source
                position = distance + source.getPosition()
                source.setPosition(position)

                #je vérifie si c'est sur une enceinte, ou entre 2 enceintes, ou si c'est terminé
                distanceZero = source.getTrajectoire().getDistanceZero()
                if position < 0 :
                    #arrivée du son dans la première enceinte
                    self.calculVolumes("fictif", None, enceintestraj[0], self.distanceEnceintesFictives*-1, 0, position)
                    self.setVolumes(source)
                elif position > distanceZero[-1] and position < distanceZero[-1] + self.distanceEnceintesFictives :
                    #départ du son dans la dernière enceinte
                    self.calculVolumes("fictif", enceintestraj[-1], None, distanceZero[-1], distanceZero[-1] + self.distanceEnceintesFictives, position)
                    self.setVolumes(source)
                elif position > distanceZero[-1] + self.distanceEnceintesFictives :
                    #source terminée
                    self.mm.delInput(source)
                    self.sourcesMobiles.remove(source)
                    self.sourcesActives[source.getTrajectoire().getIdentifiant() - 1] -= 1
                    #automatique ou pas
                    if self.automatiques[source.getTrajectoire().getIdentifiant() - 1] == 0 : #terminé
                        break
                    else : #on continue
                    #min 1sec, max 6
                        self.setTrajectoire(int(source.getTrajectoire().getIdentifiant()), random.randint(100, 600))
                else :
                    for x in range(len(distanceZero)) :
                        if position == distanceZero[x] : #si c'est sur une enceinte, je jouerai cette enceinte à 100%
                            for enceinte in self.enceintes :
                                if enceinte == enceintestraj[x+1]:
                                    self.volumesSource[enceinte.getIndex() - 1] = 1
                                self.setVolumes(source)
                            break
                        elif position < distanceZero[x] : #si c'est entre 2, je jouerai sur les 2 enceintes
                            self.calculVolumes("reel", enceintestraj[x-1], enceintestraj[x], distanceZero[x-1], distanceZero[x], position)
                            self.setVolumes(source)
                            break
            

    def calculVolumes(self, type, enceinte1, enceinte2, point1, point2, position):
        if position >= 0 :
            d1 = position - point1 + 1*10**(-5)
            d2 = point2 - position + 1*10**(-5)
        else :
            d1 = abs(point1 - position + 1*10**(-5))
            d2 = abs(position - point2 + 1*10**(-5))        

        if type == "reel" :
            v1 = round(((1)/(sqrt((1/(d1**(2*self.a)))+(1/(d2**(2*self.a))))))/(d1**self.a), 4)
            v2 = round(((1)/(sqrt((1/(d1**(2*self.a)))+(1/(d2**(2*self.a))))))/(d2**self.a), 4)
        elif type == "fictif" :
            v1 = 1 - d1 / (d1 + d2)
            v2 = 1 - d2 / (d1 + d2)

        for enceinte in self.enceintes :
            if enceinte == enceinte1 :
                self.volumesSource[enceinte.getIndex() - 1] = v1
            elif enceinte == enceinte2 :
                self.volumesSource[enceinte.getIndex() - 1] = v2


    def setVolumes(self, source):
        self.volumeTotal = [x+y for x,y in zip(self.volumeTotal, self.volumesSource)]
        self.nombreSourcesActives +=1
        for i in range(len(self.enceintes)):
            # enceintes omni de 2 à 10
            volume = float(self.volumesSource[i]) * float(self.volumeGlobal)
            self.mm.setAmp(source, self.enceintes[i].getIndex() + 1, volume)


    def testerEnceintes(self):
        try :
            for i in range(1, 9):
                self.mm.clear()
                self.message = "<communication_appli><type style=\"solo\" /><enceinte numero=\"" + str(i) + "\" /><son titre=\""+ str(i) +"\" /></communication_appli>"
                self.gestionMessage()
                self.message = "<communication_appli><type style=\"solo\" /><enceinte numero=\"" + str(i) + "\" /><volume value=\"100\" /></communication_appli>"
                self.gestionMessage()
                self.message = "<communication_appli><type style=\"solo\" /><enceinte numero=\"" + str(i) + "\" /><state value=\"on\" /></communication_appli>"
                self.gestionMessage()
                time.sleep(2.5)
                self.message = "<communication_appli><type style=\"solo\" /><enceinte numero=\"" + str(i) + "\" /><state value=\"off\" /></communication_appli>"
                self.gestionMessage()
            
            for i in range(1,9):
                self.message = "<communication_appli><type style=\"solo\" /><enceinte numero=\"" + str(i) + "\" /><son titre=\"clear\" /></communication_appli>"
                self.gestionMessage()
        except Exception as e : print(e)
