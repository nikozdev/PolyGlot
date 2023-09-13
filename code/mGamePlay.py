# imports

## standard

import time

import math
import random

import enum
import copy

## external

import pygame

# actions

def fGameOfLife():

    # consdef

    vDimX: int = 64
    vDimY: int = 64
    vDimG: int = vDimX * vDimY

    vSize: int = 8
    vRectSize = max(vSize - 1, 1)

    vNearLiveMin: int = 2
    vNearLiveMax: int = 3
    vNearMakeMin: int = 3
    vNearMakeMax: int = 3

    vTimeStep: float = 1.0 / 25

    # getters

    def fGetPosG(vPosX: int, vPosY: int):
        return ((vPosY % vDimY) * vDimX) + (vPosX % vDimX)
    ## fGetPosG
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
    ## fGetNear

    # actions

    pygame.init()

    vGridCurr: list[bool] = [False] * vDimG
    vGridNext: list[bool] = [False] * vDimG

    vTintList: list[tuple[int, int, int]] = [
        (0x10, 0x10, 0x10),
        (0x50, 0xA0, 0x50)
    ]

    vProb: int = int(math.sqrt(min(vDimX, vDimY)))
    for vPosG in range(vDimG):
        vGridCurr[vPosG] = ((random.randint(0, vProb)) == 0)

    vScreen = pygame.display.set_mode([vDimX * vSize, vDimY * vSize])

    vWorkFlag = True
    while vWorkFlag:

        for vEvent in pygame.event.get():
            match vEvent.type:
                case pygame.QUIT: vWorkFlag = False
                case _: ...

        for vPosY in range(vDimY):

            vOffY: int = vPosY * vDimX
            for vPosX in range(vDimX):

                vPosG: int = vOffY + vPosX
                vNear: int = fGetNear(vGridCurr, vPosX, vPosY)

                if vGridNext[vPosG]:
                    vGridNext[vPosG] = (vNear >= vNearLiveMin) & (vNear <= vNearLiveMax)
                else:
                    vGridNext[vPosG] = (vNear >= vNearMakeMin) & (vNear <= vNearMakeMax)

                vRectPosX = vPosX * vSize
                vRectPosY = vPosY * vSize

                vCellRect = pygame.Rect(vRectPosX, vRectPosY, vRectSize, vRectSize)

                vDrawTint = vTintList[vGridNext[vPosG]]
                pygame.draw.rect(vScreen, vDrawTint, vCellRect)

        vGridCurr = vGridNext.copy()

        pygame.display.flip()
        time.sleep(vTimeStep)

    pygame.quit()

## fGameOfLife

