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
k = korali.Engine()
e = korali.Experiment()

e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
e["Problem"]["Likelihood Model"] = calculateLogLikelihood

e["Solver"]["Type"]  = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 5000
e["Solver"]["Termination Criteria"]["Max Generations"] = 2

e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = -10.0
e["Distributions"][0]["Maximum"] = +10.0

e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Prior Distribution"] = "Uniform 0"

print("\n-------------------------------------------------------------")
print("Running first 2 generations...")
print("-------------------------------------------------------------\n")

k.run(e)

print("\n-------------------------------------------------------------")
print("Running last 2 generations...")
print("-------------------------------------------------------------\n")

e["Solver"]["Termination Criteria"]["Max Generations"] = 4
k.run(e)

