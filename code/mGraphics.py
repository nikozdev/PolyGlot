# imports

## standard

import random

# actions

def fPlotLinear():

    import matplotlib
    import matplotlib.pyplot

    vFigure = matplotlib.pyplot.figure()
    vSuplot = vFigure.add_subplot()

    vX = [ 0, 1, 2, 3, 4 ]
    vY = vX[::]
    random.shuffle(vY)

    vSuplot.plot(vX, vY)
    matplotlib.pyplot.show()
