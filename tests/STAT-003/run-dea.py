#!/usr/bin/env python3
import os
import sys
import korali

sys.path.append('./model')
from model import *

#################################################
# DEA problem definition & run
#################################################

k = korali.initialize()

k["Problem"]["Type"] = "Optimization"
k["Problem"]["Objective"] = "Minimize"
k["Problem"]["Objective Function"] = evalmodel

k["Variables"][0]["Name"] = "X";
k["Variables"][0]["Lower Bound"] = -10.0;
k["Variables"][0]["Upper Bound"] = +10.0;

k["Solver"]["Type"] = "DEA"
k["Solver"]["Population Size"] = 10
k["Solver"]["Termination Criteria"]["Max Generations"] = 100

k["Solver"]["Parent Selection Rule"] = "Random"
k["Solver"]["Accept Rule"] = "Greedy"

k["Console Output"]["Verbosity"] = "Detailed"
k["Results Output"]["Frequency"] = 1000
k["Results Output"]["Path"] = "_results_dea"
k["Random Seed"] = 1337

k.run()