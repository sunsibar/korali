#!/usr/bin/env python3
import korali
import numpy as np
import json
import scipy.stats as stats
from tools import *

def model(s,x):
  v = s["Parameters"][0]
  s["Reference Evaluations"] = x*[v];

Ns = 5000

a0 = 1; a1 = 1
b0 = 2; b1 = 10

N = 10;

L = 20;

q = np.zeros((L,3))

for i in range(L):

  # mu_star     = np.random.normal(a0,b0)
  # sigma2_star = 1/np.random.gamma(a1,1/b1)

  mu_star     = 2.4281296840717417
  sigma2_star = 6.836886103336443

  data = np.random.normal( mu_star, np.sqrt(sigma2_star), N ).tolist()

  e = korali.Experiment()

  e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference"
  e["Problem"]["Likelihood Model"] = "Additive Normal Variance"
  e["Problem"]["Reference Data"] = data
  e["Problem"]["Computational Model"] = lambda sampleData: model( sampleData, N )

  e["Distributions"][0]["Name"] = "Mu Prior"
  e["Distributions"][0]["Type"] = "Univariate/Normal"
  e["Distributions"][0]["Mean"] = a0
  e["Distributions"][0]["Standard Deviation"] = b0

  e["Distributions"][1]["Name"] = "Variance Prior"
  e["Distributions"][1]["Type"] = "Univariate/Igamma"
  e["Distributions"][1]["Shape"] = a1
  e["Distributions"][1]["Scale"] = b1

  e["Variables"][0]["Name"] = "mu"
  e["Variables"][0]["Bayesian Type"] = "Computational"
  e["Variables"][0]["Prior Distribution"] = "Mu Prior"

  e["Variables"][1]["Name"] = "variance"
  e["Variables"][1]["Bayesian Type"] = "Statistical"
  e["Variables"][1]["Prior Distribution"] = "Variance Prior"

  e["Solver"]["Type"] = "Sampler/TMCMC"
  e["Solver"]["Population Size"] = Ns

  e["Console"]["Verbosity"] = "Silent"
  results_folder = "_korali_results" + str(i).zfill(3) + "/";
  e["Results"]["Path"] = results_folder

  k = korali.Engine()
  k.run(e)


  with open( find_last_generation(results_folder) ) as json_file:
    data = json.load(json_file)

  x = np.array(data['Solver']['Internal']['Sample Database'])

  q[i,0] = ( x[:,0] < mu_star ).sum() / Ns
  q[i,1] = ( x[:,1] < sigma2_star ).sum() / Ns
  q[i,2] = ( np.sqrt(x[:,1])/x[:,0] < np.sqrt(sigma2_star)/mu_star ).sum() / Ns

  print([mu_star, sigma2_star])
  print( q[i] )
  print("-------------")


nrm = stats.norm.ppf(q)

tmp = np.sum( np.power(nrm,2), axis=0 )

p   = 1. - stats.chi2.cdf( tmp, L )

invp = np.abs( stats.norm.ppf(p) )

print( p )
print( invp )

assert( (invp<2).all() )
