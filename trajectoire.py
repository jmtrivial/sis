from enceinte import *
from math import sqrt

class Trajectoire():

    def __init__(self, identifiant, enceintes):
        self.identifiant = identifiant
        self.enceintes = enceintes

        self.distanceZero = []

        total = 0
        for i in range(len(self.enceintes)):
            if i == 0 :
                self.distanceZero.append(0)
            else :
                total += sqrt((self.enceintes[i].getX() - self.enceintes[i-1].getX())**2 + (self.enceintes[i].getY() - self.enceintes[i-1].getY())**2)
                self.distanceZero.append(total)

    def getEnceintes(self):
        return self.enceintes

    def getDistanceZero(self) :
        return self.distanceZero

    def getIdentifiant(self):
        return self.identifiant