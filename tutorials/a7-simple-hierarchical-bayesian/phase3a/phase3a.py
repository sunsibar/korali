#!/usr/bin/env python3

# Importing computational model
import korali

# Creating hierarchical Bayesian problem from previous two problems
k = korali.initialize()

k["Problem"]["Type"]  = "Evaluation/Bayesian/Hierarchical/ThetaNew"
k["Problem"]["Psi Problem Path"] = '../setup/results_phase_2/final.json'

k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -20.0
k["Distributions"][0]["Maximum"] = 40.0

k["Distributions"][1]["Name"] = "Uniform 1"
k["Distributions"][1]["Type"] = "Univariate/Uniform"
k["Distributions"][1]["Minimum"] = 0.0
k["Distributions"][1]["Maximum"] = 10.0

k["Variables"][0]["Name"] = "mu"
k["Variables"][1]["Name"] = "sigma"

k["Variables"][0]["Prior Distribution"] = "Uniform 0"
k["Variables"][1]["Prior Distribution"] = "Uniform 1"

k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 1000
k["Solver"]["Target Coefficient Of Variation"] = 0.6
k["Solver"]["Covariance Scaling"] = 0.02
k["Solver"]["Default Burn In"] = 1;

k["Conduit"]["Type"] = "External"
k["Conduit"]["Concurrent Jobs"] = 4

k["Console Output"]["Verbosity"] = "Detailed"
k["Results Output"]["Path"] = "../setup/results_phase_3a/"

k.run()
