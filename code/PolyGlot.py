import sys as mSys

vArgV = mSys.argv

vTestTab = {}
def fHello():
    print("HelloWorld")
vTestTab["Hello"] = fHello

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
