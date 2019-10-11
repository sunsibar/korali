#include "model/heat2d.h"
#include "korali.hpp"

int main(int argc, char* argv[])
{
 auto k = korali::Engine();
 auto p = heat2DInit(&argc, &argv);

 k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference";
 k["Problem"]["Likelihood Model"] = "Additive Normal";
 k["Problem"]["Reference Data"] = p.refTemp;
 k["Problem"]["Computational Model"] = &heat2DSolver;

 k["Solver"]["Type"] = "Sampler/TMCMC";
 k["Solver"]["Population Size"] = 200;

 k["Distributions"][0]["Name"] = "Uniform 0";
 k["Distributions"][0]["Type"] = "Univariate/Uniform";
 k["Distributions"][0]["Minimum"] = 10.0;
 k["Distributions"][0]["Maximum"] = 60.0;

 k["Distributions"][1]["Name"] = "Uniform 1";
 k["Distributions"][1]["Type"] = "Univariate/Uniform";
 k["Distributions"][1]["Minimum"] = 0.0;
 k["Distributions"][1]["Maximum"] = 0.5;

 k["Distributions"][2]["Name"] = "Uniform 2";
 k["Distributions"][2]["Type"] = "Univariate/Uniform";
 k["Distributions"][2]["Minimum"] = 0.6;
 k["Distributions"][2]["Maximum"] = 1.0;

 k["Distributions"][3]["Name"] = "Uniform 3";
 k["Distributions"][3]["Type"] = "Univariate/Uniform";
 k["Distributions"][3]["Minimum"] = 0.0;
 k["Distributions"][3]["Maximum"] = 20.0;

 k["Variables"][0]["Name"] = "Intensity";
 k["Variables"][0]["Bayesian Type"] = "Computational";
 k["Variables"][0]["Prior Distribution"] = "Uniform 0";

 k["Variables"][1]["Name"] = "PosX";
 k["Variables"][1]["Bayesian Type"] = "Computational";
 k["Variables"][1]["Prior Distribution"] = "Uniform 1";

 k["Variables"][2]["Name"] = "PosY";
 k["Variables"][2]["Bayesian Type"] = "Computational";
 k["Variables"][2]["Prior Distribution"] = "Uniform 2";

 k["Variables"][3]["Name"] = "Sigma";
 k["Variables"][3]["Bayesian Type"] = "Statistical";
 k["Variables"][3]["Prior Distribution"] = "Uniform 3";

 k.run();

 return 0;
}
