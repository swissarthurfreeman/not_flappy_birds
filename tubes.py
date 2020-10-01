import pygame
from pygame.locals import *

#On génère une classe qui contient deux images,
#même left mais height différent, pour tubes.
class Tube:       #Rect objects => topTube, bottomTube
    def __init__(self, topTube, bottomTube):
        self.topTube = topTube
        self.bottomTube = bottomTube

class Tourelles:
    def __init__(self):
        self.anArray = []
        #self.nbElements = 0
    
    def addTube(self, tube):
        #anArray.append(TTubes(pygame.draw.rect(form, black, (200, 200, 20, 20), 0)), pygame.draw.rect(form, black, (200, 200, 20, 20), 0)) 
        self.anArray.append(tube)
        #self.nbElements = self.nbElements + 
