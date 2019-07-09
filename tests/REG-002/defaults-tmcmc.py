#!/usr/bin/env python3
def evaluateModel( s ):
   x = s.getVariable(0)
   r = -x*x      
   s.addResult(r)

import korali
k = korali.initialize()
k.setLikelihood( evaluateModel )

k["Problem"] = "Bayesian"
k["Solver"] = "TMCMC"

k["Bayesian"]["Likelihood"]["Type"] = "Direct"

k["Variables"][0]["Name"] = "X"
k["Variables"][0]["Bayesian"]["Prior Distribution"]["Type"] = "Uniform"
k["Variables"][0]["Bayesian"]["Prior Distribution"]["Minimum"] = -10.0
k["Variables"][0]["Bayesian"]["Prior Distribution"]["Maximum"] = +10.0

k["TMCMC"]["Population Size"] = 5000
k["TMCMC"]["Termination Criteria"]["Max Generations"]["Value"] = 0

k["Result Directory"] = "_a2_sampling_tmcmc"

k.run()