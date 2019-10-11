#!/usr/bin/env python3
import sys
sys.path.append('./helpers')

from helpers import *

import korali
k = korali.initialize()

k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
k["Problem"]["Likelihood Model"] = evaluateModel

k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -10.0
k["Distributions"][0]["Maximum"] = +10.0

k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Prior Distribution"] = "Uniform 0"

k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 5000

k.dry()

###############################################################################

# Test Configuration

assert_value( k["Solver"]["Covariance Scaling"], 0.04 )
assert_value( k["Solver"]["Default Burn In"], 0 )
assert_value( k["Solver"]["Max Annealing Exponent Update"], 1.0 )
assert_value( k["Solver"]["Min Annealing Exponent Update"], 1e-5 )
assert_value( k["Solver"]["Population Size"], 5000 )

# Test Internals

assert_value( k["Solver"]["Internal"]["Accepted Samples Count"], 5000 )
assert_value( k["Solver"]["Internal"]["Annealing Exponent"], 0.0 )
assert_value( k["Solver"]["Internal"]["Coefficient Of Variation"], 0.0 )
assert_value( k["Solver"]["Internal"]["Covariance Matrix"][0], 0.0 )
assert_value( k["Solver"]["Internal"]["Proposals Acceptance Rate"], 1.0 )
assert_value( k["Solver"]["Internal"]["Selection Acceptance Rate"], 1.0 )

# Test Variables

assert_string( k["Distributions"][0]["Type"], "Univariate/Uniform" )
assert_value( k["Distributions"][0]["Minimum"], -10 )
assert_value( k["Distributions"][0]["Maximum"], 10 )

