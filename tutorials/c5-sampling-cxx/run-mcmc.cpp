#include "model/model.hpp"
#include "korali.hpp"


/* In this example, we demonstrate how Korali samples the posterior
# distribution in a bayesian problem where the likelihood
# is provided directly by the computational model.
# In this case, we use the MCMC method. */


int main(int argc, char* argv[])
{
    auto k = korali::Engine();
    auto e = korali::Experiment();

    // Selecting problem and solver types.
    e["Problem"]["Type"] = "Evaluation/Direct/Basic";
    e["Problem"]["Objective Function"] = &model;

    // Configuring the MCMC sampler parameters
    e["Solver"]["Type"]  = "Sampler/MCMC";
    e["Solver"]["Burn In"] = 500;
    e["Solver"]["Termination Criteria"]["Max Samples"] = 5000;

    // Defining problem's variables
    e["Variables"][0]["Name"] = "X";
    e["Variables"][0]["Initial Mean"] = 0.0;
    e["Variables"][0]["Initial Standard Deviation"] = 1.0;

    // Configuring output settings
    e["Results"]["Frequency"] = 500;
    e["Console"]["Frequency"] = 500;
    e["Console"]["Verbosity"] = "Detailed";

    // Starting Korali's Engine and running experiment
    k.run(e);

    return 0;
}
