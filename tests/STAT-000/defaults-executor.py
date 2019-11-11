#!/usr/bin/env python3
import korali
import math

k = korali.initialize()

k["Problem"]["Type"] = "Execution/Model"
k["Problem"]["Execution Model"] = lambda x : x

k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Loaded Values"] = []

k["Solver"]["Type"] = "Executor"
#k["Solver"]["Executions Per Generation"] = 100

#k["Console Output"]["Verbosity"] = "Detailed"

k.runDry()

###############################################################################

# Testing Configuration

assert k["Solver"]["Executions Per Generation"] == -1

# Testing Internals

assert k["Solver"]["Internal"]["Model Evaluation Count"] == 0
assert k["Solver"]["Internal"]["Sample Count"] == 0
assert k["Solver"]["Internal"]["Variable Count"] == 1
