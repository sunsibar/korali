#!/usr/bin/env python3
import sys
sys.path.append('./model')
from ackley import m_ackley
import korali

k = korali.Engine()

k["Seed"]      = 0xC0FFEE
k["Verbosity"] = "Detailed"
k["Problem"]["Type"] = "Direct"

for i in range(4):
 k["Problem"]["Variables"][i]["Name"] = "X" + str(i)
 k["Problem"]["Variables"][i]["Type"] = "Computational"
 k["Problem"]["Variables"][i]["Distribution"] = "Uniform"
 k["Problem"]["Variables"][i]["Minimum"] = -32.0
 k["Problem"]["Variables"][i]["Maximum"] = +32.0

k["Solver"]["Method"] = "CMA-ES"
k["Solver"]["Lambda"] = 10
k["Solver"]["Termination Criteria"]["Max Generations"] = 100
k["Solver"]["Termination Criteria"]["Min DeltaX"] = 1e-12

k.run(m_ackley)