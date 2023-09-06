# standard

import sys as mSys
import time as mTime
import math as mMath

# external

import tqdm as mTqdm

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
        mTime.sleep(abs(mMath.sqrt(vIter) - vRangeHalf) * 0.00025)
vTestTab["Tqdm"] = fTqdm

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
