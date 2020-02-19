import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt

from optimizer import setupV
from optimizer import getCameraLocals
from optimizer import calcTrapezoidalFOV
from optimizer import isCellCovered
from optimizer import minimizeCamCount


def solve(params, vdata):
    print("Minimizing camera count...")
    minimizeCamCount(params, vdata)
    sys.exit()
    return



def show(params):
    #fig, ax = plt.subplots()
    #ax.set_xticks()
    #ax.set_yticks()
    #ax.fill(trapezoid[:, 0], trapezoid[:, 1], fill=False)
    #ax.set(xlabel='x direction', ylabel='y direction',
    #       title='FOV')
    #ax.grid()
    #plt.show()
    pass

if __name__=="__main__":
    vdata = None
    params = None
    try:
        f = open("data/parameters.data", "rb")
        params = pickle.load(f)
        f.close()
        print("Read parameters.data!")
    except FileNotFoundError:
        f.close()
        print("Please have some parameters to solve the dang problem with!")
        sys.exit()

    assert(params is not None)
    
    try:
        f = open("data/v.data", "rb")
        vdata = pickle.load(f)
        f.close()
        print("Read v.data!")
    except FileNotFoundError:
        f.close()
        print("Creating the binary variable v...")
        vdata = setupV(params)
        with open("data/v.data", "wb") as f:
            pickle.dump(vdata, f)
        print("Saved v.data!")


    assert(vdata is not None)
    solve(params, vdata)
    # show(params)
