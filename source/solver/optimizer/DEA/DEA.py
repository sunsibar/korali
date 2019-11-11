#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt

from korali.fileIO import *
from korali.plotter.helpers import hlsColors, pauseLight, drawMulticoloredLine, checkFigure
from korali.plotter.helpers import verifyGeneration, initDefaults, getStateAndGeneration, appendStates, appendStateVectors

# Plot DEA results (read from .json files)
def plot(src, plotAll=False, live=False, generation=None, test=False, plot_mean=False ):
    plt.style.use('seaborn-dark')

    verifyGeneration(generation, 3)
    
    stateNames = ['Current Best Value', 'Best Ever Value']
    vecStateNames = ['Current Best Variables', 'Current Mean', 'Max Distances']
 
    numdim, names, colors, numeval, dfval, fval, best, fvalXvec, meanXvec, width = ([] for i in range(10))

    resultfiles = getResultFiles(src, 0, generation)
    if (resultfiles == []):
     print("[Korali] Error: Did not find Korali results in the folder...".format(src))
     exit(-1)
    
    solverName, names, numdim, gen = initDefaults(src, "initial.json", (fvalXvec, meanXvec, width))
    colors = hlsColors(numdim)
    
    updateLegend = live or plotAll
    
    fig, ax = plt.subplots(2,2,num='DEA live diagnostics: {0}'.format(src),figsize=(8,8))
    if (updateLegend):
        fig.show()
   
    while True:
        for filename in resultfiles:
            path = '{0}/{1}'.format(src, filename)
 
            with open(path) as f:
                data  = json.load(f)
                state, gen = getStateAndGeneration(data)

                if updateLegend:
                    checkFigure(fig.number)
                
                if (gen > 1):
                        
                    appendStates(state, (fval, best), stateNames)
                    appendStateVectors(state, (fvalXvec, meanXvec, width), vecStateNames)
                        
                    numeval.append(data['Solver']['Internal']['Model Evaluation Count'])
                    dfval.append(abs(state['Current Best Value'] - state['Best Ever Value']))
                    
                    if (plotAll == True):
                        draw_figure(fig, ax, src, gen, numeval, numdim, fval,
                                dfval, fvalXvec, meanXvec, width, colors, names,
                                updateLegend)

        checkFigure(fig.number) 
        draw_figure(fig, ax, src, gen, numeval, numdim, fval,
                dfval, fvalXvec, meanXvec, width, colors, names,
                updateLegend)

        if (live == False):
            break

        resultfiles = getResultFiles(src, gen+1, generation, False)
        if (resultfiles == []):
         print("[Korali] Error: Did not find Korali results in the folder...".format(src))
         exit(-1)

    plt.show()
    print("[Korali] Figure closed - Bye!")


# Create Plot from Data
def draw_figure(fig, ax, src, idx, numeval, numdim, fval, dfval, fvalXvec,
        meanXvec, width, colors, names, updateLegend):

    #fig, ax = plt.subplots(2,2,num='DEA live diagnostics: {0}'.format(src),figsize=(8,8))

    plt.suptitle( 'Generation {0}'.format(str(idx).zfill(5)), fontweight='bold', fontsize=12 )

    # Upper Left Plot
    ax[0,0].grid(True)
    ax[0,0].set_yscale('log')
    drawMulticoloredLine(ax[0,0], numeval, fval, 0.0, 'r', 'b', '$| F |$')
    ax[0,0].plot(numeval, dfval, 'x', color = '#34495e', label = '$| F - F_{best} |$')
    if ( (idx == 2) or (updateLegend == False) ):
        ax[0,0].legend(bbox_to_anchor=(0,1.00,1,0.2), loc="lower left", mode="expand", ncol = 3, handlelength=1, fontsize = 8)

    # Upper Right Plot
    ax[0,1].set_title('Objective Variables')
    ax[0,1].grid(True)
    for i in range(numdim):
        ax[0,1].plot(numeval, fvalXvec[i], color = colors[i], label=names[i])
    if ( (idx == 2) or (updateLegend == False) ):
        ax[0,1].legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, handlelength=1)

    # Lower Right Plot
    ax[1,0].set_title('Width Population')
    ax[1,0].grid(True)
    for i in range(numdim):
        ax[1,0].plot(numeval, width[i], color = colors[i])

    # Lower Left Plot
    ax[1,1].set_title('Mean Population')
    ax[1,1].grid(True)
    for i in range(numdim):
        ax[1,1].plot(numeval, meanXvec[i], color = colors[i], label=names[i])
    if ( (idx == 2) or (updateLegend == False) ):
        ax[1,1].legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, handlelength=1)

    pauseLight(0.05)

