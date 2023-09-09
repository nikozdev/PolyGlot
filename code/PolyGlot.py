# standard

import sys as mSys
import time as mTime

import math as mMath
import random as mRand

import typing as mType

# external

import tqdm as mTqdm

import matplotlib as mMpl
import matplotlib.pyplot as mMpl_Pyplot

import numpy as mNumpy
import numpy.typing as mNumpyType

import pygame as mPygame

# contents

## typedef

class tAnnLayer():

    #actions

    def fAhead(self, vIput: mNumpyType.NDArray[mNumpy.float64]):

        raise NotImplementedError()

    def fAback(self, vOput: mNumpyType.NDArray[mNumpy.float64]):

        raise NotImplementedError()

### tAnnLayer

class tAnnLayerDense(tAnnLayer):

    #codetor

    def __init__(self, vIdim: int, vOdim: int, vRate: float = 0.1):

        self.vIput = mNumpy.random.randn(vIdim, 1)
        self.vEdge = mNumpy.random.randn(vOdim, vIdim)
        self.vBias = mNumpy.random.randn(vOdim, 1)
        self.vRate = vRate

    #actions

    def fAhead(self, vIput: mNumpyType.NDArray[mNumpy.float64]):

        self.vIput = vIput
        
        return mNumpy.dot(self.vEdge, self.vIput) + self.vBias

    def fAback(self, vOput: mNumpyType.NDArray[mNumpy.float64]):

        vEdif = mNumpy.dot(vOput, self.vIput.T)
        vOdif = mNumpy.dot(self.vEdge.T, vOput) 

        self.vEdge -= self.vRate * vEdif
        self.vBias -= self.vRate * vOput

        return vOdif

    #datadef

    vIput: mNumpyType.NDArray[mNumpy.float64]
    vEdge: mNumpyType.NDArray#TODO:matrixtype
    vBias: mNumpyType.NDArray[mNumpy.float64]
    vRate: float # backward propagation scale

### tAnnLayerDense

class tAnnLayerActiv(tAnnLayer):

    #codetor

    def __init__(self, vIdim: int,
        fActiv: mType.Callable[[mNumpyType.NDArray], mNumpyType.NDArray],
        fDeriv: mType.Callable[[mNumpyType.NDArray], mNumpyType.NDArray]):

        self.fActiv = fActiv
        self.fDeriv = fDeriv

        self.vIput = mNumpy.array([0.0] * vIdim)

    #actions

    def fAhead(self, vIput: mNumpyType.NDArray[mNumpy.float64]):

        self.vIput = vIput

        return self.fActiv(vIput)

    def fAback(self, vOput: mNumpyType.NDArray[mNumpy.float64]):

        return mNumpy.multiply(vOput, self.fDeriv(self.vIput))

    #datadef

    vIput: mNumpyType.NDArray[mNumpy.float64]

### tAnnLayerActiv

class tAnnLayerActivTanh(tAnnLayerActiv):

    #codetor

    def __init__(self, vIdim: int):

        def fActiv(vIput: mNumpyType.NDArray):

            return mNumpy.tanh(vIput)

        def fDeriv(vOput: mNumpyType.NDArray):

            return 1.0 - mNumpy.power(mNumpy.tanh(vOput), 2.0)

        super(tAnnLayerActivTanh, self).__init__(vIdim, fActiv, fDeriv)

### tAnnLayerActivTanh

class tAnnLayerActivLine(tAnnLayerActiv):

    #codetor

    def __init__(self, vIdim: int):

        def fActiv(vIput: mNumpyType.NDArray):

            return vIput

        def fDeriv(vOput: mNumpyType.NDArray):

            return mNumpy.array([[]])

        super(tAnnLayerActivLine, self).__init__(vIdim, fActiv, fDeriv)

### tAnnLayerActivLine

class tAnnGraph():

    #codetor

    def __init__(self, vList: list[tAnnLayer]):

        self.vList = vList

    #getters

    def fGetCost(self, vOput: mNumpyType.NDArray, vNeed: mNumpyType.NDArray):
        return mNumpy.mean(mNumpy.power(vOput - vNeed, 2.0))

    def fGetCostPrime(self, vOput: mNumpyType.NDArray, vNeed: mNumpyType.NDArray):
        return (2.0 * (vOput - vNeed)) / mNumpy.size(vNeed)

    #actions

    def fAhead(self, vIput: mNumpyType.NDArray):

        for vIter in range(0, len(self.vList), +1):
            vIput = self.vList[vIter].fAhead(vIput)

        return vIput

    def fAback(self, vOput: mNumpyType.NDArray):

        for vIter in reversed(range(0, len(self.vList), +1)):
            vOput = self.vList[vIter].fAback(vOput)

        return vOput

    def fSolve(self, vIput: mNumpyType.NDArray):

        return self.fAhead(vIput)

    def fLearn(self, vIput: mNumpyType.NDArray, vNeed: mNumpyType.NDArray):

        vOput = self.fSolve(vIput)
        self.fAback(self.fGetCostPrime(vOput, vNeed))

        return self.fGetCost(vOput, vNeed)

    #datadef

    vList: list[tAnnLayer]

### tAnnGraph

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

def fAnnXorSolver():

    #actions

    vGraph = tAnnGraph([
        tAnnLayerDense(2, 3),
        tAnnLayerActivTanh(3),
        #tAnnLayerActivLine(3),
        tAnnLayerDense(3, 1),
        tAnnLayerActivTanh(1),
        #tAnnLayerActivLine(1),
    ])

    vImat = mNumpy.reshape([[0, 0], [0, 1], [1, 0], [1, 1]], (4, 2, 1))
    vOmat = mNumpy.reshape([[0], [1], [1], [0]], (4, 1, 1))
    vLearnCount: int = 0x1000
    for vIter in range(vLearnCount):

        vCost = mNumpy.array([[0.0]])
        for vIput, vNeed in zip(vImat, vOmat):
            vCost += vGraph.fLearn(vIput, vNeed)

        print(f'{vIter}/{vLearnCount}={vCost[0][0]:+0.2f}')

    for vIput, vNeed in zip(vImat, vOmat):
        vOput = vGraph.fSolve(vIput)
        print(f'{vIput}\n{vNeed}\noput={vOput[0][0]:+0.2f}')

vTestTab["AnnXorSolver"] = fAnnXorSolver

def fTest(vPathArr: list[str], vPathKey: int = 0, vTestRef = vTestTab):

    if vTestRef:

        if vPathKey == len(vPathArr):

            if isinstance(vTestRef, mType.Callable):
                vTestRef()
            else:
                print(f'not an executable test by path {vPathArr}')

        elif vPathArr[vPathKey] in vTestTab:
            fTest(vPathArr, vPathKey + 1, vTestTab[vPathArr[vPathKey]])
        else:
            print(f'failed to find test by path {vPathArr} with key {vPathKey}')

    else:
        print(f'failed to find test by path {vPathArr} with key {vPathKey}')

### fTest

# finalize

if __name__ == "__main__":
    if (len(vArgV) > 1):
        fTest(vArgV[1:], 0, vTestTab)
    else:
        print(f'command line arguments are expected - the path to a test function')
