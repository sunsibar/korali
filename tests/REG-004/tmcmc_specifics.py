#!/bin/bash
import os
import sys
import json
import korali

sys.path.append('./helpers')
from helpers import *


#################################################
#  Prepare Expected Values
#################################################

gen = 1
currentBurnIn = [0, 0, 10, 7, 5, 5, 5, 5, 5, 5, 5, 5]

eps = 1e-12
prevRho = 0.0
minRhoUpdate = 1e-3
maxRhoUpdate = 0.2


#################################################
# Set Up  TMCMC run
#################################################

print("[Korali] Prepare TMCMC run")

# Starting Korali's Engine
k = korali.initialize()

k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
k["Problem"]["Likelihood Model"] = evaluateLogLikelihood

k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -10.0
k["Distributions"][0]["Maximum"] = +10.0

k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 5000
k["Solver"]["Covariance Scaling"] = 0.001

k["Solver"]["Default Burn In"] = 5
k["Solver"]["Per Generation Burn In"] = [ 10, 7 ]
k["Solver"]["Max Chain Length"] = 1
k["Solver"]["Target Coefficient Of Variation"] = 0.5
k["Solver"]["Min Annealing Exponent Update"] = minRhoUpdate
k["Solver"]["Max Annealing Exponent Update"] = maxRhoUpdate

k["Random Seed"] = 314


#################################################
#  Run TMCMC
#################################################

print("[Korali] Running TMCMC...")
k.run()


#################################################
# Read Result Files
#################################################

print("[Korali] Read & Evaluate Output..")

src = "_korali_result"
resultfiles = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]
resultfiles.remove("initial.json")
resultfiles.remove("final.json")
resultfiles = sorted(resultfiles)

for filename in resultfiles:
  path   = '{0}/{1}'.format(src, filename)
        
  with open(path) as f:
    dataString = f.read()
    dataString = dataString.replace('+INFINITY', '1.0e+300').replace('-INFINITY', '-1.0e+300').replace('NaN', '-1.0e+300')
    data  = json.loads(dataString)

#################################################
# Test Result
#################################################

    print("[Korali] Checking generation {0} inside file {1} ..".format(gen, path))
    
    # Testing Burn In Assignments
    assert_value( data['Solver']['Default Burn In'], 5 )
    #assert_value( data['Solver']['Internal']['Current Burn In'], currentBurnIn[gen] )
    
    # Testing Correctness of (min/max) Rho Update
    assert_value( data['Solver']['Min Annealing Exponent Update'], minRhoUpdate )
    assert_value( data['Solver']['Max Annealing Exponent Update'], maxRhoUpdate )
    rho =  data['Solver']['Internal']['Annealing Exponent']
    
    finished = data['Internal']['Is Finished']
    if finished == True:
        assert_value(rho - prevRho >= maxRhoUpdate-eps, False)
    if finished == False:
        assert_value(rho - prevRho <= maxRhoUpdate+eps, True)
 
    # Updates
    prevRho = rho
    gen = gen + 1
