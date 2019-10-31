#!/usr/bin/env python3

# Importing computational model
import sys
sys.path.append('./model')
sys.path.append('./helpers')

from model import *
from helpers import *


# Starting Korali's Engine
import korali
k = korali.initialize()
k["Results Output"]["Path"] = "_result_run-mcmc"
k["Results Output"]["Frequency"] = 10000
k["Console Output"]["Frequency"] = 10000

# Selecting problem and solver types.
k["Problem"]["Type"] = "Evaluation/Direct/Basic"
k["Problem"]["Objective Function"] = lgaussian

# Defining problem's variables and their MCMC settings
k["Variables"][0]["Name"] = "X0"
k["Variables"][0]["Initial Mean"] = 0.0
k["Variables"][0]["Initial Standard Deviation"] = 1.0

# Configuring the MCMC sampler parameters
k["Solver"]["Type"]  = "Sampler/MCMC"
k["Solver"]["Burn In"] = 100
k["Solver"]["Rejection Levels"] = 3
k["Solver"]["Use Adaptive Sampling"] = True
k["Solver"]["Termination Criteria"]["Max Samples"] = 100000

# Running Korali
k["Random Seed"] = 1227
k.run()

verifyMean(k, [-2.0], 0.5)
verifyStd(k, [3.0], 0.5)
