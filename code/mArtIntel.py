# imports

## standard

import os
import os.path

import typing

## external

import numpy
import numpy.typing

# typedef

class tLayer():

    # actions

    def fAhead(self, vIput: numpy.typing.NDArray[numpy.float64]):

        raise NotImplementedError()

    def fAback(self, vOput: numpy.typing.NDArray[numpy.float64]):

        raise NotImplementedError()

## tLayer

class tLayerDense(tLayer):

    # codetor

    def __init__(self, vIdim: int, vOdim: int, vRate: float = 0.01):

        self.vIput = numpy.random.randn(vIdim, 1)
        self.vEdge = numpy.random.randn(vOdim, vIdim)
        self.vBias = numpy.random.randn(vOdim, 1)
        self.vRate = vRate

    # actions

    def fAhead(self, vIput: numpy.typing.NDArray[numpy.float64]):

        self.vIput = vIput
        
        return numpy.dot(self.vEdge, self.vIput) + self.vBias

    def fAback(self, vOput: numpy.typing.NDArray[numpy.float64]):

        vEdif = numpy.dot(vOput, self.vIput.T)
        vOdif = numpy.dot(self.vEdge.T, vOput) 

        self.vEdge -= self.vRate * vEdif
        self.vBias -= self.vRate * vOput

        return vOdif

    # datadef

    vIput: numpy.typing.NDArray[numpy.float64]
    vEdge: numpy.typing.NDArray#TODO:matrixtype
    vBias: numpy.typing.NDArray[numpy.float64]
    vRate: float # backward propagation scale

## tLayerDense

class tLayerActiv(tLayer):

    # codetor

    def __init__(self, vIdim: int,
        fActiv: typing.Callable[[numpy.typing.NDArray], numpy.typing.NDArray],
        fDeriv: typing.Callable[[numpy.typing.NDArray], numpy.typing.NDArray]):

        self.fActiv = fActiv
        self.fDeriv = fDeriv

        self.vIput = numpy.array([0.0] * vIdim)

    # actions

    def fAhead(self, vIput: numpy.typing.NDArray[numpy.float64]):

        self.vIput = vIput

        return self.fActiv(vIput)

    def fAback(self, vOput: numpy.typing.NDArray[numpy.float64]):

        return numpy.multiply(vOput, self.fDeriv(self.vIput))

    # datadef

    vIput: numpy.typing.NDArray[numpy.float64]

## tLayerActiv

class tLayerActivTanh(tLayerActiv):

    # codetor

    def __init__(self, vIdim: int):

        def fActiv(vIput: numpy.typing.NDArray):

            #return numpy.tanh(vIput)

            for vIter in range(vIput.size):
                vIput[vIter][0] = numpy.tanh(vIput[vIter][0])

            return vIput

        def fDeriv(vOput: numpy.typing.NDArray):

            #return 1.0 - numpy.power(numpy.tanh(vOput), 2.0)


            for vIter in range(vOput.size):
                vOput[vIter][0] = 1.0 - numpy.tanh(vOput[vIter][0]) ** 2.0

            return vOput

        super(tLayerActivTanh, self).__init__(vIdim, fActiv, fDeriv)

## tLayerActivTanh

class tLayerActivRelu(tLayerActiv):

    # codetor

    def __init__(self, vIdim: int):

        vRate: float = 0.1

        def fActiv(vIput: numpy.typing.NDArray):

            for vIter in range(vIput.size):
                if vIput[vIter][0] < 0.0:
                    vIput[vIter][0] *= vRate

            return vIput

        def fDeriv(vOput: numpy.typing.NDArray):

            for vIter in range(vOput.size):
                if vOput[vIter][0] > 0.0:
                    vOput[vIter][0] = 1.0
                else:
                    vOput[vIter][0] = vRate

            return vOput

        super(tLayerActivRelu, self).__init__(vIdim, fActiv, fDeriv)

## tLayerActivRelu

class tLayerActivLine(tLayerActiv):

    # codetor

    def __init__(self, vIdim: int):

        def fActiv(vIput: numpy.typing.NDArray):

            return vIput

        def fDeriv(vOput: numpy.typing.NDArray):

            return numpy.array([[]])

        super(tLayerActivLine, self).__init__(vIdim, fActiv, fDeriv)

## tLayerActivLine

