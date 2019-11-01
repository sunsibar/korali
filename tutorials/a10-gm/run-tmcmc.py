#!/usr/bin/env python3

import json
import numpy as np
from scipy.stats import multivariate_normal

with open('gm.json') as f:
  gm_json = json.load(f)

for gm in gm_json:
  print(gm["w"])
  print(gm["mu"])
  print(gm["sigma"])


def likelihood( p ):
  x = p["Parameters"]
  y = 0;
  # print(len(gm_json))
  for gm in gm_json:
    y += gm["w"] *  multivariate_normal.pdf(x, mean=gm["mu"], cov=gm["sigma"])

  p["logLikelihood"] = np.log( y )


import korali

k = korali.initialize()

k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Custom"
k["Problem"]["Likelihood Model"] = likelihood


k["Distributions"][0]["Name"] = "Uniform 0"
k["Distributions"][0]["Type"] = "Univariate/Uniform"
k["Distributions"][0]["Minimum"] = -20.0
k["Distributions"][0]["Maximum"] =  20.0


for i in range(4):
  k["Variables"][i]["Name"] = "X" + str(i)
  k["Variables"][i]["Prior Distribution"] = "Uniform 0"


k["Solver"]["Type"] = "Sampler/TMCMC"
k["Solver"]["Population Size"] = 5000
k["Solver"]["Target Coefficient Of Variation"] = 0.6
k["Solver"]["Covariance Scaling"] = 0.2
k["Solver"]["Default Burn In"] = 2;

k["Console Output"]["Verbosity"] = "Detailed"

k.run()
