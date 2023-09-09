# imports

## standard

import time

import math
import random

## external

import pygame

import numpy

# actions

def fGameOfLife():

    pygame.init()

    vSize = (64, 64)
    vScale = 8

    vScreen = pygame.display.set_mode([vSize[0] * vScale, vSize[1] * vScale])

    vNearLiveMin = 2
    vNearLiveMax = 3
    vNearMakeMin = 3
    vNearMakeMax = 3

    vGrid = numpy.array([[False] * vSize[0]] * vSize[1])
    vProb = int(math.sqrt(min(vSize)))
    for vPosY in range(vSize[1]):
        vLine = vGrid[vPosY]
        for vPosX in range(vSize[0]):
            vLine[vPosX] = ((random.randint(0, vProb) % vProb) == 0)

    vWorkFlag = True
    while vWorkFlag:

        for vEvent in pygame.event.get():
            match vEvent.type:
                case pygame.QUIT: vWorkFlag = False
                case _: ...

        vScreen.fill((16, 16, 16))

        vTemp = vGrid.copy()
        for vPosY in range(vSize[1]):

            vLine = vTemp[vPosY]
            for vPosX in range(vSize[0]):

                vNear = 0
                vNear += int(vGrid[(vPosY - 0) % vSize[1]][(vPosX - 1) % vSize[0]])
                vNear += int(vGrid[(vPosY + 0) % vSize[1]][(vPosX + 1) % vSize[0]])
                vNear += int(vGrid[(vPosY - 1) % vSize[1]][(vPosX - 0) % vSize[0]])
                vNear += int(vGrid[(vPosY + 1) % vSize[1]][(vPosX + 0) % vSize[0]])
                vNear += int(vGrid[(vPosY - 1) % vSize[1]][(vPosX - 1) % vSize[0]])
                vNear += int(vGrid[(vPosY - 1) % vSize[1]][(vPosX + 1) % vSize[0]])
                vNear += int(vGrid[(vPosY + 1) % vSize[1]][(vPosX + 1) % vSize[0]])
                vNear += int(vGrid[(vPosY + 1) % vSize[1]][(vPosX - 1) % vSize[0]])

                if vLine[vPosX]:

                    vLine[vPosX] = (vNear >= vNearLiveMin) & (vNear <= vNearLiveMax)

                else:

                    vLine[vPosX] = (vNear >= vNearMakeMin) & (vNear <= vNearMakeMax)

                if vLine[vPosX]:

                    vRectSize = max(vScale - 1, 1)
                    vRectPosX = vPosX * vScale
                    vRectPosY = vPosY * vScale
                    vRect = pygame.Rect(vRectPosX, vRectPosY, vRectSize, vRectSize)
                    pygame.draw.rect(vScreen, (96, 144, 96), vRect)

        vGrid = vTemp
        pygame.display.flip()
        time.sleep(0.5)

    pygame.quit()

## fGameOfLife
