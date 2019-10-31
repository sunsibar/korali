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
k["Problem"]["Likelihood Model"] = lexponentialCustom

# Configuring TMCMC parameters
k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Target Coefficient Of Variation"] = 0.2
k["Solver"]["Population Size"] = 5000

# Configuring the problem's random distributions
k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = 0.0
k["Distributions"][0]["Maximum"] = 50.0

# Configuring the problem's variables and their prior distributions
k["Variables"][0]["Name"] = "a"
k["Variables"][0]["Bayesian Type"] = "Computational"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

# Running Korali
k["Random Seed"] = 1337
k.run()

#verifyMean(k, 4.0)
#verifyStd(k, 4.0)

