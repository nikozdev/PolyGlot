# standard

import sys as mSys
import time as mTime

import math as mMath
import random as mRand

# external

import tqdm as mTqdm

import matplotlib as mMpl
import matplotlib.pyplot as mMplPlot

import numpy as mNumpy

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

def fMplPlotLinear():
    vFigure = mMplPlot.figure()
    vX = [ 0, 1, 2, 3, 4 ]
    vY = vX[::]
    mRand.shuffle(vY)
    print(f"vX={vX}\nvY={vY}")
    vSuplot = vFigure.add_subplot()
    vSuplot.plot(vX, vY)
    mMplPlot.show()
vTestTab["MplPlotLinear"] = fMplPlotLinear

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
