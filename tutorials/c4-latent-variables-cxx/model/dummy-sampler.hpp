#ifndef _SAMPLER_HPP_
#define _SAMPLER_HPP_

#include "korali.hpp"

#include <vector>
/*
void direct(korali::Sample& k)
{
  float x = k["Parameters"][0];
  k["Evaluation"] = -0.5*x*x;
}*/

void dummySampler(korali::Sample& k) //, int numberLatentVars)
// Always samples 0
{
    // Test that all input parameters are set:
  // Edit: We can't have access to those: std::vector<double> latentVars = k["Latent Variables"];

  std::vector<double> hyperparams = k["Hyperparameters"];
  size_t numberSamples = k["Number Of Samples"];
  size_t numberLatentVars = k["Number Of Latent Variables"];

  double[numberLatentVars * numberSamples] evaluations = {0};
  k["Evaluation"] = evaluations;  //-0.5*x*x;
}




#endif