class tGraph():

    # codetor

    def __init__(self, vList: list[tLayer]):

        self.vList = vList

    # getters

    def fGetCost(self, vOput: numpy.typing.NDArray, vNeed: numpy.typing.NDArray):
        return numpy.mean(vOput - vNeed)
        #return numpy.mean(numpy.power(vOput - vNeed, 2.0))
        #return numpy.mean(-vNeed * numpy.log(vOput) - (1 - vNeed) * numpy.log(1 - vOput))

    def fGetCostPrime(self, vOput: numpy.typing.NDArray, vNeed: numpy.typing.NDArray):
        return (vOput - vNeed) / numpy.size(vNeed)
        #return (2.0 * (vOput - vNeed)) / numpy.size(vNeed)
        #return ((1 - vNeed) / (1 - vOput) - vNeed / vOput) / numpy.size(vNeed)

    # actions

    def fAhead(self, vIput: numpy.typing.NDArray):

        for vIter in range(0, len(self.vList), +1):
            vIput = self.vList[vIter].fAhead(vIput)

        return vIput

    def fAback(self, vOput: numpy.typing.NDArray):

        for vIter in reversed(range(0, len(self.vList), +1)):
            vOput = self.vList[vIter].fAback(vOput)

        return vOput

    def fSolve(self, vIput: numpy.typing.NDArray):

        return self.fAhead(vIput)

    def fLearn(self, vIput: numpy.typing.NDArray, vNeed: numpy.typing.NDArray):

        vOput = self.fSolve(vIput)
        self.fAback(self.fGetCostPrime(vOput, vNeed))

        return self.fGetCost(vOput, vNeed)

    # datadef

    vList: list[tLayer]

## tGraph

# actions

def fXorSolver():

    #'''
    vGraph = tGraph([
        tLayerDense(2, 3, 0.1),
        tLayerActivTanh(3),
        tLayerDense(3, 1, 0.1),
        tLayerActivTanh(1),
    ])
    #'''
    '''
    vGraph = tGraph([
        tLayerActivRelu(2),
        tLayerDense(2, 3, 0.01),
        tLayerActivRelu(3),
        tLayerDense(3, 1, 0.01),
    ])
    #'''

    vImat = numpy.reshape([[0, 0], [0, 1], [1, 0], [1, 1]], (4, 2, 1))
    vOmat = numpy.reshape([[0], [1], [1], [0]], (4, 1, 1))
    vLearnCount: int = 0x400
    for vIter in range(vLearnCount):

        vCost = numpy.array([[0.0]])
        for vIput, vNeed in zip(vImat, vOmat):
            vCost += vGraph.fLearn(vIput, vNeed)

        print(f'{vIter}/{vLearnCount}={vCost[0][0]:+0.2f}')

    for vIput, vNeed in zip(vImat, vOmat):
        vOput = vGraph.fSolve(vIput)
        print(f'{vIput}\n{vNeed}\noput={vOput[0][0]:+0.2f}')

## fXorSolver

