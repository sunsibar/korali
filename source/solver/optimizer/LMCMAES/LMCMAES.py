#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt

from korali.fileIO import *
from korali.plotter.helpers import hlsColors, pauseLight, drawMulticoloredLine, checkFigure
from korali.plotter.helpers import verifyGeneration, initDefaults, getStateAndGeneration, appendStates, appendStateVectors

# Plot CMAES results (read from .json files)
def plot(src, plotAll=False, live=False, generation=None, test=False, plot_mean=False ):
    plt.style.use('seaborn-dark')
 
    verifyGeneration(generation, 3)
    
    stateNames = ['Current Best Value', 'Best Ever Value', 'Sigma', 'Conjugate Evolution Path L2 Norm']
    vecStateNames = ['Current Best Variables', 'Current Mean', 'Evolution Path Weights']

    names, colors, numeval, sigma, psL2, dfval, fval, best, fvalXvec, mu, evoweights = ([] for i in range(11))
 
    resultfiles = getResultFiles(src, 0, generation)
    if (resultfiles == []):
      print("[Korali] Error: Did not find Korali results in the folder...".format(src))
      exit(-1)

    solverName, names, numdim, gen = initDefaults(src, "initial.json", (fvalXvec, mu, evoweights))
    colors = hlsColors(numdim)

    updateLegend = live or plotAll
    
    fig, ax = plt.subplots(3,1,num='{0} live diagnostics'.format(solverName), figsize=(8,8))
    if (updateLegend):
        fig.show()

    while True:
        for filename in resultfiles:
            path = '{0}/{1}'.format(src, filename)
            
            with open(path) as f:
                data = json.load(f)
                state, gen = getStateAndGeneration(data)
      
                if updateLegend:
                    checkFigure(fig.number)
       
                if gen > 1:
    
                    appendStates(state, (fval, best, sigma, psL2), stateNames)
                    appendStateVectors(state, (fvalXvec, mu, evoweights), vecStateNames)

                    numeval.append(data['Solver']['Internal']['Model Evaluation Count'])
                    dfval.append(abs(state['Current Best Value'] - state['Best Ever Value']))

                    if (plotAll == True):
                        draw_figure(fig, ax, src, gen, numeval, numdim, fval, 
                                dfval, sigma, psL2, fvalXvec, mu, evoweights,
                                colors, names, plot_mean, updateLegend)
     
        checkFigure(fig.number)
        draw_figure(fig, ax, src, gen, numeval, numdim, fval, dfval,
                sigma, psL2, fvalXvec, mu, evoweights, colors, names,
                plot_mean, updateLegend)
            
        if live == False:
            break

        resultfiles = getResultFiles(src, gen+1, generation, False)
        if (resultfiles == []):
         print("[Korali] Error: Did not find Korali results in the folder...".format(src))
         exit(-1)
     
    plt.show()
    print("[Korali] Figure closed - Bye!")


# Create Plot from Data
def draw_figure(fig, ax, src, idx, numeval, numdim, fval, dfval, sigma,
        psL2, fvalXvec, mu, evoweights, colors, names, plot_mean, updateLegend):

    plt.suptitle( 'Generation {0}'.format(str(idx).zfill(5)),\
                      fontweight='bold',\
                      fontsize=12 )

    # Left Plot
    ax[0].grid(True)
    ax[0].set_yscale('log')
    drawMulticoloredLine(ax[0], numeval, fval, 0.0, 'r', 'b', '$| F |$')
    ax[0].plot(numeval, dfval, 'x', color = '#34495e', label = '$| F - F_{best} |$')
    ax[0].plot(numeval, sigma, color='#F8D030', label = '$\sigma$')
    ax[0].plot(numeval, psL2,  color='k', label = '$|| \mathbf{p}_{\sigma} ||$')
    if ( (idx == 2) or (updateLegend == False) ):
        ax[0].legend(bbox_to_anchor=(0,1.00,1,0.2), loc="lower left", mode="expand", ncol = 3, handlelength=1, fontsize = 8)

    # Mid Plot
    ax[1].set_title('Evolution Path Weights')
    ax[1].grid(True)
    ax[1].set_yscale('log')
    evonames = [ "T"+str(i) for i in range(len(evoweights)) ]
    for i in range(len(evoweights)):
        if len(evoweights[i]) > 0: # ugly hack
            ax[1].plot(numeval, evoweights[i], color = colors[i], label=evonames[i])
    if ( (idx == 2) or (updateLegend == False) ):
        ax[1].legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, handlelength=1)

    # Right Plot
    objVec = []
    if (plot_mean):
        ax[2].set_title('Mean of Objective Variables')
        objVec = mu
    else:
        ax[2].set_title('Objective Variables')
        objVec = fvalXvec

    ax[2].grid(True)
    for i in range(numdim):
        ax[2].plot(numeval, objVec[i], color = colors[i], label=names[i])
    if ( (idx == 2) or (updateLegend == False) ):
        ax[2].legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, handlelength=1)

    pauseLight(0.05)
