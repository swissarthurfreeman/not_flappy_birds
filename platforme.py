#######################################################
#                       imports                       #
#######################################################
import pygame
from pygame.locals import *
from tubes import Tourelles
from tubes import Tube
from random import randint

#######################################################
#                       OnCreate                      #
#######################################################
pygame.init()
width = 800
height = 600
size = [width, height]
form = pygame.display.set_mode(size)
black = 0, 0, 0
blue = (0, 0, 255)

platforme = pygame.image.load("platforme.png")
platformeRect = platforme.get_rect()
playerImage = pygame.image.load("player.png")
player = playerImage.get_rect()
player.top = 400
player.left = 400
form.blit(platforme, (0, height-platforme.get_height())) #Blit, takes image and position in paramaters.  #Cannot take rectangle in parameter.                                                        
pygame.key.set_repeat(1, 3)             
continuer = 1
speedX, speedY = 0, 0
clock = pygame.time.Clock()
notJumping = True
gravity = 1
tubesInstance = Tourelles()
#testVariable = Tube(pygame.draw.rect(form, black, (200, 200, 20, 20), 0), pygame.draw.rect(form, black, (200, 200, 20, 20), 0))


#######################################################
#                       Functions                     #
#######################################################
#Pas le choix, collideRect ne fonctionne pas pour des TRectangle...?!?!
#Cette fonction n'est pas la mienne: https://www.dropbox.com/s/wldf3kdylsfxio1/collision_detect.py
def collideRectangle(rect1, rect2): 
    x1, y1, w1, h1 = rect1.left, rect1.top, rect1.width, rect1.height
    x2, y2, w2, h2 = rect2.left, rect2.top, rect2.width, rect2.height
    if (x2+w2>=x1>=x2 and y2+h2>=y1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1>=y2): 
        return True
    elif (x2+w2>=x1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    elif (x2+w2>=x1+w1>=x2 and y2+h2>=y1+h1>=y2):
        return True
    else: 
        return False

def enDehors(player):
    if player.left + player.width > 800:
        player.left = 800 - player.width
    if player.left <= 0:
        player.left = 0

#######################################################
#                       MainLoop                      #
#######################################################
while continuer:
    speedY = speedY + gravity
    clock.tick(60)
    #Boucle sur tous les événements gérés par Pygame
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            # La fenêtre a été fermée ou La touche ESC a été pressée.
            continuer = 0 # Indique de sortire de la boucle.


        #DÉPLACEMENT   
        if event.type == KEYDOWN:  
            if event.key == K_UP:
                speedY = -20       
            if event.key == K_RIGHT:
                speedX = 20
            if event.key == K_LEFT:
                speedX = -20
               
            if event.key == K_SPACE:
                print("Added Tube")
                tubesInstance.addTube(Tube(pygame.draw.rect(form, blue, (randint(0,600), 200, 20, 20), 0), pygame.draw.rect(form, blue, (randint(0,600), 300, 20, 20), 0)))    

    #tubesInstance.move()
    for i in range(0, len(tubesInstance.anArray)):
        tubesInstance.anArray[i].bottomTube.move(-1,0)
        print("Works?")
        
    player.top = player.top + speedY            
    player.left = player.left + speedX

    #player = player.move(speedX, speedY)              
    #Dieu sait pourquoi mais platformeRect.top est à 25 si on ne fait pas ça...?!
    """
    platformeRect.top = 600 - 25
    if collideRectangle(player, platformeRect):
        player.top = platformeRect.top - player.height
        speedY = 0
    """
    enDehors(player)
  
    #form.fill(black) #On efface ce qui a été précédémment déssiné.
    #pygame.draw.rect(form, blue, (200, 200, 20, 20), 0)
    
    form.blit(playerImage, player) #Place l'image sur le canvas.
    form.blit(platforme, (0, height-platforme.get_height())) #Blit, takes image and position in paramaters.   
    pygame.display.flip() #Mets à jour l'écran.
    speedX = 0 #On remet le déplacement à zéro, pas que ce soit constant.
    
pygame.display.quit() # ferme la fenêtre, c.f. https://www.pygame.org/docs/ref/display.html
pygame.quit() # quitte pygame, c.f. https://www.pygame.org/docs/ref/pygame
