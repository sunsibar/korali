/* In this example, we demonstrate how Korali finds values for the
variables that maximize the objective function, given by a
user-provided computational model. */

#include "model/direct.hpp"
#include "korali.hpp"

int main(int argc, char* argv[])
{

auto k = korali::Engine();

// Configuring Problem.
k["Problem"]["Type"] = "Evaluation/Direct/Basic";
k["Problem"]["Objective"] = "Maximize";
k["Problem"]["Objective Function"] = &direct;

// Defining the problem's variables.
k["Variables"][0]["Name"] = "X";
k["Variables"][0]["Lower Bound"] = -10.0;
k["Variables"][0]["Upper Bound"] = +10.0;

// Configuring CMA-ES parameters
k["Solver"]["Type"] = "Optimizer/CMAES";
k["Solver"]["Population Size"] = 32;
k["Solver"]["Termination Criteria"]["Min Value Difference Threshold"] = 1e-7;
k["Solver"]["Termination Criteria"]["Max Generations"] = 100;

// Running Korali
k.runSingle();

}
