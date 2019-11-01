#!/usr/bin/env python3

## In this example, we demonstrate how Korali finds values for the
## variables that maximize the objective function, given by a
## user-provided computational model.

# Importing computational model
import sys
sys.path.append('./model')
from model import *

# Starting Korali's Engine
import korali
k = korali.initialize()

# Configuring Problem.
k["Problem"]["Type"] = "Evaluation/Direct/Basic"
k["Problem"]["Objective"] = "Maximize"
k["Problem"]["Objective Function"] = model

# Defining the problem's variables.
k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Lower Bound"] = -10.0
k["Variables"][0]["Upper Bound"] = +10.0

# Configuring CMA-ES parameters
k["Solver"]["Type"] = "Optimizer/CMAES"
k["Solver"]["Population Size"] = 11
k["Solver"]["Termination Criteria"]["Min Value Difference Threshold"] = 1e-7
k["Solver"]["Termination Criteria"]["Max Generations"] = 100

k["Conduit"]["Type"] = "External"
k["Conduit"]["Concurrent Jobs"] = 8 

# Running Multiple Korali Instances
k.runMultiple(8)
