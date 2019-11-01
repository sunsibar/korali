#!/usr/bin/env python3

# Importing computational model
import sys
sys.path.append('./model')
sys.path.append('./helpers')

from model import *
from helpers import *

lg5 = lambda x : lgaussianxdCustom( x, 5 )

# Starting Korali's Engine
import korali
k = korali.initialize()
k["Results Output"]["Path"] = "_result_run-tmcmc"

# Setting up custom likelihood for the Bayesian Problem
k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
k["Problem"]["Likelihood Model"] = lg5

# Configuring TMCMC parameters
k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 20000

k["Solver"]["Target Coefficient Of Variation"] = 0.4

# Configuring the problem's random distributions
for i in range(5):
  k["Distributions"][i]["Name"] = "Uniform " + str(i)
  k["Distributions"][i]["Type"] = "Univariate/Uniform"
  k["Distributions"][i]["Minimum"] = -15.0
  k["Distributions"][i]["Maximum"] = +15.0

  # Configuring the problem's variables and their prior distributions
  k["Variables"][i]["Name"] = "a"
  k["Variables"][i]["Bayesian Type"] = "Computational"
  k["Variables"][i]["Prior Distribution"] = "Uniform 0"

# Running Korali
k.run()
k["Random Seed"] = 1337

#verifyMean(k, [0.0, 0.0, 0.0, 0.0, 0.0], 0.05)
#verifyStd(k, [1.0, 1.0, 1.0, 1.0, 1.0], 0.05)
