#ifndef _KORALI_SOLVER_TMCMC_HPP_
#define _KORALI_SOLVER_TMCMC_HPP_

#include "solvers/base.hpp"
#include <gsl/gsl_rng.h>
#include <gsl/gsl_vector.h>

namespace Korali { namespace Solver {

class TMCMC : public Base
{
 private:

 gsl_rng  *range;
 void setBurnIn();
 void processGeneration();
 void updateDatabase(double* point, double fitness);
 void generateCandidate(size_t candidate);
 void evaluateSample(size_t candidate);
 void computeChainCovariances(std::vector< std::vector<double> >& chain_cov, size_t newchains);
 void minSearch(double const *fj, size_t fn, double pj, double objTol, double& xmin, double& fmin);
 bool isFeasibleCandidate(size_t candidate);
 static double tmcmc_objlogp(double x, const double *fj, size_t fn, double pj, double zero);
 static double objLog(const gsl_vector *v, void *param);

 public:

 TMCMC();
 ~TMCMC();

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

#endif // _KORALI_SOLVER_TMCMC_HPP_