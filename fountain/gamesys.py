# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import pickle
import sys

class game:
    
    def __init__(self, title = 'Fountain', winSize = (800, 600), renderFps = 60, ogl = True, fs = False):
        pygame.init()
        self.calcClock = pygame.time.Clock()
        self.renderClock = pygame.time.Clock()
        pygame.display.set_caption(title)
        winState = DOUBLEBUF | HWSURFACE
        if ogl == True:
            winState |= OPENGL
        if fs == True:
            winState |= FULLSCREEN
        self.winSurf = pygame.display.set_mode(winSize, winState)
        self.rect = self.winSurf.get_rect()
        self.winSize = self.rect.size
        #self.grabornot = True
        self.renderFps = renderFps

    def eventSolve(self):
        self.mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    pygame.quit()
                    sys.exit()

    def renderEnd(self):
        pygame.display.flip()
        self.renderClock.tick(self.renderFps)

