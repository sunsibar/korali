#ifndef _KORALI_SOLVERS_CCMAES_HPP_
#define _KORALI_SOLVERS_CCMAES_HPP_

#include "solvers/base.hpp"
#include <chrono>
#include <vector>
#include <map>

namespace Korali { namespace Solver {

class CMAES : public Base
{
 private:

  std::shared_ptr<Variable> _gaussianGenerator;
  std::shared_ptr<Variable> _uniformGenerator;

  void prepareGeneration();
  void sampleSingle(size_t sampleIdx); /* sample individual */
  void evaluateSamples(); /* evaluate all samples until done */
  void adaptC(int hsig); /* CMAES covariance matrix adaption */
  void updateSigma(); /* update Sigma */
  void updateEigensystem(std::vector<double>& M);
  void numericalErrorTreatment();
  void eigen(size_t N, std::vector<double>& C, std::vector<double>& diag, std::vector<double>& Q) const;
  void sort_index(const std::vector<double>& vec, std::vector<size_t>& _sortingIndex, size_t n) const;
  bool isFeasible(size_t sampleIdx) const; /* check if sample inside lower & upper bounds */
  // Private CCMAES-Specific Methods
  void initMuWeights(size_t numsamples); /* init _muWeights and dependencies */
  void initCovariance(); /* init sigma, C and B */
  void checkMeanAndSetRegime(); /* check if mean inside valid domain, if yes, update internal vars */
  void updateConstraints();
  void updateViabilityBoundaries(); /* update & shrink viability boundaries */
  void handleConstraints(); /* covariance adaption for invalid samples */
  void reEvaluateConstraints(); /* re evaluate constraints, in handleConstraints,  count violations etc.. */
  // Integer Optimization
  void updateDiscreteMutationMatrix();

 public:

 CMAES();
 ~CMAES();

 bool checkTermination() override;
 void updateDistribution();
 void initialize() override;
 void runGeneration() override;
 void processSample(size_t sampleId, double fitness) override;
 void finalize() override;
 void setConfiguration() override;
 void getConfiguration() override;
 void printGeneration() override;
};

} // namespace Korali::Solver

} // namespace Korali

#endif // _KORALI_SOLVERS_CCMAES_HPP_