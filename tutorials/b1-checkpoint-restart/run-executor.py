#!/usr/bin/env python3
import os
import sys
sys.path.append('./model/')
from model import *

import numpy as np
import korali

resultDir = '_result_run-executor'

Ns        = 100
means     = [-5, 5, 10, 15, 20]
variances = [1, 1, 1, 1, 1]

fileName = '_executor_output/samplesOut.dat'

prepareFile( fileName )

k = korali.initialize()

k["Problem"]["Type"] = "Execution/Model"
k["Problem"]["Execution Model"] = lambda modelData: put_normal_rnds(modelData, Ns, fileName)

k["Variables"][0]["Name"] = "Mean"
k["Variables"][0]["Loaded Values"] = means

k["Variables"][1]["Name"] = "Variance"
k["Variables"][1]["Loaded Values"] = variances

k["Solver"]["Type"] = "Executor"
k["Solver"]["Executions Per Generation"] = 1
k["Solver"]["Termination Criteria"]["Max Model Evaluations"] = 2

k["Console Output"]["Verbosity"] = "Detailed"
k["Results Output"]["Path"] = resultDir

k.run()

print("\n-------------------------------------------------------------")
print("Now loading results from Gen 2 and running remaining samples.")
print("-------------------------------------------------------------\n")

resultFile = korali.getLatestResult(resultDir)
k.loadState(resultFile)
k.run()

