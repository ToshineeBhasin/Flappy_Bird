'''
Created on 10-Jun-2020

@author: Toshinee Bhasin
'''

import random # for generting random numbers
import sys #use to exit function
import pygame, sys, random
from pygame.locals import * #basic pygame imports
from turtledemo.nim import SCREENWIDTH, SCREENHEIGHT
from _ast import In
from pygame.constants import K_ESCAPE, KEYDOWN, K_SPACE, K_UP
import math  


#global variables
FPS = 32 #frame per Second
SCREENWIDTH = 288
SCREENHEIGHT = 512
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'D:/Flappy Bird/gallery/sprites/bird.png'
BACKGROUND = 'D:/Flappy Bird/gallery/sprites/background.png'
PIPE = 'D:/Flappy Bird/gallery/sprites/pipe.png'


def welcomeScreen():
    #shows welcome screen
    
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['Player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            #if user click cross button close the game
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['Player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)
                
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0
    
    #pygame.image.load('D:/Flappy Bird/gallery/sprites/level1.jpg').convert_alpha()
    
    
    #create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    #my list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y' : newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : newPipe2[0]['y']}
        ]
    #my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y' : newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y' : newPipe2[1]['y']}
        ]
    
    pipeVolX= -4
    playerVolY = -9
    playerMaxVolY = 10
    playerMinVolY = -8
    playerAccY = 1
    
    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False #it is true only when the bird is flapping
    
    while True:
        for event in pygame.event.get():
            if event.type  == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery> 0:
                    playerVolY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
    
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        #player is crashed
        if crashTest:
            return 
        
        #check for score
        playerMidPos = playerx + GAME_SPRITES['Player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
            
        if playerVolY <  playerMaxVolY and not playerFlapped:
            playerVolY += playerAccY
            
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['Player'].get_height()
        playery = playery + min(playerVolY,GROUNDY - playery - playerHeight)
   
        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVolX
            lowerPipe['x'] += pipeVolX
        
        #add a new pipe when the first is about to cross the leftmost part of the screen screen
        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        
        #if the pipe is put of the screen remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
    
    
        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
    
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['Player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2
    
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > GROUNDY -25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x'])< GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    
    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['Player'].get_height() > pipe['y']) and abs(playerx - pipe['x'])< GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False
    
    
    
def getRandomPipe():
    #generate  positions of 2 pipes(one bottom straight and one top rotated) for blitting on screen
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset  = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH +10
    y1= pipeHeight - y2 + offset
    pipe = [
        {'x':pipeX, 'y': -y1},  #upper pipe
        {'x':pipeX, 'y': y2}  #lower pipe
        ]
    return pipe



if __name__ == "__main__":
    #main function from where our game will start
    pygame.init() #initialize pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy bird by Toshinee')
    GAME_SPRITES['numbers']= (
        pygame.image.load('D:/Flappy Bird/gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('D:/Flappy Bird/gallery/sprites/9.png').convert_alpha(),
        )
    
    GAME_SPRITES['message']= pygame.image.load('D:/Flappy Bird/gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('D:/Flappy Bird/gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
        )
    #GAME_SPRITES['gameover'] = pygame.image.load('D:/Flappy Bird/gallery/sprites/gameover.png').convert_alpha()
    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('D:/Flappy Bird/gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('D:/Flappy Bird/gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('D:/Flappy Bird/gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('D:/Flappy Bird/gallery/audio/Swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('D:/Flappy Bird/gallery/audio/wing.wav')
    
    GAME_SPRITES['background'] =  pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['Player'] = pygame.image.load(PLAYER).convert_alpha()
    
while True:
    welcomeScreen()  #shows welcome screen to the user until he press a button
    mainGame() #shows welcome screen to the user until he press a button
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    