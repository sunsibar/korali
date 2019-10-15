#!/usr/bin/env python3

# In this example, we demonstrate how a Korali experiment can
# be resumed from any point (generation). This is a useful feature
# for continuing jobs after an error, or to fragment big jobs into
# smaller ones that can better fit a supercomputer queue.

# First, we run a simple Korali experiment.

import sys
sys.path.append('model')
from model import *

import korali
k = korali.initialize()

resultDir = '_result_run-cmaes'

k["Problem"]["Type"] = "Evaluation/Direct/Gradient"
k["Problem"]["Objective"] = "Maximize"
k["Problem"]["Objective Function"] = model_with_gradient

k["Solver"]["Type"] = "Optimizer/Rprop"
k["Solver"]["Termination Criteria"]["Max Generations"] = 50
k["Solver"]["Termination Criteria"]['Parameter Relative Tolerance'] = 1e-8;

k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Initial Value"] = -10.

k["Console Output"]["Frequency"] = 10
k["Results Output"]["Path"] = resultDir

k.run()


print("\n-------------------------------------------------------------")
print("Now loading results from Gen 50 and running until Gen 100...")
print("-------------------------------------------------------------\n")

resultFile = korali.getLatestResult(resultDir)
k.loadState(resultFile)
k["Solver"]["Termination Criteria"]["Max Generations"] = 100
k.run()