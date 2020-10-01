#############################################################
# Programme: Jeu sur le concept de flappy birds.            #
# Auteur: Arthur Freeman              Date: Février 13 2019 #
#############################################################

#############################################################
# To do:                                                    #
# Optimise code.                                            #
# Encapsuler toutes les variables dans un objet.            #
# Fait pour objet scores, je dois encore le faire pour le   #s
# programme principal.                                      #
#############################################################

#############################################################
#                                                           #
#                       Imports                             #
#                                                           #
#############################################################
import pygame
from pygame.locals import *
from time import sleep
import random
import pygame_textinput #Text input permet de créer des boîtes de texte.
import scores #Librairie qui gèrent l'accès au score.
#############################################################
#                                                           #
#                       OnCreate                            #
# Ici on ne mets QUE les variables que l'on ne modifie pas  #
# par la suite, si oui, on les mets dans menu()             #
#############################################################
pygame.init()
width, height = 800, 600
size = [width, height]
screen = pygame.display.set_mode(size)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

width, height = 800, 600
size = [width, height]
screen = pygame.display.set_mode(size)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

playerImage = pygame.image.load("./ressources/player.png")
player = playerImage.get_rect()
topTube = pygame.image.load("./ressources/tube.png")
topTubeRect = topTube.get_rect()
topTubeRect.left = width
topTubeRect.top = 0

bottomTube = pygame.image.load("./ressources/tube.png")
bottomTubeRect = bottomTube.get_rect()
bottomTubeRect.left = width
bottomTubeRect.top = height - bottomTubeRect.width
coolDown = True

pygame.font.init()
default_font = pygame.font.get_default_font()
font_renderer = pygame.font.Font(default_font, 72)
labelScore = font_renderer.render("Score: " ,1, (255,0,0)) # RGB Color
textBox = pygame_textinput.TextInput(initial_string = 'ENTER NAME HERE') #On crée une "boite de texte"
name = ''
#############################################################
#                                                           #
#                  Déclaration de Fonctions                 #
#                                                           #
#############################################################
def text_objects(text, font):
    textSurface = font.render(text, True, black) #Retoruene un TSurface.
    return textSurface, textSurface.get_rect() #Retourne deux objets, un TSurface, et un TRectangle.
                                               #Il faut blitter la surface sur le rectangle, pour la mettre à jour.
   
#Fonction qui affiche le menu.
def menu():
    #On doit préciser que ces variables sont globales dans les fonctions, sinon python en crée
    #des locales et plus rien n'a de sens.
    global speedY, continuer, score, topTubes, bottomTubesImages, bottomTubes,topTubesImages, player, gravity, vitesseTubes, textBox, name #Mettre dans un objet pour éviter de devoir déclarer tout en global. Object globVar avec une grosse création.
    global continuer
    scores.loadScores()
    scores.scoresVar.sort()
    print(scores.scoresVar.listOfLists)
    print("HELELLWOKAOJOIFWJAOJO")
    while True:
        continuer = True
        player.top = 100
        player.left = 100
        #Il faut reinitialiser les valeurs du tableau.
        topTubes = [] #Tableau de rectangles, tubes du haut.
        bottomTubes = [] #Tableau de rectangles, tubes du bas.
        topTubesImages = [] #Images...
        bottomTubesImages = [] #Images correspondantes...        
        
        score = 0
        speedY = 0
        gravity = 0.2
        vitesseTubes = 5    

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()
                
            if event.type == KEYDOWN: #Si on appuie sur Enter, alors
                if event.key == K_RETURN:
                    name = textBox.get_text() #On récupère ce qui à été écrit.
                    textBox.clear_text() #On efface le texte.
                    
        screen.fill(white) #Couleur de fond.
        largeText = pygame.font.SysFont("Times",115) #Retourne un objet de type Font.
        smallText = pygame.font.SysFont("Times",15)

        scoreboardSurfaces = ["","","","",""]
        scoreboardRectangles = ["","","","",""]

       
   
        for i in range(0, 5): #5 boites de texte.
            scoreboardSurfaces[i], scoreboardRectangles[i] = text_objects( str(scores.scoresVar.listOfLists[i]["name"]) + ":" + str(scores.scoresVar.listOfLists[i]["score"]), smallText)
            scoreboardRectangles[i].center = ( width / 2, height - 150 + 25*i)
            screen.blit(scoreboardSurfaces[i], scoreboardRectangles[i])
           
        TextSurf, TextRect = text_objects("Not flappy birds.", largeText) #On récupère les 5 premiers scores que l'on mets dans un tableau de labels.      
        TextRect.center = ((width/2),(height/2) - 100) #Place le rectangle au milieu de l'écran.
        screen.blit(TextSurf, TextRect) #Affiche le texte.
        
        button("GO!",150,450,100,50,(0,40,0),(40,0,0),game_loop) #génère les bouttons via les méthodes ci-dessous.
        button("Quit",550,450,100,50,(40,0,0),(0,40,0),exit)
         
                       
        textBox.update(events)
        screen.blit(textBox.get_surface(), (300,350)) #On affiche.
        pygame.display.update()

