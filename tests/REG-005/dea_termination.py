#!/bin/bash
import os
import sys
import json
import korali
import argparse

sys.path.append('./helpers')
from helpers import *

#################################################
# DEA run method
#################################################

def run_dea_with_termination_criterion(criterion, value):

    print("[Korali] Prepare DEA run with Termination Criteria "\
            "'{0}'".format(criterion))

    k = korali.initialize()

    k["Problem"]["Type"] = "Evaluation/Direct"
    k["Problem"]["Objective"] = "Maximize"
    k["Problem"]["Objective Function"] = evaluateModel

    k["Variables"][0]["Name"] = "X";
    k["Variables"][0]["Lower Bound"] = +1.0;
    k["Variables"][0]["Upper Bound"] = +10.0;

    k["Solver"]["Type"] = "Optimizer/DEA"
    k["Solver"]["Population Size"] = 10
    k["Solver"]["Termination Criteria"][criterion] = value

    k["Results Output"]["Frequency"] = 1000
    k["Random Seed"] = 1337

    k.run()

    if (criterion == "Max Generations"):
        assert_value(k["Internal"]["Current Generation"], value)
        
    elif (criterion == "Max Infeasible Resamplings"):
        assert_greatereq(k["Solver"]["Internal"]["Infeasible Sample Count"], value)
    
    elif (criterion == "Max Value"):
        assert_greatereq(k["Solver"]["Internal"]["Best Ever Value"], value)
  
    elif (criterion == "Min Value Difference Threshold"):
        previous = k["Solver"]["Internal"]["Previous Best Ever Value"]
        current  = k["Solver"]["Internal"]["Best Ever Value"]
        assert_smallereq(previous-current, value)
 
    elif (criterion == "Min Step Size"):
        print("TODO: Min Val")
 
    elif (criterion == "Min Value"):
        print("TODO: Min Val")
 
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
    
    run_dea_with_termination_criterion(args.criterion, args.value)



 
