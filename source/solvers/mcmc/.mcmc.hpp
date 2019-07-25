#ifndef _KORALI_SOLVER_MCMC_HPP_
#define _KORALI_SOLVER_MCMC_HPP_

#include "solvers/base.hpp"
#include "variable.hpp"
#include <gsl/gsl_rng.h>

namespace Korali { namespace Solver {

class MCMC : public Base
{
 private: 

  Korali::Variable* _gaussianGenerator; /* Gaussian random number generator */
 Korali::Variable* _uniformGenerator; /* Uniform random number generator */

 double recursiveAlpha(double& D, const double llk0, const double* logliks, size_t N) const; /* calculate acceptance ratio alpha_N */
 void evaluateSample();
 void updateState();
 bool setCandidatePriorAndCheck(size_t sampleIdx);
 void generateCandidate(size_t sampleIdx);
 void sampleCandidate(size_t sampleIdx);
 void updateDatabase(std::vector<double>&, double fitness);
 void choleskyDecomp(const std::vector<double>& inC, std::vector<double>& outL) const;
 void acceptReject(size_t trial); /* Accept or reject sample with multiple trials */

 public:

 MCMC();
 ~MCMC();

 void initialize() override;
 void finalize() override;
 void runGeneration() override;
 void processSample(size_t c, double fitness) override;
 bool checkTermination() override;
 void setConfiguration() override;
 void getConfiguration() override;
 void printGeneration() override;
};

} } // namespace Korali::Solver

#endif // _KORALI_SOLVER_MCMC_HPP_