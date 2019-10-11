#include "korali.hpp"
#include "model/jacobi.h"

int main(int argc, char* argv[])
{
 MPI_Init(&argc, &argv);
 auto k = korali::Engine();
 if (argc != 2) { printf("Error: this example requires 'Ranks Per Team' passed as argument.\n"); exit(-1); }

 k["Problem"]["Type"] = "Evaluation/Bayesian/Inference/Reference";
 k["Problem"]["Likelihood Model"] = "Additive Normal";
 k["Problem"]["Reference Data"] = getReferenceData();
 k["Problem"]["Computational Model"] = &jacobi;

 k["Distributions"][0]["Name"] = "Uniform 0";
 k["Distributions"][0]["Type"] = "Univariate/Uniform";
 k["Distributions"][0]["Minimum"] = +0.0;
 k["Distributions"][0]["Maximum"] = +5.0;

 k["Distributions"][1]["Name"] = "Uniform 1";
 k["Distributions"][1]["Type"] = "Univariate/Uniform";
 k["Distributions"][1]["Minimum"] = -5.0;
 k["Distributions"][1]["Maximum"] = +0.0;

 k["Distributions"][2]["Name"] = "Uniform 2";
 k["Distributions"][2]["Type"] = "Univariate/Uniform";
 k["Distributions"][2]["Minimum"] = +1.0;
 k["Distributions"][2]["Maximum"] = +6.0;

 k["Distributions"][3]["Name"] = "Uniform 3";
 k["Distributions"][3]["Type"] = "Univariate/Uniform";
 k["Distributions"][3]["Minimum"] = -4.0;
 k["Distributions"][3]["Maximum"] = +1.0;

 k["Distributions"][4]["Name"] = "Uniform 4";
 k["Distributions"][4]["Type"] = "Univariate/Uniform";
 k["Distributions"][4]["Minimum"] = +2.0;
 k["Distributions"][4]["Maximum"] = +7.0;

 k["Distributions"][5]["Name"] = "Uniform 5";
 k["Distributions"][5]["Type"] = "Univariate/Uniform";
 k["Distributions"][5]["Minimum"] = -3.0;
 k["Distributions"][5]["Maximum"] = +2.0;

 k["Distributions"][6]["Name"] = "Uniform 6";
 k["Distributions"][6]["Type"] = "Univariate/Uniform";
 k["Distributions"][6]["Minimum"] = 0.0;
 k["Distributions"][6]["Maximum"] = +20.0;

 k["Variables"][0]["Name"] = "X0";
 k["Variables"][0]["Bayesian Type"] = "Computational";
 k["Variables"][0]["Prior Distribution"] = "Uniform 0";

 k["Variables"][1]["Name"] = "X1";
 k["Variables"][1]["Bayesian Type"] = "Computational";
 k["Variables"][1]["Prior Distribution"] = "Uniform 1";

 k["Variables"][2]["Name"] = "Y0";
 k["Variables"][2]["Bayesian Type"] = "Computational";
 k["Variables"][2]["Prior Distribution"] = "Uniform 2";

 k["Variables"][3]["Name"] = "Y1";
 k["Variables"][3]["Bayesian Type"] = "Computational";
 k["Variables"][3]["Prior Distribution"] = "Uniform 3";

 k["Variables"][4]["Name"] = "Z0";
 k["Variables"][4]["Bayesian Type"] = "Computational";
 k["Variables"][4]["Prior Distribution"] = "Uniform 4";

 k["Variables"][5]["Name"] = "Z1";
 k["Variables"][5]["Bayesian Type"] = "Computational";
 k["Variables"][5]["Prior Distribution"] = "Uniform 5";

 k["Variables"][6]["Name"] = "Sigma";
 k["Variables"][6]["Bayesian Type"] = "Statistical";
 k["Variables"][6]["Prior Distribution"] = "Uniform 6";

 k["Solver"]["Type"] = "Sampler/TMCMC";
 k["Solver"]["Covariance Scaling"] = 0.02;
 k["Solver"]["Population Size"] = 100;
 k["Solver"]["Termination Criteria"]["Max Generations"] = 20;

 k["Conduit"]["Type"] = "MPI";
 k["Conduit"]["Ranks Per Team"] = atoi(argv[1]);

 k.run();

 return 0;
}
