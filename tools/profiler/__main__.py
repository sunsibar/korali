#!/usr/bin/env python3

import os
import sys
import json
import signal
import os.path
from os import path
import matplotlib
from matplotlib import cm
import matplotlib.colors as colors
import argparse
import numpy as np

signal.signal(signal.SIGINT, lambda x, y: exit(0))

parser = argparse.ArgumentParser(prog='korali.plotter', description='Show profiling information of a Korali execution.')
parser.add_argument('--dir', help='Directory of result files', default='_korali_result', required = False)
parser.add_argument('--test', help='Run without graphics (for testing purpose)', action='store_true', required = False)
args = parser.parse_args()

filePath = args.dir + '/profiling.json'
if (not path.exists(filePath) ):
 print('[Korali] Error: Could not find result file "profiling.json" in folder: ' + args.dir + '.')
 exit(-1)
 
if (args.test == True):
 print('[Korali] Testing profiler plotter for file: ' + filePath + '...') 
 matplotlib.use('Agg')

from matplotlib import pyplot

with open(filePath) as f:
 jsString = f.read()
js  = json.loads(jsString)

timelines = []
labels = []
solverCount = js["Solver Count"]
elapsedTime = js["Elapsed Time"]

for x in js["Timelines"]:
  timelines.append(js["Timelines"][x])
  labels.append(x)

######################## Creating Time-based figure

fig, axs = pyplot.subplots(2, 1, sharex=True, figsize=(25, 10))
fig.subplots_adjust(hspace=0)

#### Creating Timeline Plot

# Calculating segment durations
startLists = []
durationLists = []
solverIdLists = []
for list in timelines:
 currentStartList = []
 currentDurationList = []
 currentSolverIdList = []
 for segment in list:
  currentStartList.append(segment["Start Time"])
  currentDurationList.append(segment["End Time"] - segment["Start Time"])
  currentSolverIdList.append(segment["Solver Id"])
 startLists.append(currentStartList)
 durationLists.append(currentDurationList)
 solverIdLists.append(currentSolverIdList)
  
# Setting Y-axis limits 
upperLimit = 10 + len(timelines) * 10
axs[0].set_ylim(0, upperLimit) 
  
# Setting X-axis limits 
axs[0].set_xlim(0, elapsedTime) 
  
# Setting ticks on y-axis 
yticks = [] 
for i in range(len(timelines)):
 yticks.append(10 + i*10)
 
axs[0].set_yticks([10, upperLimit-10]) 
axs[0].set_yticklabels(['0', str(len(startLists))]) 
axs[0].set_ylabel('Worker Timelines')

# Setting graph attribute 
axs[0].grid(False) 

# Creating Color list
cMap = pyplot.get_cmap('inferno')
cNorm  = colors.Normalize(vmin=0, vmax=solverCount-1)
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cMap)
colorMap = [ scalarMap.to_rgba(i) for i in range(solverCount) ]

for i in range(len(startLists)):
 colorList = [ 'tab:blue', 'blue' ]
 if (solverCount > 1): colorList = [ colorMap[solverIdLists[i][j]] for j in range(0, len(solverIdLists[i])) ]
 segList = [ (startLists[i][j], durationLists[i][j]) for j in range(0, len(startLists[i])) ]
 axs[0].broken_barh(segList, (yticks[i] - 5, 9), facecolors = tuple(colorList) )

#### Creating Efficiency Plot 
N = 1000
dt =  elapsedTime / N

xdim = []
for i in range(1, N):
 xdim.append(dt*i)

ydims = []
for i in range(len(startLists)):
 ydims.append([])
 for ct in xdim:
  busyTime = 0.0
  for j in range(len(startLists[i])):
   if (startLists[i][j] > ct):
    break;
   if (startLists[i][j] + durationLists[i][j] > ct): 
    busyTime += ct - startLists[i][j];
    break;  
   if (startLists[i][j] + durationLists[i][j] < ct): 
    busyTime += durationLists[i][j];
  efficiency = busyTime / ct;
  ydims[i].append(efficiency)

averageEfficiency = [] 
for j in range(len(xdim)): 
 totalEfficiency = 0.0
 for i in range(len(startLists)):
  totalEfficiency += ydims[i][j]
 averageEfficiency.append(totalEfficiency / len(startLists))
 
minLimit = min(ydims[-1])*0.9
maxLimit = max(ydims[-1])*1.1
if (maxLimit > 1.0): maxLimit = 1.0
if (minLimit < 0.0): minLimit = 0.0
axs[1].set_ylim(minLimit, maxLimit)
axs[1].set_xlim(0, elapsedTime)
effLabels = []
if (len(ydims) < 10):
 for y in ydims: axs[1].plot(xdim, y)
 effLabels = labels
axs[1].plot(xdim, averageEfficiency, '--')
axs[1].legend(effLabels + [ 'Average' ])
axs[1].set_ylabel('Worker Efficiency')  
 
######################## Creating Generation-based figure

if (solverCount == 1):
 maxGeneration = 0
 for segment in timelines[0]:
  if (segment["Current Generation"] > maxGeneration): maxGeneration = segment["Current Generation"]
 
 genMaxTimes = []
 genTotalTimes = []
 genAvgTimes = []
 genTimeCounts = []
 genBalanceRatios = []

 for i in range(maxGeneration):
  genMaxTimes.append(0)
  genTotalTimes.append(0)
  genTimeCounts.append(0)
  genAvgTimes.append(0)
  genBalanceRatios.append(0)
 
 for t in timelines:
  for segment in t:
   currentTime = segment["End Time"] - segment["Start Time"]
   currGen = segment["Current Generation"] - 1
   genTotalTimes[currGen] += currentTime
   if (currentTime > genMaxTimes[currGen]): genMaxTimes[currGen] = currentTime
   genTimeCounts[currGen] = genTimeCounts[currGen] + 1 

 for i in range(maxGeneration):
  genAvgTimes[i] = genTotalTimes[i] / genTimeCounts[i]
  genBalanceRatios[i] = 1 + (genMaxTimes[i] - genAvgTimes[i]) / genAvgTimes[i]

 xdim = np.arange(1, maxGeneration+1, 1.0)
 figGen, genaxs = pyplot.subplots(1, 1, figsize=(25, 5))
 genaxs.set_xticks(xdim)
 genaxs.set_ylim(0, max(genAvgTimes))
 genaxs.set_xlim(1, maxGeneration)
 genaxs.plot(xdim, genAvgTimes)
 
 genaxs.set_ylabel('Average Time Per Sample (s)')
 genaxs.set_xlabel('Generation #')  
 
 ####################### Creating Plots

pyplot.show() 