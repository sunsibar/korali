#!/usr/bin/env python3

# Importing computational model
import sys
import os
import korali

# Creating hierarchical Bayesian problem from previous two problems
e = korali.Experiment()

e["Problem"]["Type"]  = "Evaluation/Bayesian/Hierarchical/Psi"
for i in range(4):
  e["Problem"]["Subproblems"][i]["Path"]   = 'setup/results_phase_1/' + str(i).zfill(3)
  e["Problem"]["Subproblems"][i]["Conditional Priors"] = ["Conditional 0", "Conditional 1"]

for i in range(4,5):
  e["Problem"]["Subproblems"][i]["Path"]   = 'setup/results_phase_1/' + str(i).zfill(3)
  e["Problem"]["Subproblems"][i]["Conditional Priors"] = ["Conditional 0", "Conditional 2"]


# Add probability of theta given psi, one per subproblem variable.
e["Variables"][0]["Name"] = "Psi 1"
e["Variables"][1]["Name"] = "Psi 2"
e["Variables"][2]["Name"] = "Psi 3"
e["Variables"][3]["Name"] = "Psi 4"
e["Variables"][4]["Name"] = "Psi 5"
e["Variables"][5]["Name"] = "Psi 6"

e["Variables"][0]["Prior Distribution"] = "Uniform 0"
e["Variables"][1]["Prior Distribution"] = "Uniform 1"
e["Variables"][2]["Prior Distribution"] = "Uniform 2"
e["Variables"][3]["Prior Distribution"] = "Uniform 3"
e["Variables"][4]["Prior Distribution"] = "Uniform 4"
e["Variables"][5]["Prior Distribution"] = "Uniform 5"

# Configuring the problem's random distributions
e["Distributions"][0]["Name"] = "Conditional 0"
e["Distributions"][0]["Type"] = "Univariate/Gaussian"
e["Distributions"][0]["Mean"] = "Psi 1"
e["Distributions"][0]["Standard Deviation"] = "Psi 2"

e["Distributions"][1]["Name"] = "Conditional 1"
e["Distributions"][1]["Type"] = "Univariate/LogNormal"
e["Distributions"][1]["Mu"]    = "Psi 3"
e["Distributions"][1]["Sigma"] = "Psi 4"

e["Distributions"][2]["Name"] = "Conditional 2"
e["Distributions"][2]["Type"] = "Univariate/LogNormal"
e["Distributions"][2]["Mu"]    = "Psi 5"
e["Distributions"][2]["Sigma"] = "Psi 6"

e["Distributions"][3]["Name"] = "Uniform 0"
e["Distributions"][3]["Type"] = "Univariate/Uniform"
e["Distributions"][3]["Minimum"] = 0.0
e["Distributions"][3]["Maximum"] = 20.0

e["Distributions"][4]["Name"] = "Uniform 1"
e["Distributions"][4]["Type"] = "Univariate/Uniform"
e["Distributions"][4]["Minimum"] = 0.0
e["Distributions"][4]["Maximum"] = 20.0

e["Distributions"][5]["Name"] = "Uniform 2"
e["Distributions"][5]["Type"] = "Univariate/Uniform"
e["Distributions"][5]["Minimum"] = -2.0
e["Distributions"][5]["Maximum"] = +2.0

e["Distributions"][6]["Name"] = "Uniform 3"
e["Distributions"][6]["Type"] = "Univariate/Uniform"
e["Distributions"][6]["Minimum"] = 0.0
e["Distributions"][6]["Maximum"] = 5.0

e["Distributions"][7]["Name"] = "Uniform 4"
e["Distributions"][7]["Type"] = "Univariate/Uniform"
e["Distributions"][7]["Minimum"] = -4.0
e["Distributions"][7]["Maximum"] = +4.0

e["Distributions"][8]["Name"] = "Uniform 5"
e["Distributions"][8]["Type"] = "Univariate/Uniform"
e["Distributions"][8]["Minimum"] = 0.0
e["Distributions"][8]["Maximum"] = 10.0

e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 2000
e["Solver"]["Default Burn In"] = 1;
e["Solver"]["Target Coefficient Of Variation"] = 0.6
e["Solver"]["Covariance Scaling"] = 0.1

e["Console"]["Verbosity"] = "Detailed"
e["Results"]["Path"] = "setup/results_phase_2/"

# Starting Korali's Engine and running experiment
k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4
k.run(e)
