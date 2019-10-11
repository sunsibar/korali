#!/usr/bin/env python3

# Importing computational model
import korali

# Creating hierarchical Bayesian problem from previous two problems
k = korali.initialize()

k["Problem"]["Type"]  = "Evaluation/Bayesian/Hierarchical/ThetaNew"

k["Problem"]["Psi Problem Path"] = '../setup/results_phase_2/final.json'

k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = 280.0
k["Distributions"][0]["Maximum"] = 320.0

k["Distributions"][1]["Name"] = "Uniform 1"
k["Distributions"][1]["Type"] = "Univariate/Uniform"
k["Distributions"][1]["Minimum"] = 10.0
k["Distributions"][1]["Maximum"] = 70.0

k["Distributions"][2]["Name"] = "Uniform 2"
k["Distributions"][2]["Type"] = "Univariate/Uniform"
k["Distributions"][2]["Minimum"] = 0.0
k["Distributions"][2]["Maximum"] = 5.0

k["Distributions"][3]["Name"] = "Uniform 3"
k["Distributions"][3]["Type"] = "Univariate/Uniform"
k["Distributions"][3]["Minimum"] = 0.0
k["Distributions"][3]["Maximum"] = 20.0

k["Variables"][0]["Name"] = "C1"
k["Variables"][1]["Name"] = "C2"
k["Variables"][2]["Name"] = "C3"
k["Variables"][3]["Name"] = "Sigma"

k["Variables"][0]["Prior Distribution"] = "Uniform 0"
k["Variables"][1]["Prior Distribution"] = "Uniform 1"
k["Variables"][2]["Prior Distribution"] = "Uniform 2"
k["Variables"][3]["Prior Distribution"] = "Uniform 3"

k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 100
k["Solver"]["Target Coefficient Of Variation"] = 0.6
k["Solver"]["Covariance Scaling"] = 0.02
k["Solver"]["Default Burn In"] = 1;
k["Solver"]["Max Chain Length"] = 1;

k["Conduit"]["Type"] = "External"
k["Conduit"]["Concurrent Jobs"] = 8

k["Console Output"]["Verbosity"] = "Detailed"
k["Results Output"]["Path"] = "../setup/results_phase_3a/"

k.run()
