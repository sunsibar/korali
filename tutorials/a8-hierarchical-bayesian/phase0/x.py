#!/usr/bin/env python3
import sys
import numpy as np
sys.path.append('../setup/model')
from model import *

import korali

N = 10;

k = korali.initialize()

k["Problem"]["Type"] = "Execution/Model"
k["Problem"]["Execution Model"] = lambda modelData: logistic_reference(modelData)

k["Variables"][0]["Name"] = "V1"
k["Variables"][1]["Name"] = "V2"
k["Variables"][2]["Name"] = "V3"
k["Variables"][3]["Name"] = "V4"

k["Variables"][0]["Loaded Values"] = (300*np.ones(N)).tolist()
k["Variables"][1]["Loaded Values"] = np.random.normal( 40, 4, N ).tolist()
k["Variables"][2]["Loaded Values"] = np.random.lognormal( 0, 0.5, N ).tolist()
k["Variables"][3]["Loaded Values"] = (5*np.ones(N)).tolist()

k["Solver"]["Type"] = "Executor"
k["Console Output"]["Verbosity"] = "Detailed"

k.run()
