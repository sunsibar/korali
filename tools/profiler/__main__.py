#!/usr/bin/env python3

import os
import sys
import json
import signal
import os.path
from os import path
import matplotlib
from matplotlib import cm
import argparse

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

timeLists = []
labels = []
elapsedTime = js["Elapsed Time"]

for x in js["Timelines"]:
 if (not "Engine" in x):
  timeLists.append(js["Timelines"][x])
  labels.append(x)

#### Creating Figure

fig, axs = pyplot.subplots(3, 1, sharex=True, figsize=(25, 10))
fig.subplots_adjust(hspace=0)

#### Creating Timeline Plot

# Calculating segment durations
startLists = []
durationLists = []
for i in range(len(timeLists)):
 startLists.append([])
 durationLists.append([])
 for j in range(0, len(timeLists[i]), 2):
  startLists[i].append(timeLists[i][j])
  durationLists[i].append(timeLists[i][j+1] - timeLists[i][j])
  
# Declaring a figure "axs[0]" 
pyplot.figure(1, figsize=(25, 10))
  
# Setting Y-axis limits 
upperLimit = 10 + len(timeLists) * 10
axs[0].set_ylim(0, upperLimit) 
  
# Setting X-axis limits 
axs[0].set_xlim(0, elapsedTime) 
  
# Setting ticks on y-axis 
yticks = [] 
for i in range(len(timeLists)):
 yticks.append(10 + i*10)
 
axs[0].set_yticks([10, upperLimit-10]) 
axs[0].set_yticklabels(['0', str(len(startLists))]) 
axs[0].set_ylabel('Worker Timelines')

# Setting graph attribute 
axs[0].grid(False) 

for i in range(len(startLists)):
 segList = [ (startLists[i][j], durationLists[i][j]) for j in range(0, len(startLists[i])) ]
 axs[0].broken_barh(segList, (yticks[i] - 5, 9), facecolors = ('tab:blue', 'blue') )

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
 
#### Creating Load Imbalance Plot

loadImbalances = []
for ct in xdim:
 busyTime = 0.0
 maxThreadTime = 0.0
 for i in range(len(startLists)):
  threadTime = 0.0
  for j in range(len(startLists[i])):
   if (startLists[i][j] > ct):
    break;
   if (startLists[i][j] + durationLists[i][j] > ct): 
    threadTime += ct - startLists[i][j];
    break;  
   if (startLists[i][j] + durationLists[i][j] < ct): 
    threadTime += durationLists[i][j];
  if (threadTime > maxThreadTime): maxThreadTime = threadTime;
  busyTime += threadTime
 averageThreadTime = busyTime / len(startLists)
 loadImbalance = 0.0
 if(busyTime > 0.0): loadImbalance = ((maxThreadTime - averageThreadTime) / busyTime)*100
 loadImbalances.append(loadImbalance)

# Declaring load imbalance plot
minLimit = min(loadImbalances)*0.9
maxLimit = max(loadImbalances)*1.1
if (maxLimit > 1.0): maxLimit = 1.0
if (minLimit < 0.0): minLimit = 0.0
axs[2].set_ylim(minLimit, maxLimit)
axs[2].set_xlim(0, elapsedTime)
axs[2].plot(xdim, loadImbalances)

# Setting labels for x-axis and y-axis
axs[2].set_ylabel('Load Imbalance %')  
axs[2].set_xlabel('Time Elapsed (seconds)') 

pyplot.show() 