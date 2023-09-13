# imports

##standard

import sys
import typing

##localmod

import mGraphics
import mGamePlay
import mArtIntel

# content

## datadef

vArgV = sys.argv

vTestTab = {
    'Hello': lambda: print("HelloWorld"),
    'Graphics': {
        'PlotLinear': mGraphics.fPlotLinear,
    },#Graphics
    'GamePlay': {
        'GameOfLife': mGamePlay.fGameOfLife,
        'SnakEat': mGamePlay.fSnakEat,
    },#GamePlay
    'ArtIntel': {
        'XorSolver': mArtIntel.fXorSolver,
        'DigitReader': mArtIntel.fDigitReaderFromKeras,
    },#ArtIntel
}

def fTest(vPathArr: list[str], vPathKey: int, vTestRef):

    if vPathKey == len(vPathArr):

        if isinstance(vTestRef, typing.Callable): vTestRef()
        else: print(f'not a callable test found by path {vPathArr}')

    else:

        vPathRef = vPathArr[vPathKey]
        fTest(vPathArr, vPathKey + 1, vTestRef[vPathRef])

### fTest

# finalize

if __name__ == "__main__":
    if (len(vArgV) > 1):
        fTest(vArgV[1:], 0, vTestTab)
    else:
        print(f'command line arguments are expected - the path to a test function')
