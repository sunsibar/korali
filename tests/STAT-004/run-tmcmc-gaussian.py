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
k["Problem"]["Likelihood Model"] = lgaussianCustom

# Configuring TMCMC parameters
k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 50000

# Configuring the problem's random distributions
k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -15.0
k["Distributions"][0]["Maximum"] = +15.0

# Configuring the problem's variables and their prior distributions
k["Variables"][0]["Name"] = "a"
k["Variables"][0]["Bayesian Type"] = "Computational"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

# Running Korali
k.run()
k["Random Seed"] = 5467

verifyMean(k, [-2.0], 0.05)
verifyStd(k, [3.0], 0.05)
