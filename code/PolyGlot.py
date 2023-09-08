# standard

import sys as mSys
import time as mTime

import math as mMath
import random as mRand

# external

import tqdm as mTqdm

import matplotlib as mMpl
import matplotlib.pyplot as mMpl_Pyplot

import numpy as mNumpy

import pygame as mPygame

# contents

## datadef

vArgV = mSys.argv

vTestTab = {}

## actions

def fHello():
    print("HelloWorld")
vTestTab["Hello"] = fHello

def fTqdm():
    vRangeFull = 100
    vRangeHalf = vRangeFull / 2
    for vIter in mTqdm.tqdm(range(vRangeFull)):
        mTime.sleep(abs(mMath.sqrt(vIter) - vRangeHalf) * 0.0001)
vTestTab["Tqdm"] = fTqdm

def fMpl_Pyplot_Linear():
    vFigure = mMpl_Pyplot.figure()
    vX = [ 0, 1, 2, 3, 4 ]
    vY = vX[::]
    mRand.shuffle(vY)
    print(f"vX={vX}\nvY={vY}")
    vSuplot = vFigure.add_subplot()
    vSuplot.plot(vX, vY)
    mMpl_Pyplot.show()
vTestTab["Mpl_Pyplot_Linear"] = fMpl_Pyplot_Linear

def fPygame_GameOfLife():
    mPygame.init()
    vSize = (64, 64)
    vScale = 8
    vNearLiveMin = 2
    vNearLiveMax = 3
    vNearMakeMin = 3
    vNearMakeMax = 3
    vScreen = mPygame.display.set_mode([vSize[0] * vScale, vSize[1] * vScale])
    vGrid = mNumpy.array([[False] * vSize[0]] * vSize[1])
    vProb = int(mMath.sqrt(min(vSize)))
    for vPosY in range(vSize[1]):
        vLine = vGrid[vPosY]
        for vPosX in range(vSize[0]):
            vLine[vPosX] = ((mRand.randint(0, vProb) % vProb) == 0)
    vWorkFlag = True
    while vWorkFlag:
        for vEvent in mPygame.event.get():
            match vEvent.type:
                case mPygame.QUIT: vWorkFlag = False
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
                    #if vNear >= vNearLiveMin:
                    #    if vNear <= vNearLiveMax:
                    #        vLine[vPosX] = True
                    vLine[vPosX] = (vNear >= vNearLiveMin) & (vNear <= vNearLiveMax)
                else:
                    #if vNear >= vNearMakeMin:
                    #    if vNear <= vNearMakeMax:
                    #        vLine[vPosX] = True
                    vLine[vPosX] = (vNear >= vNearMakeMin) & (vNear <= vNearMakeMax)
                if vLine[vPosX]:
                    vRectSize = max(vScale - 1, 1)
                    vRectPosX = vPosX * vScale
                    vRectPosY = vPosY * vScale
                    vRect = mPygame.Rect(vRectPosX, vRectPosY, vRectSize, vRectSize)
                    mPygame.draw.rect(vScreen, (96, 144, 96), vRect)
        vGrid = vTemp
        mPygame.display.flip()
        mTime.sleep(0.5)
    mPygame.quit()
vTestTab["Pygame_GameOfLife"] = fPygame_GameOfLife


# finalize

if __name__ == "__main__":
    if (vArgV[1] == "test") if (len(vArgV) > 1) else False:
        if (len(vArgV) > 2):
            vTestKey = vArgV[2]
            vTestFun = vTestTab[vArgV[2]]
            if vTestFun:
                print(f"{vTestKey}?")
                vTestFun()
                print(f"{vTestKey}!")
            else:
                print(f"failed to find test by key: {vTestKey}")
        else:
            for vTestKey, vTestFun in vTestTab.items():
                print(f"{vTestKey}?")
                vTestFun()
                print(f"{vTestKey}!")
    else:
        print(vArgV)
