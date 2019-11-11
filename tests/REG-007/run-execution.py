#!/usr/bin/env python3
import korali

def dummy(d):
    return

k = korali.initialize()

k["Problem"]["Type"] = "Execution/Model"
k["Problem"]["Execution Model"] = dummy

k["Variables"][0]["Name"] = "X0"
k["Variables"][0]["Loaded Values"] = [1.0, 2.0, 3.0, 4.0, 5.0]

k["Variables"][1]["Name"] = "X1"
k["Variables"][1]["Loaded Values"] = [1.0, 2.0, 3.0, 4.0, 5.0]

k["Solver"]["Type"] = "Executor"
k["Solver"]["Executions Per Generation"] = 2

k["Console Output"]["Verbosity"] = "Detailed"

k.run()

assert k["Solver"]["Internal"]["Model Evaluation Count"] == 5
assert k["Solver"]["Internal"]["Sample Count"] == 5
assert k["Solver"]["Internal"]["Variable Count"] == 2
assert k["Solver"]["Internal"]["Current Generation"] == 3
