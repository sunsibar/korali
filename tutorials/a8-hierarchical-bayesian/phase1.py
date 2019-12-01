#!/usr/bin/env python3
import sys
import os
import shutil
sys.path.append('setup/model')
from model import *
import korali

# Creating Bayesian Problem List
eList = []
for i in range(5):
  e = korali.Experiment()
  
  # Getting Reference Points
  x = getReferencePoints("setup/data/", i);
  
  e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference"
  e["Problem"]["Likelihood Model"] = "Additive Gaussian"
  e["Problem"]["Reference Data"] = getReferenceData("setup/data/", i);
  e["Problem"]["Computational Model"] = lambda d: logistic( x, d);
  
  # Configuring the problem's random distributions
  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = 280.0
  e["Distributions"][0]["Maximum"] = 320.0
  
  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = 10.0
  e["Distributions"][1]["Maximum"] = 70.0
  
  e["Distributions"][2]["Name"] = "Uniform 2"
  e["Distributions"][2]["Type"] = "Univariate/Uniform"
  e["Distributions"][2]["Minimum"] = 0.0
  e["Distributions"][2]["Maximum"] = 5.0
  
  e["Distributions"][3]["Name"] = "Uniform 3"
  e["Distributions"][3]["Type"] = "Univariate/Uniform"
  e["Distributions"][3]["Minimum"] = 0.0
  e["Distributions"][3]["Maximum"] = 30.0
  
  e["Variables"][0]["Name"] = "C1"
  e["Variables"][0]["Prior Distribution"] = "Uniform 0"
  
  e["Variables"][1]["Name"] = "C2"
  e["Variables"][1]["Prior Distribution"] = "Uniform 1"
  
  e["Variables"][2]["Name"] = "C3"
  e["Variables"][2]["Prior Distribution"] = "Uniform 2"
  
  e["Variables"][3]["Name"] = "Sigma"
  e["Variables"][3]["Bayesian Type"] = "Statistical"
  e["Variables"][3]["Prior Distribution"] = "Uniform 3"
  
  e["Solver"]["Type"] = "Sampler/TMCMC"
  e["Solver"]["Population Size"] = 2000
  e["Solver"]["Target Coefficient Of Variation"] = 0.6
  e["Solver"]["Covariance Scaling"] = 0.02
  e["Solver"]["Default Burn In"] = 2;
  
  e["Results"]["Path"] = "setup/results_phase_1/" + str(i).zfill(3)
  e["Console"]["Verbosity"] = "Detailed"
  eList.append(e)

k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4

k.run(eList)

