#!/usr/bin/env python3
import sys
sys.path.append('setup/model')
from model import *
import numpy as np

# N : number of datasets
N = 5 

# Ns: number os samples in each dataset
Ns = 100

# Creating new experiment
import korali
e = korali.Experiment()

e["Problem"]["Type"] = "Execution/Model"
e["Problem"]["Execution Model"] = lambda modelData: normal_rnds(modelData, Ns)

e["Variables"][0]["Name"] = "V1"
e["Variables"][1]["Name"] = "V2"
e["Variables"][0]["Loaded Values"] = np.random.normal( 10, 4, N ).tolist()
e["Variables"][1]["Loaded Values"] = np.random.lognormal( 0, 1, N ).tolist()

e["Solver"]["Type"] = "Executor"
e["Solver"]["Executions Per Generation"] = 1

e["Results"]["Path"] = "setup/results_phase_0/"
e["Console"]["Verbosity"] = "Detailed"

# Starting Korali's Engine and running experiment
k = korali.Engine()
k.run(e)
