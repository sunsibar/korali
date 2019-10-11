#!/bin/bash
import os
import sys
import json
import korali
import argparse

sys.path.append('./helpers')
from helpers import *

#################################################
# TMCMC run method
#################################################

def run_tmcmc_with_termination_criterion(criterion, value):

    print("[Korali] Prepare DEA run with Termination Criteria "\
            "'{0}'".format(criterion))

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
    k["Solver"]["Termination Criteria"][criterion] = value

    k["Results Output"]["Frequency"] = 1000
    k["Random Seed"] = 1337

    k.run()

    if (criterion == "Max Generations"):
        assert_value(k["Internal"]["Current Generation"], value)
        
    elif (criterion == "Target Annealing Exponent"):
        assert_greatereq(k["Solver"]["Internal"]["Annealing Exponent"], value)
    
    else:
        print("Termination Criterion not recognized!")
        exit(-1)


#################################################
# Main (called from run_test.sh with args)
#################################################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='cmaes_termination', description='Check Termination Criterion.')
    parser.add_argument('--criterion', help='Name of Termination Criterion', action='store', required = True)
    parser.add_argument('--value', help='Value of Termination Criterion', action='store', type = float, required = True)
    args = parser.parse_args()
    
    run_tmcmc_with_termination_criterion(args.criterion, args.value)



 