def fDigitReaderFromFile():

    vRootPath: str = os.getcwd()
    print(f'working from {vRootPath}')
    vDataPath: str = f'{vRootPath}/data'

    print(f'reading files from {vDataPath}')

    def fReadInt(vFile) -> int:
        vInt: int = ord(vFile.read(1)) << 24
        vInt += ord(vFile.read(1)) << 16
        vInt += ord(vFile.read(1)) << 8
        vInt += ord(vFile.read(1))
        return vInt

    #'''
    # learn

    vLearnLabelName: str = 'mnist-train-labels.idx1-ubyte'
    vLearnLabelPath: str = f'{vDataPath}/{vLearnLabelName}'

    vLearnLabelFile = open(vLearnLabelPath, 'rb')
    vLearnLabelSize: int = os.path.getsize(vLearnLabelPath)
    vLearnLabelMagN: int = fReadInt(vLearnLabelFile)

    vLearnLabelDimG: int = fReadInt(vLearnLabelFile)

    vLearnLabelData: list[int] = [0] * vLearnLabelDimG
    for vLearnLabelIter in range(vLearnLabelDimG):
        vLearnLabelData[vLearnLabelIter] = ord(vLearnLabelFile.read(1))

    print(
        f'LearnLabel?\n'
        f'File: {vLearnLabelFile}; Size: {vLearnLabelSize};\n'
        f'DimG: {vLearnLabelDimG}; List: {len(vLearnLabelData)};\n'
        f'LearnLabel!\n'
    )

    vLearnImageName: str = 'mnist-train-images.idx3-ubyte'
    vLearnImagePath: str = f'{vDataPath}/{vLearnImageName}'

    vLearnImageFile = open(vLearnImagePath, 'rb')
    vLearnImageSize: int = os.path.getsize(vLearnImagePath)
    vLearnImageMagN: int = fReadInt(vLearnImageFile)

    vLearnImageDimG: int = fReadInt(vLearnImageFile)
    vLearnImageDimX: int = fReadInt(vLearnImageFile)
    vLearnImageDimY: int = fReadInt(vLearnImageFile)
    vLearnImageDimG *= vLearnImageDimX * vLearnImageDimY

    vLearnImageData: list[float] = [0.0] * vLearnImageDimG
    for vLearnImageIter in range(vLearnImageDimG):
        vLearnImageData[vLearnImageIter] = float(ord(vLearnImageFile.read(1))) / 255.0

    print(
        f'LearnImage?\n'
        f'File: {vLearnImageFile}; Size: {vLearnImageSize};\n'
        f'Dims: {vLearnImageDimX} * {vLearnImageDimY} = {vLearnImageDimG};\n'
        f'List: {len(vLearnImageData)};\n'
        f'LearnImage?\n'
    )

    # trial

    vTrialLabelName: str = 'mnist-t10k-labels.idx1-ubyte'
    vTrialLabelPath: str = f'{vDataPath}/{vTrialLabelName}'

    vTrialLabelFile = open(vTrialLabelPath, 'rb')
    vTrialLabelSize: int = os.path.getsize(vTrialLabelPath)
    vTrialLabelMagN: int = fReadInt(vTrialLabelFile)

    vTrialLabelDimG: int = fReadInt(vTrialLabelFile)

    vTrialLabelData: list[int] = [0] * vTrialLabelDimG
    for vTrialLabelIter in range(vTrialLabelDimG):
        vTrialLabelData[vTrialLabelIter] = ord(vTrialLabelFile.read(1))

    print(
        f'TrialLabel?\n'
        f'File: {vTrialLabelFile}; Size: {vTrialLabelSize};\n'
        f'DimG: {vTrialLabelDimG};\n'
        f'List: {len(vTrialLabelData)};\n'
        f'TrialLabel?\n'
    )

    vTrialImageName: str = 'mnist-t10k-images.idx3-ubyte'
    vTrialImagePath: str = f'{vDataPath}/{vTrialImageName}'

    vTrialImageFile = open(vTrialImagePath, 'rb')
    vTrialImageSize: int = os.path.getsize(vTrialImagePath)
    vTrialImageMagN: int = fReadInt(vTrialImageFile)

    vTrialImageDimG: int = fReadInt(vTrialImageFile)
    vTrialImageDimX: int = fReadInt(vTrialImageFile)
    vTrialImageDimY: int = fReadInt(vTrialImageFile)
    vTrialImageDimG *= vTrialImageDimX * vTrialImageDimY

    vTrialImageData: list[float] = [0.0] * vTrialImageDimG
    for vTrialImageIter in range(vTrialImageDimG):
        vTrialImageData[vTrialImageIter] = float(ord(vTrialImageFile.read(1))) / 255.0

    print(
        f'TrialImage?\n'
        f'File: {vTrialImageFile}; Size: {vTrialImageSize}; MagN: {vTrialImageMagN}\n'
        f'Dims: {vTrialImageDimX} * {vTrialImageDimY} = {vTrialImageDimG};\n'
        f'List: {len(vTrialImageData)}\n'
        f'TrialImage?\n'
    )

    # graph

    vDimI: int = max(vTrialImageDimX * vTrialImageDimY, vLearnImageDimX * vLearnImageDimY)
    vDimO: int = 10

    print(f'creating the graph with input dimension {vDimI}')

    vGraph = tGraph([
        tLayerDense(vDimI, 32),
        tLayerActivTanh(32),
        tLayerDense(32, 16),
        tLayerActivTanh(16),
        tLayerDense(16, vDimO),
        tLayerActivTanh(vDimO),
    ])

    # learn

    for vLearnIter in range(vLearnLabelDimG):
        vMove = vLearnIter * vDimI
        vData = numpy.reshape([vLearnImageData[vMove : vMove + vDimI : +1]], (vDimI, 1))
        vIput = numpy.reshape(vData, (vDimI, 1))
        vTrue = numpy.reshape([vLearnLabelData[vLearnIter]], (1, 1))
        vCost = vGraph.fLearn(vIput, vTrue)

        if (vLearnIter + 1) % (vLearnLabelDimG // 100) == 0:
            print(f'{vLearnIter}/{vLearnLabelDimG}={vCost:0.2f}')

    # trial

    for vTrialIter in range(vTrialLabelDimG):
        vMove = vTrialIter * vDimI
        vIput = numpy.reshape([vTrialImageData[vMove : vMove + vDimI : +1]], (vDimI, 1))
        vTrue = numpy.reshape([vTrialLabelData[vTrialIter]], (1, 1))
        vOput = vGraph.fSolve(vIput)
        if (vTrialIter + 1) % (vTrialLabelDimG // 10) == 0:
            vOkey: int = 0
            vOnum: float = -1.0
            for vIter in range(vDimO):
                if vOput[vIter][0] > vOnum:
                    vOnum = vOput[vIter][0]
                    vOkey = vIter
            print(f'{vTrialIter}/{vTrialLabelDimG}, Onum={vOnum:0.2f}, Okey={vOkey}, True={vTrue}')
    #'''

    '''
    vDimX = 28
    vDimY = 28
    vDimG = vDimX * vDimY

    vDimI = vDimG
    vDimO = 10

    vGraph = tGraph([
        tLayerDense(vDimG, 32),
        tLayerActivTanh(32),
        tLayerDense(32, 16),
        tLayerActivTanh(16),
        tLayerDense(16, vDimO),
        tLayerActivTanh(vDimO),
    ])
    '''

## fDigitReaderFromFile

def fDigitReaderFromKeras():

    import keras
    import keras.datasets
    import keras.datasets.mnist
    import keras.utils

    (vLearnIput, vLearnOput), (vTrialIput, vTrialOput) = keras.datasets.mnist.load_data()

    def fProcData(vIput, vOput, vSize: int):

        vIput = vIput.reshape(vIput.shape[0], vIput.shape[1] * vIput.shape[2], 1)
        vIput = vIput.astype("float32") / 255.0

        # encode output which is a number in range [0,9] into a vector of size 10
        # e.g. number 3 will become [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

        vOput = keras.utils.to_categorical(vOput)
        vOput = vOput.reshape(vOput.shape[0], 10, 1)

        return vIput[:vSize], vOput[:vSize]

    ## fProcData

    vLearnSize: int = vLearnIput.shape[0]
    vLearnIput, vLearnOput = fProcData(vLearnIput, vLearnOput, vLearnSize)

    print("vLearnIput.shape = ", vLearnIput.shape)
    vGraphIputSize: int = vLearnIput.shape[1] * vLearnIput.shape[2]

    print("vLearnOput.shape = ", vLearnOput.shape)
    vGraphOputSize: int = vLearnOput.shape[1]

    vLayerOputSize: int = int(numpy.sqrt(vGraphIputSize))
    #'''
    vGraph = tGraph([
        tLayerDense(vGraphIputSize, vLayerOputSize, vRate = 0.030111),
        tLayerActivTanh(vLayerOputSize),
        tLayerDense(vLayerOputSize, vGraphOputSize, vRate = 0.030111),
        tLayerActivTanh(vGraphOputSize),
    ])
    #'''
    '''
    vGraph = tGraph([
        tLayerDense(vGraphIputSize, vLayerOputSize, 0.001),
        tLayerActivRelu(vLayerOputSize),
        tLayerDense(vLayerOputSize, vGraphOputSize, 0.001),
        tLayerActivRelu(vGraphOputSize),
    ])
    #'''

    vRepsCount: int = 10
    for vIrep in range(vRepsCount):

        vCost = numpy.reshape([[0.0]], (1, 1))

        for vIter in range(vLearnSize):

            vCost += vGraph.fLearn(vLearnIput[vIter], vLearnOput[vIter])

        vCost /= len(vLearnIput)
        print(f'[{vIrep}/{vRepsCount}]={vCost}')

    vTrialSize: int = vTrialIput.shape[0]
    vTrialIput, vTrialOput = fProcData(vTrialIput, vTrialOput, vTrialSize)

    print("vTrialIput.shape = ", vTrialIput.shape)
    print("vTrialOput.shape = ", vTrialOput.shape)

    vGuessCount: int = 0
    for vIter in range(vTrialSize):

        vAnswer = numpy.argmax(vTrialOput[vIter])
        vResult = numpy.argmax(vGraph.fSolve(vTrialIput[vIter]))

        vGuessCount += int(vResult == vAnswer)

    print(f'performance = {vGuessCount}/{vTrialSize}')
    
    #import matplotlib
    #from matplotlib import pyplot

    #for vIter in range(9):
    #    pyplot.subplot(330 + 1 + vIter)
    #    pyplot.imshow(vLearnIput[vIter], cmap = pyplot.get_cmap('gray'))
    #pyplot.show()

## fDigitReaderFromKeras
