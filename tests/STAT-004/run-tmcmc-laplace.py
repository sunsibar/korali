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
k["Results Output"]["Path"] = "_result_run-tmcmc"

# Setting up custom likelihood for the Bayesian Problem
k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
k["Problem"]["Likelihood Model"] = llaplaceCustom

# Configuring TMCMC parameters
k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 5000

# Configuring the problem's random distributions
k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -10.0
k["Distributions"][0]["Maximum"] = +10.0

k["Distributions"][1]["Name"] = "Uniform 1"
k["Distributions"][1]["Type"] = "Univariate/Uniform"
k["Distributions"][1]["Minimum"] = -10.0
k["Distributions"][1]["Maximum"] = +10.0

# Configuring the problem's variables and their prior distributions
k["Variables"][0]["Name"] = "a"
k["Variables"][0]["Bayesian Type"] = "Computational"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

k["Variables"][1]["Name"] = "b"
k["Variables"][1]["Bayesian Type"] = "Computational"
k["Variables"][1]["Prior Distribution"] = "Uniform 1"

# Running Korali
k["Random Seed"] = 1337
k.run()

#verifyMean(k, 4.0)
#verifyStd(k, 1.0)

