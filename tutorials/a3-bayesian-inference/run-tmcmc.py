#!/usr/bin/env python3

# In this example, we demonstrate how Korali samples the posterior distribution
# in a bayesian problem where the likelihood is calculated by providing
# reference data points and their objective values.

# Importing the computational model
import sys
sys.path.append('./model')
from model import *
import korali

k = korali.initialize()

# Setting up the reference likelihood for the Bayesian Problem
k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference"
k["Problem"]["Likelihood Model"] = "Additive Normal"
k["Problem"]["Reference Data"] = getReferenceData()
k["Problem"]["Computational Model"] = lambda sampleData: model(sampleData, getReferencePoints())

# Configuring TMCMC parameters
k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 5000

# Configuring the problem's random distributions
k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -5.0
k["Distributions"][0]["Maximum"] = +5.0

k["Distributions"][1]["Name"] = "Uniform 1"
k["Distributions"][1]["Type"] = "Univariate/Uniform"
k["Distributions"][1]["Minimum"] = -5.0
k["Distributions"][1]["Maximum"] = +5.0

k["Distributions"][2]["Name"] = "Uniform 2"
k["Distributions"][2]["Type"] = "Univariate/Uniform"
k["Distributions"][2]["Minimum"] = 0.0
k["Distributions"][2]["Maximum"] = +5.0

# Configuring the problem's variables and their prior distributions
k["Variables"][0]["Name"] = "a"
k["Variables"][0]["Bayesian Type"] = "Computational"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

k["Variables"][1]["Name"] = "b"
k["Variables"][1]["Bayesian Type"] = "Computational"
k["Variables"][1]["Prior Distribution"] = "Uniform 1"

k["Variables"][2]["Name"] = "Sigma"
k["Variables"][2]["Bayesian Type"] = "Statistical"
k["Variables"][2]["Prior Distribution"] = "Uniform 2"

# Running Korali
k.run()
