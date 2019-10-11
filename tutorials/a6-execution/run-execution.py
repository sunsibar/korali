#!/usr/bin/env python3
import os
import sys
sys.path.append('./model/')
from work import *

import numpy as np
import korali

# Ns: number of samples to draw per variable
Ns = 100

# fileName: output directory
fileName = 'samplesOut.dat'

# Prepare file
prepareOutputDir()

# Variables
means = [-5, 5]
variances = [1, 3]

k = korali.initialize()

k["Problem"]["Type"] = "Execution"
k["Problem"]["Execution Model"] = lambda modelData: put_normal_rnds(modelData, Ns, fileName)

k["Variables"][0]["Name"] = "Mean"
k["Variables"][0]["Loaded Values"] = means

k["Variables"][1]["Name"] = "Variance"
k["Variables"][1]["Loaded Values"] = variances

k["Solver"]["Type"] = "Executor"
k["Solver"]["Executions Per Generation"] = 1

k["Console Output"]["Verbosity"] = "Detailed"

k.run()
