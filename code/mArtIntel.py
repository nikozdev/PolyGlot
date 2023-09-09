# imports

## standard

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

    def __init__(self, vIdim: int, vOdim: int, vRate: float = 0.1):

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

            return numpy.tanh(vIput)

        def fDeriv(vOput: numpy.typing.NDArray):

            return 1.0 - numpy.power(numpy.tanh(vOput), 2.0)

        super(tLayerActivTanh, self).__init__(vIdim, fActiv, fDeriv)

## tLayerActivTanh

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
        return numpy.mean(numpy.power(vOput - vNeed, 2.0))

    def fGetCostPrime(self, vOput: numpy.typing.NDArray, vNeed: numpy.typing.NDArray):
        return (2.0 * (vOput - vNeed)) / numpy.size(vNeed)

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

    vGraph = tGraph([
        tLayerDense(2, 3),
        tLayerActivTanh(3),
        tLayerDense(3, 1),
        tLayerActivTanh(1),
    ])

    vImat = numpy.reshape([[0, 0], [0, 1], [1, 0], [1, 1]], (4, 2, 1))
    vOmat = numpy.reshape([[0], [1], [1], [0]], (4, 1, 1))
    vLearnCount: int = 0x1000
    for vIter in range(vLearnCount):

        vCost = numpy.array([[0.0]])
        for vIput, vNeed in zip(vImat, vOmat):
            vCost += vGraph.fLearn(vIput, vNeed)

        print(f'{vIter}/{vLearnCount}={vCost[0][0]:+0.2f}')

    for vIput, vNeed in zip(vImat, vOmat):
        vOput = vGraph.fSolve(vIput)
        print(f'{vIput}\n{vNeed}\noput={vOput[0][0]:+0.2f}')

## fXorSolver
