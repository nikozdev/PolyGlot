# imports

## standard

import time

import math
import random

## external

import pygame

import numpy
import numpy.typing

# actions

def fGameOfLife():

    pygame.init()

    vDimX: int = 64
    vDimY: int = 64
    vDimG: int = vDimX * vDimY

    vSize: int = 8

    vFaceColor = (96, 144, 96)
    vBackColor = (16, 16, 16)

    vTimeStep: float = 1.0 / 25

    vScreen = pygame.display.set_mode([vDimX * vSize, vDimY * vSize])

    vNearLiveMin: int = 2
    vNearLiveMax: int = 3
    vNearMakeMin: int = 3
    vNearMakeMax: int = 3

    vGrid: list[bool] = [False] * vDimG
    def fGetPosG(vPosX: int, vPosY: int):
        return ((vPosY % vDimY) * vDimX) + (vPosX % vDimX)
    #fGetPosG
    def fGetNear(vGrid: list[bool], vPosX: int, vPosY: int):
        vNear: int = 0
        vNear += int(vGrid[fGetPosG(vPosX - 1, vPosY - 0)])
        vNear += int(vGrid[fGetPosG(vPosX + 1, vPosY + 0)])
        vNear += int(vGrid[fGetPosG(vPosX - 0, vPosY - 1)])
        vNear += int(vGrid[fGetPosG(vPosX + 0, vPosY + 1)])
        vNear += int(vGrid[fGetPosG(vPosX - 1, vPosY - 1)])
        vNear += int(vGrid[fGetPosG(vPosX + 1, vPosY - 1)])
        vNear += int(vGrid[fGetPosG(vPosX + 1, vPosY + 1)])
        vNear += int(vGrid[fGetPosG(vPosX - 1, vPosY + 1)])
        return vNear
    # fGetNear

    vProb: int = int(math.sqrt(min(vDimX, vDimY)))
    for vPosG in range(vDimG):
        vGrid[vPosG] = ((random.randint(0, vProb)) == 0)

    vWorkFlag = True
    while vWorkFlag:

        for vEvent in pygame.event.get():
            match vEvent.type:
                case pygame.QUIT: vWorkFlag = False
                case _: ...

        vScreen.fill(vBackColor)

        vTemp: list[bool] = vGrid.copy()
        for vPosY in range(vDimY):

            vOffY: int = vPosY * vDimX
            for vPosX in range(vDimX):

                vPosG: int = vOffY + vPosX
                vNear: int = fGetNear(vGrid, vPosX, vPosY)

                if vTemp[vPosG]:
                    vTemp[vPosG] = (vNear >= vNearLiveMin) & (vNear <= vNearLiveMax)
                else:
                    vTemp[vPosG] = (vNear >= vNearMakeMin) & (vNear <= vNearMakeMax)

                if vTemp[vPosG]:

                    vRectSize = max(vSize - 1, 1) # i wanna c deez lil cells
                    vRectPosX = vPosX * vSize
                    vRectPosY = vPosY * vSize
                    vRect = pygame.Rect(vRectPosX, vRectPosY, vRectSize, vRectSize)

                    pygame.draw.rect(vScreen, vFaceColor, vRect)

        vGrid = vTemp

        pygame.display.flip()
        time.sleep(vTimeStep)

    pygame.quit()

## fGameOfLife

def fSnakEat():

    pygame.init()

    vDimX: int = 64
    vDimY: int = 64
    vSize: int = 8

    vWorkFlag: bool = True
    while vWorkFlag:
        pygame.display.flip()
        time.sleep(0.5)

    vScreen = pygame.display.set_mode([vDimX * vSize, vDimY * vSize])

    pygame.quit()

## fSnakEat
