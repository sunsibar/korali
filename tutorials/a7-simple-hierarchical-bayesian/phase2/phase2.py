#!/usr/bin/env python3

# Importing computational model
import sys
import os
import korali

# Creating hierarchical Bayesian problem from previous two problems
k = korali.initialize()

k["Problem"]["Type"]  = "Evaluation/Bayesian/Hierarchical/Psi"
k["Problem"]["Sub Problems"] = ['../setup/results_phase_1/' + str(i).zfill(3) + '/final.json' for i in range(5)]


# Add probability of theta given psi, one per subproblem variable.

k["Variables"][0]["Name"] = "Psi 1"
k["Variables"][1]["Name"] = "Psi 2"
k["Variables"][2]["Name"] = "Psi 3"
k["Variables"][3]["Name"] = "Psi 4"

k["Variables"][0]["Prior Distribution"] = "Uniform 0"
k["Variables"][1]["Prior Distribution"] = "Uniform 1"
k["Variables"][2]["Prior Distribution"] = "Uniform 2"
k["Variables"][3]["Prior Distribution"] = "Uniform 3"

k["Problem"]["Conditional Priors"] = [ "Conditional 0", "Conditional 1" ]

# Configuring the problem's random distributions
k["Distributions"][0]["Name"] = "Conditional 0"
k["Distributions"][0]["Type"] = "Univariate/Normal"
k["Distributions"][0]["Mean"] = "Psi 1"
k["Distributions"][0]["Standard Deviation"] = "Psi 2"

k["Distributions"][1]["Name"] = "Conditional 1"
k["Distributions"][1]["Type"] = "Univariate/LogNormal"
k["Distributions"][1]["Mu"]    = "Psi 3"
k["Distributions"][1]["Sigma"] = "Psi 4"

k["Distributions"][2]["Name"] = "Uniform 0"
k["Distributions"][2]["Type"] = "Univariate/Uniform"
k["Distributions"][2]["Minimum"] = 0.0
k["Distributions"][2]["Maximum"] = 20.0

k["Distributions"][3]["Name"] = "Uniform 1"
k["Distributions"][3]["Type"] = "Univariate/Uniform"
k["Distributions"][3]["Minimum"] = 0.0
k["Distributions"][3]["Maximum"] = 20.0

k["Distributions"][4]["Name"] = "Uniform 2"
k["Distributions"][4]["Type"] = "Univariate/Uniform"
k["Distributions"][4]["Minimum"] = -2.0
k["Distributions"][4]["Maximum"] = +2.0

k["Distributions"][5]["Name"] = "Uniform 3"
k["Distributions"][5]["Type"] = "Univariate/Uniform"
k["Distributions"][5]["Minimum"] = 0.0
k["Distributions"][5]["Maximum"] = 5.0



k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 2000
k["Solver"]["Default Burn In"] = 1;
k["Solver"]["Target Coefficient Of Variation"] = 0.6
k["Solver"]["Covariance Scaling"] = 0.1

k["Conduit"]["Type"] = "External"
k["Conduit"]["Concurrent Jobs"] = 4

k["Console Output"]["Verbosity"] = "Detailed"
k["Results Output"]["Path"] = "../setup/results_phase_2/"

k.run()
