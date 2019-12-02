#!/usr/bin/env python3
import sys
import os
import shutil
sys.path.append('setup/model')
from model import *
import korali

# Creating Experiment List
eList = []
for i in range(5):
  e = korali.Experiment()
  
  e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Approximate"
  e["Problem"]["Likelihood Model"] = "Gaussian"
  e["Problem"]["Reference Data"] = getReferenceData("setup/data/",i);
  
  # Configuring the problem's random distributions
  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = 0.0
  e["Distributions"][0]["Maximum"] = 20.0
  
  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = 0.0
  e["Distributions"][1]["Maximum"] = 10.0
 
  e["Distributions"][2]["Name"] = "Uniform 2"
  e["Distributions"][2]["Type"] = "Univariate/Uniform"
  e["Distributions"][2]["Minimum"] = 0.0
  e["Distributions"][2]["Maximum"] = 20.0
  
  e["Variables"][0]["Name"] = "mu"
  e["Variables"][0]["Bayesian Type"] = "Statistical"
  e["Variables"][0]["Prior Distribution"] = "Uniform 0"
 
  if i < 4:
    e["Variables"][1]["Name"] = "sigma1"
    e["Variables"][1]["Bayesian Type"] = "Statistical"
    e["Variables"][1]["Prior Distribution"] = "Uniform 1"
  else:
    e["Variables"][1]["Name"] = "sigma2"
    e["Variables"][1]["Bayesian Type"] = "Statistical"
    e["Variables"][1]["Prior Distribution"] = "Uniform 2"

  e["Solver"]["Type"] = "Sampler/TMCMC"
  e["Solver"]["Population Size"] = 1000
  e["Solver"]["Target Coefficient Of Variation"] = 0.6
  e["Solver"]["Covariance Scaling"] = 0.02
  e["Solver"]["Default Burn In"] = 0;
  
  e["Results"]["Path"] = "setup/results_phase_1/" + str(i).zfill(3)
  e["Console"]["Verbosity"] = "Detailed"
  eList.append(e)

# Starting Korali's Engine and running experiment
k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4
k.run(eList)
