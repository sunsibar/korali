import os
import json
import colorsys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


# For simple exit after keyboard interrupt
def sig(a, b):
    print("[Korali] Keyboard Interrupt - Bye!")
    exit(0)


# Initialize list of lists and return solver & variable names, dimension, and
# generation
def initDefaults(directory, filename, lists):
    path   = '{0}/{1}'.format(directory, filename)
    with open(path) as f:
        data = json.load(f)
 
        solver = data['Solver']['Type']
        gen    = data['General']['Current Generation']
        numdim = len(data['Variables'])
        names  = [ data['Variables'][i]['Name'] for i in range(numdim) ]

        for li in lists:
            for i in range(numdim):
                li.append([])

    return (solver, names, numdim, gen)


# Extract state from data and return current ceneration
def getStateAndGeneration(data): 
    state = data['Solver']['Internal']
    gen   = data['General']['Current Generation']
    return (state, gen)


# Append data to lists read from states (stateNames)
def appendStates(state, lists, stateNames):
    for i, name in enumerate(stateNames):
        lists[i].append(state[name])


# Append data (list) to lists read from states (stateNames)
def appendStateVectors(state, lists, stateNames):
    for i, name in enumerate(stateNames):
        for dim, data in enumerate(state[name]):
            lists[i][dim].append(data)


# Verify if figure exists and exit if not
def checkFigure(num):
    if ( plt.fignum_exists(num) == False ):
        print("[Korali] Figure closed - Bye!")
        exit(0)
     

# Read result files
def readFiles(src, start=None, end=None, noisy=True):
    resultfilesTmp = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
    resultfilesTmp = sorted(resultfilesTmp)
    if ('final.json' in resultfilesTmp): resultfilesTmp.remove('final.json')

    if (resultfilesTmp == []):
        print("[Korali] Error: Did not find file {0} in the result folder...".format(src))
        exit(-1)

    runId       = -1 # Init Run Id
    resultfiles = [] # Init Return Value

    for filename in resultfilesTmp:
        path   = '{0}/{1}'.format(src, filename)
        
        with open(path) as f:
            data = json.load(f)
            gen  = data['General']['Current Generation']
            if (runId == -1):
                runId  = data['General']['Run ID']
            
            if verifyFile(data, path, runId, start, end, noisy):
                resultfiles.append(filename)
    
    return resultfiles


# Open file and verify runId and current generation in [start, end]
def verifyFile(data, path, runId, start=None, end=None, noisy=True): 
    currentGeneration = data['General']['Current Generation']

    if ( (start is not None) and (currentGeneration < start)):
        return False

    if ( (end is not None) and (currentGeneration > end)):
        return False

    if (data['General']['Run ID'] != runId):
       
        if(noisy == True):
            print("[Korali] Warning: Skipping file {0}, results origin from a "\
                " different experiment (different runid)".format(path))
        return False

 
    return True


# Get a list of evenly spaced colors in HLS huse space.
def hlsColors(num, h = 0.01, l=0.6, s=0.65):
    hues = np.linspace(0, 1, num + 1)[:-1]
    hues += h
    hues %= 1
    hues -= hues.astype(int)
    palette = [ list(colorsys.hls_to_rgb(h_i, l, s)) for h_i in hues ]
    return palette


# Plot pause without focus
def pauseLight(interval):
    backend = plt.rcParams['backend']
    if backend in matplotlib.rcsetup.interactive_bk:
        figManager = matplotlib._pylab_helpers.Gcf.get_active()
        if figManager is not None:
            canvas = figManager.canvas
            if canvas.figure.stale:
                canvas.draw()
            canvas.start_event_loop(interval)
            return


# Finds the continuous segments of colors and returns those segment
def findContiguousColors(y, threshold, clow, chigh):
    colors = []
    for val in y:
        if (val < 0): colors.append(clow) 
        else:         colors.append(chigh)
    segs = []
    curr_seg = []
    prev_color = ''
    for c in colors:
        if c == prev_color or prev_color == '':
            curr_seg.append(c)
        else:
            segs.append(curr_seg)
            curr_seg = []
            curr_seg.append(c)
            curr_seg.append(c)
        prev_color = c
    segs.append(curr_seg)
    return segs


# Plots abs(y-threshold) in two colors
#   clow for y < threshold and chigh else
def drawMulticoloredLine(ax,x,y,threshold,clow,chigh,lab):
    segments = findContiguousColors(y, threshold, clow, chigh)
    start = 0
    absy = [ abs(val) for val in y ]
    labelled = set()
    for seg in segments:
        end = start + len(seg)
        if seg[0] in labelled:
            l, = ax.plot( x[start:end], absy[start:end], c=seg[0] ) 
        else:
            l, = ax.plot( x[start:end], absy[start:end], c=seg[0], label=lab ) 
            labelled.add(seg[0])
        start = end - 1