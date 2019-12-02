#!/usr/bin/env python3

import os
import sys
import korali

def read_matrix_for_gp( fileName, lastColumnIsData=True ):
  f = open( fileName, "r" )
  data = [ [ float(n) for n in line.split()]  for line in f]
  f.close()

  if( lastColumnIsData == True ):
    x = [row[:-1] for row in data]
    y = [row[ -1] for row in data]
  else:
    x = data
    y = []

  return x,y

x, y = read_matrix_for_gp('data/sincos1d_train.dat')
e0 = korali.Experiment()
e0["Problem"]["Type"] = "Evaluation/GaussianProcess"
e0["Problem"]["Covariance Function"] = "CovSum ( CovSEiso, CovNoise)"
e0["Problem"]["X Data"] = x
e0["Problem"]["Y Data"] = y
e0["Solver"]["Type"] = "Optimizer/Rprop"
e0["Solver"]["Termination Criteria"]["Max Generations"] = 200
e0["Solver"]["Termination Criteria"]["Parameter Relative Tolerance"] = 1e-8
e0["Console"]["Verbosity"] = "Normal"
e0["Console"]["Frequency"] = 10
e0["Results"]["Frequency"] = 100
e0["Results"]["Path"] = "_korali_result_train"

x, y = read_matrix_for_gp('data/sincos1d_test.dat')
e1 = korali.Experiment()
e1["Problem"]["Type"] = "Execution/GaussianProcess"
e1["Problem"]["Gaussian Process Json File"] =  "_korali_result_train/final.json"
e1["Problem"]["X Data"] = x
e1["Problem"]["Y Data"] = y
e1["Solver"]["Type"] = "Executor"
e1["Solver"]["Executions Per Generation"] = 1
e1["Console"]["Verbosity"] = "Normal"
e1["Console"]["Frequency"] = 10
e1["Results"]["Frequency"] = 100
e1["Results"]["Path"] = "_korali_result_test"

x, y = read_matrix_for_gp('data/sincos1d_new.dat',lastColumnIsData=True)
e2 = korali.Experiment()
e2["Problem"]["Type"] = "Execution/GaussianProcess"
e2["Problem"]["Gaussian Process Json File"] =  "_korali_result_train/final.json"
e2["Problem"]["X Data"] = x
e2["Problem"]["Y Data"] = y
e2["Solver"]["Type"] = "Executor"
e2["Solver"]["Executions Per Generation"] = 1
e2["Console"]["Verbosity"] = "Normal"
e2["Console"]["Frequency"] = 10
e2["Results"]["Frequency"] = 100
e2["Results"]["Path"] = "_korali_result_new"

k = korali.Engine()
k.run(e0)
k.run(e1)
k.run(e2)
