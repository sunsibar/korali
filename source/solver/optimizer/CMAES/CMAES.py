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
    vecStateNames = ['Current Best Variables', 'Current Mean', 'Axis Lengths']

    names, colors, numeval, sigma, cond, psL2, dfval, fval, best, fvalXvec, mu, axis, ssdev = ([] for i in range(13))
 
    resultfiles = getResultFiles(src, 0, generation)
    if (resultfiles == []):
      print("[Korali] Error: Did not find Korali results in the folder...".format(src))
      exit(-1)

    solverName, names, numdim, gen = initDefaults(src, "initial.json", (fvalXvec, mu, axis, ssdev))
    colors = hlsColors(numdim)

    updateLegend = live or plotAll
    
    fig, ax = plt.subplots(2,2,num='{0} live diagnostics'.format(solverName), figsize=(8,8))
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
                    appendStateVectors(state, (fvalXvec, mu, axis), vecStateNames)

                    numeval.append(data['Solver']['Internal']['Model Evaluation Count'])
                    cond.append(state['Maximum Covariance Eigenvalue']/state['Minimum Covariance Eigenvalue'])
                    dfval.append(abs(state['Current Best Value'] - state['Best Ever Value']))

                    for i in range(numdim):
                       ssdev[i].append(sigma[-1]*np.sqrt(state['Covariance Matrix'][i*numdim+i]))
                
                    if (plotAll == True):
                        draw_figure(fig, ax, src, gen, numeval, numdim, fval, 
                                dfval, cond, sigma, psL2, fvalXvec, mu, axis,
                                ssdev, colors, names, plot_mean, updateLegend)
     
        checkFigure(fig.number)
        draw_figure(fig, ax, src, gen, numeval, numdim, fval, dfval, cond,
                sigma, psL2, fvalXvec, mu, axis, ssdev, colors, names,
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
def draw_figure(fig, ax, src, idx, numeval, numdim, fval, dfval, cond, sigma,
        psL2, fvalXvec, mu, axis, ssdev, colors, names, plot_mean, updateLegend):

    plt.suptitle( 'Generation {0}'.format(str(idx).zfill(5)),\
                      fontweight='bold',\
                      fontsize=12 )

    # Upper Left Plot
    ax[0,0].grid(True)
    ax[0,0].set_yscale('log')
    drawMulticoloredLine(ax[0,0], numeval, fval, 0.0, 'r', 'b', '$| F |$')
    ax[0,0].plot(numeval, dfval, 'x', color = '#34495e', label = '$| F - F_{best} |$')
    ax[0,0].plot(numeval, cond, color='#98D8D8', label = '$\kappa(\mathbf{C})$')
    ax[0,0].plot(numeval, sigma, color='#F8D030', label = '$\sigma$')
    ax[0,0].plot(numeval, psL2,  color='k', label = '$|| \mathbf{p}_{\sigma} ||$')
    if ( (idx == 2) or (updateLegend == False) ):
        ax[0,0].legend(bbox_to_anchor=(0,1.00,1,0.2), loc="lower left", mode="expand", ncol = 3, handlelength=1, fontsize = 8)

    # Upper Right Plot
    objVec = []
    if (plot_mean):
        ax[0,1].set_title('Mean of Objective Variables')
        objVec = mu
    else:
        ax[0,1].set_title('Objective Variables')
        objVec = fvalXvec

    ax[0,1].grid(True)
    for i in range(numdim):
        ax[0,1].plot(numeval, objVec[i], color = colors[i], label=names[i])
    if ( (idx == 2) or (updateLegend == False) ):
        ax[0,1].legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, handlelength=1)

    # Lower Right Plot
    ax[1,0].set_title('Square Root of Eigenvalues of $\mathbf{C}$')
    ax[1,0].grid(True)
    ax[1,0].set_yscale('log')
    for i in range(numdim):
        ax[1,0].plot(numeval, axis[i], color = colors[i])

    # Lower Left Plot
    ax[1,1].set_title('$\sigma \sqrt{diag(\mathbf{C})}$')
    ax[1,1].grid(True)
    ax[1,1].set_yscale('log')
    for i in range(numdim):
        ax[1,1].plot(numeval, ssdev[i], color = colors[i], label=names[i])
        
    pauseLight(0.05)
