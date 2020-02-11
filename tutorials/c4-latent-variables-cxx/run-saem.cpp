#include "model/heat2d.h"
#include "korali.hpp"

int main(int argc, char* argv[])
{
 auto k = korali::Engine();
 auto e = korali::Experiment();
 auto p = heat2DInit(&argc, &argv);

 e["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference";
 e["Problem"]["Likelihood Model"] = "Additive Normal";
 e["Problem"]["Reference Data"] = p.refTemp;
 e["Problem"]["Computational Model"] = &heat2DSolver;

 e["Solver"]["Type"] = "Optimizer/CMAES";
 e["Solver"]["Population Size"] = 32;
 e["Solver"]["Termination Criteria"]["Max Generations"] = 100;

 e["Distributions"][0]["Name"] = "Uniform 0";
 e["Distributions"][0]["Type"] = "Univariate/Uniform";
 e["Distributions"][0]["Minimum"] = 10.0;
 e["Distributions"][0]["Maximum"] = 60.0;

 e["Distributions"][1]["Name"] = "Uniform 1";
 e["Distributions"][1]["Type"] = "Univariate/Uniform";
 e["Distributions"][1]["Minimum"] = 0.0;
 e["Distributions"][1]["Maximum"] = 0.5;

 e["Distributions"][2]["Name"] = "Uniform 2";
 e["Distributions"][2]["Type"] = "Univariate/Uniform";
 e["Distributions"][2]["Minimum"] = 0.6;
 e["Distributions"][2]["Maximum"] = 1.0;

 e["Distributions"][3]["Name"] = "Uniform 3";
 e["Distributions"][3]["Type"] = "Univariate/Uniform";
 e["Distributions"][3]["Minimum"] = 0.0;
 e["Distributions"][3]["Maximum"] = 20.0;

 e["Variables"][0]["Name"] = "Intensity";
 e["Variables"][0]["Bayesian Type"] = "Computational";
 e["Variables"][0]["Prior Distribution"] = "Uniform 0";
 e["Variables"][0]["Initial Mean"] = 30.0;
 e["Variables"][0]["Initial Standard Deviation"] = 5.0;

 e["Variables"][1]["Name"] = "PosX";
 e["Variables"][1]["Bayesian Type"] = "Computational";
 e["Variables"][1]["Prior Distribution"] = "Uniform 1";
 e["Variables"][1]["Initial Mean"] = 0.25;
 e["Variables"][1]["Initial Standard Deviation"] = 0.01;

 e["Variables"][2]["Name"] = "PosY";
 e["Variables"][2]["Bayesian Type"] = "Computational";
 e["Variables"][2]["Prior Distribution"] = "Uniform 2";
 e["Variables"][2]["Initial Mean"] = 0.8;
 e["Variables"][2]["Initial Standard Deviation"] = 0.1;

 e["Variables"][3]["Name"] = "Sigma";
 e["Variables"][3]["Bayesian Type"] = "Statistical";
 e["Variables"][3]["Prior Distribution"] = "Uniform 3";
 e["Variables"][3]["Initial Mean"] = 10.0;
 e["Variables"][3]["Initial Standard Deviation"] = 1.0;

 k.run(e);

 return 0;
}
