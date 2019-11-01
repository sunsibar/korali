#!/usr/bin/env python3

# In this example, we demonstrate how a Korali experiment can
# be resumed from any point (generation). This is a useful feature
# for continuing jobs after an error, or to fragment big jobs into
# smaller ones that can better fit a supercomputer queue.
#
# First, we run a simple Korali experiment.

import sys
sys.path.append('./model')
from model import *

import korali
k = korali.initialize()

resultDir = '_result_run-mcmc'

k["Problem"]["Type"] = "Evaluation/Direct/Basic"
k["Problem"]["Objective Function"] = model

k["Solver"]["Type"]  = "Sampler/MCMC"
k["Solver"]["Burn In"] = 500
k["Solver"]["Termination Criteria"]["Max Samples"] = 1000

k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Initial Mean"] = 0.0
k["Variables"][0]["Initial Standard Deviation"] = 1.0

k["Console Output"]["Frequency"] = 1000
k["Results Output"]["Frequency"] = 1000
k["Results Output"]["Path"] = resultDir

k.run()

print("\n-------------------------------------------------------------")
print("Now continuing from Sample #1000 until Sample #5000...")
print("-------------------------------------------------------------\n")

resultFile = korali.getLatestResult(resultDir)
k.loadState(resultFile)
k["Solver"]["Termination Criteria"]["Max Samples"] = 5000
k.run()
