#ifndef _MODEL_HPP_
#define _MODEL_HPP_

#include "korali.hpp"

void model(korali::Sample& k)
{
  float x = k["Parameters"][0];
  k["Evaluation"] = -0.5*x*x;
}

#endif