#Position x,y width, height, ic et ac sont des couleurs, action détermine si on a clické ou pas, command est la procédure passée en paramètre.
def button(msg,x,y,w,h,ic,ac,command=None): #Procédure pour générer un boutton.
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() #On récupère la position de la souris. 
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        #Si on est compris dans la zone, on dessine un rectangle de couleur ac.
        pygame.draw.rect(screen, ac,(x,y,w,h))
        #Si on clicke, et que il y a une action, alors action.
        if click[0] == 1 and command != None:
            #print("hello")
            command() #On appelle la fonction passée en paramètre.        
    else:
        #Sinon on affiche le boutton normal.
        pygame.draw.rect(screen, ic,(x,y,w,h))

    #On génère le texte.
    smallText = pygame.font.SysFont("Times",20) #msg est le paramètre message de la fonction.
    textSurf, textRect = text_objects(msg, smallText) #On crée les objets,
    textRect.center = ( (x+(w/2)), (y+(h/2)) ) #On les affiche.
    screen.blit(textSurf, textRect) #On affiche le texte dans le rectangle.

    
#Procédure qui ajoute un tube.
def addTube(topTubes, topTubeRect, topTubesImages, bottomTubes, bottomTubeRect, bottomTubesImages):
    topTube = pygame.image.load("./ressources/tube.png")
    topTube = pygame.transform.scale(topTube, ( 60, random.randint(100, 260) ) ) #On la redimensionne aléatoirement en y.
    topTubeRect = topTube.get_rect() #On répupère son rectangle.
    topTubeRect.left = width #On la place.
    topTubeRect.top = 0
    topTubes.append(topTubeRect) #On ajoute le rectangle au tableau approprié.
    topTubesImages.append(topTube) #Et l'image au tableau approprié.

    bottomTube = pygame.image.load("./ressources/tube.png") #Idem pour l'autre image.
    bottomTube = pygame.transform.scale(bottomTube, ( 60, random.randint(100,260) ) ) #On lui donne une dimension en y entre 0 et 60.
    bottomTubeRect = bottomTube.get_rect()
    bottomTubeRect.left = width
    bottomTubeRect.top = height - bottomTubeRect.height #On la place en bas.
    bottomTubes.append(bottomTubeRect) #On l'append au tableau approprié.
    bottomTubesImages.append(bottomTube)
    
def deplacements():
    global speedY, gravity, coolDown
    #Le joueur tombe en MRUA, donc on accélère.
    speedY = speedY + gravity
    #Vitesse maximale, au dela de laquelle on arrête d'accélérer.
    if speedY > 10:
        gravity = 0
    else:
        gravity = 0.2 #Si on n'a pas cette vitesse, alors on tombe normalement.
            
    #On boucle sur tous les évènements de pygame.
    for event in pygame.event.get():
        #Si on ferme la fenêtre ou si on appuie sur escape, alors on ne continue plus.
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            continuer = False

        if event.type == KEYDOWN:
            #Si on appuie sur la touche droite, alors on ajoute un tube.
            if event.key == K_RIGHT and coolDown:
                addTube(topTubes, topTubeRect, topTubesImages, bottomTubes, bottomTubeRect,bottomTubesImages)
                coolDown = False
            if event.key == K_LEFT:
                coolDown = True
            if event.key == K_UP:
                speedY = -5

#############################################################
#                                                           #
#                       MainLoop                            #
#                                                           #
#############################################################

def game_loop():
    #Bizzareries de Python...
    global continuer, labelScore, score, name
    print(continuer)
    while continuer:
        #Si on appuie sur fermer ou escape....
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
                
        #On rempli l'écran de noir.
        screen.fill(black)

        #Intervalle de temps de jeux.
        sleep(0.01)

        #On appelle la procédure qui gère les déplacements.
        deplacements()

        #On parcoure le tableau des tubes du haut.
        for i in range(0, len(topTubes)):

            #Si le joueur touche un tube du bas ou du haut, alors on arrête le jeu.
            if player.colliderect(bottomTubes[i]) or player.colliderect(topTubes[i]):
                row = [name, score/6] #On crée une ligne, (de strings)
                #scores.sheet.insert_row(row, 2) #On l'insère dans la fiche.
                scores.scoresVar.sheet.insert_row(row, 2) #On l'insère dans la fiche.
                scores.loadScores()
                scores.scoresVar.sort()
                continuer = False
                
            #Déplacement des tubes. Vitesse négative, car gradué positif positif.
            topTubes[i].left = topTubes[i].left - vitesseTubes
            bottomTubes[i].left = bottomTubes[i].left - vitesseTubes

            #Détéction de si le joueur est passé entre un tube ou pas.
            if player.top > topTubes[i].bottom and player.bottom < bottomTubes[i].top and player.left > topTubes[i].left and player.right < topTubes[i].right:
                score = score + 1

            #Procédure de surpression des tubes en dehors de l'écran.
            if bottomTubes[i].right < 0:
                del bottomTubes[i]          #On supprime les rectangles
                del bottomTubesImages[i]    #et les images.
                del topTubes[i]
                del topTubesImages[i]
                break #Break essentiel, car il faut mettre à jour la boucle et éviter
                      #des erreurs d'indexation.

            #On place l'image à leur nouvelle position.
            screen.blit(topTubesImages[i], (topTubes[i].left, 0) )
            screen.blit(bottomTubesImages[i], (bottomTubes[i].left, height - bottomTubes[i].height) )
            
        #Affichage du texte.
        screen.blit(labelScore, (0,0))
        #Modification du label en fonction du score.
        labelScore = font_renderer.render("Score: " + str(round(score / 6)) ,1, (255,0,0))

        #Déplacement du joueur.    
        player.top = player.top + speedY
        screen.blit(playerImage, player)

        #On mets à jour l'écran.
        pygame.display.flip()
        pygame.display.update()

menu() #Si on break en dehors du main_loop, on retourne au menu.
game_loop() #Si on sort du menu, on vas au game_loop.
