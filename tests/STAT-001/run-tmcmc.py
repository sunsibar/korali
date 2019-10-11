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
k["Random Seed"] = 0xC0FFEE
k["Results Output"]["Path"] = "_result_run-tmcmc"

# Configuring problem
k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
k["Problem"]["Likelihood Model"] = model

k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -100000.0
k["Distributions"][0]["Maximum"] = +100000.0
 
k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

# Defining problem's variables and prior distribution for TMCMC
k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"
# Configuring the TMCMC sampler parameters
k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 5000
k["Solver"]["Covariance Scaling"] = 0.04

# Running Korali
k.run()

checkMean(k, 0.0, 0.05)
checkStd(k, 1.0, 0.05)
