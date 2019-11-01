#!/usr/bin/env python3

# Importing computational model
import sys
sys.path.append('./model')
sys.path.append('./helpers')

from model import *
from helpers import *

lg5 = lambda x : lgaussianxd( x, 5 )

# Starting Korali's Engine
import korali
k = korali.initialize()
k["Results Output"]["Path"] = "_result_run-mcmc"

# Selecting problem and solver types.
k["Problem"]["Type"] = "Evaluation/Direct/Basic"
k["Problem"]["Objective Function"] = lg5

# Defining problem's variables and their MCMC settings
for i in range(5):
  k["Variables"][i]["Name"] = "X" + str(i)
  k["Variables"][i]["Initial Mean"] = -1.0
  k["Variables"][i]["Initial Standard Deviation"] = 1.0

# Configuring the MCMC sampler parameters
k["Solver"]["Type"]  = "Sampler/MCMC"
k["Solver"]["Burn In"] = 500
k["Solver"]["Use Adaptive Sampling"] = False

k["Solver"]["Termination Criteria"]["Max Samples"] = 50000

# Running Korali
k["Random Seed"] = 1337
k.run()

verifyMean(k, [0.0, 0.0, 0.0, 0.0, 0.0], 0.05)
verifyStd(k, [1.0, 1.0, 1.0, 1.0, 1.0], 0.05)
