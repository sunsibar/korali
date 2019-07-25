#ifndef _KORALI_SOLVERS_DEA_HPP_
#define _KORALI_SOLVERS_DEA_HPP_

#include "solvers/base.hpp"
#include <chrono>
#include <map>

namespace Korali { namespace Solver {

class DEA : public Base
{
 private:

 Variable* _gaussianGenerator;
 Variable* _uniformGenerator;

 void mutateSingle(size_t sampleIdx); /* sample individual */
 bool isFeasible(size_t sampleIdx) const; /* check if sample inside lower & upper bounds */
 void fixInfeasible(size_t sampleIdx); /* force sample inside lower & upper bounds */
 void updateSolver(); /* update states of DEA */
 void evaluateSamples(); /* evaluate all samples until done */
 void initSamples();
 void prepareGeneration();

 public:

 DEA();
 ~DEA();

  bool checkTermination() override;
 void initialize() override;
 void finalize() override;
 void runGeneration() override;
 void processSample(size_t sampleId, double fitness) override;
 void setConfiguration() override;
 void getConfiguration() override;
 void printGeneration() override;
};

} } // namespace Korali::Solver

#endif // _KORALI_SOLVERS_DEA_HPP_