def fSnakEat():

    pygame.init()

    vTimeStep: float = 1.0 / 25.0

    vDimX: int = 64
    vDimY: int = 64
    vDimG: int = vDimX * vDimY

    vSize: int = 8
    vRectSize: int = max(vSize - 1, 1)

    class tCellEnum(enum.Enum):

        eNone = 0
        eBody = 1
        eWall = 2
        eFood = 3

    ## tCellEnum

    class tCellUnit:

        def __init__(self, vEnum: tCellEnum, vTint: tuple[int, int, int]):

            self.vEnum = vEnum
            self.vTint = vTint

        vEnum: tCellEnum = tCellEnum.eNone
        vTint: tuple[int, int, int] = (0xff, 0xff, 0xff)

        vPosX: int = 0
        vPosY: int = 0
        vDirX: int = 0
        vDirY: int = 0

    ## tCellUnit

    vCellNone: tCellUnit = tCellUnit(tCellEnum.eNone, vTint = (0x10, 0x10, 0x10))
    vCellBody: tCellUnit = tCellUnit(tCellEnum.eBody, vTint = (0x50, 0xA0, 0x50))
    vCellFood: tCellUnit = tCellUnit(tCellEnum.eFood, vTint = (0xA0, 0x50, 0x50))
    vCellWall: tCellUnit = tCellUnit(tCellEnum.eWall, vTint = (0x50, 0x50, 0xA0))

    vHead: tCellUnit = tCellUnit(tCellEnum.eNone, vTint = (0x80, 0xA0, 0x80))
    vBody: list[tCellUnit] = [vHead]
    vHead.vPosX = vDimX // 2
    vHead.vPosY = vDimY // 2
    vHead.vDirX = 0
    vHead.vDirY = 1

    def fGetPosX(vPosG: int) -> int: return (vPosG % vDimX)
    def fGetPosY(vPosG: int) -> int: return (vPosG // vDimX) % vDimY
    def fGetPosG(vPosX: int, vPosY: int) -> int:
        return ((vPosY * vDimX) % vDimY) + (vPosX % vDimX)

    def fGetCell(vGrid: list[tCellUnit], vPosX: int, vPosY: int) -> tCellUnit:
        return vGrid[fGetPosG(vPosX, vPosY)]

    def fSetCell(vGrid: list[tCellUnit], vPosX: int, vPosY: int, vCopy: tCellUnit):

        vCell: tCellUnit = copy.deepcopy(vCopy)

        vCell.vPosX = vPosX
        vCell.vPosY = vPosY

        vGrid[fGetPosG(vPosX, vPosY)] = vCell

    def fSetLineHor(vGrid: list[tCellUnit], vPosY: int, vFrom: int, vInto: int, vCopy: tCellUnit):
        for vPosX in range(vFrom, vInto):
            fSetCell(vGrid, vPosX, vPosY, vCopy)
    def fSetLineVer(vGrid: list[tCellUnit], vPosX: int, vFrom: int, vInto: int, vCopy: tCellUnit):
        for vPosY in range(vFrom, vInto):
            fSetCell(vGrid, vPosX, vPosY, vCopy)

    vGridCurr: list[tCellUnit] = [copy.deepcopy(vCellNone)] * vDimG

    for vPosG in range(vDimG):
        fSetCell(vGridCurr, fGetPosX(vPosG), fGetPosY(vPosG), vCellNone)

    fSetLineHor(vGridCurr, 1, 0, vDimX - 1, vCellWall)
    fSetLineHor(vGridCurr, vDimY - 1, 0, vDimX, vCellWall)
    fSetLineVer(vGridCurr, 1, 0, vDimY - 1, vCellWall)
    fSetLineVer(vGridCurr, vDimX - 1, 0, vDimY, vCellWall)

    vGridNext: list[tCellUnit] = vGridCurr.copy()

    vScreen = pygame.display.set_mode([vDimX * vSize, vDimY * vSize])

    vWorkFlag: bool = True
    while vWorkFlag:

        for vEvent in pygame.event.get():
            match vEvent.type:
                case pygame.QUIT: vWorkFlag = False
                case _: ...

        #for vIter in range(1, len(vBody) - 1):

        #    vCellPrev: tCellUnit = vBody[vIter - 1]
        #    vCellCurr: tCellUnit = vBody[vIter]
        #    vCellNext: tCellUnit = vBody[vIter + 1]

        #    vCellNext.vDirX = vCellCurr.vDirX
        #    vCellNext.vDirY = vCellCurr.vDirY

        #    vGridNext[vCellNext.vPosY * vDimX + vCellNext.vPosX].vEnum = tCellEnum.eBody

        for vPosG in range(vDimG):

            vCell = vGridCurr[vPosG]
            vPosXCurr: int = vCell.vPosX
            vPosYCurr: int = vCell.vPosY
            vPosXNext: int = vPosXCurr + vCell.vDirX
            vPosYNext: int = vPosYCurr + vCell.vDirY

            #print(f'Enum?{vCell.vEnum}Enum!',
            #    f'PosXCurr?{vPosXCurr}PosXCurr!', f'PosYCurr?{vPosYCurr}PosYCurr!',
            #    f'PosXNext?{vPosXNext}PosXNext!', f'PosYNext?{vPosYNext}PosYNext!'
            #)

            # update

            #fSetCell(vGridNext, vCell.vPosX, vCell.vPosY, vCellNone)
            #fSetCell(vGridNext, vCell.vPosX + vCell.vDirX, vCell.vPosY + vCell.vDirY, vCell)

            # render

            vRectPosX: int = vPosXCurr * vSize
            vRectPosY: int = vPosYCurr * vSize

            vRectPosX = (vRectPosX // 2) + vSize * 2
            vRectPosY = (vRectPosY // 2) + vSize * 2

            vCellRect = pygame.Rect(vRectPosX, vRectPosY, vRectSize, vRectSize)

            pygame.draw.rect(vScreen, vCell.vTint, vCellRect)

        #vGridCurr = copy.deepcopy(vGridNext)

        pygame.display.flip()
        time.sleep(vTimeStep)

    pygame.quit()

## fSnakEat
